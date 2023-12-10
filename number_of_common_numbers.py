import buttons
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram import F
import random

router = Router()

# Два массива в которых будет осуществляться поиск общих чисел
first_array = []
second_array = []
# Количество общих чисел двух массивов
num_of_common_numbers = None

users_dict = dict()
state = ''
ft_init_farray = False
ft_init_sarray = False
ft_init_fsize = False
ft_init_ssize = False


# Задача №1
async def main_menu_number_of_common_numbers(callback: CallbackQuery | Message, state_from_main, users_dict_from_main):
    """
    Функция реализующая главное меню задачи №1 в телеграмм боте.
    :param callback: Ответ от сервера (нажатие кнопки или сообщение);
    :param state_from_main: текущее состояние бота;
    :param users_dict_from_main: словарь с текущими пользователями.
    """
    global state
    global users_dict
    users_dict = users_dict_from_main
    state = state_from_main
    if isinstance(callback, CallbackQuery):
        await callback.answer()
        await callback.message.answer(
            text='<b>Проверка двух массивов на количество общих чисел</b>',
            reply_markup=buttons.any_task_menu()
        )
    else:
        await callback.answer(
            text='<b>Проверка двух массивов на количество общих чисел</b>',
            reply_markup=buttons.any_task_menu()
        )


# Условие задачи
@router.callback_query(F.data == 'task')
async def show_task(callback: CallbackQuery):
    """
    Функция реализующая вывод условия задачи в чате телеграмм бота.
    """
    global state
    if state == 'first_task':
        await callback.message.answer(
            text='<b>Входные данные</b>: два массива с числами. <b>Требуется</b> проверить сколько у массивов общих чисел. '
                 'Также число будет считаться общим если оно входит в один массив, а в другом массиве находится '
                 'его перевернутая версия.'
        )
        await callback.answer()


# Ввод исходных данных
@router.callback_query(F.data == 'input_data')
async def input_data_menu(callback: CallbackQuery):
    """
    Функция реализующая начальную точку ввода исходных данных.
    """
    global state
    if state == 'first_task':
        await callback.answer()
        global first_array
        global second_array
        first_array = []
        second_array = []
        if users_dict[callback.from_user.id]['user_auth']:
            await callback.message.answer(
                text='Как вы хотите заполнить исходные массивы чисел?',
                reply_markup=buttons.init_method()
            )
        else:
            await init_by_hand_menu(callback)


# Инициализация массивов вручную
@router.callback_query(F.data == 'by_hand')
async def init_by_hand_menu(callback: CallbackQuery | Message, array_number=1):
    """
    Функция реализующая диалог с пользователем для ввода исходных массивов.
    :param callback: Ответ от сервера (нажатие кнопки или сообщение);
    :param array_number: номер массива, который нужно ввести пользователю.
    """
    global state
    if state == 'first_task':
        global ft_init_fsize
        global ft_init_ssize
        ft_init_fsize = False
        ft_init_ssize = False
        if array_number == 1:
            await callback.answer()
            global ft_init_farray
            ft_init_farray = True
            await callback.message.answer(text=f"Отправьте {array_number}-й массив чисел записанных через пробел:")
        elif array_number == 2:
            global ft_init_sarray
            ft_init_sarray = True
            await callback.answer(text=f"Отправьте {array_number}-й массив чисел записанных через пробел:")


async def init_by_hand(message: Message):
    """
    Функция реализующая ввод пользователем исходных массивов вручную.
    :param message: Сообщение от пользователя, которое будет проверяться на корректность
    (был введен массив или какие то другие данные).
    """
    global first_array
    global second_array
    global ft_init_farray
    global ft_init_sarray
    try:
        if ft_init_farray:
            first_array = list(map(lambda x: float(x), message.text.split(' ')))
            ft_init_farray = False
            await init_by_hand_menu(message, 2)
            return
        if ft_init_sarray:
            second_array = list(map(lambda x: float(x), message.text.split(' ')))
            ft_init_sarray = False
            await message.answer(
                text=f"<b>Инициализация массивов прошла успешно</b> ✔️\n"
                     f"Первый массив: {first_array}\n"
                     f"Второй массив: {second_array}"
            )
            await main_menu_number_of_common_numbers(message, state, users_dict)
    except ValueError:
        await message.answer(
            text='<u>Все элементы</u> массива должны принимать <u>числовые значения</u>.\n'
                 'Попробуйте еще раз:'
        )


async def auto_init(message: Message):
    """
    Функция реализующая ввод пользователем размеров массивов, которые будут инициализированы случайным образом.
    :param message: Сообщение от пользователя, которое будет проверяться на корректность
    (корректный размер массива или нет).
    """
    global first_array
    global second_array
    global ft_init_fsize
    global ft_init_ssize
    try:
        if ft_init_fsize:
            if int(message.text) > 0:
                auto_init_array(first_array, int(message.text))
                ft_init_fsize = False
                await auto_init_menu(message, 2)
                return
            else:
                raise ValueError
        if ft_init_ssize:
            if int(message.text) > 0:
                auto_init_array(second_array, int(message.text))
                ft_init_ssize = False
                await message.answer(
                    text=f"<b>Инициализация массивов прошла успешно</b> ✔️️\n"
                         f"Первый массив: {first_array}\n"
                         f"Второй массив: {second_array}"
                )
                await main_menu_number_of_common_numbers(message, state, users_dict)
            else:
                raise ValueError
    except ValueError:
        await message.answer(
            text='<u>Размер массива</u> должен принимать <u>целочисленные значения больше 0</u>.\n'
                 'Попробуйте еще раз.'
        )


# Инициализация массивов случайным образом
@router.callback_query(F.data == 'auto_init')
async def auto_init_menu(callback: CallbackQuery | Message, array_number=1):
    """
    Функция реализующая диалог с пользователем для ввода размеров исходных массивов.
    :param callback: Ответ от сервера (нажатие кнопки или сообщение);
    :param array_number: номер массива, размер которого нужно ввести пользователю.
     """
    global state
    if state == 'first_task':
        global ft_init_farray
        global ft_init_sarray
        ft_init_farray = False
        ft_init_sarray = False
        if array_number == 1:
            global ft_init_fsize
            ft_init_fsize = True
            await callback.message.answer(
                text=f"Введите размер {array_number}-го массива который будет заполнен автоматически:"
            )
            await callback.answer()
        elif array_number == 2:
            global ft_init_ssize
            ft_init_ssize = True
            await callback.answer(
                text=f"Введите размер {array_number}-го массива который будет заполнен автоматически:"
            )


@router.message()
async def message_handler(message: Message):
    """
    Функция реализующая обработку сообщение, которые не прошли ни один фильтр.
    :param message: Сообщение введенное пользователем.
    """
    global state
    if state == 'first_task':
        # Инициализация вручную
        await init_by_hand(message)
        # Инициализация автоматически
        await auto_init(message)


def auto_init_array(array, size):
    """
    Функция реализующая заполнение массива случайными вещественными числами от -10 до 10.
    :param array: Список, который будет заполняться числами;
    :param size: количество случайных чисел.
    """
    for i in range(size):
        array.append(round(random.random() * 10 * ((-1) ** random.randint(1, 2)), 1))


# Выполнение алгоритма
@router.callback_query(F.data == 'execute_algorithm')
async def execute_algorithm(callback: CallbackQuery):
    """
    Функция реализующая выполнение алгоритма для задачи №1.
    """
    global state
    if state == 'first_task':
        await callback.answer()
        global first_array
        global second_array
        global num_of_common_numbers
        if len(first_array) < 1 or len(second_array) < 1:
            await callback.message.answer(
                text='❌ Невозможно выполнить алгоритм, так как один или оба исходных массива пустые. '
                     'Заполните исходные данные и попробуйте еще раз.'
            )
        else:
            num_of_common_numbers = number_of_common_numbers(first_array, second_array)
            await callback.message.answer(text='<b>Алгоритм успешно выполнен!</b> ✔️')


# Вывод результатов работы алгоритма
@router.callback_query(F.data == 'show_results')
async def show_results(callback: CallbackQuery):
    """
    Функция реализующая вывод результатов работы алгоритма в чат телеграмм бота.
    """
    global state
    if state == 'first_task':
        await callback.answer()
        global num_of_common_numbers
        if num_of_common_numbers is not None:
            await callback.message.answer(
                text=f"<b>Результат работы алгоритма</b>\n"
                     f"Первый массива: {' '.join(map(str, first_array))}\n"
                     f"Второй массив: {' '.join(map(str, second_array))}\n"
                     f"Количество общих чисел в обоих массивах: {num_of_common_numbers}"
            )
        else:
            await callback.message.answer(
                text='❌ Невозможно вывести результат работы алгоритма, так как алгоритм не был выполнен. '
                     'Запустите работу алгоритма и попробуйте еще раз.'
            )


@router.callback_query(F.data == 'exit_to_main_menu')
async def exit_to_main_menu(callback: CallbackQuery):
    """
    Функция реализующая выход в главное меню телеграмм бота.
    """
    from main import tasks_menu
    global state
    if state == 'first_task':
        await callback.answer()
        global first_array
        global second_array
        global num_of_common_numbers
        first_array = []
        second_array = []
        num_of_common_numbers = None
        state = ''
        await tasks_menu(callback)


def number_of_common_numbers(first_array, second_array):
    """
    Функция находит количество общих чисел в двух массивах.
    Также, число считается общим если оно входит в один массив, а в другом
    находится его перевернутая версия.
    :param first_array: Первый массив чисел;
    :param second_array: второй массив чисел.
    :return: Возвращает количество общих чисел двух массивов.
    """
    num_of_common_numbers = 0
    # Список в который будут добавляться общие числа
    list_of_common_numbers = []
    for elem in first_array:
        # Если число из первого массива или его обратная версия находятся во втором массиве
        # И это число еще не обрабатывалось прежде т. е. его нет в списке общих чисел
        # То оно добавляется в список и кол-во общих чисел увеличивается на 1
        if ((str(elem) in list(map(str, second_array)) or str(elem)[::-1] in list(map(str, second_array))) and
                elem not in list_of_common_numbers):
            num_of_common_numbers += 1
            list_of_common_numbers.append(elem)
    return num_of_common_numbers
