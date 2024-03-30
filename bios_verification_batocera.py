import os
import glob
import sys
import getopt
import hashlib

def args_retrieving(argv):
    arg_readme = "./readme.txt"
    arg_bios_dir = "./"
    arg_help = \
f"""ERROR PARSING ARGUMENTS
-----------------------
{argv[0]} -r <readme file> -d <bios directory path>"""
    
    try:
        opts, args = getopt.getopt(argv[1:], "hr:d:", ["help","readme=", "biosdir="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-h', '--help']:
            print(arg_help)
            sys.exit(2)
        if opt in ['-r', '--readme']:
            arg_readme = arg
        if opt in ['-d', '--biosdir']:
            arg_bios_dir = arg 
    
    return arg_readme, arg_bios_dir

def get_bios_md5(arg_bios_dir):
    md5_dict = {}
    for root, dirs, files in os.walk(arg_bios_dir):
        for file in files:
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, arg_bios_dir)
            with open(filepath, "rb") as f:
                data = f.read()
                md5_hash = hashlib.md5(data).hexdigest()
                md5_dict[relative_path] = md5_hash
    return md5_dict



if __name__ == "__main__":
    arg_readme, arg_bios_dir = args_retrieving(sys.argv)
    bios_md5 = get_bios_md5(arg_bios_dir)
