import random
import cfg
from bots.chat import send_message
from phone_utils import check_phone_card_plan
class Agent:

    def __init__(self):
        self.phone_number = ""
        self.id_number = ""

    def get_response(self, bot_text, bot_label, user_text):
        plan = check_phone_card_plan(self.phone_number)  # Calling the function from the imported script

        # Prepare the response message
        msg = f"您的手机卡套餐为：{plan['package']}，月租：{plan['monthly rent']}元，流量：{plan['remain_data']}，剩余通话时长：{plan['remain_call']}分钟"
 #您是我司电信靓号-89用户，具体资费内容为套餐费89元/月，赠送60分钟全国主叫通话和20G全国流量，超出后语音0.15元/分钟，流量3元/G日包，当日有效，自动续订；短信0.1元/条，彩信0.5元/条，赠送来电显示，其它执行标准资费。入网当月按天折算套餐费和资源；合约期2年，期间禁止停机保号仅可变更为同系列高档套餐次月生效。

        return msg




