from aiogram.utils.callback_data import CallbackData

schedule_callback = CallbackData("schedule", "date")
scheduled_lesson_callback = CallbackData("scheduled_lesson", "scheduled_lesson_id")
scheduled_lesson_add_note_callback = CallbackData("scheduled_lesson_add_note", "scheduled_lesson_id")
scheduled_lesson_note_callback = CallbackData("scheduled_lesson_note", "scheduled_lesson_note_id")

orders_callback = CallbackData("orders")
profile_callback = CallbackData("profile")

academic_performance = CallbackData("academic_performance")
academic_performance_semester = CallbackData("academic_performance_semester", "semester_number")
academic_performance_lesson = CallbackData("academic_performance_lesson", "semester_number", "lesson_id")
