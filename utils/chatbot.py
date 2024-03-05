# coding = utf-8
# @Time    : 2024-02-05  15:27:34
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Use Qwen API.

import requests
import json
import dashscope
from utils.log_wrapper import logger

def chat(Q,history):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
    messages.append({"role": "user", "content": Q})

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',
    )
    logger.info(f"Q(chat): {Q}")
    logger.info(f"A: {response['output']['choices'][0]['message']['content']}")
    return response['output']['choices'][0]['message']['content'], history

def llm_chat(query, system):
    messages = [{'role': 'system', 'content': system}]
    messages.append({"role": "user", "content": query})
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',
    )
    logger.info(f"Q(llm_chat): {query}")
    logger.info(f"A: {response['output']['choices'][0]['message']['content']}")
    return response['output']['choices'][0]['message']['content']

if __name__ == '__main__':
    Q = "你好"
    history = []
    response = chat(Q, history)
    print(response)
    print("Done.")