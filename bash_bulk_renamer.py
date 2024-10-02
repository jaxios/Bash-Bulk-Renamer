import os
import sys

def print_help():
    syntax = open("README.md", "r")
    print(syntax.read())

dry_run=False
in_place=False

#Check arguments and syntax

if len(sys.argv) < 2:
    print_help()
    exit(1)

if "--help" in sys.argv:
    print_help()
    exit(0)

template = sys.argv[1]
if not os.path.isfile("./templates/"+template):
    print_help()
    exit(1)

if "--dry-run" in sys.argv:
    print("Dry run active")
    dry_run = True

if "--in-place" in sys.argv:
    print("Dry run active")
    in_place = True
