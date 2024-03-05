import json
import datetime
from phone_utils import check_phone_balance
from bots.chat import send_message
import cfg

class Agent:

    def __init__(self):
        self.phone_number = ""
        self.id_number = ""



    def get_response(self, bot_text, bot_label, user_text):

        balance = check_phone_balance(self.phone_number)

        # Adjust the response message based on the balance
        if balance < 0:
            msg = f"您好，查询您号码目前已欠费，欠费金额为{abs(balance)}元"
        else:
            msg = f"您好，您查询号码余额为：{balance}元"

        return msg
