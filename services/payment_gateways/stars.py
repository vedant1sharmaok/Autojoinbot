from services.payment_gateways.base import PaymentGateway
from logger import logger


class TelegramStarsGateway(PaymentGateway):
    name = "telegram_stars"

    async def create_payment(self, user_id: int, plan: str):
        """
        Telegram Stars payment is initiated via invoice.
        The handler will send the invoice using returned payload.
        """
        self.log(f"Creating Stars invoice user={user_id} plan={plan}")

        return {
            "provider": "telegram_stars",
            "user_id": user_id,
            "plan": plan,
            "currency": "XTR",
            "payload": f"stars:{user_id}:{plan}"
        }

    async def verify_payment(self, payload: dict) -> bool:
        """
        Telegram confirms payment via successful payment update.
        """
        self.log(f"Verifying Stars payload={payload}")
        return payload.get("provider") == "telegram_stars"
