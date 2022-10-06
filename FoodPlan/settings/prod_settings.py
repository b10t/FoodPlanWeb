from FoodPlan.settings.default_settings import *


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['0.0.0.0', '81.163.26.170', 'localhost'])
