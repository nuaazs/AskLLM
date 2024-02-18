# coding = utf-8
# @Time    : 2024-02-06  14:08:56
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Logger.

import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('chat.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Print to console
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# stream_handler.setLevel(logging.INFO)
# logger.addHandler(stream_handler)

