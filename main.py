from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
import buttons
import texts
from number_of_common_numbers import main_menu_number_of_common_numbers, message_handler, router as ft_router


API_TOKEN = '*'
tg_bot = Bot(token=API_TOKEN, parse_mode='HTML')
disp = Dispatcher(bot=tg_bot)

state = ''
users_dict = dict()


@disp.message(Command('start'))
async def welcome_message(message: Message):
    global state
    state = 'start'
    if message.from_user.id not in users_dict.keys():
        users_dict[message.from_user.id] = {'name': '', 'age': 0, 'user_auth': False}
    await message.answer(
        text=texts.welcome_message,
        reply_markup=buttons.welcome_menu()
    )


@disp.message(Command('tasks'))
@disp.callback_query(F.data == 'tasks')
async def tasks_menu(callback: CallbackQuery):
    global state
    state = 'tasks_menu'
    if isinstance(callback, CallbackQuery):
        await callback.answer()
        await callback.message.answer(text='<b>Главное меню задач</b>', reply_markup=buttons.tasks_menu())
    else:
        await callback.answer(text='<b>Главное меню задач</b>', reply_markup=buttons.tasks_menu())


@disp.message(Command('info'))
@disp.callback_query(F.data == 'info')
async def info(callback: CallbackQuery | Message):
    global state
    state = 'info'
    if users_dict[callback.from_user.id]['user_auth']:
        if isinstance(callback, CallbackQuery):
            await callback.answer()
            await callback.message.answer(text=texts.auth_help)
        else:
            await callback.answer(text=texts.auth_help)
        await go_to_tasks(callback)
    else:
        if isinstance(callback, CallbackQuery):
            await callback.answer()
            await callback.message.answer(text=texts.not_auth_help, reply_markup=buttons.user_auth())
        else:
            await callback.answer(text=texts.not_auth_help, reply_markup=buttons.user_auth())


@disp.callback_query(F.data == 'user_auth')
async def user_auth(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text='Введите свое имя:')
    global state
    state = 'auth_name'
    users_dict[callback.from_user.id]['user_auth'] = True


@disp.callback_query(F.data == 'first_task')
async def first_task(callback: CallbackQuery):
    global state
    state = 'first_task'
    await callback.answer()
    await main_menu_number_of_common_numbers(callback, state, users_dict)


@disp.callback_query(F.data == 'second_task')
async def second_task(callback: CallbackQuery):
    pass


@disp.callback_query(F.data == 'third_task')
async def third_task(callback: CallbackQuery):
    pass


@disp.message()
async def other_messages(message: Message):
    global state
    if state == 'auth_name':
        users_dict[message.from_user.id]['name'] = message.text
        await message.answer(text='Введите свой возраст:')
        state = 'auth_age'
    elif state == 'auth_age':
        if message.text.isdigit() and int(message.text) > 5:
            users_dict[message.from_user.id]['age'] = message.text
            await message.answer(text='Регистрация прошла успешно!')
            state = 'start'
            await go_to_tasks(message)
        else:
            await message.reply(
                text='Чтобы пользоваться ботом тебе должно быть <u>больше 5 лет</u> '
                     '(помни: возраст должен быть целым положительным числом).\n'
                     'Попробуйте еще раз.'
            )
    elif state == 'first_task':
        await message_handler(message)


@disp.callback_query(F.data == 'pass_auth')
async def go_to_tasks(callback: CallbackQuery | Message):
    if state == 'info' or state == 'start':
        if isinstance(callback, CallbackQuery):
            await callback.answer()
            await callback.message.answer(text='Перейти к задачам?', reply_markup=buttons.go_to_tasks())
        else:
            await callback.answer(text='Перейти к задачам?', reply_markup=buttons.go_to_tasks())


if __name__ == '__main__':
    disp.include_router(ft_router)
    disp.run_polling(tg_bot, close_bot_session=True)
