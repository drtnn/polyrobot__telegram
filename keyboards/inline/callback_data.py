from aiogram.utils.callback_data import CallbackData

schedule_callback = CallbackData("schedule", "date")

orders_callback = CallbackData("orders")

academic_performance = CallbackData("academic_performance")
academic_performance_semester = CallbackData("academic_performance_semester", "semester_number")
academic_performance_lesson = CallbackData("academic_performance_lesson", "semester_number", "lesson_id")
