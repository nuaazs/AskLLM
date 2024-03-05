import random
from phone_utils import check_phone_resource
from bots.chat import send_message
import cfg

class Agent:

    def __init__(self):
        self.phone_number = ""
        self.id_number = ""

    def get_response(self, bot_text, bot_label, user_text):
        total_resource = 100  # Assuming total available resource is 100GB
        resource = check_phone_resource(self.phone_number)
        remaining_resource = total_resource - resource

        # Prepare the response message
        msg = f"查询您号码包含{total_resource}GB，截至目前已使用{resource}GB，现剩余{remaining_resource}GB"

        return msg

        #口径：查询您号码包含xx分钟/G，截止目前已使用xx分钟/G，现剩余xx分钟/G。

