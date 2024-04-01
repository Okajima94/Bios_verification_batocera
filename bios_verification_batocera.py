import os
import sys
import getopt
import hashlib


def args_retrieving(argv):
    arg_readme = "./readme.txt"
    arg_bios_dir = "./"
    arg_help = f"""ERROR PARSING ARGUMENTS
-----------------------
{argv[0]} -r <readme file> -d <bios directory path>"""

    try:
        opts, _ = getopt.getopt(argv[1:], "hr:d:", ["help", "readme=", "biosdir="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print(arg_help)
            sys.exit(2)
        if opt in ["-r", "--readme"]:
            arg_readme = arg
        if opt in ["-d", "--biosdir"]:
            arg_bios_dir = arg

    return arg_readme, arg_bios_dir


def get_bios_md5(arg_bios_dir):
    md5_dict = {}
    for root, _, files in os.walk(arg_bios_dir):
        for file in files:
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, arg_bios_dir)
            relative_path_with_prefix = os.path.join("bios", relative_path)
            with open(filepath, "rb") as f:
                data = f.read()
                md5_hash = hashlib.md5(data).hexdigest()
                md5_dict[relative_path_with_prefix] = md5_hash
    return md5_dict


def read_md5(arg_readme):
    md5_sums = {}
    with open(arg_readme, "r") as f:
        for line in f.readlines():
            line = line.strip("\n")
            line = line.split(" ")
            if len(line) == 2 and len(line[0]) > 0 and line[1].startswith("bios/"):
                if md5_sums.get(line[1]):
                    md5_sums[line[1]].append(line[0])
                else:
                    md5_sums[line[1]] = [line[0]]
    return md5_sums


def compare_bios(bios_md5: dict, md5_sums: dict) -> tuple[list[str], list[str]]:
    unlisted = []
    wrong_sums = []
    for path, md5 in bios_md5.items():
        sums = md5_sums.get(path)
        if sums:
            if md5 not in sums:
                wrong_sums.append(path)
        else:
            unlisted.append(path)
    return unlisted, wrong_sums


if __name__ == "__main__":
    # ANSI escape code for red color
    RED = "\033[91m"
    # ANSI escape code for orange color
    ORANGE = "\033[38;2;255;165;0m"
    # ANSI escape code to reset color
    RESET = "\033[0m"
    arg_readme, arg_bios_dir = args_retrieving(sys.argv)
    bios_md5 = get_bios_md5(arg_bios_dir)
    md5_sums = read_md5(arg_readme)
    unlisted, wrong_sums = compare_bios(bios_md5, md5_sums)
    print(f"{ORANGE}Unlisted BIOS files\n{RESET}{chr(10).join(unlisted)}\n")
    print(f"{RED}Wrong BIOS files\n{RESET}{chr(10).join(wrong_sums)}")
