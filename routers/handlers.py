from aiogram.types import CallbackQuery, Message
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import base
import text
from base import cursor

import kb

router_handlers = Router()
flag_media_id = None

@router_handlers.message(Command("start")) #Описание
async def f_start(message: Message):
    if message.from_user.username is not None:
        cursor.execute("""SELECT id FROM data_users WHERE id = (?)""", (message.from_user.id,))
        if cursor.fetchone() is None:
            await message.answer(text.description, reply_markup=kb.start_kb)
        else:
            await message.answer(text.description, reply_markup=kb.start_if_reg_user)
    else:
        await message.answer(text.error_username)



@router_handlers.callback_query(F.data == "back_to_main") #Вернуться в главное меню
async def f_back_to_main(callback:CallbackQuery):
    cursor.execute("""SELECT id FROM data_users WHERE id = (?)""", (callback.from_user.id,))
    if cursor.fetchone() is None:
        await callback.message.edit_text(text.description, reply_markup=kb.start_kb)
    else:
        await callback.message.edit_text(text.description, reply_markup=kb.start_if_reg_user)

@router_handlers.callback_query(F.data == "back_to_main2") #Вернуться в главное меню после прерывания заполнения анкеты
async def f_back_to_main2(callback:CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text.description, reply_markup=kb.start_kb)

@router_handlers.callback_query(F.data == "back_to_main_after_done_anketa") #Вернуться в главное меню после просмотра анкеты
async def f_back_to_main_after_done_anketa(callback:CallbackQuery):
    cursor.execute("""SELECT id FROM data_users WHERE id = (?)""", (callback.from_user.id,))
    if cursor.fetchone() is None:
        await callback.message.answer(text.description, reply_markup=kb.start_kb)
    else:
        await callback.message.answer(text.description, reply_markup=kb.start_if_reg_user)


@router_handlers.callback_query(F.data == "discription") #Подробнее
async def f_discription(callback: CallbackQuery):
    await callback.message.edit_text(text.more_description, reply_markup=kb.back_to_main_kb)


@router_handlers.callback_query(F.data == "user_anketa") #Просмотр своей анкеты пользователем
async def f_user_anketa(callback: CallbackQuery):

    name = list(cursor.execute(f"SELECT name FROM data_users WHERE id = (?)", (callback.from_user.id,)).fetchone())[0]
    occupation = list(cursor.execute(f"SELECT occupation FROM data_users WHERE id = (?)", (callback.from_user.id,)).fetchone())[0]
    education = list(cursor.execute(f"SELECT education FROM data_users WHERE id = (?)", (callback.from_user.id,)).fetchone())[0]
    about = list(cursor.execute(f"SELECT about FROM data_users WHERE id = (?)", (callback.from_user.id,)).fetchone())[0]
    photo = list(cursor.execute(f"SELECT photo FROM data_users WHERE id = (?)", (callback.from_user.id,)).fetchone())[0]
    username = callback.from_user.username

    await callback.message.answer_photo(photo,
text.ank1 + '\n' + '\n' + text.ank2 + name + '\n' + text.ank3 + occupation + '\n' + text.ank4 + education + '\n' + '\n'
+ text.ank5 + '\n' + '\n' + about + '\n' + '\n' + "@"+username, reply_markup=kb.back_to_main_after_done_anketa_kb)



@router_handlers.callback_query(F.data == "user_anketa1") #После создания анкеты пользователем нажата кнопка АНКЕТА
async def f_user_anketa1(callback:CallbackQuery):
    await callback.message.edit_text(text.choice, reply_markup=kb.anketa_choice_kb)


@router_handlers.callback_query(F.data == "get_chat") #Получить чаты
async def f_get_chat(callback:CallbackQuery):
    await callback.message.edit_text(text.after_get_chat, reply_markup=kb.individual_for_get_chat_kb)


@router_handlers.callback_query(F.data == "info_users")
async def f_info_users(callback: CallbackQuery):
    users = ""

    for name in cursor.execute("SELECT username FROM data_users"):
        users += "@" + name[0] + "\n"

    await callback.message.edit_text(text.list_users + "\n" + "\n" + users, reply_markup=kb.back_to_main_kb)


@router_handlers.message(Command("info")) #Пробив по никнейму ТГ
async def f_get_info_another_user(message: Message):
    cursor.execute("SELECT photo FROM data_users WHERE id = (?)", (message.from_user.id,))
    if cursor.fetchone() is None:
        await message.answer(text.description, reply_markup=kb.start_kb)
    else:
        username = message.text[7:]
        if cursor.execute("SELECT username FROM data_users WHERE username = ?", (username,)).fetchone() is not None:
            info = cursor.execute(f"SELECT * FROM data_users WHERE username = ?", (username,)).fetchone()


            await message.answer_photo(info[5], '\n' + text.ank2 + info[1] + '\n' + text.ank3 + info[2] + '\n'
+ text.ank4 + info[3] + '\n' + '\n'+ text.ank5 + '\n' + '\n' + info[4] + '\n' + '\n' + "@"+username, reply_markup=kb.back_to_main_after_done_anketa_kb)
        else:
            await message.answer(text.no_user_in_list, reply_markup=kb.back_to_main_kb)
