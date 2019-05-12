English:
This project is aimed to create a search system for finding events by the date and place where they take place. It will take the user's filled form into consideration and display the available events on a map of a given by user region. For more details see wiki.

Information about available events will be taken from the eventful.com API, which allows to access their database of different events all over the world by providing an API key. If you want to get yours, please go to https://api.eventful.com/docs.
 
 Ukrainian:

Призначення та коротка характеристика програми

Призначення цієї програми допомогти користувачеві максимально швидко та зручно оцінити місцезнаходження подій незалежно від їхнього місцязнаходження для вибраного проміжку часу. Програма повністю написана на Python з використанням бібліотек flask, flask_sqlalchemy, flask_mail,flask_wtf,wtforms,geopy,requests,threading,time,folium та кількох інших.Програма реалізована згідно з принципами об'єктно-орієнтованого програмування і поділено на такі 5 класів: Authentificator, User,Event,RegistrationForm,LoginForm. Програма відповідає вимогам pep8 та містить вичерпну документацію.
 
Вхідні та вихідні дані програми

  При запуску сайту, користувач реєструється, тобто вводить свій email, name, password, confirm password. Ці дані заносяться у sqlite базу даних і дозволяють користувачу увійти в систему. Користувач вводить вхідні дані: місце події, початкову та кінцеву дату. Тоді подається REST-запит до eventful API, результатом якого є json файл, з якого використовуваними є такі поля:id, title,start_time,city_name,latitude,longitude,end_time,url. Вихідними даними є візуалізація даних з json у вигляді карти, яка містить лейбли з назвами подій, які є посиланнями для переходу на сайт eventful для реєстрації користувача на подію.
  
Структура програми з коротким описом модулів, функцій, класів та методів.

  Програма містить пакети модулів data та templates. У data міститься data.json, data.db та requirements.txt. У templates містяться html файли: confirm_email.html,email_already_exists.html, index.html, login.html, mail.html, map.html, register.html, register_success.html. 
  Є модулі:
  data_structure.py - тут містяться структури даних усі, крім абстрактної, а також backend проекту.
  linked_list.py - тут міститься ADT Set(структура даних LinkedList)
  
Коротка інструкція по користуванню програмою.

Після запуску програми користувач натискає кнопку Sign-in, яка розташована зліва у лівому кутку. Після цього користувач заповнює поля name,email,password,confirmpassword. Або ж обирає пароль, який радить йому система, як сильний. Тоді користувач повинен перейти на вказану пошту і натиснути на гіперпосилання CONFIRM EMAIL. На відкритій сторінці перейти по гіперпосиланню SIGN IN та ввести пошту та пароль або ж  у випадку, якщо система запам'ятала користувача з його дозволу натиснути кнопку Register. Далі користувач уже у системі і може запонвити форму, де вказує місто, початкову та кінцеву дати і натискає кнопку "Search". На карті буде відображено карту вказаного міста та події, які проходять там у вказаний час. Щоб зареєструватись на подію, користувачеві потрібно натиснути на потрібне гіперпосилання на карті та перейти на сайт eventful. Для того, щоб вийти з системи слід натиснути на Sign out у лівому верхньому кутку.
Опис тестових прикладів для первірки працездатності програми.
