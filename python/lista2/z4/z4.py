import os
import sys
import hashlib

directory = sys.argv[1]


def repchecker(path) -> [str]:
    # filename : path
    rep_files = {}
    # (file_hash, file_size) : file_size
    file_dict = {}

    for root, dirs, files in os.walk(path):
        print("root: " + root)
        for file in files:
            file_data = open(file, 'r').read()
            file_hash = hashlib.md5(file_data.encode()).hexdigest()
            file_size = os.stat(file).st_size

            print("file: " + file)
            print("File hash: " + file_hash)
            print("Size: ", + file_size)

            if (file_hash, file_size) in file_dict.keys():
                rep_files[file] = root
            else:
                file_dict[(file_hash, file_size)] = file

    return rep_files


data = repchecker(directory)
print(data)
