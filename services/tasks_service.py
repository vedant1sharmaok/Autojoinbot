from db import db
from logger import logger
from models.credits import CREDIT_RULES, CreditSource


async def create_task(
    task_id: str,
    title: str,
    description: str,
    reward_key: str,
    requires_manual: bool = False
):
    """
    Owner-only task creation
    """
    await db.tasks.update_one(
        {"task_id": task_id},
        {
            "$set": {
                "title": title,
                "description": description,
                "reward_key": reward_key,
                "requires_manual": requires_manual,
                "active": True
            }
        },
        upsert=True
    )

    logger.info(f"TASK_CREATED {task_id}")


async def submit_task(user_id: int, task_id: str, proof: dict | None = None):
    """
    User submits a task for completion
    """
    existing = await db.task_submissions.find_one({
        "user_id": user_id,
        "task_id": task_id
    })

    if existing:
        return False

    task = await db.tasks.find_one({
        "task_id": task_id,
        "active": True
    })

    if not task:
        return False

    await db.task_submissions.insert_one({
        "user_id": user_id,
        "task_id": task_id,
        "proof": proof,
        "approved": not task["requires_manual"]
    })

    logger.info(f"TASK_SUBMITTED user={user_id} task={task_id}")
    return True


async def approve_task(user_id: int, task_id: str):
    """
    Owner manually approves a task
    """
    submission = await db.task_submissions.find_one({
        "user_id": user_id,
        "task_id": task_id,
        "approved": False
    })

    if not submission:
        return False

    task = await db.tasks.find_one({"task_id": task_id})
    reward = CREDIT_RULES.get(task["reward_key"], 0)

    await db.task_submissions.update_one(
        {"user_id": user_id, "task_id": task_id},
        {"$set": {"approved": True}}
    )

    await db.credits.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": reward}},
        upsert=True
    )

    logger.info(
        f"TASK_APPROVED user={user_id} task={task_id} +{reward}"
    )
    return True
