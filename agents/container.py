from agents.check_phone_balance import Agent as check_phone_balance
from agents.check_phone_bill import Agent as check_phone_bill
from agents.check_phone_card_plan import Agent as check_phone_card_plan
from agents.check_phone_location import Agent as check_phone_location
from agents.check_phone_recharge import Agent as check_phone_recharge
from agents.check_phone_resource import Agent as check_phone_resource
from agents.check_phone_status import Agent as check_phone_status



agent_check_phone_balance = check_phone_balance()
agent_check_phone_bill = check_phone_bill()
agent_check_phone_card_plan = check_phone_card_plan()
agent_check_phone_location = check_phone_location()
agent_check_phone_recharge = check_phone_recharge()
agent_check_phone_resource = check_phone_resource()
agent_check_phone_status = check_phone_status()

ALL_AGENTS = {
    "check_phone_balance": agent_check_phone_balance,
    "check_phone_bill": agent_check_phone_bill,
    "check_phone_card_plan": agent_check_phone_card_plan,
    "check_phone_location": agent_check_phone_location,
    "check_phone_recharge": agent_check_phone_recharge,
    "check_phone_resource": agent_check_phone_resource,
    "check_phone_status": agent_check_phone_status,
}