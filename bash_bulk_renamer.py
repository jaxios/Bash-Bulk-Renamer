import os
import sys
import datetime
import pathlib
from PIL import Image, ExifTags

def print_help():
    syntax = open("README.md", "r")
    print(syntax.read())


def sanitize_folder_name(folder):
    folder = folder.split(' ', 1)[1]
    folder = folder.replace("/", "")
    return folder

def get_exif_data(file, data):

    #extract EXIF information from file

    mediafile = Image.open(file)
    mediafile_exif = mediafile.getexif()
    # <class 'PIL.Image.Exif'>

    if mediafile_exif is None:
        print('Sorry, image has no exif data.')
    else:
        for key, val in mediafile_exif.items():
            if key in ExifTags.TAGS:
                if data in f'{ExifTags.TAGS[key]}:{val}':
                    if data == "DateTime":
                        exif_date = val
                        exif_date = datetime.datetime.strptime(exif_date, "%Y:%m:%d %H:%M:%S")
                        exif_date = exif_date.strftime("%Y%m%d_%H%M%S")
                        result = exif_date
                    elif data == "Model":
                        exif_device = val
                        result = exif_device
            #else:
                #exif_infos.add(f'{key}:{val}')

    return result



def name_from_template(path, target_file, renamer_template, folder):

    file_extension = os.path.splitext(target_file)[1]

    #replace wildcard in renamer_template with data
    renamer_template = renamer_template.replace("[", "")
    renamer_template = renamer_template.replace("%", "")
    renamer_template = renamer_template.replace("]", "")
    renamer_template = renamer_template.replace("$folder", folder)
    renamer_template = renamer_template.replace("$datetime", get_exif_data(path+target_file, "DateTime"))
    renamer_template = renamer_template.replace("$device", get_exif_data(path+target_file, "Model"))

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
    print("Non-existent target folder")
    print("==================================================")
    print_help()
    sys.exit(1)

target_path = sys.argv[1]

print("Target: "+target_path)

if not os.path.isfile("./templates/"+sys.argv[2]):
    print("Non-existent template")
    print("==================================================")
    print_help()
    sys.exit(1)

if "--dry-run" in sys.argv:
    DRY_RUN=True
if "--in-place" in sys.argv:
    IN_PLACE=True

print("Dry run: "+str(DRY_RUN))
print("In place: "+str(IN_PLACE))

print("==================================================")

#Sanitize folder name
folder_name = sanitize_folder_name(target_path)
complete_path = str(pathlib.Path(__file__).parent.resolve()) + target_path.replace(".", "")

#Read and interpret template

renamer_template = open("./templates/"+sys.argv[2], "r")
renamer_template = renamer_template.read()
index_digits = renamer_template.count("%")


#cicle trough files sorts them

original_files = [f for f in os.listdir(target_path) 
                  if os.path.isfile(os.path.join(target_path, f))]

sorted_files = set()
for target_file in original_files:
    sorted_files.add(target_file, get_exif_data(target_file, "DateTime"))

#rename files

i = 1
for target_file in original_files:
    new_name = "[" + str(i).rjust(index_digits, "0") + "]" + name_from_template(complete_path,target_file, renamer_template,folder_name)
    print(target_file + " > " + new_name)
    i+=1
