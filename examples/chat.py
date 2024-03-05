import gradio as gr

def chat_with_bot(messages):
    responses = []
    for msg in messages:
        user_message = msg["message"]  # 用户的文本消息
        text_response = f"Echo: {user_message}"  # 文本回复
        # 音频文件链接，这里使用本地文件路径作为例子，实际应用中应使用可访问的URL
        audio_response = "/home/zhaosheng/Documents/AI_XIAOYI/asklm/tmp/1708926712.wav"
        # 将音频文件路径作为文本消息的一部分返回
        audio_message = f"Listen to the audio response here: file://{audio_response}"
        # 将文本回复和音频消息链接添加到回复中
        responses.extend([
            {"message": text_response, "is_user": False},
            {"message": audio_message, "is_user": False}
        ])
    return responses

iface = gr.Interface(
    fn=chat_with_bot,
    inputs=gr.Chatbot(),
    outputs=gr.Chatbot(),
    theme="default"
)

iface.launch()
