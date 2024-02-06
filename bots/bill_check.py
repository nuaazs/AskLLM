from utils.agent import get_phone_number_list
from utils.phone_utils import check_phone_bill
from bots.chat import send_message
import cfg

class Agent:

    def __init__(self,history,phones):
        self.history = history
        self.phones = phones

    def agent_chat(self,bot_text,human_text):
        """ Get the status of the phone number list """
        self.history.append((bot_text,human_text))
        phone_number_list = get_phone_number_list(human_text)
        self.phones.extend(phone_number_list)
        self.phones = list(set(self.phones))
        phone_status = check_phone_bill(self.phones)
        msg = "你好，为您查询到的手机号码状态如下：\n"
        
        if phone_status == []:
            return "未找到有效的手机号码"

        for i in range(len(self.phones)):
            msg += f"手机号：{self.phones[i]}，的账单详情为：{phone_status[i]}"
        msg += "详细查询结果会发送到您的手机上，请注意查收。"
        msg += "\n请问还有什么可以帮到您的吗？"
        return msg