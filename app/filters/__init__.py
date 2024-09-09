from loader import dp
from .admin import Admin
from .create_profile_filtres import Gender, FindGender, Photo, Name, Age, City, Description



if __name__ == 'bot.filters':
    dp.filters_factory.bind(Admin)
    dp.filters_factory.bind([Gender, FindGender, Photo, Name, Age, City, Description])

