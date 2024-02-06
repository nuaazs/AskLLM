# coding = utf-8
# @Time    : 2024-02-05  15:27:34
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Use Qwen API.

import requests
import json
import dashscope

def chat(Q,history):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
    messages.append({"role": "user", "content": Q})

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',
    )
    new_history = history
    new_history.append((Q,response['output']['choices'][0]['message']['content']))
    return response['output']['choices'][0]['message']['content'], new_history

if __name__ == '__main__':
    Q = "你好"
    history = []
    response = chat(Q, history)
    print(response)
    print("Done.")