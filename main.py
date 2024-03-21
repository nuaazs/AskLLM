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

# init chat server
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chatchat():
    init_time = time.time()
    
    # 1. Get session_id
    if cfg.MODE == "phone" or cfg.MODE == "chat":
        session_id = request.form.get('session_id')
    elif cfg.MODE == "wechat":
        session_id = request.form.get('openid')
    else:
        return jsonify(
            {"code":0,
             "A": "Please check your request.",
             "data":{
                "type":"text",
                "title":"Error",
                "description":"Please check your request.",
                "pic_url":"",
                "text":"Please check your request."},
            "message":"Success",
            })
    
    phone_num = request.form.get('phone_num','15151832002')
    # 2. Get history qid from redis
    history = get_from_redis(f"{session_id}_history",[])
    now_qid = get_from_redis(f"{session_id}_qid",0)
    if now_qid < 0:
        now_qid = 0
    meet_qid = get_from_redis(f"{session_id}_meet_qid",[])
    # 3. clean history
    history = [i for i in history if len(i) > 1]
    history = history[-cfg.HISTORY_LEN:]
    # 4. init Bot
    bot = Bot(history=history,meet_qid=meet_qid)
    logger.info(f"Init time: {time.time()-init_time}")
    
    if cfg.MODE == "phone":
        # 5. ASR
        asr_start_time = time.time()
        audio_file = request.files['audio']
        Q = bot.wav2text(audio_file)
        logger.info(f"ASR time: {time.time()-asr_start_time}")
    elif cfg.MODE == "chat":
        Q = request.form.get('Q')
    elif cfg.MODE == "wechat":
        Q = request.form.get('text')
    
    bot_time = time.time()
    A,next_q_id = bot.get_response(Q,now_qid)
    history.append((Q, A))
    # 6. update history to redis
    save_to_redis(f"{session_id}_history",history)
    save_to_redis(f"{session_id}_qid",next_q_id)
    save_to_redis(f"{session_id}_meet_qid",meet_qid)
    logger.info(f"Bot time: {time.time()-bot_time}")
    

    if cfg.MODE == "phone":
        return jsonify({"A":A,"audio_id":['id001',"我是周坤坤，我不是鸡哥，我是鸡王",'id019']})
        # 7. TTS (stream) and return
        # tts_start_time = time.time()
        # chunks = bot.text2wav(A)
        # def generate_audio(chunks):
        #     i = 0
        #     for chunk in chunks:
        #         if chunk:
        #             if i==0:
        #                 logger.info(f"TTS time: {time.time()-tts_start_time}")
        #             i += 1
        #             segment = AudioSegment(chunk, frame_rate=32000, sample_width=2, channels=1)
        #             filepath = f"/tmp/{i}.wav"
        #             segment.export(filepath, format='wav')
        #             data = open(filepath, "rb").read()[44:] # remove wav header
        #             yield data
        # return Response(stream_with_context(generate_audio(chunks)), content_type="audio/wav")
    elif cfg.MODE == "chat":
        return jsonify({"A":A})
    elif cfg.MODE == "wechat":
        return jsonify(
            {"code":0,
             "data":{
                "type":"text",
                "title":"",
                "description":"",
                "pic_url":"",
                "text":A},
            "message":"Success",
            })
    else:
        return jsonify({"A":A})
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=cfg.PORT, debug=False)