from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

import base
import text
import kb
from states import Anketa

router_registration = Router()

#================АНКЕТА===================
@router_registration.callback_query(F.data == "join")
async def f_join(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text.q_start, reply_markup=kb.skiper)
    await callback.message.answer(text.q_name, reply_markup=kb.back_to_main_kb2)
    await state.set_state(Anketa.name)

@router_registration.message(Anketa.name)
async def get_name(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer(text.q_err_name, reply_markup=kb.back_to_main_kb2)
    else:
        if message.text == text.skip:
            await message.answer(text.q_occupation, reply_markup=kb.back_to_main_kb2)
            await state.update_data(name="-")
            await state.set_state(Anketa.occupation)
        else:
            await state.update_data(name = message.text)
            await message.answer(text.q_occupation, reply_markup=kb.back_to_main_kb2)
            await state.set_state(Anketa.occupation)

@router_registration.message(Anketa.occupation)
async def get_occupation(message: Message, state: FSMContext):
    if message.text is None:
        await message.answer(text.q_err_occupation, reply_markup=kb.back_to_main_kb2)
    else:
        if message.text == text.skip:
            await message.answer(text.q_education, reply_markup=kb.back_to_main_kb2)
            await state.update_data(occupation="-")
            await state.set_state(Anketa.education)
        else:
            await state.update_data(occupation = message.text)
            await message.answer(text.q_education, reply_markup=kb.back_to_main_kb2)
            await state.set_state(Anketa.education)

@router_registration.message(Anketa.education)
async def get_education(message: Message, state: FSMContext):
    if message.text is None:
        await message.answer(text.q_err_education, reply_markup=kb.back_to_main_kb2)
    else:
        if message.text == text.skip:
            await message.answer(text.q_about, reply_markup=kb.back_to_main_kb2)
            await state.update_data(education="-")
            await state.set_state(Anketa.about)
        else:
            await state.update_data(education = message.text)
            await message.answer(text.q_about, reply_markup=kb.back_to_main_kb2)
            await state.set_state(Anketa.about)

@router_registration.message(Anketa.about)
async def get_about(message: Message, state: FSMContext):
    if message.text is None:
        await message.answer(text.q_err_about, reply_markup=kb.back_to_main_kb2)
    else:
        if message.text == text.skip:
            await message.answer(text.q_photo, reply_markup=kb.back_to_main_kb2)
            await state.update_data(about="-")
            await state.set_state(Anketa.photo)
        else:
            await state.update_data(about = message.text)
            await message.answer(text.q_photo, reply_markup=kb.back_to_main_kb2)
            await state.set_state(Anketa.photo)

@router_registration.message(Anketa.photo)
async def get_photo_and_output_anketa(message: Message, state: FSMContext):
    if message.text == text.skip:
        await state.update_data(photo=None)
    else:
        global flag_media_id
        if message.photo:
            if message.media_group_id and not flag_media_id:
                flag_media_id = message.media_group_id
                await message.answer(text.alotphoto, reply_markup=kb.back_to_main_kb2)
            else:
                if not message.media_group_id:
                    flag_media_id = None
                    await state.update_data(photo = message.photo[-1].file_id)

        else:
            await message.answer(text.q_err_photo, reply_markup=kb.back_to_main_kb2)

    data = await state.get_data()
    username = message.from_user.username
    base.add_user(message.from_user.id, data, username)
    await message.answer(text.get_anketa, reply_markup=kb.after_reg_kb)
    await state.clear()