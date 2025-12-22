from aiogram import Router, types
from services.tasks_service import submit_task
from db import db

router = Router()


@router.message(commands=["tasks"])
async def show_tasks(message: types.Message):
    tasks = db.tasks.find({"active": True})
    text = "📝 *Available Tasks:*\n\n"

    async for task in tasks:
        text += f"• *{task['title']}*\n{task['description']}\n\n"

    await message.answer(text, parse_mode="Markdown")


@router.callback_query(lambda c: c.data.startswith("task_submit:"))
async def handle_task_submit(call: types.CallbackQuery):
    task_id = call.data.split(":")[1]
    user_id = call.from_user.id

    success = await submit_task(user_id, task_id)

    if success:
        await call.message.answer(
            "✅ Task submitted successfully!\n"
            "You will receive credits after verification."
        )
    else:
        await call.message.answer(
            "❌ Task already submitted or invalid."
        )
