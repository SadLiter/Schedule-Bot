from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from states import Register

from groups import get_schedule, student_groups, df

router = Router()

@router.message(CommandStart())
async def register(message: Message, state: FSMContext):
    await message.answer('Бот находится в ранней стадии разработки, пользуйтесь осторожно!')
    await state.set_state(Register.group_number)
    await message.answer("Введите номер вашей группы: ")

@router.message(Register.group_number)
async def process_group_number(message: Message, state: FSMContext):
    if message.text.upper() in student_groups:
        await state.update_data(group_number=message.text.upper())
        await message.answer("Группа найдена!")
        await message.answer(f"Ваша группа: {message.text.upper()}")
        await state.set_state(Register.today_day)
        await message.answer("Выберите день недели:\nпн\nвт\nср\nчт\nпт")
    else:
        await message.answer("Упс! Такой группы нету! Попробуйте снова.")
        await state.clear()

@router.message(Register.today_day)
async def group(message: Message, state: FSMContext):
    await state.update_data(today_day=message.text.lower())
    data = await state.get_data()
    group_number = data.get('group_number')
    today_day = data.get('today_day')
    schedule = get_schedule(df, group_number, today_day)
    await message.answer(f"📖Расписание {schedule}")
