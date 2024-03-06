import json
import datetime
from utils.phone_utils import check_phone_recharge
from bots.chat import send_message
import cfg
from utils.chatbot import llm_chat

class Agent:

    def __init__(self):
        self.phone_number = ""
        self.id_number = ""

    @staticmethod
    def extract_date(input_str):
        try:
            # 从字符串中提取日期
            date_str = json.loads(input_str)[0]  # 假设日期是列表中的第一个元素
            # 将日期字符串转换为 datetime 对象
            date = datetime.datetime.strptime(date_str, '%Y%m%d')
            # 将 datetime 对象格式化为指定的字符串格式
            formatted_date = date.strftime('%Y-%m-%d')

            # 构建结果字典
            result = {
                "date": formatted_date
            }
        except Exception as e:
            # 如果未提取到日期信息，返回 None
            return None
        return result

    def get_response(self, bot_text, user_text):
        response_text = llm_chat(
            query=f"<用户文本>{user_text}</用户文本>\n请你帮我从用户文本中，抽取出他需要查询的时间。比如['20240401'],如果只有月份，则提取到月份，比如['202404']",
            system="你是一个聊天机器人，你可以帮我从用户文本中，抽取出他需要查询的时间。比如['20240401'],如果只有月份，则提取到月份，比如['202404']具体格式为：['查询时间']]",
        )
        time_info = self.extract_date(response_text)

        if time_info is None or len(time_info["date"]) == 6:
            # 如果未提供查询时间或者只提供了月份，则查询当月所有充值记录
            today = datetime.datetime.today()
            start_date = today.replace(day=1).strftime('%Y-%m-%d')  # 当月第一天
            end_date = today.strftime('%Y-%m-%d')  # 当天
            recharge_records = check_phone_recharge(self.phone_number, start_date, end_date)
            if recharge_records:
                # 准备当月所有充值记录的响应消息
                msg = "查询到您本月的充值记录如下：\n"
                for record in recharge_records:
                    msg += f"日期：{record['date']}，金额：{record['amount']}\n"
            else:
                msg = "本月未找到任何充值记录。"
        else:
            query_date = time_info["date"]
            # 调用 check_phone_recharge 函数查询充值记录
            recharge_records = check_phone_recharge(self.phone_number, query_date)

            if recharge_records:
                # 准备充值记录的响应消息
                msg = "查询到您的充值记录如下：\n"
                for record in recharge_records:
                    msg += f"日期：{record['date']}，金额：{record['amount']}\n"
            else:
                # 如果未找到指定日期的充值记录，则查询距离指定日期最近一次的充值记录
                last_record = check_phone_recharge(self.phone_number, query_date)
                if last_record:
                    msg = f"查询到最近的一次充值记录如下：\n日期：{last_record[0]['date']}，金额：{last_record[0]['amount']}"
                else:
                    msg = f"在指定时间 {query_date} 未找到任何充值记录。"

        return msg
