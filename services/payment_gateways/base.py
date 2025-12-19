from abc import ABC, abstractmethod
from logger import logger


class PaymentGateway(ABC):
    """
    Base class for all payment gateways.
    """

    name: str = "base"
    maintenance: bool = False

    def __init__(self, maintenance: bool = False):
        self.maintenance = maintenance

    def is_available(self) -> bool:
        """
        Returns False if gateway is under maintenance.
        """
        return not self.maintenance

    @abstractmethod
    async def create_payment(self, user_id: int, plan: str):
        """
        Creates a payment request.
        """
        pass

    @abstractmethod
    async def verify_payment(self, payload: dict) -> bool:
        """
        Verifies payment success.
        """
        pass

    def log(self, message: str):
        logger.info(f"[{self.name.upper()}] {message}")
