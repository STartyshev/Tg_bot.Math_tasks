from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import buttons
import texts
from number_of_common_numbers import pre_main_menu_number_of_common_numbers, router as ft_router


API_TOKEN = '*'
tg_bot = Bot(token=API_TOKEN, parse_mode='HTML')
disp = Dispatcher(bot=tg_bot)
users_dict = dict()


class FSMMathTasks(StatesGroup):
    default_state = State()
    info = State()
    auth_name = State()
    auth_age = State()
    pass_auth = State()
    ready_to_tasks = State()
    tasks = State()
    first_task = State()
    second_task = State()
    third_task = State()


@disp.message(Command('start'))
async def welcome_message(message: Message, state: FSMContext):
    """
    Функция реализующая вывод приветственного меню и начальную инициализацию информации о пользователе.
    """
    if message.from_user.id not in users_dict.keys():
        users_dict[message.from_user.id] = {'name': '', 'age': 0, 'user_auth': False}
    await message.answer(
        text=texts.welcome_message,
        reply_markup=buttons.welcome_menu()
    )
    await state.set_state(FSMMathTasks.default_state)


@disp.message(Command('tasks'), StateFilter(FSMMathTasks.default_state, FSMMathTasks.ready_to_tasks))
@disp.callback_query(F.data == 'tasks', StateFilter(FSMMathTasks.default_state, FSMMathTasks.ready_to_tasks))
async def tasks_menu(callback: CallbackQuery, state: FSMContext):
    """
    Функция реализующая вывод главного меню задач.
    """
    if isinstance(callback, CallbackQuery):
        await callback.answer()
        await callback.message.answer(text='<b>Главное меню задач</b>', reply_markup=buttons.tasks_menu())
    else:
        await callback.answer(text='<b>Главное меню задач</b>', reply_markup=buttons.tasks_menu())
    await state.set_state(FSMMathTasks.tasks)


@disp.message(
    Command('info'),
    StateFilter(
        FSMMathTasks.default_state, FSMMathTasks.pass_auth, FSMMathTasks.ready_to_tasks,
        FSMMathTasks.tasks
    )
)
@disp.callback_query(
    F.data == 'info',
    StateFilter(
        FSMMathTasks.default_state, FSMMathTasks.pass_auth, FSMMathTasks.ready_to_tasks,
        FSMMathTasks.tasks
    )
)
async def info(callback: CallbackQuery | Message, state: FSMContext):
    """
    Функция реализующая вывод информации о задачах для разного состояния авторизации.
    """
    if users_dict[callback.from_user.id]['user_auth']:
        if isinstance(callback, CallbackQuery):
            await callback.answer()
            await callback.message.answer(text=texts.help_with_auth)
        else:
            await callback.answer(text=texts.help_with_auth)
        await state.set_state(FSMMathTasks.info)
        await go_to_tasks(callback, state)
    else:
        if isinstance(callback, CallbackQuery):
            await callback.answer()
            await callback.message.answer(text=texts.help_without_auth, reply_markup=buttons.user_auth())
        else:
            await callback.answer(text=texts.help_without_auth, reply_markup=buttons.user_auth())
        await state.set_state(FSMMathTasks.info)


@disp.callback_query(F.data == 'user_auth', StateFilter(FSMMathTasks.info))
async def user_auth(callback: CallbackQuery, state: FSMContext):
    """
    Функция реализующая запрос к пользователю на ввод имени.
    """
    await callback.answer()
    await callback.message.answer(text='Введите свое имя:')
    await state.set_state(FSMMathTasks.auth_name)


@disp.message(StateFilter(FSMMathTasks.auth_name))
async def auth_name(message: Message, state: FSMContext):
    """
    Функция реализующая запись имени пользователя и запрос на ввод возраста.
    """
    users_dict[message.from_user.id]['name'] = message.text
    await message.answer(text='Введите свой возраст:')
    await state.set_state(FSMMathTasks.auth_age)


@disp.message(StateFilter(FSMMathTasks.auth_age), F.text.isdigit())
async def auth_age(message: Message, state: FSMContext):
    """
    Функция реализующая запись возраста пользователя при вводе числового значения.
    """
    if int(message.text) > 5:
        users_dict[message.from_user.id]['age'] = message.text
        users_dict[message.from_user.id]['user_auth'] = True
        await message.answer(text='Регистрация прошла успешно!')
        await state.update_data(users_dict=users_dict)
        await go_to_tasks(message, state)
    else:
        await message.reply(
            text='Чтобы пользоваться ботом тебе должно быть <u>больше 5 лет</u> '
                 '(помни: возраст должен быть целым положительным числом).\n'
                 'Попробуйте еще раз.'
        )


@disp.message(StateFilter(FSMMathTasks.auth_age))
async def incorrect_age(message: Message):
    await message.reply(
        text='<b>Возраст</b> должен быть <u>целым положительным числом</u>.\n'
             'Попробуйте еще раз.'
    )


@disp.callback_query(F.data == 'pass_auth', StateFilter(FSMMathTasks.info))
async def go_to_tasks(callback: CallbackQuery | Message, state: FSMContext):
    """
    Функция реализующая запрос к пользователю для перехода в меню задач.
    """
    await state.set_state(FSMMathTasks.ready_to_tasks)
    if isinstance(callback, CallbackQuery):
        await callback.answer()
        await callback.message.answer(text='Перейти к задачам?', reply_markup=buttons.go_to_tasks())
    else:
        await callback.answer(text='Перейти к задачам?', reply_markup=buttons.go_to_tasks())


@disp.callback_query(F.data == 'first_task', StateFilter(FSMMathTasks.tasks))
async def first_task(callback: CallbackQuery, state: FSMContext):
    """
    Функция реализующая переход в меню первой задачи.
    """
    await callback.answer()
    await state.set_state(FSMMathTasks.first_task)
    await pre_main_menu_number_of_common_numbers(callback, state)


@disp.callback_query(F.data == 'second_task', StateFilter(FSMMathTasks.ready_to_tasks))
async def second_task():
    pass


@disp.callback_query(F.data == 'third_task', StateFilter(FSMMathTasks.ready_to_tasks))
async def third_task():
    pass


@disp.message(
    StateFilter(
        FSMMathTasks.default_state, FSMMathTasks.info, FSMMathTasks.pass_auth,
        FSMMathTasks.ready_to_tasks, FSMMathTasks.tasks
    )
)
async def other_messages(message: Message):
    """
    Функция реализующая обработку сообщений, которые не прошли ни один фильтр.
    """
    await message.reply(text='🤔 Я не знаю такой команды.')


if __name__ == '__main__':
    disp.include_router(ft_router)
    disp.run_polling(tg_bot, close_bot_session=True)
