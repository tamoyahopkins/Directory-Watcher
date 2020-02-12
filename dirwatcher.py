#!/usr/bin/env python

import signal
import os
import argparse
import sys
import logging
import time
import datetime

__author__ = 'tamoyahopkins'

# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s: %(levelname)s : %(message)s')
file_handler = logging.FileHandler('dirwatcher.log', 'a')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# add stream to include Traceback in logs
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# exit option
close_program = False


def action_signal(sig_num, frame):
    '''Actions incoming signals and closes program if needed'''
    logger.warning(f'INCOMING SIGNAL - {signal.Signals(sig_num).name}')
    global close_program
    close_program = True


# handle interval
interval = 0

# program globals
current_dict = {}
state = {}


def watch_dir(dir_, search_text, ext=None):
    '''Loops thru filenames in a dir & searches for magic str.
        If filename already in dic, updates lineno, if not in dict, gives
        default value of 0. Returns dict
    '''
    # global current_dict
    if os.path.isdir(dir_):
        dir_files = []

        for dirpath, _, filenames in os.walk(dir_):
            for f in filenames:
                dir_files.append(os.path.abspath(os.path.join(dirpath, f)))
        if not ext:
            # if ext is NOT set
            for file_ in dir_files:
                # if not in current_dict, make key and set to 0
                if file_ not in current_dict:
                    current_dict[file_] = 0

        elif ext:
            # if ext IS set
            for file_ in dir_files:
                file_ending = file_[file_.rindex('.'):]
                # and file has correct extension
                if file_ending == ext:
                    # and not in current_dict, add to current_dir
                    if file_ not in current_dict:
                        current_dict[file_] = 0

        # parse current_dict for search_text and update
        search_dict(current_dict, search_text)

        # compare state_dict w/ current_dict and log changes
        global state
        compare(state=state, dict=current_dict)
        # update state
        state = current_dict


def search_dict(dict_, text):
    '''Searches dict files for text.  Stores last line searched and
        Returns updated dict. Updates state.
    '''
    if dict_:
        line_count = 0
        for path, value in dict_.items():
            line_count = value
            with open(path) as f:
                for line in f.readlines()[line_count:]:
                    line_count += 1
                    if text in line:
                        logger.info(
                            f'Found "{text}" in "{path}" (Line {line_count})')
            dict_[path] = line_count
        return dict_

    else:
        logger.info('Directory has no searchable files!')


def compare(state=state, dict=current_dict):
    '''compares state with current_dir and logs any changes'''
    if len(state) < len(current_dict):
        for path in current_dict:
            if path not in state:
                logger.info(f'"{path}" added to directory.')
    if len(state) > len(current_dict):
        for path in state:
            if path not in current_dict:
                logger.info(f'"{path}" removed from directory.')


def create_parser():
    '''creates parser that defines acceptable options flags (args)'''
    parser = argparse.ArgumentParser(
        description="Program searches directory files for indicated text.")
    parser.add_argument(
        'directory', help="Provide a directory path as a string. The program"
        "will parse files in the directory for the search_text provided.",
        type=str)
    parser.add_argument(
        'search_text',
        help="Provide a text string to search directory files."
        " If found, program will return filename and line number of text's"
        "location.", type=str)
    parser.add_argument(
        '--interval', '-i', help="Provide an integer (in seconds).  "
        "Program will re-run itself once per second(s) indicated.", type=int)
    parser.add_argument(
        '--extension', '-e',
        help="Provide a string text extension (e.g. '.pdf')"
        ".  Program will filter query to only search for"
        "indicated file types.", type=str)
    return parser


def log_banner(msg, name, time, end=''):
    '''create a log banner that executes at program startup and shutdown'''
    text = ('----------------------------------------------------------\n'
            f'{time} - {msg} PROGRAM {name}\n{end}'
            '----------------------------------------------------------\n')
    with open('dirwatcher.log', 'a') as f:
        f.write(text)


def main():
    '''runs progam and polls continuously and logs info/errors
    unless signaled to shutdown'''

    timer = time.time()
    start_formatted = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_banner('RUNNING', ''.join(sys.argv[:1]).upper(), start_formatted)

    # parse sys args passed
    parser = create_parser()
    args = sys.argv[1:]
    ns = parser.parse_args(args)

    # exit program if signal received
    signal.signal(signal.SIGTERM, action_signal)
    signal.signal(signal.SIGINT, action_signal)

    while not close_program:
        try:
            if not args:
                parser.print_usage()

            if not os.path.isdir(ns.directory):
                logger.error(
                    f'"{ns.directory}" is not a directory.'
                    'Please provide a directory string as'
                    'your first argument.')
                parser.print_usage()

            if ns.extension is not None:
                watch_dir(ns.directory, ns.search_text, ext=ns.extension)

            if ns.extension is None:
                watch_dir(ns.directory, ns.search_text)
        except KeyboardInterrupt:
            logger.error("This program does not exit using CTRL + C")
        except OSError as e:
            logger.error(f'OSError: {e}')
        except Exception as e:
            logger.error(e)

    if not ns.interval:
        time.sleep(1.0)
    if ns.interval:
        time.sleep(ns.interval)

    end_formatted = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    stop_timer = time.time() - timer
    log_banner(
        'CLOSING', ''.join(sys.argv[:1]).upper(), end_formatted,
        end='TOTAL RUNTIME: {:.3f} \n'.format(stop_timer))


if __name__ == '__main__':
    main()
