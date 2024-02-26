import sys
sys.path.append('..')

import re
from utils.chatbot import chat

def replace_non_digits_with_space(s):
    # 使用正则表达式替换非数字字符为一个空格
    return re.sub(r'\D', ' ', s)

def request_Q(Q, history):
    """ Chat with the model (offline) """
    response, history = chat(Q, history=history)
    print(f"response: #{response} #")
    return response, history

def get_phone_number_list(text):
    """ Get the phone number list from the model (offline) """
    Q = f"请你以下内容，帮我提取所有有效的手机号码，以列表的形式给我：\n"
    Q += f"<内容>：{text}</内容>"
    Q += f"\n告诉我答案，不需要任何解释，不需要任何其他文本。回答格式<json>，例如：[\"12345678901\",\"12345678902\"]"
    response, history = request_Q(Q, [])
    # 从response中提取手机号码列表
    # 将response中非数字字符替换为空格
    response = replace_non_digits_with_space(response).strip()
    # 按照连续的空格分割字符串
    phone_number_list = response.split()
    return phone_number_list

def get_choosed_result(item_list, history, question):
    """ Get the choosed result from the model (offline) """
    # print(f"item_list: {item_list}")
    # print(f"history: {history}")
    # print(f"question: {question}")

    Q = f"请你以下对话，然后回答：\n"

    Q += f"<历史对话>"
    for i in range(len(history)):
        Q += f"\n机器：{history[i][0]}"
        if len(history[i]) > 1:
            Q += f"\n人类：{history[i][1]}"
    Q += f"\n</历史对话>"

    Q += f"\n<问题>：{question}</问题>"
    Q += f"\n<选项>："
    for i in range(len(item_list)):
        Q += f"\n{i+1}. {item_list[i]}"
    Q += f"\n</选项>"
    Q += f"\n告诉我答案序号，不需要任何解释，不需要任何其他文本。回答格式<数字>，例如：1"
    # print(f"Q: {Q}")
    response, history = request_Q(Q, history)
    # 去除response中的换行符
    response = response.replace("\n", "")
    # print(f"response: {response}")
    try:
        print("response: ", response)
        print(''.join(filter(str.isdigit, response))[0])
        print(item_list)
        select_index = int(''.join(filter(str.isdigit, response))[0]) - 1
        print(f"select_index: {select_index}")
        selected_a = item_list[select_index]
        # print(f"select_index: {select_index}, selected_a: {selected_a}")
    except:
        selected_a = "无法识别"
        select_index = -1
        print(f"# ERROR! 无法识别")
    return select_index

def get_choosed_result_n_times_try(item_list, history, question, n=1):
    """ Get the choosed result from the model (offline) """
    choosed_result = []
    for i in range(n):
        selected_a_index = get_choosed_result(item_list, history, question)
        choosed_result.append(selected_a_index)
    # 返回出现次数最多的结果
    # print(f"choosed_result: {choosed_result}")
    r_index = max(set(choosed_result), key = choosed_result.count)
    r_text = item_list[r_index]
    return r_index, r_text


if __name__ == "__main__":
    r = get_phone_number_list("我要查找三个手机号，第一个12345678901，第二个是15151832002，还有一个85 两个4 7854三个零。")
    print(r)