# coding = utf-8
# @Time    : 2024-02-27  14:32:41
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Agent Common Module.

import pandas as pd
import importlib
import requests
import cfg
import time

from utils.agent import get_choosed_result_n_times_try
from bots.chat import send_message
from utils.log_wrapper import logger

# Load all agents
from agents.container import ALL_AGENTS

# Import specific data, split by \t
df = pd.read_csv(cfg.data_path, encoding='utf-8', dtype={'a_id':str}, sep='\t')
logger.info(f"# Load data from {cfg.data_path}")

def get_aid(qid,a_text):
    """ Get the aid by qid and r_text """
    df_selected = df[df['q_id'] == int(qid)]
    df_selected = df_selected[df_selected['a'] == a_text]
    aid = df_selected['a_id'].values[0]
    return aid

def next_q(qid,aid):
    """ Get the next question """
    qid = int(qid)
    # print(f"Qid: {qid}, Aid: {aid}")
    next_bot_q_id = df[(df['q_id'] == qid) & (df['a_id'] == aid)]['next_q_id'].values[0]
    next_bot_text = df[df['q_id'] == int(next_bot_q_id)]['text'].values[0]
    next_agent = df[df['q_id'] == int(next_bot_q_id)]['agent'].values[0]
    label = df[df['q_id'] == int(next_bot_q_id)]['label'].values[0]
    # if_error = df[df['q_id'] == int(next_bot_q_id)]['if_error'].values[0]
    prefix = df[df['q_id'] == int(next_bot_q_id)]['prefix'].values[0]
    prefix_first = df[df['q_id'] == int(next_bot_q_id)]['prefix_first'].values[0]
    return {
        "next_bot_q_id": next_bot_q_id,
        "next_bot_text": next_bot_text,
        "next_agent": next_agent,
        "error_bot_q_id": None,
        "next_bot_label": label,
        "prefix": prefix,
        "prefix_first": prefix_first,
        "if_error": None
    }

class Bot():
    def __init__(self,history):
        self.history = history

    def wav2text(self,wav_file_content):
        payload={"spkid":"zhaosheng"}
        files=[
        ('wav_file',(f'audio_{int(time.time())}.wav',wav_file_content))
        ]
        headers = {
            'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)'
            }
        response = requests.request("POST", cfg.ASR_URL, headers=headers, data=payload, files=files)
        return response.json()['transcription']['text']

    def text2wav(self,text,oss=False):
        headers = {'Content-Type': 'application/json'}
        data = {
            'ref_wav_path': '/datasets_ssd/models/badXT-GPT-SoVITS/audio/badXT/badXT_88.wav',
            'prompt_text': '你如果没有办法证明这句话是，真的的话那它就是假的，懂了吧这就是。',
            'prompt_language': '中文',
            'text': text,
            'text_language': '中文',
            'how_to_cut': '不切', # 按标点符号切
            'top_k': 5,
            'top_p': 1.0,
            'temperature': 1.0
        }
        response = requests.post(cfg.TTS_URL, json=data, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    def get_response(self,user_question,now_qid=0):
        choose_list = df[df['q_id'] == int(now_qid)]['a'].values
        r_index,r_text = get_choosed_result_n_times_try(
            item_list = choose_list,
            history = self.history,
            human_question = user_question,
            question = "用户的表达的意思是什么？",
            n = 1
        )
        # Get answer type id
        aid = get_aid(now_qid,r_text)
        # Get the next question and other information
        result = next_q(now_qid,aid)

        next_q_id = result['next_bot_q_id']
        bot_response = result['next_bot_text']
        next_agent = result['next_agent']
        next_bot_label = result['next_bot_label']

        if next_agent and next_agent in ALL_AGENTS:
            agent = ALL_AGENTS[next_agent]
            agnet_response = agent.get_response(bot_response,next_bot_label,user_question)
            next_q_id = 0
            return agnet_response,next_q_id
        else:
            return bot_response,next_q_id

