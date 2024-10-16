# Bash utility for renaming items based on a given template

Usage: bash_bulk_renamer.py [target_path] [template_name] [--help] [--dry-run] [--in-place]

template_name : name of .template file in the ./templates folders
`--dry-run` : Print output without applying changes, implicit if using `--conformity-check`
`--in-place` : Renames files without backup (default behaviour: move original files in a "backup" folder)
`--ignore-missing-data` : Continues even if not all files have EXIF data, implicit if using `--dry-run`
`--restore` : automatic restore using .json log files (option to choose which version in case of multiple logs)
`--verbose` : Verbose output, implicit if using `--dry-run`
`--conformity-check` : Checks how many files are do not conform to the template
`--y` : Proceeds without asking for user input

Template guidelines:

- \# = Increasing number, increase number for leading zeros
- $datetime("YYYYmmdd_hhss") = datetime in the indicated format
- $device = the device based on EXIF data
- $folder = Name of the parent folder, excluding the first word (eg. [000] name, the "[000]" will get ignored)

- Extension is kept the same as the origin file and converted to lower case.
- Files are renamed base on ascending time.