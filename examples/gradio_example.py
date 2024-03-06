import gradio as gr
import requests
import cfg
import random

# 设置 Flask 服务的 URL
FLASK_SERVER_URL = f"http://127.0.0.1:{cfg.PORT}/chat"
# 初始化对话历史
chat_history = []

def chat_with_bot(question,session_id,history):
    """向 Flask 应用发送问题并获取回答，同时更新对话历史"""
    # 设置一个固定的 session_id，并附加一个随机数以确保唯一性
    # session_id = "test" + str(random.randint(1000, 9999))
    data = {
        'session_id': session_id,
        'Q': question
    }
    response = requests.post(FLASK_SERVER_URL, data=data)
    R = response.json().get('A', '无法获取回答')
    history.append((question, R))
    return history




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

    # 试听init.wav
    gr.Audio("/home/zhaosheng/Documents/AI_XIAOYI/asklm/examples/init.wav", autoplay=False, label="音色示例") #, description="点击播放示例")
    # Random generate session_id for each user
    session_id = str(random.randint(100000, 999999))

    with gr.Row():
        init_message = cfg.start_text
        history = [("", init_message)]
        chatbot = gr.Chatbot(value=history, label="对话历史")
    with gr.Column():
        with gr.Row():
            # with gr.Column():
                # session_id = gr.Textbox(visible=True, label="对话ID", value="15151832002")
            # with gr.Column():
            user_input = gr.Textbox(label="用户输入")
            session_id = gr.Textbox(label="对话ID", value=session_id)
        with gr.Row():
            clear_button = gr.Button("清除 💣")
            send_button = gr.Button("发送 🚀")
            

            
    # def get_new_history():
    #     history_text = 

    def clear_chatbot():
        chatbot.value = []  # Clear chatbot history directly
        session_id = str(random.randint(100000, 999999))
        return session_id,[]

    send_button.click(chat_with_bot, inputs=[user_input,session_id,chatbot], outputs=[chatbot])
    clear_button.click(clear_chatbot, inputs=[], outputs=[session_id,chatbot])
# port 7863
demo.launch(server_name='0.0.0.0',server_port=7863)