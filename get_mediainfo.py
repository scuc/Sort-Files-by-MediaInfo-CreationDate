#!/usr/bin/env python3

import logging
import os

from pymediainfo import MediaInfo

import config as cfg

logger = logging.getLogger(__name__)

config = cfg.get_config()


def get_mediainfo(mp4, path):
    """
    Get the mediainfo on a file, and check for a creation date. 
    """
    # check_mediainfo_msg = f"Checking mediainfo for file: {mp4}"
    # logger.info(check_mediainfo_msg)

    media_info = MediaInfo.parse(os.path.join(path, mp4))

    for track in media_info.tracks:
        if track.track_type == 'General':
            encoded_date = track.encoded_date

    logger.info(f"{mp4} Encoded_date = {encoded_date}")
    return encoded_date


if __name__ == '__main__':
    get_mediainfo(mp4="GX016550.MP4", mp4_path="/Users/stevencucolo/Desktop/test/GX016550.MP4")
