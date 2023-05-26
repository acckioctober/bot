import sqlite3
from sqlite3 import Error
import random
from config import bot, ADMINS
from aiogram import types, Dispatcher

global db, cursor

def sql_create():
    global db, cursor
    db = sqlite3.connect('bot.db')
    cursor = db.cursor()
    if db:
        print('База подключена!')
    # create = '''CREATE TABLE IF NOT EXISTS bot_tab
    #             (id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             tg_id INTEGER,
    #             username VARCHAR (255),
    #             cake TEXT,
    #             weight FLOAT,
    #             name TEXT,
    #             address TEXT,
    #             apartment_floor TEXT,
    #             phone TEXT,
    #             add_information TEXT,
    #             delivery TEXT,
    #             payment_methods TEXT)'''
    # db.execute(create)
    # db.commit()

    db.execute('''CREATE TABLE IF NOT EXISTS product_table
                (cake_type TEXT NOT NULL,
                taste TEXT,
                filling TEXT,
                topping TEXT,
                weight_kg DECIMAL(10, 2),
                price_rub DECIMAL(10, 2),
                rating TEXT,
                photo TEXT)''')

    db.execute('''CREATE TABLE IF NOT EXISTS cakes
                (cake_type TEXT NOT NULL,
                cake_description TEXT)''')

    db.execute('''CREATE TABLE IF NOT EXISTS tastes
                (taste TEXT NOT NULL,
                taste_description TEXT)''')

    db.execute('''CREATE TABLE IF NOT EXISTS fillings
                (filling TEXT NOT NULL,
                filling_description TEXT)''')

    db.execute('''CREATE TABLE IF NOT EXISTS toppings
                (topping TEXT NOT NULL,
                topping_description TEXT)''')

    db.execute('''CREATE TABLE IF NOT EXISTS Orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_full_name TEXT NOT NULL,
                cake_type TEXT NOT NULL,
                taste TEXT NOT NULL,
                filling TEXT NOT NULL,
                topping TEXT NOT NULL,
                weight_kg REAL NOT NULL,
                price_rub INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                photo TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    db.commit()
def insert_data():
    product = [('Бисквитные торты', 'Кофейный', 'Кофейный крем', 'Ягоды', 1, 250, 'new', ' '),
    ('Слоеные торты', 'Малиновый', 'Карамельный крем', 'Шоколадные стружки', 1.5, 350, 'actual', ' '),
    ('Шифоновые торты', 'Лимонный', 'Лимонный курд', 'Фруктовые дольки', 1.5, 350, 'actual', ' ')]
    cursor.executemany('''INSERT INTO product_table (cake_type, taste, filling, topping, 
            weight_kg, price_rub, rating, photo) VALUES (?,?,?,?,?,?,?,?)''', product)

    cake = [('Печеные торты', 'Торты, которые приготавливаются путем выпекания теста в духовке. Это наиболее распространенный способ приготовления тортов.'), ('Бисквитные торты', 'Торты, которые готовятся на основе воздушного бисквитного теста без добавления масла или маргарина.'), ('Замороженные торты', 'Торты, которые готовятся с помощью замораживания различных слоев и компонентов, обычно на основе сливочного крема или фруктового пюре.'), ('Эклеры', 'Воздушные пирожные из заварного теста, обычно с начинкой из сливочного крема или шоколадного ганаша.'), ('Профитроли', 'Маленькие пирожные из теста шу, заполненные сливочным кремом или мороженым.'), ('Макаронс', 'Деликатесные пирожные из миндаля с кремовой начинкой между двумя печеньями.'), ('Бисквитные рулеты', 'Тонкий бисквит, свернутый с начинкой внутри, часто с добавлением взбитых сливок, фруктов или шоколада.'), ('Сырники', 'Рулеты на основе сырного теста, заполненные сырной начинкой и другими добавками.'), ('Торты с ягодами', 'Торты, в которых ягоды используются как начинка или украшение, например, клубника, малина, черника и т.д.'), ('Торты с фруктами', 'Торты, где фрукты, такие как яблоки, груши, ананасы и др., используются в качестве начинки или декора.'), ('Слоеные торты', 'Торты, состоящие из нескольких слоев бисквита, разделенных начинкой или кремом.'), ('Шифоновые торты', 'Легкие и пышные торты, приготовленные на основе шифонового теста, которое включает в себя взбитые белки.'), ('Брауни', 'Плотные и шоколадные пирожные, обычно с глазурью или орехами.'), ('Пироги', 'Торты с крошечным основанием из теста и начинкой, такой как фрукты, ягоды, шоколад или сыр.'), ('Муссы', 'Легкие и воздушные торты, приготовленные на основе муссовых текстур, таких как шоколадный, фруктовый или карамельный мусс.'), ('Чизкейки', 'Торты на основе сыра, с плотным основанием из печенья или песочного теста, с добавлением различных начинок или топпингов.'), ('Рулеты', 'Тонкие слои бисквита, свернутые с начинкой внутри.'), ('Десерты с глазурью', 'Торты или пирожные, покрытые слоем глазури или крема.')]
    cursor.executemany('''INSERT INTO cakes (cake_type, cake_description)
                    VALUES (?,?)''', cake)

    taste = [('Ванильный', 'Классический вкус с нежным ароматом ванили.'), ('Шоколадный', 'Богатый и насыщенный вкус шоколада.'), ('Карамельный', 'Сладкий и нежный вкус карамели.'), ('Клубничный', 'Свежий и фруктовый вкус клубники.'), ('Малиновый', 'Нежный и ароматный вкус малины.'), ('Лимонный', 'Освежающий и кисловатый вкус лимона.'), ('Мятный', 'Прохладный и освежающий вкус мяты.'), ('Кокосовый', 'Экзотический и сладкий вкус кокоса.'), ('Кофейный', 'Богатый и ароматный вкус кофе.'), ('Фруктовый', 'Комбинация различных фруктовых вкусов.')]
    cursor.executemany('''INSERT INTO tastes (taste, taste_description)
                       VALUES (?,?)''', taste)

    filling = [('Сливочный крем', ' '), ('Шоколадный ганаш', ' '), ('Фруктовая начинка', 'клубника, малина, вишня и т.д.'), ('Карамельный крем', ' '), ('Лимонный курд', ' '), ('Крем с мятой', ' '), ('Ореховая начинка', 'грецкие орехи, миндаль, фундук и т.д.'), ('Кофейный крем', '')]
    cursor.executemany('''INSERT INTO fillings (filling, filling_description)
                           VALUES (?,?)''', filling)

    topping = [('Шоколадные стружки', ' '), ('Фруктовые дольки', 'клубника, киви, манго и т.д.'), ('Шоколадные капли', ' '), ('Орехи', 'грецкие орехи, миндаль, фундук и т.д.'), ('Взбитые сливки', ' '), ('Шоколадный соус', ' '), ('Карамельный соус', ' '), ('Ягоды', 'клубника, малина, черника и т.д.')]
    cursor.executemany('''INSERT INTO toppings (topping, topping_description)
                           VALUES (?,?)''', topping)
    db.commit()


def get_product_list():
    product_list = cursor.execute('''SELECT * FROM product_table''').fetchall()
    cake_descriptions = []
    for product in product_list:
        cake_description = cursor.execute("SELECT cake_description FROM cakes WHERE cake_type = ?",
                                          (product[0],)).fetchall()
        cake_descriptions.append(cake_description[0][0])  # Получить первое описание из списка fetchall()
    return product_list, cake_descriptions

def get_product_data(cake_type):
    cursor.execute("SELECT * FROM product_table WHERE cake_type = ?", (cake_type,))
    product_data = cursor.fetchone()  # Получение первой строки результата запроса
    return product_data

def save_order_data(user_id, user_full_name, product_data):
    order_data = (user_id, user_full_name, *product_data)
    cursor.execute("INSERT INTO Orders (user_id, user_full_name, cake_type, taste, "
                   "filling, topping, weight_kg, price_rub, rating, photo) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", order_data)
    db.commit()


def get_button_names_from_product_table():
    button_names = cursor.execute('''SELECT cake_type FROM product_table''').fetchall()
    return button_names


async def sql_command_insert(state):
    async with state.proxy() as data:
        sql = '''INSERT INTO tastes (tg_id, username, cake, weight, name, 
                address, apartment_floor, phone, add_information, 
                delivery, payment_methods) VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
        cursor.execute(sql, tuple(data.values()))
        db.commit()


async def sql_commands_apdate(state):
    async with state.proxy() as data:
        cursor.execute("UPDATE product_table SET photo=? WHERE cake_type=?", tuple(data.values()))
        db.commit()


async def get_data(message: types.Message):
    results = cursor.execute('''SELECT * FROM bot_tab''').fetchall()
    random_data = random.choice(results)
    await bot.send_photo(message.from_user.id, random_data[-3])
    print('Запрос исполнен')


def request_db(dp: Dispatcher):
    '''Функция регистрации обработчиков'''
    dp.register_message_handler(get_data, commands=['photo'])
