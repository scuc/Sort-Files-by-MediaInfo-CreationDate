#! /usr/bin/env python3

import exiftool
import json
import logging
import os
import subprocess

from pathlib import Path

import config as cfg

logger = logging.getLogger(__name__)

config = cfg.get_config()

root_path = config["paths"]["root_path"]


def get_exifinfo(f):

    os.chdir(root_path)
    print(os.getcwd())
    # file = os.path.join(root_path, f)
    file = f

    print("")
    print(file)
    print("")

    # exif_cmd = [ "exiftool", "-j", file ]

    # try: 
    #     sp = subprocess.Popen(
    #                         exif_cmd,
    #                         shell=False,
    #                         universal_newlines=True,
    #                         stdout=subprocess.PIPE
    #                         ).communicate()

    #     # output = sp.communicate()

    #     print("="*20)
    #     print(sp[0].splitlines())
    #     print("="*20)

    #     exif_output = sp
    #     exifdata = json.dumps(exif_output)

    #     print(f"\n EXIF OUTPUT: {exifdata} \n")

    #     exif_dict = exifdata.strip()
    #     encode_date = exif_dict["DateTimeOriginal"]
    #     print(f"\n ENCODE DATE: {encode_date} \n")


    # except Exception as excp:
    #     encode_err_msg = f"Exif error: {excp}"
    #     logger.error(encode_err_msg)



    with exiftool.ExifTool() as et:

        metadata = et.get_metadata(file)
        tags = et.get_tags(metadata, file)

        for key, value in tags.items(): 
            print(key, value)

    for tag in tags: 
        print(tag, tag.value())
        imagesize = et.get_tag('ImageSize', file)
        print(imagesize)
        imagesize = str(imagesize).split()
        print(imagesize)
    for d in metadata:
        print(d)

    #generate unique ID: 
    # date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    # UID = f"{str(date)}-{str(imagesize[0])}-{str(imagesize[1])}"
    # print(UID)

get_exifinfo(f="GOPR6483.JPG")