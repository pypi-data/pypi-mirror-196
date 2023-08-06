#!/usr/bin/env python3

import json
import os
import pathlib
from pathlib import Path
import re
from typing import Tuple, List


def is_identical(fpath_1: str, fpath_2: str) -> bool:
    file_contents = []
    for i, fpath in enumerate([fpath_1, fpath_2]):
        try:
            with open(fpath, "rb") as f:
                file_contents.append(f.read())
        except FileNotFoundError:
            print(f"Could not find file {fpath}")
        except UnicodeError:
            print(f"Unicode error while trying to read {fpath}")
        except:
            print(f"Could not read file {fpath}")

    if len(file_contents) == 2:
        return file_contents[0] == file_contents[1]
    return False


def load_json(fpath: str) -> dict:
    with open(fpath, "r") as f:
        data = json.load(f)
    return data


def get_all_fpaths_by_extension(root_fdir: str, exts: Tuple[str, ...], recursive=True) -> List[str]:
    """
    Recursively extracts all file paths to files ending with the given extension down the folder hierarchy (i.e. it
    includes subfolders).
    :param root_fdir: str. Root directory from where to start searching
    :param exts: Tuple of extension strings. e.g. (".txt", "WAV")
    :param recursive:
    :return: sorted list of file paths
    """

    # Standardise the extensions tuple.
    exts = (ext.lower() for ext in exts)
    # Make sure they have a preceding period
    exts = tuple([ext if ext.startswith(".") else "." + ext for ext in exts])

    if recursive:
        file_paths = [str(path) for path in Path(root_fdir).rglob('*') if path.suffix.lower() in exts]
    else:
        file_paths = [os.path.join(root_fdir, fname) for fname in sorted(os.listdir(root_fdir)) if fname.endswith(exts)]
    return sorted(file_paths)


def add_numbering_to_mp3splt_files(fdir):
    files: list[str] = sorted(os.listdir(fdir))
    timestamp_pattern = re.compile(r"_\d{3}m_\d\ds__\d{3}m_\d\ds(_\d\dh)?")
    for i, fname in enumerate(files):
        print(f"Processing {fname}.")
        file_timestamp = timestamp_pattern.search(string=fname).group()
        fname_new = f"{i + 1:02} - {fname.replace(file_timestamp, '')}"
        src = pathlib.Path(fdir, fname)
        dst = pathlib.Path(fdir, fname_new)
        src.rename(dst)  # No need to read/write as binary with "with open()" etc.



if __name__ == "__main__":
    fpath_1 = "/media/findux/DATA/potholes/Potholes Dataset-20230123T145709Z-007b.zip"
    fpath_2 = "/media/findux/DATA/potholes/Potholes Dataset-20230123T145709Z-007.zip"
    # print(is_identical(fpath_1, fpath_2))
    add_numbering_to_mp3splt_files("/home/findux/Desktop/DMI/test1/")


