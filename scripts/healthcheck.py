import asyncio
from app.core.health import bot_health

async def main():
    ok = await bot_health()
    raise SystemExit(0 if ok else 1)

if __name__ == "__main__":
    asyncio.run(main())
