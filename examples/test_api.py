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
import io

def test(user_audio,session_id):
    url = "http://localhost:8765/chat"
    # 审查HTTP头部：确保您的 Response 头部正确设置，特别是 Content-Type 应该设置为 audio/wav。
    response = requests.post(url, files={"audio": open(user_audio, "rb")}, data={"session_id": session_id}, stream=True)
   
    # if response.status_code == 200:
    print("开始接收流式数据")
    # 合并保存成一个output.wav
    output = []
    i = 0
    format = "wav"
    # 迭代响应的流式内容
    # 去除response中的非音频数据
    for chunk in response.iter_content(chunk_size=1024):  # 您可以根据需要调整 chunk_size 的大小
        if chunk:
            i += 1
            file_path = f"{tempfile.gettempdir()}/{i}.{format}"
            print(file_path)
            # 使用 pydub 处理音频数据
            # save chunk to tmp.wav
            # chunk.save(file_path)
            segment = AudioSegment.from_raw(io.BytesIO(chunk), sample_width=2, frame_rate=32000, channels=1)
            segment.export(file_path, format="wav")
            audio_data,sr = torchaudio.load(file_path)
            output.append(audio_data.reshape(-1))
    output = torch.cat(output)
    output = output.reshape(1,-1)
    torchaudio.save(f"output3.wav", output, sr)
    return

if __name__ == "__main__":
    test('init.wav', "zs130")



# import requests
# import torchaudio
# import torch

# def save_streamed_audio(url, audio_data, params):
#     """
#     发送音频数据到服务器，并流式接收响应音频，保存到文件中。
#     """
#     with requests.post(url, files=audio_data, data=params, stream=True) as r:
#         r.raise_for_status()
#         output = []
#         i = 0
#         # with open('received_audio.wav', 'wb') as f:
#         format = "wav"
#         total_size = 0
#         times = 0
#         for chunk in r.iter_content(chunk_size=1024):
#             times+=1
#             total_size += len(chunk)
#             #去掉chunk的前44byte
#             print(len(chunk))
#             # 打印 chunk的大小
#             # chunk = chunk[30:-30]
#             # 讲chunk转为16进制打印
#             chunk_text = chunk.hex()
#             print(chunk_text)
#             i += 1
#             # print(chunk)
#             file_path = f"{tempfile.gettempdir()}/{i}.{format}"
#             segment = AudioSegment(chunk, frame_rate=32000, sample_width=2, channels=1)
#             segment.export(file_path, format=format)
#             print("write")
#             audio_data,sr = torchaudio.load(file_path)
#             output.append(audio_data.reshape(-1))
#         print(total_size)
#         print(times)
#         output = torch.cat(output)
#         output = output.reshape(1,-1)
#         torchaudio.save(f"output3.wav", output, sr)


# if __name__ == '__main__':
#     url = "http://localhost:8765/chat"
#     audio_data = {'audio': open('init.wav', 'rb')}
#     params = {'session_id': 'zhaoshen1g213'}
#     save_streamed_audio(url, audio_data, params)

