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

# Embedding Model
from BCEmbedding import EmbeddingModel
from BCEmbedding import RerankerModel
import numpy as np
# init embedding model
model = EmbeddingModel(model_name_or_path="maidalun1020/bce-embedding-base_v1")


# Import specific data, split by \t
df = pd.read_csv(cfg.data_path, encoding='utf-8', dtype={'a_id':str}, sep='\t')
# fill nan with ""
df = df.fillna("")
# 如果df不存在pattern列，则添加pattern列，值为""
if 'pattern' not in df.columns:
    df['pattern'] = ""
re_text_aid_list = df[['a_id','text','pattern']].values.tolist()
re_text_aid_list = [(a_id,text,pattern) for a_id,text,pattern in re_text_aid_list if text]
def get_aid_by_re(text):
    for a_id,text,pattern in re_text_aid_list:
        pattern_list = pattern.split("@@")
        for p in pattern_list:
            if p == "":
                continue
            if re.search(p,text):
                return a_id,text,pattern
    return None,None,None

# Load all text database
df_text = pd.read_csv(cfg.text_data_path, encoding='utf-8', dtype={'a_id':str}, sep='\t')
print(df_text.head())
# return_text列用""填充Nan
df_text = df_text.fillna("")
text_list = df_text[['a_id','text','return_text','next_q_id']].values.tolist()
text_embedding_list = [(a_id,model.encode([text])[0],text,return_text,next_q_id) for a_id,text,return_text,next_q_id in text_list if text]

def cosine_similarity(embedding1,embedding2):
    return np.dot(embedding1,embedding2)/(np.linalg.norm(embedding1)*np.linalg.norm(embedding2))

def get_top_n_similar_text(query_text,n=10):
    query_embedding = model.encode([query_text])[0]
    sim_list = [(a_id,cosine_similarity(query_embedding,text_embedding),text,return_text,next_q_id) for a_id,text_embedding,text,return_text,next_q_id in text_embedding_list]
    sim_list = sorted(sim_list,key=lambda x:x[1],reverse=True)
    return sim_list[:n]


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
    print(f"Function next_q: {qid}, {aid}")
    try:
        next_bot_q_id = df[(df['q_id'] == qid) & (df['a_id'] == aid)]['next_q_id'].values[0]
    except:
        q_id = 0
        next_bot_q_id = 0
    next_bot_q_id = int(next_bot_q_id)
    print(f"Found next bot qid: {next_bot_q_id}")
    next_bot_text = df[df['q_id'] == int(next_bot_q_id)]['text'].values[0]
    next_agent = df[df['q_id'] == int(next_bot_q_id)]['agent'].values[0]
    jump_text = df[df['q_id'] == int(next_bot_q_id)]['jump_text'].values[0]
    prefix_first = df[df['q_id'] == int(next_bot_q_id)]['prefix_first'].values[0]

    # 如果next_bot_q_id的text只有一个
    if len(df[df['q_id'] == int(next_bot_q_id)]) == 1:
        print(f"Only one text: {next_bot_q_id}")
        next_next_bot_q_id = df[df['q_id'] == int(next_bot_q_id)]['next_q_id'].values[0]
        if next_next_bot_q_id == 0:
            next_next_bot_text = df[df['q_id'] == int(next_bot_q_id)]['text'].values[0]
            next_next_agent = df[df['q_id'] == int(next_bot_q_id)]['agent'].values[0]
            next_next_jump_text = df[df['q_id'] == int(next_bot_q_id)]['jump_text'].values[0]

            next_bot_q_id = int(next_next_bot_q_id)
            next_bot_text = next_next_bot_text + "\n" + next_next_jump_text
        
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
        # response = requests.request("POST", cfg.ASR_URL, headers=headers, data=payload, files=files)
        # return response.json()['transcription']['text']

        
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

    def query_text_by_re(self,text):
        a_id,text,pattern = get_aid_by_re(text)
        if a_id:
            return a_id,text,pattern
        else:
            return None,None,None
        

    def query_text(self,text,n=10,rerank=False):
        # extract embeddings
        sim_list = get_top_n_similar_text(text,n=n)

        # if rerank:
        #     query = text
        #     passages = [sim[1] for sim in sim_list]
        #     ids = [sim[0] for sim in sim_list]
        #     # construct sentence pairs
        #     sentence_pairs = [[query, passage] for passage in passages]
        #     # init reranker model
        #     model = RerankerModel(model_name_or_path="maidalun1020/bce-reranker-base_v1")
        #     # method 0: calculate scores of sentence pairs
        #     scores = model.compute_score(sentence_pairs)
        #     # method 1: rerank passages
        #     rerank_results = model.rerank(query, passages)
        #     sim_list = list(zip(ids,rerank_results))

        best_a_id = sim_list[0][0]
        best_score = sim_list[0][1]
        found_text = sim_list[0][2]
        return_text = sim_list[0][3] if sim_list[0][3] else ""
        next_q_id = sim_list[0][4] if sim_list[0][4] else 0

        print(sim_list)
    
        if best_score > cfg.SCORE_THRESHOLD:
            return best_a_id,best_score,found_text,return_text,next_q_id
        else:
            return None,None,None,None,None


    def get_response(self,user_question,now_qid=0):
        aid,text,pattern = self.query_text_by_re(user_question)
        if not aid:
            aid,score,found_text,return_text,next_q_id_from_query = self.query_text(user_question)
            if not aid:
                choose_list = df[df['q_id'] == int(now_qid)]['a'].values
                if now_qid == 0:
                    self.history = []
                r_index,r_text = get_choosed_result_n_times_try(
                    item_list = choose_list,
                    history = self.history,
                    human_question = user_question,
                    question = "用户最后的回复中表达的意思是什么？",
                    n = cfg.query_times
                )
                # Get answer type id
                aid = get_aid(now_qid,r_text)
                # Get the next question and other information
            else:
                print(return_text)
                return_text = return_text.strip()
                print(f"Found aid: {aid} with score: {score} and text: {found_text}")
                print(f"Skip choose list.")
        else:
            print(f"Found aid by re: {aid} with text: {text} and pattern: {pattern}")
            print(f"Skip choose list.")

        
        if return_text:
            print(f"return_text: {return_text}")
            bot_response = return_text
            next_q_id = next_q_id_from_query
            return bot_response,next_q_id

        else:
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

