import random


def check_phone_status(phone_number):
    """用户希望查询手机卡状态"""
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
    return status[random.randint(0, 2)]


def check_phone_balance(phone_number):
    """用户希望查询手机卡余额"""
    # 随机生成一个带有两位小数的余额
    balance = round(random.uniform(0, 100), 2)
    return balance


def check_phone_card_plan(phone_number):
    """用户希望查询手机卡资费（套餐）"""
    plans = [
        {
            "package": "39元套餐",
            "monthly rent": "39",
            "remain_data": "10GB",
            "remain_call": "100分钟",
        },
        {
            "package": "59元套餐",
            "monthly rent": "59",
            "remain_data": "20GB",
            "remain_call": "200分钟",
        },
        {
            "package": "99元套餐",
            "monthly rent": "99",
            "remain_data": "50GB",
            "remain_call": "500分钟",
        },
    ]
    # 随机返回一个套餐
    return plans[random.randint(0, 2)]


def check_phone_resource(phone_number):
    """用户希望查询资源余量（流量）"""
    # 随机生成一个流量
    remain_data = round(random.uniform(0, 100), 2)
    return remain_data


def check_phone_bill(phone_number,start_date="", end_date=""):
    """用户希望进行账单查询"""
    bill_record = [
        {"date": "2024-01-01 12:00:00", "amount": "100元"},
        {"date": "2024-01-05 12:00:00", "amount": "20元"},
        {"date": "2024-02-02 12:00:00", "amount": "50元"},
        {"date": "2024-02-04 12:00:00", "amount": "15元"},
        {"date": "2024-03-03 12:00:00", "amount": "25元"},
        {"date": "2024-03-04 12:00:00", "amount": "1000元"},
    ]
    return bill_record




def check_phone_detail(phone_number, start_date="", end_date=""):
    """用户希望进行详单查询"""
    detail = [
        {"date": "2021-01-01", "type": "通话", "duration": "10分钟", "fee": "0.5元"},
        {"date": "2021-01-02", "type": "短信", "duration": "1条", "fee": "0.1元"},
        {"date": "2021-01-03", "type": "流量", "duration": "100MB", "fee": "1元"},
    ]
    return detail


def check_phone_location(phone_number):
    """用户希望进行归属地/PIN/ICCID查询"""
    location = {
        "province": "江苏",
        "city": "南京",
        "operator": "中国移动",
    }
    return location



def check_phone_recharge(phone_number, date=""):
    """
    用户希望进行充值记录查询
    """
    recharge_record = [
        {"date": "2024-01-01 12:00:00", "amount": "100元"},
        {"date": "2024-01-05 12:00:00", "amount": "20元"},
        {"date": "2024-02-02 12:00:00", "amount": "50元"},
        {"date": "2024-02-04 12:00:00", "amount": "15元"},
        {"date": "2024-03-03 12:00:00", "amount": "25元"},
        {"date": "2024-03-04 12:00:00", "amount": "1000元"},
    ]
    return recharge_record
