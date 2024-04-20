from aiogram.types import CallbackQuery, Message
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

import text
from base import cursor, db
from states import edit_ank

import kb

router_edit = Router()

#================РЕДАКТИРОВАНИЕ АНКЕТЫ===================
@router_edit.callback_query(F.data == "edit_ank")
async def f_join(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text.q_name, reply_markup=kb.individual_for_edit_anketa)
    await state.set_state(edit_ank.name)

@router_edit.message(edit_ank.name)
async def get_name(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer(text.q_err_name, reply_markup=kb.individual_for_edit_anketa)
    else:
        if message.text == text.leave_it_as_it_was:
            await message.answer(text.q_occupation, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.occupation)
        else:
            cursor.execute("""UPDATE data_users SET name = (?) WHERE id = (?)""", (message.text, message.from_user.id))
            db.commit()
            await state.update_data(name=message.text)

            await message.answer(text.q_occupation, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.occupation)


@router_edit.message(edit_ank.occupation)
async def get_occupation(message: Message, state: FSMContext):
    if message.text == None:

        await message.answer(text.q_err_occupation, reply_markup=kb.individual_for_edit_anketa)
    else:
        if message.text == text.leave_it_as_it_was:
            await message.answer(text.q_education, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.education)
        else:
            cursor.execute("""UPDATE data_users SET occupation = (?) WHERE id = (?)""", (message.text, message.from_user.id))
            db.commit()
            await state.update_data(occupation=message.text)
            await message.answer(text.q_education, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.education)


@router_edit.message(edit_ank.education)
async def get_education(message: Message, state: FSMContext):
    if message.text == None:

        await message.answer(text.q_err_education, reply_markup=kb.individual_for_edit_anketa)
    else:
        if message.text == text.leave_it_as_it_was:
            await message.answer(text.q_about, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.about)
        else:
            cursor.execute("""UPDATE data_users SET education = (?) WHERE id = (?)""",(message.text, message.from_user.id))
            db.commit()
            await state.update_data(education=message.text)

            await message.answer(text.q_about, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.about)


@router_edit.message(edit_ank.about)
async def get_about(message: Message, state: FSMContext):
    if message.text == None:

        await message.answer(text.q_err_about, reply_markup=kb.individual_for_edit_anketa)
    else:
        if message.text == text.leave_it_as_it_was:
            await message.answer(text.q_photo, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.photo)
        else:
            cursor.execute("""UPDATE data_users SET about = (?) WHERE id = (?)""",(message.text, message.from_user.id))
            db.commit()
            await state.update_data(about=message.text)

            await message.answer(text.q_photo, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.photo)


flag_media_id = None
@router_edit.message(edit_ank.photo)
async def get_photo_and_output_edit_ank(message: Message, state: FSMContext):
    global flag_media_id
    if message.photo:
        if message.media_group_id and not flag_media_id:
            flag_media_id = message.media_group_id

            await message.answer(text.alotphoto, reply_markup=kb.individual_for_edit_anketa)

        else:
            if not message.media_group_id:
                flag_media_id = None
                await state.update_data(photo=message.photo[-1].file_id)
                cursor.execute("""UPDATE data_users SET photo = (?) WHERE id = (?)""", (message.photo[-1].file_id, message.from_user.id))
                db.commit()
                await state.clear()

                await message.answer(text.redacted, reply_markup=kb.after_reg_kb)


    else:
        if message.text == text.leave_it_as_it_was:
            await state.clear()
            await message.answer(text.redacted, reply_markup=kb.after_reg_kb)
        else:
            await message.answer(text.q_err_photo, reply_markup=kb.individual_for_edit_anketa)