import os
import sys


directory = sys.argv[1]


def to_lowercase(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for d in dirs:
            try:
                os.rename(os.path.join(root, d), os.path.join(root, d.lower()))
            except OSError:
                pass

        for file in files:
            try:
                os.rename(os.path.join(root, file), os.path.join(root, file.lower()))
            except OSError:
                pass


def to_uppercase(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for d in dirs:
            try:
                os.rename(os.path.join(root, d), os.path.join(root, d.upper()))
            except OSError:
                pass

        for file in files:
            if file == "z3.py":
                continue
            try:
                os.rename(os.path.join(root, file), os.path.join(root, file.upper()))
            except OSError:
                pass


to_lowercase(directory)
# to_uppercase(directory)
