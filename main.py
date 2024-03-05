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


# init chat server
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chatchat():
    # 1. Get audio file and session_id
    audio_file = request.files['audio']
    session_id = request.form.get('session_id')
    # 2. Get history qid from redis
    history = get_from_redis(f"{session_id}_history",[])
    now_qid = get_from_redis(f"{session_id}_qid",0)
    # 3. clean history
    history = [i for i in history if len(i) > 1]
    # 4. init Bot
    bot = Bot(history=history)
    # 5. ASR
    Q = bot.wav2text(audio_file)
    A,next_q_id = bot.get_response(Q,now_qid)
    history.append((Q, A))
    # 6. update history to redis
    save_to_redis(f"{session_id}_history",history)
    save_to_redis(f"{session_id}_qid",next_q_id)
    # 7. TTS (stream) and return
    chunks = bot.text2wav(A)
    def generate_audio(chunks):
        i = 0
        for chunk in chunks:
            if chunk:
                i += 1
                segment = AudioSegment(chunk, frame_rate=32000, sample_width=2, channels=1)
                filepath = f"/tmp/{i}.wav"
                segment.export(filepath, format='wav')
                data = open(filepath, "rb").read()[44:] # remove wav header
                yield data
    return Response(stream_with_context(generate_audio(chunks)), content_type="audio/wav")
    
if __name__ == "__main__":
    # Start chat server, 0.0.0.0 port 8765
    app.run(host='0.0.0.0', port=cfg.PORT, debug=False)