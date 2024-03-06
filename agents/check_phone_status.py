from utils.phone_utils import check_phone_status
import cfg
from bots.chat import send_message
from utils.chatbot import llm_chat

class Agent:

    def __init__(self):
        self.phone_number = ""
        self.id_number = ""

    def get_response(self, bot_text, user_text):
        phone_status = check_phone_status(self.phone_number)  # Calling the function from the imported script

        # Prepare the response message based on the phone status
        if phone_status["status"] == "正常":
            msg = f"您好，您的手机卡状态为正常，当前余额为{phone_status['balance']}元，套餐为{phone_status['package']}，剩余流量为{phone_status['remain_data']}，剩余通话时长为{phone_status['remain_call']}分钟。"
        elif phone_status["status"] == "停机":
            msg = "您好，您的手机卡已停机。"
        elif phone_status["status"] == "欠费":
            msg = f"您好，您的手机卡已欠费，欠费金额为{abs(float(phone_status['balance']))}元，请及时充值以恢复使用。"

        return msg
