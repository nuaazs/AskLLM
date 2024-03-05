import random

def check_phone_status(phone_number_list):
    """ Check the status of the phone number list """
    status = [
        {
            "status": "正常",
            "balance": "100",
            "package": "39元套餐",
            "remain_data": "1.5GB",
            "remain_call": "100分钟",
        },
        {
            "status": "停机",
            "balance": "0",
            "package": "无",
            "remain_data": "0",
            "remain_call": "0",
        },
        {
            "status": "欠费",
            "balance": "-100",
            "package": "无",
            "remain_data": "0",
            "remain_call": "0",
        },
    ]
    # random return a status
    phone_status = []
    for phone_number in phone_number_list:
        status_index = random.randint(0, 2)
        phone_status.append(status[status_index])
    return phone_status

def check_phone_bill(phone_number_list):
    """ Check the bill of the phone number list """
    return ["消费59元，其中包括固定套餐39元以及套餐外流量消耗20元。"] * len(phone_number_list)