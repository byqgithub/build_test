# -*- coding: utf-8 -*-

import os
import difflib

root_path = "D:\\download\\http_range_download\\backup_20190408\\hua_jun\\"


def get_file_range(file_name):
    """  """
    start = 0
    size = -1
    file_range = file_name.partition('(')[-1].partition(")")[0].split("-")
    if len(file_range) == 2:
        start = int(file_range[0]) if len(file_range[0]) != 0 else 0
        size = (int(file_range[1]) - start + 1) if len(file_range[1]) != 0 else -1
    return start, size


def compare_file(path):
    """  """
    compare_result = False
    file_list = list()
    all_file_name = str()
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if "all" not in file_name:
                file_list.append(file_name)
            else:
                all_file_name = file_name

    if all_file_name:
        with open(os.path.join(path, all_file_name), errors="ignore") as all_file:
            for name in file_list:
                start, size = get_file_range(name)
                all_file.seek(start)
                with open(os.path.join(path, name), errors="ignore") as f:
                    content_range = f.read()
                    content_part = all_file.read(len(content_range)).splitlines()
                    content_range = content_range.splitlines()
                    matcher = difflib.SequenceMatcher(None, content_range, content_part)
                    print("")
                    print("part len: %s; range len: %s" % (len(content_part), len(content_range)))
                    if round(matcher.ratio(), 3) == 1:
                        compare_result = True

    return compare_result


if "__main__" == __name__:
    result = compare_file(root_path)
    print("Compare result: %s" % result)
