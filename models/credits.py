from enum import Enum


class CreditSource(str, Enum):
    REFERRAL = "referral"
    TASK = "task"
    MANUAL = "manual"


CREDIT_RULES = {
    "referral_join": 10,
    "task_complete": 5,
    "boost_channel": 20
}
