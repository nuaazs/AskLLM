from phone_utils import check_phone_location
import cfg
from bots.chat import send_message

class Agent:

    def __init__(self):
        self.phone_number = ""
        self.id_number = ""

    def get_response(self, bot_text, bot_label, user_text):
        location_info = check_phone_location(self.phone_number)  # Calling the function from the imported script

        # Prepare the response message
        msg = f"您好，查询您的号码归属地为：{location_info}"
    #您好，查询您的号码归属地为xx，您好，查询您的PIN码为xxx，（PUK码仅可告知PUK1码，PIN码如不对可告知尝试初始值0000。），您好，查询您的ICCID码为xxx，仅可根据号码查询ICCID码，无法根据ICCID码反向查询号码，如果用户有ICCID不知道号码，建议用户把卡板合照拍到公众号客服后查询
        return msg
