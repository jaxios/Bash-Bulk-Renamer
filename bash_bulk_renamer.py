import os
import shutil
import sys
from datetime import datetime
import json
import re
import mediaExifExtractor

VALID_FORMATS = [".jpg",".mp4",".jpeg"]



def print_help():
    syntax = open("README.md", "r", encoding="UTF-8")
    print(syntax.read())


def sanitize_folder_name(raw_folder):

    if (re.search(r"\[(.*)\]", raw_folder)) is not None: #Checks if there is an index before the folder name

        processed_folder = raw_folder.split('/')
        if processed_folder[-1] == "":
            return processed_folder[-2].split(' ', 1)[1]
        else:
            return processed_folder[-1].split(' ', 1)[1]
    else:
        processed_folder = raw_folder.split('/')
        if processed_folder[-1] == "":
            return processed_folder[-2]
        else:
            return processed_folder[-1]


def rename_file(path, raw_file, renamer_template, folder_name):

    file_extension = os.path.splitext(raw_file)[1]

    # for datetime we need to extract the format too
    date_format = re.search(r"datetime\(\"(.*)\"\)", renamer_template)
    date_format = str(date_format.group(1))

    renamer_template = renamer_template.replace(f"$datetime(\"{date_format}\")", mediaExifExtractor.get_exif_data(path+raw_file, "datetime", date_format))

    # replace wildcard in renamer_template with data
    renamer_template = re.sub("\[(.*)\]", "", renamer_template)
    renamer_template = renamer_template.replace("$folder", folder_name)
    renamer_template = renamer_template.replace("$device", mediaExifExtractor.get_exif_data(path+raw_file, "device", None)) 

    # convert extension to lower case
    new_file_name = renamer_template + file_extension.lower()

    return new_file_name

#==================================================================================================#

parameters = {
"DRY_RUN" : False,
"IN_PLACE" : False,
"RECURSIVE" : False,
"RESTORE" : False,
"IGNORE_MISSING_DATA" : False,
"VERBOSE" : False,
"CONFORMITY_CHECK" : False,
"NO_USER_INPUT" : False,
}
#Check arguments and syntax

if "--help" in sys.argv:
    print_help()
    sys.exit(0)

print("==================================================")

if len(sys.argv) < 3:
    print_help()
    sys.exit(1)

if not os.path.exists(sys.argv[1]):
    print("Non-existent target folder [" + sys.argv[1] + "]")
    print("==================================================")
    print_help()
    sys.exit(1)

target_path = sys.argv[1]
if target_path[-1] != "/": # add final slash if missing
    target_path = target_path + "/"

if "--restore" in sys.argv:
    parameters["RESTORE"] = True
else:
    if not os.path.isfile("./templates/"+sys.argv[2]):
        print("Non-existent template")
        print("==================================================")
        print_help()
        sys.exit(1)

if "--ignore-missing-data" in sys.argv:
    parameters["IGNORE_MISSING_DATA"] = True

if "--dry-run" in sys.argv:
    parameters["DRY_RUN"] = True
    parameters["VERBOSE"] = True
    parameters["IGNORE_MISSING_DATA"] = True

if "--in-place" in sys.argv:
    parameters["IN_PLACE"] = True

if "--recursive" in sys.argv:
    parameters["RECURSIVE"] = True

if "--verbose" in sys.argv:
    parameters["VERBOSE"] = True

if "--conformity-check" in sys.argv:
    parameters["CONFORMITY_CHECK"] = True
    parameters["DRY_RUN"] = True

print("Target path: " + target_path)
for key,val in parameters.items():
    print(f"{key} : {val}")

print("==================================================")


if parameters["RESTORE"]:
    log_list = []
    for f in os.listdir(target_path):
        ext = os.path.splitext(f)[1]
        if (os.path.isfile(target_path + f) and ext.lower() == ".json"):
            log_list.append(f)

    if len(log_list) == 1:
        target_log = log_list[0]
    else:
        i = 0
        for log in log_list:
            print(f"{i}: {log}")
            i+=1
        target_log = log_list[int(input("Which version to restore?: "))]

    with open(target_path + target_log, 'r', encoding="UTF-8") as openfile:
        #  Reading from json file
        backup = json.load(openfile)

    for old, new in backup.items():
        if old == "Datetime":
            continue

        print(new + " > " + old)
        if not parameters["DRY_RUN"]:
            shutil.move(target_path + new, target_path + old)

    sys.exit(0)


folders_list = []

if parameters["RECURSIVE"]:
    for subfolder in next(os.walk(target_path))[1]:
        folders_list.append(target_path + subfolder + "/")
else:
    folders_list.append(target_path)
    if len(next(os.walk(target_path))[1]) > 1:
        recursive_check = input("Subfolders detected, but no --recursive option used, are you sure to continue? (y/n) ")
        if "y" not in recursive_check:
            sys.exit(1)

for working_folder in folders_list:
    print("==================================================\n|_" + working_folder)

    # Sanitize folder name
    folder_name = sanitize_folder_name(working_folder) # returns folder name without leading index ([###])

    # Read and interpret template

    renamer_template = open("./templates/"+sys.argv[2], "r", encoding="UTF-8")
    renamer_template = renamer_template.read()
    index_digits = renamer_template.count("#")

    # cicle trough files and imports only certain formats

    original_files = []
    for f in os.listdir(working_folder):
        ext = os.path.splitext(f)[1]
        if (os.path.isfile(working_folder + f) and ext.lower() in VALID_FORMATS):
            original_files.append(f)

    # sort files by EXIF datetime
    sorted_files = []

    i=0
    for target_file in original_files:
        sorted_files.append([target_file, mediaExifExtractor.get_exif_data(working_folder+target_file,"datetime","%Y%m%d_%H%M%S")])
        print(f"Analyzing {i} files", end="\r")
        i+=1
    print(f"{i} files analyzed")
    sorted_files = sorted(sorted_files, key=lambda x:x[1])

    # rename files with log

    TIMESTAMP = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    if not parameters["DRY_RUN"] and not parameters["IN_PLACE"] and not os.path.exists(working_folder + "backup_ " + TIMESTAMP +"/"):
        os.makedirs(working_folder + "backup_ " + TIMESTAMP +"/")


    i = 1
    FILENAME_CHANGES = 0
    NO_EXIF = 0

    changelog = {} # store old and new name for logging and restore
    changelog["Datetime"] = TIMESTAMP

    for target_file in sorted_files:

        new_name = "[" + str(i).rjust(index_digits, "0") + "]" + rename_file(working_folder,target_file[0], renamer_template,folder_name)
        if parameters["VERBOSE"]:
            print("  |_ " + target_file[0] + "  ->  " + new_name)
        changelog[target_file[0]] = new_name

        if target_file[0] != new_name:
            FILENAME_CHANGES += 1
        if "No EXIF data" in new_name:
            NO_EXIF += 1

        if not parameters["DRY_RUN"]:

            print(f"Renamed {i} files", end="\r")

            if "No EXIF data" in new_name and parameters["IGNORE_MISSING_DATA"] is False:
                no_data_check = input("Not all files have complete EXIF data, continue anyway? (y/n) ")
                if "n" in no_data_check:
                    sys.exit(1)
                else:
                    parameters["IGNORE_MISSING_DATA"] = True

            if not parameters["IN_PLACE"]:
                shutil.copy2(working_folder + target_file[0], working_folder + "backup_ " + TIMESTAMP +"/" + target_file[0])
            shutil.move(working_folder + target_file[0], working_folder + new_name)
        else:
            print(f"Previewed {i} files", end="\r")
        i+=1

    if FILENAME_CHANGES > 0 and not parameters["DRY_RUN"]:

        print(f"{FILENAME_CHANGES} files renamed")
        # write log to json
        with open(working_folder + TIMESTAMP + ".json", "w", encoding="UTF-8") as outfile:
            outfile.write(json.dumps(changelog, indent=4))


    # Conformity check

    if parameters["CONFORMITY_CHECK"]:
        if FILENAME_CHANGES > 0:
            print(f"{FILENAME_CHANGES} files in {working_folder} do not conform to the template selected, {NO_EXIF} have missing EXIF data")
        else:
            print("Nothing to do")
