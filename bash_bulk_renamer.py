import os
import sys
from PIL import Image, ExifTags
import datetime
import pathlib

def print_help():
    syntax = open("README.md", "r")
    print(syntax.read())


def sanitize_folder_name(folder):
    folder = folder.split(' ', 1)[1]
    folder = folder.replace("/", "")
    return folder

def name_from_template(path, file, template, folder):

    #Get template and filename components
    template_components = template.read().split()
    file_name, file_extension = os.path.splitext(file)
    
    #replace wildcard in template with actual foldername
    template = folder.replace("$folder", folder)

    #extract EXIF information from file

    mediafile = Image.open(path+file)
    mediafile_exif = mediafile.getexif()
    print(type(mediafile_exif))
    # <class 'PIL.Image.Exif'>

    if mediafile_exif is None:
        print('Sorry, image has no exif data.')
    else:
        for key, val in mediafile_exif.items():
            if key in ExifTags.TAGS:
                print(f'{ExifTags.TAGS[key]}:{val}')
            else:
                print(f'{key}:{val}')


    new_file_name = template + file_extension

    return new_file_name







dry_run=False
in_place=False

#Check arguments and syntax

if "--help" in sys.argv:
    print_help()
    exit(0)

print("==================================================")
if len(sys.argv) < 3:
    print_help()
    exit(1)

if not os.path.exists(sys.argv[1]):
    print("Non-existent target folder")
    print("==================================================")
    print_help()
    exit(1)

target_path = sys.argv[1]

print("Target: "+target_path)

if not os.path.isfile("./templates/"+sys.argv[2]):
    print("Non-existent template")
    print("==================================================")
    print_help()
    exit(1)

if "--dry-run" in sys.argv:
    dry_run=True
if "--in-place" in sys.argv:
    in_place=True

print("Dry run: "+str(dry_run))
print("In place: "+str(in_place))

print("==================================================")

#Sanitize folder name
folder_name = sanitize_folder_name(target_path)
complete_path = str(pathlib.Path(__file__).parent.resolve()) + target_path.replace(".", "")

#Read and interpret template

template = open("./templates/"+sys.argv[2], "r")
original_files = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]

for file in original_files:
    new_name = name_from_template(complete_path,file, template,folder_name)
    print(new_name)

