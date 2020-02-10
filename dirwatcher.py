#!/usr/bin/env python

import os, argparse, logging

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

    else:
        # kill program?
        print(f'{dir_} is NOT a directory!')


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
    parser = argparse.ArgumentParser()
    parser.add_argument()
    return parser


def main(args):
    parser = create_parser()

    if not args:
        # LOG later?
            parser.print_usage()


if __name__ == '__main__':
    watch_dir('/Users/tamoya/desktop/test_dir', 'hello', ext='.txt')
