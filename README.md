# Directory Watcher Program
This program will search an entire directory's files (or defined segment of a directory's files) for specified text.  If text is in the directory, the program will output the filename and line number of text location.

# Program configuration
To start the program, use $python <directory path> <search> <optional flag>.

Directory path: full path string that you want to search (e.g. '/Users/tamoya/Desktop/Directory-Watcher')
Search: string to parse the directory with.  (e.g. 'hello world')
Optional Flags:
    --interval or -i: customize the program to poll itself every Nseconds.  Default setting is: 1.0 seconds.
    (Example: $dirwatcher.py 'Users/jane/Desktop/Directory-Watcher' 'hello world' -i 2)

    --extension or -e: filter the directory to only search files with specific extensions. Program searches all files by default.
    (Example: $dirwatcher.py 'Users/jane/Desktop/Directory-Watcher' 'hello world' -i 2 -e '.pdf')