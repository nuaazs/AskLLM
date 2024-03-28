# coding = utf-8
# @Time    : 2024-02-26  11:46:24
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: AI Chat bot.

import os
import time
import torch
import tempfile
import gradio as gr
import pandas as pd
from argparse import ArgumentParser
from flask import Flask, request, jsonify, Response, stream_with_context
from pydub import AudioSegment
import torchaudio
import io

# utils
import cfg
from bots.common import Bot
from utils.database import save_to_redis, get_from_redis

# log
from utils.log_wrapper import logger
logger.info("Start chat server.")

if __name__ == "__main__":
   
    history = []
    now_qid = 0
    meet_qid = []
    bot = Bot(history=history,meet_qid=meet_qid)
    a_id,score,found_text = bot.query_text("查话费")
    print(a_id,score,found_text)