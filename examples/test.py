# coding = utf-8
# @Time    : 2024-02-26  11:46:24
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: AI Chat bot.

import os
import time
import torch
import gradio as gr
import pandas as pd
from argparse import ArgumentParser
from flask import Flask, request, jsonify

# utils
import cfg
from bots.common import Bot

# init bot
bot = Bot()

bot_audio_file = bot.text2wav("你好，我是智能客服小助手，很高兴为您服务。")
bot_asr_result = bot.wav2text(bot_audio_file)
print(f"bot_audio_file: {bot_audio_file}")
print(f"bot_asr_result: {bot_asr_result}")