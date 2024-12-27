from loader import dp
from .admin import IsAdmin
from .create_profile_filtres import IsGender, IsFindGender, IsPhoto, IsName, IsAge, IsCity, IsDescription



if __name__ == 'bot.filters':
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind([IsGender, IsFindGender, IsPhoto, IsName, IsAge, IsCity, IsDescription])

