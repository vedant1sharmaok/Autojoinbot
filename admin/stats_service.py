from db import db


async def get_global_stats():
    """
    High-level system overview
    """
    users = await db.users.count_documents({})
    channels = await db.channels.count_documents({})
    broadcasts = await db.broadcasts.count_documents({})
    premium_users = await db.users.count_documents({"is_premium": True})

    return {
        "users": users,
        "channels": channels,
        "broadcasts": broadcasts,
        "premium_users": premium_users
    }


async def get_broadcast_stats():
    """
    Broadcast health & delivery stats
    """
    sent = await db.broadcast_logs.count_documents({"status": "sent"})
    failed = await db.broadcast_logs.count_documents({"status": "failed"})
    pending = await db.broadcasts.count_documents({"status": "pending"})

    return {
        "sent": sent,
        "failed": failed,
        "pending": pending
    }


async def get_credit_stats():
    """
    Credits distribution
    """
    total_credits = 0
    async for row in db.credits.find({}):
        total_credits += row.get("balance", 0)

    return {
        "total_credits": total_credits
    }


async def get_task_stats():
    """
    Task performance
    """
    tasks = await db.tasks.count_documents({})
    submissions = await db.task_submissions.count_documents({})
    pending = await db.task_submissions.count_documents({"approved": False})

    return {
        "tasks": tasks,
        "submissions": submissions,
        "pending": pending
    }
