import buttons
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random

router = Router()


class FSMFirstTask(StatesGroup):
    data_filling_method = State()
    first_task_menu = State()
    init_first_array = State()
    init_second_array = State()
    init_first_array_size = State()
    init_second_array_size = State()
    data_is_filled_in = State()
    algorithm_completed = State()


# Задача №1
async def pre_main_menu_number_of_common_numbers(callback: CallbackQuery | Message, state: FSMContext):
    """
    Костыль.
    """
    await state.set_state(FSMFirstTask.first_task_menu)
    await main_menu_number_of_common_numbers(callback)


async def main_menu_number_of_common_numbers(callback: CallbackQuery | Message):
    """
    Функция реализующая главное меню первой задачи.
    """
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
@router.callback_query(
    F.data == 'task',
    StateFilter(
        FSMFirstTask.first_task_menu, FSMFirstTask.data_is_filled_in, FSMFirstTask.algorithm_completed
    )
)
async def show_task(callback: CallbackQuery):
    """
    Функция реализующая вывод условия задачи.
    """
    await callback.message.answer(
        text='<b>Входные данные</b>: два массива с числами. <b>Требуется</b> проверить сколько у массивов общих чисел. '
             'Также число будет считаться общим если оно входит в один массив, а в другом массиве находится '
             'его перевернутая версия.'
    )
    await callback.answer()


# Ввод исходных данных
@router.callback_query(
    F.data == 'input_data',
    StateFilter(
        FSMFirstTask.first_task_menu, FSMFirstTask.data_is_filled_in, FSMFirstTask.algorithm_completed
    )
)
async def input_data_menu(callback: CallbackQuery, state: FSMContext):
    """
    Функция реализующая начальную точку ввода исходных данных (если пользователь авторизован,
    то предлагается выбор способа инициализации данных, если нет, то сразу переход к ручной инициализации).
    """
    await callback.answer()
    if 'users_dict' in (await state.get_data()):
        await callback.message.answer(
            text='Как вы хотите заполнить исходные массивы чисел?',
            reply_markup=buttons.init_method()
        )
        await state.set_state(FSMFirstTask.data_filling_method)
    else:
        await init_by_hand_menu(callback, state)


# Инициализация массивов вручную
@router.callback_query(F.data == 'by_hand', StateFilter(FSMFirstTask.data_filling_method))
async def init_by_hand_menu(callback: CallbackQuery | Message, state: FSMContext):
    """
    Функция реализующая запрос к пользователю для ввода первого массива чисел.
    """
    await callback.answer()
    await callback.message.answer(text=f"Отправьте 1-й массив чисел записанных через пробел:")
    await state.set_state(FSMFirstTask.init_first_array)


@router.message(StateFilter(FSMFirstTask.init_first_array))
async def init_first_array(message: Message, state: FSMContext):
    """
    Функция реализующая сохранение первого массива и запрос на ввод второго массива.
    """
    try:
        await state.update_data(first_array=list(map(lambda x: float(x), message.text.split(' '))))
        await message.answer(text=f"Отправьте 2-й массив чисел записанных через пробел:")
        await state.set_state(FSMFirstTask.init_second_array)
    except ValueError:
        await message.answer(
            text='<u>Все элементы</u> массива должны принимать <u>числовые значения</u>.\n'
                 'Попробуйте еще раз:'
        )


@router.message(StateFilter(FSMFirstTask.init_second_array))
async def init_second_array(message: Message, state: FSMContext):
    """
    Функция реализующая сохранение второго массива и вывод сохраненных массивов в чат.
    """
    try:
        await state.update_data(second_array=list(map(lambda x: float(x), message.text.split(' '))))
        await message.answer(
            text=f"<b>Инициализация массивов прошла успешно</b> ✔️\n"
                 f"Первый массив: {' '.join(map(str, (await state.get_data())['first_array']))}\n"
                 f"Второй массив: {' '.join(map(str, (await state.get_data())['second_array']))}"
        )
        await state.set_state(FSMFirstTask.data_is_filled_in)
        await main_menu_number_of_common_numbers(message)
    except ValueError:
        await message.answer(
            text='<u>Все элементы</u> массива должны принимать <u>числовые значения</u>.\n'
                 'Попробуйте еще раз:'
        )


# Инициализация массивов случайным образом
@router.callback_query(F.data == 'auto_init', StateFilter(FSMFirstTask.data_filling_method))
async def auto_init_menu(callback: CallbackQuery | Message, state: FSMContext):
    """
    Функция реализующая запрос к пользователю для ввода размера первого массива.
     """
    await callback.message.answer(
        text=f"Введите размер 1-го массива который будет заполнен автоматически:"
    )
    await callback.answer()
    await state.set_state(FSMFirstTask.init_first_array_size)


@router.message(StateFilter(FSMFirstTask.init_first_array_size), F.text.isdigit())
async def init_first_array_size(message: Message, state: FSMContext):
    """
    Функция реализующая сохранение первого массива (со случайными числами)
    и запрос на ввод размера второго массива.
    """
    if int(message.text) > 0:
        await state.update_data(
            first_array=[round(random.random() * 10 * ((-1) ** random.randint(1, 2)), 1)
                         for _ in range(int(message.text))]
        )
        await message.answer(
            text=f"Введите размер 2-го массива который будет заполнен автоматически:"
        )
        await state.set_state(FSMFirstTask.init_second_array_size)
    else:
        await message.answer(
            text='<u>Размер массива</u> должен быть <u>больше 0</u>.\n'
                 'Попробуйте еще раз.'
        )


@router.message(StateFilter(FSMFirstTask.init_second_array_size), F.text.isdigit())
async def init_second_array_size(message: Message, state: FSMContext):
    """
    Фунция реализующая сохранение второго массива (со случайными числами) и вывод сохраненных массивов в чат.
    """
    if int(message.text) > 0:
        await state.update_data(
            second_array=[round(random.random() * 10 * ((-1) ** random.randint(1, 2)), 1)
                          for _ in range(int(message.text))]
        )
        await message.answer(
            text=f"<b>Инициализация массивов прошла успешно</b> ✔️️\n"
                 f"Первый массив: {' '.join(map(str, (await state.get_data())['first_array']))}\n"
                 f"Второй массив: {' '.join(map(str, (await state.get_data())['second_array']))}"
        )
        await state.set_state(FSMFirstTask.data_is_filled_in)
        await main_menu_number_of_common_numbers(message)
    else:
        await message.answer(
            text='<u>Размер массива</u> должен быть <u>больше 0</u>.\n'
                 'Попробуйте еще раз.'
        )


@router.message(StateFilter(FSMFirstTask.init_first_array_size, FSMFirstTask.init_second_array_size))
async def incorrect_array_size(message: Message):
    await message.answer(
        text='<u>Размер массива</u> должен принимать <u>целочисленные значения больше 0</u>.\n'
             'Попробуйте еще раз.'
    )


# Выполнение алгоритма
@router.callback_query(F.data == 'execute_algorithm', StateFilter(FSMFirstTask.data_is_filled_in))
async def execute_algorithm(callback: CallbackQuery, state: FSMContext):
    """
    Функция реализующая выполнение алгоритма для первой задачи.
    """
    await callback.answer()
    await state.update_data(num_of_common_numbers=number_of_common_numbers(
        (await state.get_data())['first_array'],
        (await state.get_data())['second_array']
    )
    )
    await callback.message.answer(text='<b>Алгоритм успешно выполнен!</b> ✔️')
    await state.set_state(FSMFirstTask.algorithm_completed)


@router.callback_query(F.data == 'execute_algorithm', StateFilter(FSMFirstTask.first_task_menu))
async def incorrect_execute_algorithm(callback: CallbackQuery):
    """
    Функция реализующая обработку ранней попытки запустить алгоритм.
    """
    await callback.message.answer(
        text='❌ Невозможно выполнить алгоритм, так как исходные массивы пустые. '
             'Заполните исходные данные и попробуйте еще раз.'
    )


@router.callback_query(F.data == 'execute_algorithm', StateFilter(FSMFirstTask.algorithm_completed))
async def incorrect_execute_algorithm(callback: CallbackQuery):
    """
    Функция реализующая обработку излишней попытки запустить алгоритм.
    """
    await callback.message.answer(
        text='❔ Для заданных исходных значений алгоритм уже выполнен.\n'
             'Вы можете вывести результаты работы алгоритма или ввести новые данные.'
    )


# Вывод результатов работы алгоритма
@router.callback_query(F.data == 'show_results', StateFilter(FSMFirstTask.algorithm_completed))
async def show_results(callback: CallbackQuery, state: FSMContext):
    """
    Функция реализующая вывод результатов работы алгоритма.
    """
    await callback.message.answer(
        text=f"<b>Результат работы алгоритма</b>\n"
             f"Первый массива: {' '.join(map(str, (await state.get_data())['first_array']))}\n"
             f"Второй массив: {' '.join(map(str, (await state.get_data())['second_array']))}\n"
             f"Количество общих чисел в обоих массивах: {(await state.get_data())['num_of_common_numbers']}"
    )
    await callback.answer()


@router.callback_query(F.data == 'show_results', StateFilter(FSMFirstTask.data_is_filled_in))
async def incorrect_show_results(callback: CallbackQuery):
    """
    Функция реализующая обработку ранней попытки вывести результаты (не выполнен алгоритм).
    """
    await callback.message.answer(
        text='❌ Невозможно вывести результат работы алгоритма, так как алгоритм не был выполнен. '
             'Запустите работу алгоритма и попробуйте еще раз.'
    )


@router.callback_query(F.data == 'show_results', StateFilter(FSMFirstTask.first_task_menu))
async def incorrect_show_results(callback: CallbackQuery):
    """
    Функция реализующая обработку ранней попытки вывести результаты (не заполнены данные).
    """
    await callback.message.answer(
        text='❌ Невозможно вывести результат работы алгоритма, так как исходные данные не заполнены. '
             'Заполните исходные данные и попробуйте еще раз.'
    )


@router.callback_query(
    F.data == 'exit_to_main_menu',
    StateFilter(
        FSMFirstTask.data_filling_method, FSMFirstTask.first_task_menu,
        FSMFirstTask.init_first_array, FSMFirstTask.init_second_array,
        FSMFirstTask.init_first_array_size, FSMFirstTask.init_second_array_size,
        FSMFirstTask.data_is_filled_in, FSMFirstTask.algorithm_completed,
    )
)
async def exit_to_main_menu(callback: CallbackQuery, state: FSMContext):
    """
    Функция реализующая выход в главное меню.
    """
    from main import tasks_menu
    await callback.answer()
    await state.clear()
    await tasks_menu(callback, state)


@router.message()
async def message_handler(message: Message):
    """
    Функция реализующая обработку сообщений, которые не прошли ни один фильтр.
    """
    await message.reply(text='🤔 Я не знаю такой команды.')


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
