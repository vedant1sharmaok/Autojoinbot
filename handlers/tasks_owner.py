from aiogram import Router, types
from services.tasks_service import approve_task
from db import db
from config import OWNER_ID

router = Router()


def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID


@router.message(commands=["task_submissions"])
async def view_submissions(message: types.Message):
    if not is_owner(message.from_user.id):
        return

    submissions = db.task_submissions.find({"approved": False})
    text = "⏳ *Pending Task Submissions:*\n\n"

    async for sub in submissions:
        text += (
            f"User: `{sub['user_id']}`\n"
            f"Task: `{sub['task_id']}`\n"
            f"/approve_{sub['user_id']}_{sub['task_id']}\n\n"
        )

    await message.answer(text, parse_mode="Markdown")


@router.message(lambda m: m.text and m.text.startswith("/approve_"))
async def approve_submission(message: types.Message):
    if not is_owner(message.from_user.id):
        return

    _, user_id, task_id = message.text.split("_")
    success = await approve_task(int(user_id), task_id)

    if success:
        await message.answer("✅ Task approved and credits awarded.")
    else:
        await message.answer("❌ Approval failed.")
