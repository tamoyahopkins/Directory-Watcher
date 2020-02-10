#!/usr/bin/env python

import os, argparse, sys, logging

__author__ = 'tamoyahopkins'

# logging config
startup_banner = ''
shutdown_banner = ''
logger = ''

# program
current_dict = {}
print(f'ORIGINAL DICT: {current_dict}')
state = {}


def watch_dir(dir_, search_text, ext=None):
    '''Loops thru filenames in a dir & searches for magic str.
        If filename already in dic, updates lineno, if not in dict, gives
        default value of 0. Returns dict
    '''
    # if isinstance(dir_, str):
    if os.path.isdir(dir_):
        # print(f'Yep {dir_} is a directory :)')
        dir_files = []
        for dirpath, _, filenames in os.walk(dir_):
            for f in filenames:
                dir_files.append(os.path.abspath(os.path.join(dirpath, f)))
        # print(dir_files)
        if ext is None:
            # ext is NOT set
            for file_ in dir_files:
                # if not in current_dict, make key and set to 0
                if file_ not in current_dict:
                    current_dict[file_] = 0
                    search_dict(current_dict, search_text)
                else:
                # if in current_dict, parse for search_txt
                    search_dict(current_dict, search_text)

        else:
            # if ext IS set
            for file_ in dir_files:
                file_ending = file_[file_.rindex('.'):]
                # and file has correct extension
                if file_ending == ext:
                    # add to current_dir
                    if file_ not in current_dict:
                        current_dict[file_] = 0
                        search_dict(current_dict, search_text)
                    else:
                        search_dict(current_dict, search_text)

        print(f'DICT AFTER WATCH_DIR FUNCT RUN:{current_dict}')
        # update state here
        state = current_dict
        compare(state=state, dict=current_dict)

    # else:
    #     # kill program?
    #     print(f'{dir_} is NOT a directory!')


def search_dict(dict_, text):
    '''Searches dict files for text.  Updates last line searched.
        Returns updated dict.
    '''
    if dict_:
        line_count = 0
        for path, value in dict_.items():
            print(f'START LINECOUNT: {path} ({line_count})')
            line_count = value
            with open(path) as f:
                for line in f.readlines()[line_count:]:
                    line_count += 1
                    if text in line:
                        # ----LOG
                        print(f'Found "{text}" in "{path}" (Line {line_count})')
            dict_[path] = line_count
        print(f'END LINECOUNT: {path} ({line_count})')
        # may not need
        return dict_

    else:
        print('Internal_dictionary IS empty!!!')


def compare(state=state, dict=current_dict):
    '''compares state with current_dir and logs any changes'''
    print(f'Current: {len(current_dict)}, state:{len(state)}')
    if len(state) < len(current_dict):
        for path in current_dict:
            if path not in state:
                print(f'"{path}" added to directory.')
    if len(state) > len(current_dict):
        for path in state:
            if path not in current_dict:
                print(f'"{path}" removed from directory.')


#-------left off here
def create_parser():
    parser = argparse.ArgumentParser(description="Program searches directory files for indicated text.")
    parser.add_argument('directory', help="Provide a directory path as a string.  The program will parse files in the directory for the search_text provided.", type=str)
    parser.add_argument('search_text', help="Provide a text string to search directory files.  If found, program will return filename and line number of text's location.", type=str)
    parser.add_argument('--interval', '-i', help="Provide an integer (in seconds).  Program will re-run itself once per second(s) indicated.", type=int)
    parser.add_argument('--extension', '-e', help="Provide a string text extension (e.g. '.pdf').  Program will filter query to only search for indicated file types.", type=str)
    return parser

def check_if_dirpath(path):
    if os.path.exists(os.path.dirname(path)):
        return str
    return None


def main(args):
    # ArgumentParser(prog='dirwatcher.py', usage=None, description=None,
        # formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error',
        # add_help=True)
    parser = create_parser()
    # Namespace(directory='/Users/tamoya/desktop/test_dir',
        # extension=None, interval=None, search_text='hello')
    ns = parser.parse_args(args)
    print(ns)

    if not args:
        # LOG
        parser.print_usage()

    if not os.path.exists(os.path.dirname(ns.directory)):
        # LOG
        print(f'ERROR: "{ns.directory}" is not a directory.  Please provide a directory string as your first argument.')
        parser.print_usage()

    # allow this to take array of filetypes?
    if ns.extension is not None:
        watch_dir(ns.directory, ns.search_text, ext=ns.extension)

    watch_dir(ns.directory, ns.search_text)




if __name__ == '__main__':
    main(sys.argv[1:])

# argparse args, logging, polling