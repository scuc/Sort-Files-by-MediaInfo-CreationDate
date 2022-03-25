
import logging
import logging.config
import os
from turtle import end_fill
import yaml

from datetime import datetime, date
from time import localtime, strftime

import config as cfg
# import get_exifinfo as exifinfo
import get_mediainfo as mediainfo
import sort_by_date as sort

logger = logging.getLogger(__name__)

config = cfg.get_config()

path_list = config["source paths"]


def set_logger():
    """
    Setup logging configuration
    """
    path = './logging.yaml'

    with open(path, 'rt') as f:
        config = yaml.safe_load(f.read())

    # get the file name from the handlers, append the date to the filename. 
        for i in (config["handlers"].keys()):
            if 'filename' in config['handlers'][i]:
                log_filename = config["handlers"][i]["filename"]
                base, extension = os.path.splitext(log_filename)
                today = datetime.today()
                log_filename = "{}_{}{}".format(base,
                                                today.strftime("%Y%m%d"),
                                                extension)
                config["handlers"][i]["filename"] = log_filename
            else:
                continue

        logger = logging.config.dictConfig(config)

    return logger


def main(): 
    """

    """
    date_start = str(strftime('%A, %d. %B %Y %I:%M%p', localtime()))

    start_msg = f"\n\
    ==================================================================================\n\
                 CLEAN and SORT BY DATE - Start - {date_start} \n\
    ==================================================================================\n\
   "

    logger.info(start_msg)
    encoded_none = []
    tuple_list = []

    for path in path_list: 
        sorted_file_list = sort.get_sort_list(path)

        for f in sorted_file_list: 
            if ( 
                f.lower().endswith(".mp4") or
                f.lower().endswith(".mov")
                ):
                encoded_date = mediainfo.get_mediainfo(f, path)
            
            else: 
                continue
             
            # if (
            #     f.lower().endswith(".jpg")
            #     or f.lower().endswith(".jpeg")
            #     or f.lower().endswith(".png")
            #     ):
            #     # encoded_date = exifinfo.get_exifinfo(f)
            #     continue

            if encoded_date == None:  
                continue
            else:
                tuple_list.append((f, encoded_date))
                
        sorted_bydate_list = sorted(tuple_list, key = lambda x: x[1])  

        # for x in sort_bydate_list:
        #     print(x)   
    
        sort.sort_into_dirs(sorted_bydate_list, path)
 
    complete_msg()

    
def complete_msg():

    date_end = str(strftime('%A, %d. %B %Y %I:%M%p', localtime()))

    complete_msg = f"\n\
    ================================================================================\n\
                    Complete - {date_end} \n\
    ================================================================================\n\
    "

    logger.info(complete_msg)

    return 


if __name__ == '__main__':
    set_logger()
    main()