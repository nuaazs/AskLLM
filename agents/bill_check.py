from utils.agent import get_phone_number_list
from utils.phone_utils import check_phone_bill
from bots.chat import send_message
import cfg
import datetime
import json
from utils.llm import llm_chat
class Agent:

    def __init__(self):
        self.phone_number = ""
        self.id_number = ""
        pass
    
    def extract_dates(input_str):
        try:
            # 从字符串中提取日期
            dates = json.loads(input_str)
            start_date_str, end_date_str = dates
            
            # 将日期字符串转换为datetime对象
            start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d')
            
            # 将datetime对象格式化为指定的字符串格式
            formatted_start_date = start_date.strftime('%Y-%m-%d')
            formatted_end_date = end_date.strftime('%Y-%m-%d')
            
            # 构建结果字典
            result = {
                "start_date": formatted_start_date,
                "end_date": formatted_end_date
            }
        except Exception as e:
            # 出错时使用默认日期
            today = datetime.datetime.today()
            one_year_ago = today - datetime.timedelta(days=365)
            
            result = {
                "start_date": one_year_ago.strftime('%Y-%m-%d'),
                "end_date": today.strftime('%Y-%m-%d')
            }
        
        return json.dumps(result, indent=4)
    def get_response(self,bot_text,bot_label,user_text):
        response_text = llm_chat(
            query=f"<用户文本>{user_text}</用户文本>\n请你帮我从用户文本中，抽取出他需要查询的时间区间。比如['20240401','20240430']",
            system="你是一个聊天机器人，你可以帮我从用户文本中，抽取出他需要查询的时间区间。比如['20240401','20240430']具体格式为：['开始时间','结束时间']",
        )
        time_interval = self.extract_dates(response_text)
        start_date = time_interval["start_date"]
        end_date = time_interval["end_date"]
        ....
        msg = ""
        return msg