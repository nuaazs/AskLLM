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



# init chat server
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chatchat():
    # init bot
    
    # 1. user audio file  2. history string
    file_path = request.form.get('file_path')
    history_text = request.form.get('history')
    now_qid = request.form.get('qid',0)
    # 2. change history to list
    history_list_1 = history_text.split("@@")
    history = [tuple(i.split("&&")) for i in history_list_1]
    print(f"Raw history: {history}")
    # 去除空字符串或者长度小于2的项
    history = [i for i in history if len(i) > 1]
    # 3. bot chat
    # bot.history = history
    bot = Bot(history=history)


    Q = bot.wav2text(file_path)
    A,next_q_id = bot.get_response(Q,now_qid)
    # 4. return response
    # if history == []:
    #     history = [("您好，这边是长江时代客服中心，请问有什么可以帮您？", Q)]
    # else:
    history.append((Q, A))
    print(history)
    history_text = "@@".join(["&&".join(i) for i in history])
    bot_audio_url = bot.text2wav(A,oss=True)
    return jsonify({'bot_audio': bot_audio_url, 'history': history_text, 'next_q_id': next_q_id})

if __name__ == "__main__":
    # Start chat server, 0.0.0.0 port 5000
    app.run(host='0.0.0.0', port=8765, debug=False)