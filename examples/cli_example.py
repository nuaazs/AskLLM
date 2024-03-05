import requests
import cfg
import random
# 设置 Flask 服务的 URL
FLASK_SERVER_URL = f"http://127.0.0.1:{cfg.PORT}/chat"
# 设置一个固定的 session_id
SESSION_ID = "test"
random_session_id = str(random.randint(1000, 9999))
SESSION_ID = SESSION_ID + random_session_id
def chat_with_bot(question):
    """向 Flask 应用发送问题并获取回答"""
    data = {
        'session_id': SESSION_ID,
        'Q': question
    }
    response = requests.post(FLASK_SERVER_URL, data=data)
    if response.status_code == 200:
        return response.json().get('A', '无法获取回答')
    else:
        return "请求失败"

def main():
    print("欢迎与机器人对话。输入 '退出' 来结束对话。")
    print("机器人：您好，这里是长江时代人工智能机器人。有什么可以帮助您的吗？")
    while True:
        user_input = input("你: ")
        if user_input.lower() == '退出':
            print("对话结束。")
            break
        bot_response = chat_with_bot(user_input)
        print(f"机器人: {bot_response}")

if __name__ == "__main__":
    main()
