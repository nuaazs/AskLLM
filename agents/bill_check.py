from utils.agent import get_phone_number_list
from utils.phone_utils import check_phone_bill
from bots.chat import send_message
import cfg

class Agent:

    def __init__(self):
        pass

    def get_response(self,bot_text,bot_label,user_text):
        phone_number_list = get_phone_number_list(user_text)
        phone_number_list = list(set(phone_number_list))
        phone_status = check_phone_bill(phone_number_list)
        msg = "你好，为您查询到的手机号码状态如下：\n"
        if phone_status == []:
            return "未找到有效的手机号码"
        for i in range(len(phone_number_list)):
            msg += f"手机号：{phone_number_list[i]}，的账单详情为：{phone_status[i]}"
        msg += "详细查询结果会发送到您的手机上，请注意查收。"
        msg += "\n请问还有什么可以帮到您的吗？"
        return msg