from enum import Enum


class PremiumPlan(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


PREMIUM_PLANS = {
    PremiumPlan.FREE: {
        "price": 0,
        "broadcast_limit_per_day": 1,
        "can_pin": False,
        "can_schedule": False,
        "force_join_limit": 0,
        "approval_required": True
    },
    PremiumPlan.BASIC: {
        "price": 49,
        "broadcast_limit_per_day": 5,
        "can_pin": False,
        "can_schedule": False,
        "force_join_limit": 1,
        "approval_required": True
    },
    PremiumPlan.PRO: {
        "price": 149,
        "broadcast_limit_per_day": 20,
        "can_pin": True,
        "can_schedule": True,
        "force_join_limit": 5,
        "approval_required": False
    },
    PremiumPlan.ENTERPRISE: {
        "price": 499,
        "broadcast_limit_per_day": 100,
        "can_pin": True,
        "can_schedule": True,
        "force_join_limit": 20,
        "approval_required": False
    }
}
