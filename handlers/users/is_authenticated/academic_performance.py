from aiogram.types import Message, CallbackQuery

from keyboards.default.base import ACADEMIC_PERFORMANCE_BUTTON
from keyboards.inline.callback_data import academic_performance_semester, academic_performance_lesson, \
    academic_performance
from keyboards.inline.academic_performance import select_semester_buttons, select_lesson_buttons, lesson_buttons
from loader import dp
from utils.polyrobot.user import User
from utils.polyrobot.messages import performance_semester_message_text, performance_lesson_message_text


@dp.message_handler(text=ACADEMIC_PERFORMANCE_BUTTON, is_authenticated=True, state='*')
@dp.message_handler(commands=["performance"], is_authenticated=True, state='*')
async def bot_academic_performance_command(message: Message):
    user = User(message.from_user.id, message.from_user.full_name, message.from_user.username)
    profile = await user.profile()
    semesters_count = 2 * int(profile.course)

    await message.answer(text=performance_semester_message_text(),
                         reply_markup=select_semester_buttons(semesters_count))


@dp.callback_query_handler(academic_performance.filter(), state='*')
async def bot_academic_performance_callback(call: CallbackQuery, callback_data: dict):
    user = User(call.from_user.id, call.from_user.full_name, call.from_user.username)
    profile = await user.profile()
    semesters_count = 2 * int(profile.course)

    await call.message.edit_text(text=performance_semester_message_text(),
                                 reply_markup=select_semester_buttons(semesters_count))


@dp.callback_query_handler(academic_performance_semester.filter(), state='*')
async def bot_academic_performance_semester_callback(call: CallbackQuery, callback_data: dict):
    user = User(call.from_user.id, call.from_user.full_name, call.from_user.username)
    academic_performances = await user.academic_performance(semester_number=callback_data['semester_number'])

    if academic_performances:
        await call.message.edit_text(
            text=performance_lesson_message_text(academic_performances),
            reply_markup=select_lesson_buttons(
                semester_number=callback_data['semester_number'],
                id_to_lesson_title={
                    academic_performance.id: academic_performance.name for academic_performance in academic_performances
                }
            )
        )
    else:
        await call.answer("Данных за этот семестр нет, попробуй другой!")


@dp.callback_query_handler(academic_performance_lesson.filter(), state='*')
async def bot_academic_performance_lesson_callback(call: CallbackQuery, callback_data: dict):
    user = User(call.from_user.id, call.from_user.full_name, call.from_user.username)
    academic_performances = await user.academic_performance()
    academic_performance = [academic_performance_tmp for academic_performance_tmp in academic_performances
                            if academic_performance_tmp.id == callback_data['lesson_id']][0]

    await call.message.edit_text(text=academic_performance.to_message_text(),
                                 reply_markup=lesson_buttons(callback_data['semester_number']))
