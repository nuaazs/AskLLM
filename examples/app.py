import gradio as gr
import requests
from IPython import embed
import soundfile as sf
import time
import torchaudio
import torch

# 定义与您的聊天服务器交互的函数
def chat_with_bot(user_audio, history,qid=0):
    if not qid:
        qid = 0
    # 指定您的聊天机器人服务的URL
    url = "http://localhost:8765/chat"
    # embed()
    # print(user_audio)
    # print(history)
    # 准备请求的数据，包括用户音频和历史记录
    
    data = {'history': history, 'qid': qid}
    

    # user_audio 是一个元组，包含采样率和音频数据
    sampling_rate, np_audio_data = user_audio
    audio_data = torch.tensor(np_audio_data, dtype=torch.float32).unsqueeze(0)  # Adds a channel dimension

    # 指定保存音频文件的路径和名称
    filename = f'/home/zhaosheng/Documents/AI_XIAOYI/asklm/tmp/{int(time.time())}.wav'
    torchaudio.save(filename, audio_data, sampling_rate)
    # files = {'user_audio': open(filename, 'rb')}
    data["file_path"] = filename
    response = requests.post(url, data=data)
    
    # 解析响应
    if response.status_code == 200:
        response_data = response.json()
        bot_audio_url = response_data['bot_audio']
        updated_history = response_data['history']
        qid = response_data['next_q_id']
        
        # 返回机器人的音频URL和更新后的历史记录
        return bot_audio_url, updated_history,qid
    else:
        # 发生错误时返回错误信息
        return "Error communicating with chat server", history,0

# 创建 Gradio 接口
iface = gr.Interface(
    fn=chat_with_bot,  # 指定处理函数
    # 定义输入：将用户麦克风录制的音频和历史记录文本框
    inputs=[gr.Audio(label="User Audio"), gr.Textbox(label="History"), gr.Textbox(label="Qid")],
    # 定义输出：机器人响应的音频和更新后的历史记录文本框
    outputs=[gr.Audio(label="Bot Response"), gr.Textbox(label="Updated History"), gr.Textbox(label="Qid")],
    live=False,  # 开启实时模式
)

# 启动 Gradio 应用
iface.launch()
