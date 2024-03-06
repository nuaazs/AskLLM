# coding = utf-8
# @Time    : 2024-02-27  14:32:41
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Agent Common Module.

import pandas as pd
import importlib
import requests
import cfg
import time
import asyncio
import websockets
import ssl
import json
import os

from utils.agent import get_choosed_result_n_times_try
from bots.chat import send_message
from utils.log_wrapper import logger

# Load all agents
from agents.container import ALL_AGENTS

# Import specific data, split by \t
df = pd.read_csv(cfg.data_path, encoding='utf-8', dtype={'a_id':str}, sep='\t')
# fill nan with ""
df = df.fillna("")

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
    next_bot_q_id = int(next_bot_q_id)
    next_bot_text = df[df['q_id'] == int(next_bot_q_id)]['text'].values[0]
    next_agent = df[df['q_id'] == int(next_bot_q_id)]['agent'].values[0]
    jump_text = df[df['q_id'] == int(next_bot_q_id)]['jump_text'].values[0]
    prefix_first = df[df['q_id'] == int(next_bot_q_id)]['prefix_first'].values[0]
    return {
        "next_bot_q_id": next_bot_q_id,
        "next_bot_text": next_bot_text,
        "next_agent": next_agent,
        "error_bot_q_id": None,
        "jump_text": jump_text,
        "prefix_first": prefix_first,
        "if_error": None
    }

async def send_audio_file_and_receive_text(WEBSOCKET_HOST,audio_file_path):
    ssl_context = ssl.SSLContext()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    uri = f"wss://{WEBSOCKET_HOST}"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        with open(audio_file_path, 'rb') as f:
            audio_data = f.read()
        await websocket.send(audio_data)
        await websocket.send(json.dumps({"is_speaking": False}))
        result = await websocket.recv()
        result_dict = json.loads(result)
        return result_dict.get('text', '')

class Bot():
    def __init__(self,history,meet_qid):
        self.history = history
        self.meet_qid = meet_qid
        logger.info(f"Init Bot with history: {history}, meet_qid: {meet_qid}")

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

        
        ASR_WEBSOCKET_HOST = cfg.ASR_WEBSOCKET_HOST
        # return asyncio.get_event_loop().run_until_complete(send_audio_file_and_receive_text(ASR_WEBSOCKET_HOST,audio_file_path))

        # save wav_file_content to audio_file_path
        # wav_file_content is FileStorage object
        audio_file_path = f"/tmp/{int(time.time())}.wav"
        with open(audio_file_path, 'wb') as f:
            f.write(wav_file_content.read())
        # make audio_file_path to 1 channel, 16k by ffmpeg
        audio_file_output_path = f"/tmp/{int(time.time())}_16k.wav"
        os.system(f"ffmpeg -i {audio_file_path} -ac 1 -ar 16000 {audio_file_output_path}")

        return asyncio.run(send_audio_file_and_receive_text(ASR_WEBSOCKET_HOST, audio_file_output_path))

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
            n = cfg.query_times
        )
        # Get answer type id
        aid = get_aid(now_qid,r_text)
        # Get the next question and other information
        result = next_q(now_qid,aid)

        next_q_id = result['next_bot_q_id']
        bot_response = result['next_bot_text']
        next_agent = result['next_agent']
        prefix_first = result['prefix_first']
        add_prefix = False
        if now_qid not in self.meet_qid:
            self.meet_qid.append(now_qid)
            bot_response = prefix_first + "\n" + bot_response
            add_prefix = True

        if next_agent and next_agent in ALL_AGENTS:
            agent = ALL_AGENTS[next_agent]
            agent_response = agent.get_response(bot_response,user_question)
            msg = ""
            # if agent, update data
            logger.info(f"Before update: {next_q_id}")
            msg += f"{bot_response}"
            next_q_id = int(df[df['q_id'] == next_q_id]['next_q_id'].values[0])
            new_prefix_first = str(df[df['q_id'] == int(next_q_id)]['prefix_first'].values[0])
            new_text = str(df[df['q_id'] == int(next_q_id)]['text'].values[0])
            
            if add_prefix:
                msg += f"\n{new_prefix_first}\n{agent_response}\n{new_text}"
            else:
                msg += f"\n{agent_response}\n{new_text}"
            logger.info(f"Agent response: {agent_response}")
            logger.info(f"Bot response: {bot_response}")
            logger.info(f"Pefix first: {prefix_first}")
            logger.info(f"Now qid: {now_qid}, Next qid: {next_q_id}")
            logger.info(f"Next qid: {next_q_id}")
            logger.info(f"New prefix first: {new_prefix_first}")
            logger.info(f"New text: {new_text}")
            return msg,0
        else:
            return bot_response,next_q_id

