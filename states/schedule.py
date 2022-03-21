from aiogram.dispatcher.filters.state import StatesGroup, State


class ScheduledLessonNoteState(StatesGroup):
    scheduled_lesson_id = State()
    scheduled_lesson_note_id = State()
    text = State()
    file = State()
