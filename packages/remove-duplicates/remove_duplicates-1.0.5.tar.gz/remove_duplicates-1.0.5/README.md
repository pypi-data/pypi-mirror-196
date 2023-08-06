Utility to recursive search and move/delete duplicate files of the same size and context in specified folder.

If the storage folder (recycle_bin) is not specified, then duplicate files will be deleted!
If the number of command line parameters is zero, then the search folder = current folder.

### Command line parameters
    -st, --start_folder (first parameter): the folder with which the recursive search begins
    -rb, --recycle_bin (second parameter): optional folder for storing duplicate files (move file).
    -log, --log_file: log file.
    -fnp, --fn_pattern: File name pattern. Only files matching the pattern are processed!
                   Provides support for Unix shell-style wildcards. Default value is "*.*"
    -nr, --not_recursively": If this parameter is set, then recursive search is disabled!

### Call example
    rmdup --start_folder=E:\YoutubeChannelsCopy --recycle_bin=E:\reserved --log_file=E:\reserved\logfile.txt --fn_pattern="*.png" 
## Work log
![alt text](https://github.com/octaprog7/remove_duplicates/blob/master/warn_del.png)
## PyPi
https://pypi.org/project/remove-duplicates/

After installation use rmdup --help instead of remove_dup

## Internationalization
Most of the program messages are translated into five languages: English, Russian, German, Spanish, French.