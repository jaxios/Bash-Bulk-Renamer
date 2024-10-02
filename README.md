Bash utility for renaming items based on a given template

% = Increasing number, increase number for leading zeros
$datetime("YYYYmmdd_hhss") = datetime in the indicated format
$device = the device based on EXIF data
$folder = Name of the parent folder, excluding index if present (eg. [000] lorem ipsum)

Extension is kept the same as the origin file and converted to lower case.
Files are renamed base on ascending time.