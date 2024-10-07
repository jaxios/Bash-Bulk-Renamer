import os
import shutil
import sys
import mediaExifExtractor

def print_help():
    syntax = open("README.md", "r")
    print(syntax.read())


def sanitize_folder_name(folder):
    folder = folder.split('/')
    
    if folder[-1] == "":
        return folder[-2].split(' ', 1)[1]
    else:
        return folder[-1].split(' ', 1)[1]

def get_exif_data(file, data):

    #extract EXIF information from file

    result = mediaExifExtractor.get_exif_data(file, data)

    return result



def rename_file(path, target_file, renamer_template, folder):

    file_extension = os.path.splitext(target_file)[1]

    #replace wildcard in renamer_template with data
    renamer_template = renamer_template.replace("[", "")
    renamer_template = renamer_template.replace("%", "")
    renamer_template = renamer_template.replace("]", "")
    renamer_template = renamer_template.replace("$folder", folder)
    renamer_template = renamer_template.replace("$datetime", get_exif_data(path+target_file, "datetime"))
    renamer_template = renamer_template.replace("$device", get_exif_data(path+target_file, "device"))

    #convert extension to lower case
    new_file_name = renamer_template + file_extension.lower()

    return new_file_name

#==================================================================================================#

DRY_RUN=False
IN_PLACE=False

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

if not os.path.isfile("./templates/"+sys.argv[2]):
    print("Non-existent template")
    print("==================================================")
    print_help()
    sys.exit(1)

if "--dry-run" in sys.argv:
    DRY_RUN=True
if "--in-place" in sys.argv:
    IN_PLACE=True

print(target_path)
print("Dry run: "+str(DRY_RUN))
print("In place: "+str(IN_PLACE))

print("==================================================")

#Sanitize folder name
folder_name = sanitize_folder_name(target_path)
#complete_path = str(pathlib.Path(__file__).parent.resolve()) + target_path.replace(".", "")
complete_path = target_path
#create log and write parameters

log_file = open(complete_path + "log.txt", "w")
log_file.write("Target: "+ target_path + "\n")
log_file.write("Dry run: "+str(DRY_RUN) + "\n")
log_file.write("In place: "+str(IN_PLACE) + "\n\n")



#Read and interpret template

renamer_template = open("./templates/"+sys.argv[2], "r")
renamer_template = renamer_template.read()
index_digits = renamer_template.count("%")


#cicle trough files and imports only certain formats

valid_formats = [".jpg",".mp4",".jpeg"]
original_files = []
for f in os.listdir(target_path):
    ext = os.path.splitext(f)[1]
    if (os.path.isfile(target_path + f) and ext.lower() in valid_formats):
        original_files.append(f)

#sort files by EXIF datetime
sorted_files = []
for target_file in original_files:
    sorted_files.append([target_file, get_exif_data(complete_path+target_file,"datetime")])

sorted_files = sorted(sorted_files, key=lambda x:x[1])

#rename files with log

if not DRY_RUN and not os.path.exists(target_path + "backup/"):
    os.makedirs(target_path + "backup/")


i = 1
IGNORE_MISSING_DATA = False

for target_file in sorted_files:
    new_name = "[" + str(i).rjust(index_digits, "0") + "]" + rename_file(complete_path,target_file[0], renamer_template,folder_name)
    print(target_file[0] + " > " + new_name)
    log_file.write(target_file[0] + " > " + new_name + "\n")

    if not DRY_RUN:

        if "No EXIF data" in new_name and IGNORE_MISSING_DATA is False:
            no_data_check = input("Not all files have complete EXIF data, continue anyway? (y/n)")
            if "n" in no_data_check:
                sys.exit(1)
            else:
                IGNORE_MISSING_DATA = True

        if not IN_PLACE:
            shutil.copy2(target_path + target_file[0], target_path + "backup/" + target_file[0])
        shutil.move(target_path + target_file[0], target_path + new_name)


    i+=1

log_file.close()
