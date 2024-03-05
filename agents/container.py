from agents.bill_check import Agent as BillAgent
from agents.status_check import Agent as StatusAgent


status_agent = StatusAgent()
bill_agent = BillAgent()

ALL_AGENTS = {
    "status_check": status_agent,
    "bill_check": bill_agent
}