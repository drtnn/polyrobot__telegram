from filters.date_regexp import IsDate
from filters.polyrobot import IsAuthenticated
from loader import dp

if __name__ == "filters":
    dp.filters_factory.bind(IsAuthenticated)
    dp.filters_factory.bind(IsDate)
