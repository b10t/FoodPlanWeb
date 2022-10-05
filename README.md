## Аренда бокса

### Описание

Сайт "[SelfStorage](http://b10trus.eu.pythonanywhere.com/)" позволяет арендовать бокс для хранения вещей.    

### Установка
`Python3` должен быть уже установлен. Затем используйте `pip` (или `pip3`,
если есть конфликт с `Python2`) для установки зависимостей:
```bash
pip install -r requirements.txt
```

### Первоначальная настройка

Скопируйте файл `.env.Example` и переименуйте его в `.env`.  

Заполните переменные окружения в файле `.env`:  
`ALLOWED_HOSTS` - Разрешенные хосты. Указываются через запятую, например: `127.0.0.1,localhost`.  
`SECRET_KEY` - Секретный ключ.  
`DEBUG` - Если нужно включить режим отладки web-сервера, установите значение в `True`.  
`STRIPE_API_KEY` - Секретный ключ от [API Stripe](https://dashboard.stripe.com/apikeys/).  
`EMAIL_HOST` - Адрес почтового SMTP сервера.  
`EMAIL_PORT` - Порт почтового SMTP сервера.  
`EMAIL_HOST_USER` - Логин почты.  
`EMAIL_USE_SSL` - Использует ли почтовый сервер SSL.
`EMAIL_HOST_PASSWORD` - Пароль почты.  

### Запуск 
```bash
python manage.py runserver 0.0.0.0:8000
```
или
```bash
python manage.py runserver localhost:80
```
### Демо сервер  

Сервер для ознакомления доступен по адресу: [ссылка](http://b10trus.eu.pythonanywhere.com/)  
