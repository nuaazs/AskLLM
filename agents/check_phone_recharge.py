import json
import datetime
from phone_utils import check_phone_recharge
from bots.chat import send_message
import cfg

class Agent:

    def __init__(self):
        self.phone_number = ""
        self.id_number = ""

    @staticmethod
    def extract_dates(input_str):
        try:
            # Extract dates from the string
            dates = json.loads(input_str)
            start_date_str, end_date_str = dates
            # Convert date strings to datetime objects
            start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d')
            # Format datetime objects to specified string format
            formatted_start_date = start_date.strftime('%Y-%m-%d')
            formatted_end_date = end_date.strftime('%Y-%m-%d')

            # Build result dictionary
            result = {
                "start_date": formatted_start_date,
                "end_date": formatted_end_date
            }
        except Exception as e:
            # Return None if no dates are provided
            return None
        return result

    def get_response(self, bot_text, bot_label, user_text):
        response_text = llm_chat(
            query=f"<用户文本>{user_text}</用户文本>\n请你帮我从用户文本中，抽取出他需要查询的时间区间。比如['20240401','20240430']",
            system="你是一个聊天机器人，你可以帮我从用户文本中，抽取出他需要查询的时间区间。比如['20240401','20240430']具体格式为:['开始时间','结束时间']",
        )
        time_interval = self.extract_dates(response_text)

        if time_interval is None:
            # No time interval provided, retrieve the most recent record
            recharge_records = check_phone_recharge(self.phone_number)
            if recharge_records:
                # Extract the most recent record
                most_recent_record = max(recharge_records,key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'))
                # Prepare the response message for the most recent record
                msg = f"查询到您最近的充值记录如下：\n日期：{most_recent_record['date']}，金额：{most_recent_record['amount']}"
            else:
                msg = "抱歉，没有找到任何充值记录。"
        else:
            start_date = time_interval["start_date"]
            end_date = time_interval["end_date"]
            # Retrieve recharge records within the specified time interval
            recharge_records = check_phone_recharge(self.phone_number, start_date, end_date)

            if recharge_records:
                # Prepare the response message for the recharge records within the specified time interval
                msg = "查询到您的充值记录如下：\n"
                for record in recharge_records:
                    msg += f"日期：{record['date']}，金额：{record['amount']}\n"
            else:
                msg = "在指定时间范围内未找到任何充值记录。"

        return msg
