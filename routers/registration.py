from aiogram.types import CallbackQuery, Message
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

import text
import kb
from states import Anketa
from base import cursor, db

from base import (delete_user)

router_registration = Router()

#================АНКЕТА===================
@router_registration.callback_query(F.data == "join")
async def f_join(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    delete_user(callback.from_user.id)
    cursor.execute(f"""INSERT INTO data_users VALUES (?, ?, ?, ?, ?, ?, ?)""", (callback.from_user.id, 0, 0, 0, 0, 0, callback.from_user.username))
    db.commit()
    
    await callback.message.answer(text.q_name, reply_markup=kb.back_to_main_kb2)
    await state.set_state(Anketa.name)

@router_registration.message(Anketa.name)
async def get_name(message: Message, state: FSMContext):
    if message.text == None:
        
        await message.answer(text.q_err_name, reply_markup=kb.back_to_main_kb2)
    else:
        cursor.execute("""UPDATE data_users SET name = (?) WHERE id = (?)""", (message.text, message.from_user.id))
        await state.update_data(name = message.text)
        
        await message.answer(text.q_occupation, reply_markup=kb.back_to_main_kb2)
        await state.set_state(Anketa.occupation)

@router_registration.message(Anketa.occupation)
async def get_occupation(message: Message, state: FSMContext):
    if message.text is None:
        
        await message.answer(text.q_err_occupation, reply_markup=kb.back_to_main_kb2)
    else:
        await state.update_data(occupation = message.text)
        cursor.execute("""UPDATE data_users SET occupation = (?) WHERE id = (?)""", (message.text, message.from_user.id))
        db.commit()
        
        await message.answer(text.q_education, reply_markup=kb.back_to_main_kb2)
        await state.set_state(Anketa.education)

@router_registration.message(Anketa.education)
async def get_education(message: Message, state: FSMContext):
    if message.text is None:
        
        await message.answer(text.q_err_education, reply_markup=kb.back_to_main_kb2)
    else:
        await state.update_data(education = message.text)
        cursor.execute("""UPDATE data_users SET education = (?) WHERE id = (?)""", (message.text, message.from_user.id))
        db.commit()
        
        await message.answer(text.q_about, reply_markup=kb.back_to_main_kb2)
        await state.set_state(Anketa.about)

@router_registration.message(Anketa.about)
async def get_about(message: Message, state: FSMContext):
    if message.text is None:
        
        await message.answer(text.q_err_about, reply_markup=kb.back_to_main_kb2)
    else:
        await state.update_data(about = message.text)
        cursor.execute("""UPDATE data_users SET about = (?) WHERE id = (?)""", (message.text, message.from_user.id))
        db.commit()
        
        await message.answer(text.q_photo, reply_markup=kb.back_to_main_kb2)
        await state.set_state(Anketa.photo)

@router_registration.message(Anketa.photo)
async def get_photo_and_output_anketa(message: Message, state: FSMContext):
    global flag_media_id
    if message.photo:
        if message.media_group_id and not flag_media_id:
            flag_media_id = message.media_group_id
            
            await message.answer(text.alotphoto, reply_markup=kb.back_to_main_kb2)

        else:
            if not message.media_group_id:
                flag_media_id = None
                await state.update_data(photo = message.photo[-1].file_id)
                cursor.execute("""UPDATE data_users SET photo = (?) WHERE id = (?)""", (message.photo[-1].file_id, message.from_user.id))
                db.commit()
                await state.clear()
                
                await message.answer(text.get_anketa, reply_markup=kb.after_reg_kb)


    else:
        
        await message.answer(text.q_err_photo, reply_markup=kb.back_to_main_kb2)