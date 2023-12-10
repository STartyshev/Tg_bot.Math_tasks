from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def welcome_menu():
    tasks = InlineKeyboardButton(text='Старт 👍🏻', callback_data='tasks')
    info = InlineKeyboardButton(text='Инфо 📋', callback_data='info')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[tasks, info]])
    return keyboard


def user_auth():
    auth = InlineKeyboardButton(text='Да ✔️', callback_data='user_auth')
    not_auth = InlineKeyboardButton(text='Нет ❌', callback_data='pass_auth')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[auth, not_auth]])
    return keyboard

def tasks_menu():
    first_task = InlineKeyboardButton(text='Проверка двух массивов на количество общих чисел', callback_data='first_task')
    second_task = InlineKeyboardButton(text='Расстояние между точками', callback_data='second_task')
    third_task = InlineKeyboardButton(text='Логическое следствие элементов трех массивов', callback_data='third_task')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[first_task], [second_task], [third_task]])
    return keyboard

def go_to_tasks():
    lets_go = InlineKeyboardButton(text='Перейти 👍🏻', callback_data='tasks')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[lets_go]])
    return keyboard

def any_task_menu():
    task = InlineKeyboardButton(text='Условие задачи', callback_data='task')
    input_of_initial_data = InlineKeyboardButton(text='Ввод исходных данных', callback_data='input_data')
    execute_algorithm = InlineKeyboardButton(text='Выполнение алгоритма', callback_data='execute_algorithm')
    output_results = InlineKeyboardButton(text='Вывод результатов работы алгоритма', callback_data='show_results')
    exit_to_main_menu = InlineKeyboardButton(text='Выход в главное меню', callback_data='exit_to_main_menu')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[task], [input_of_initial_data], [execute_algorithm],
        [output_results], [exit_to_main_menu]]
    )
    return keyboard

def init_method():
    by_hand = InlineKeyboardButton(text='Вручную', callback_data='by_hand')
    auto_init = InlineKeyboardButton(text='Автоматически', callback_data='auto_init')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[by_hand], [auto_init]])
    return keyboard
