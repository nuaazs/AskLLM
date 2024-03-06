import json
import datetime
from utils.phone_utils import check_phone_bill  # Importing the required function
from bots.chat import send_message
import cfg
from utils.chatbot import llm_chat
import re
class Agent:

    def __init__(self):
        self.phone_number = ""
        self.id_number = ""

    @staticmethod
    def extract_dates(input_str):
        try:
            # Extract dates from the string
            # dates = json.loads(input_str)
            # start_date_str, end_date_str = dates
            # # Convert date strings to datetime objects
            # start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d')
            # end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d')
            # # Format datetime objects to specified string format
            # formatted_start_date = start_date.strftime('%Y-%m-%d')
            # formatted_end_date = end_date.strftime('%Y-%m-%d')

            # input str中除了数字外，还有其他所有非数字字符直接替换为空格
            input_str = re.sub(r'\D', ' ', input_str)
            print(input_str)
            # 用空格分隔字符串
            start_date_str = input_str.split()[-2]
            end_date_str = input_str.split()[-1]
            # Convert date strings to datetime objects
            formatted_start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d').strftime('%Y-%m-%d')
            formatted_end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d').strftime('%Y-%m-%d')

            # Build result dictionary
            result = {
                "start_date": formatted_start_date,
                "end_date": formatted_end_date
            }
        except Exception as e:
            print(e)
            # Use default dates when an error occurs, from the 1st of the current month to the current day
            today = datetime.datetime.today()
            start_date = today.replace(day=1)  # First day of the current month
            end_date = today

            result = {
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d')
            }
        return result

    def get_response(self, bot_text, user_text):
        today_str = datetime.datetime.today().strftime('%Y年%m月%d日')
        response_text = llm_chat(
            query=f"<用户文本>{user_text}</用户文本>\n请你帮我从用户文本中，抽取出他需要查询的时间区间。具体格式为:['开始时间','结束时间'],比如用户说1月份，你返回：['20240401','20240430']\n比如用户说3月份，你返回：['20240301','20240330']\n\n注：今天日期为：{today_str},如果时间在今天之后，则年份应该是前一年的",
            system=f"你是一个聊天机器人，你可以帮我从用户文本中，抽取出他需要查询的时间区间。具体格式为:['开始时间','结束时间'],比如用户说1月份，你返回：['20240401','20240430']\n比如用户说3月份，你返回：['20240301','20240330']\n\n注：今天日期为：{today_str}",
        )
        time_interval = self.extract_dates(response_text)

        if time_interval is None:  # 如果未提取到时间
            today = datetime.datetime.today()
            start_date = today.replace(day=1)  # 当月第一天
            end_date = today
        else:
            start_date = time_interval["start_date"]
            end_date = time_interval["end_date"]

        # 调用 check_phone_bill 函数查询账单信息
        bill_info = check_phone_bill(self.phone_number, start_date, end_date)
        print(f"start_date: {start_date}, end_date: {end_date}")
        print(f"bill_info: {bill_info}")
        # start_date -> YYYY-MM-DD
        # end_date -> YYYY-MM-DD
        start_date_str = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y年%m月%d日')
        end_date_str = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y年%m月%d日')
        if bill_info:
            # 准备账单信息的响应消息
            msg = f"查询到{start_date_str}到{end_date_str}时间内，您的账单信息如下：\n"
            for record in bill_info:
                msg += f"日期：{record['date']}，金额：{record['amount']}\n"
        else:
            msg = "抱歉，未能查询到您的账单信息"

        return msg