from filters.polyrobot import IsAuthenticated
from loader import dp

if __name__ == "filters":
    dp.filters_factory.bind(IsAuthenticated)
