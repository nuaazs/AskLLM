import gradio as gr
import requests
import soundfile as sf
import time
import torchaudio
import torch
import cfg
import tempfile
from flask import Flask, request, jsonify, Response
from pydub import AudioSegment

def chat_with_bot(user_audio,session_id):

    url = "http://localhost:8765/chat"
    sampling_rate, np_audio_data = user_audio
    audio_data = torch.tensor(np_audio_data, dtype=torch.float32).unsqueeze(0)
    filename = f'/tmp/{int(time.time())}.wav'
    torchaudio.save(filename, audio_data, sampling_rate)
    # 发送请求，并确保设置 stream=True 来获取流式响应
    response = requests.post(url, files={"audio": open(filename, "rb")}, data={"session_id": session_id}, stream=True)

    # if response.status_code == 200:
    print("开始接收流式数据")
    i = 0
    format = "wav"
    # 迭代响应的流式内容
    for chunk in response.iter_content(chunk_size=1024):  # 您可以根据需要调整 chunk_size 的大小
        if chunk:  # 过滤掉保活新行
            i += 1
            file_path = f"{tempfile.gettempdir()}/{i}.{format}"
            print(file_path)
            # 使用 pydub 处理音频数据
            segment = AudioSegment(chunk, frame_rate=32000, sample_width=2, channels=1)
            segment.export(file_path, format=format)
            yield file_path


with gr.Blocks(title='AI-XiaoXu') as demo:
    # 使用 gr.HTML 来实现图片和文本的居中
    gr.HTML(value="""
    <div style='text-align: center;'>
        <img src='https://shengbucket.oss-cn-hangzhou.aliyuncs.com/files/xiaoxu2.png' style='display: block; margin-left: auto; margin-right: auto; max-width: 10%; height: auto;' />
        <h1>AI-XiaoXu (A Customer Service Robot)</h1>
        <h3>Danxiaoxu intelligent customer service robot internal demonstration and interactive system</h3>
        <h3>版权所有@龙垣科技</h3>
    </div>
    """)
    with gr.Row():
        init_message = cfg.start_text
        chatbot = gr.Chatbot(value=[("bot", init_message)])
    with gr.Column():
        with gr.Row():
            with gr.Column():
                session_id = gr.Textbox(visible=True, label="对话ID")
                gr.Markdown("请上传您的语音文件")
                audio = gr.Audio()
            with gr.Column():
                gr.Markdown("机器人回复")
                bot_response_audio = gr.Audio(value="init.wav",
                                              streaming=True,
                                              autoplay=True,
                                              interactive=False)
        with gr.Row():
            send_button = gr.Button("发送 🚀")
            clear_button = gr.Button("清除 💣")
        with gr.Row():
            qid = gr.Textbox(visible=False, label="qid")

            
    # def get_new_history():
    #     history_text = 

    def clear_chatbot():
        chatbot.value = []  # Clear chatbot history directly

    send_button.click(chat_with_bot, inputs=[audio,session_id], outputs=[bot_response_audio])
    clear_button.click(clear_chatbot, inputs=[], outputs=[chatbot])

demo.launch()
