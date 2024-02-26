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

# init chat server
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chatchat():
    # 1. user audio file  2. history string
    user_audio = request.files.get('user_audio')
    history = request.form.get('history')
    # 2. change history to list
    history = history.split("@@")
    history = [tuple(i.split("&&")) for i in history]
    # 3. bot chat
    bot.history = history
    Q = bot.wav2text(user_audio)
    A = bot.get_response(Q)
    # 4. return response
    history.append((Q, A))
    history = "@@".join(["&&".join(i) for i in history])
    bot_audio_url = bot.text2wav(A,oss=True)
    return jsonify({'bot_audio': bot_audio_url, 'history': history})

if __name__ == "__main__":
    # Start chat server, 0.0.0.0 port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)