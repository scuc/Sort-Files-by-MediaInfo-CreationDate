#!/usr/bin/env python3

import logging
import os
import re
import shutil

from pathlib import Path

import config as cfg

logger = logging.getLogger(__name__)

config = cfg.get_config()

dir_dest_path = config["destination path"]


def get_sort_list(dir_path):
    """
    Create are list of MP4 files in a given directory. 
    """
    sorted_file_list = sorted(
        [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        )

    dir_msg = f"Checking dir path for files:  {dir_path}"
    mp4_list_msg = f"{len(sorted_file_list)} unsorted files found."

    logger.info(dir_msg)
    logger.info(mp4_list_msg)

    return sorted_file_list


def sort_into_dirs(sorted_bydate_list, path):
    """
    Takes a list of files, checks metadata for a creation date.
    """

    print(f"================== PATH: {path}   ============================")
    count = 0
    start_sort_msg = f"Starting Sort for files in dir: {path}"
    logger.info(start_sort_msg)

    for tup in sorted_bydate_list:

        mp4, file_src_path, dir_name = check_subdirs(tup, path)

        source_path = Path(path, mp4)
        file_dst_path = Path(dir_dest_path, dir_name, mp4)
        print(f"================== FILE SRC PATH: {file_src_path}   ============================")
        print(f"================== FILE DST PATH: {file_dst_path}   ============================")
        shutil.move(source_path, file_dst_path)

        sort_msg = f"{mp4} moved to: {dir_name}" 
        logger.info(sort_msg)

    return 


def check_subdirs(tup, path): 
    """
    Check the subdir for existing year-month dirs, if they dont already
    exist, mkdir. 
    """

    mp4 = tup[0]
    file_src_path = Path(path, mp4)

    datetime = tup[1].split()

    year = datetime[1][:4]
    month = datetime[1][5:7]
    day = datetime[1][8:10]

    dir_name = f"{year}-{month}-{day}"
    dir_dst_path = Path(dir_dest_path, dir_name)

    chk_subdir_msg = f"Checking sub-directories for {dir_dst_path}"
    logger.info(chk_subdir_msg)

    if not dir_dst_path.exists():
        dir_dst_path.mkdir()
        dir_msg = f"Creating new directory {dir_dst_path}"
        logger.info(dir_msg)
    else: 
        dir_msg = f"Directory already exists for:  {dir_dst_path}"
        logger.info(dir_msg)

    file_dst_path = Path(dir_dst_path, mp4)
    if not file_dst_path.exists(): 
        file_msg = f"{mp4} does not exist in: {dir_dst_path}"
        logger.info(file_msg)
        file_src_path = Path(path, mp4)

    else:
        file_msg = f"{mp4} already exists in: {dir_dst_path}\n\
                                        Appending file name before move."
        logger.info(file_msg)
        mp4_split = mp4.split(".")
        mp4 = f"{mp4_split[0]}_{year}{month}{day}.{mp4_split[1]}"
        
        source = Path(path, tup[0])
        target = Path(path, mp4)
        source.replace(target)

        file_src_path = Path(path, mp4)
        

    return mp4, file_src_path, dir_name
            

    #         mp4 = nchk.append_filename(dir_path, month_path, mp4, mp4_output_path)
    #         mp4_path = Path(dir_path, mp4)
    
    # return year, month, mp4_path



if __name__ == '__main__':
    get_sort_list()
