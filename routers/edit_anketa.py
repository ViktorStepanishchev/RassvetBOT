from aiogram.types import CallbackQuery, Message
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

import text
from base import cursor, db, update_user
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
    if message.text == text.skip:
        await message.answer(text.q_occupation, reply_markup=kb.individual_for_edit_anketa)
        await state.update_data(name="-")
        await state.set_state(edit_ank.occupation)
    else:
        if message.text == text.leave_it_as_it_was:
            await state.update_data(name=cursor.execute("""SELECT name FROM data_users WHERE id = ?""", (message.from_user.id,)).fetchone()[0])
            await message.answer(text.q_occupation, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.occupation)
        else:

            await state.update_data(name=message.text)

            await message.answer(text.q_occupation, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.occupation)


@router_edit.message(edit_ank.occupation)
async def get_occupation(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer(text.q_err_occupation, reply_markup=kb.individual_for_edit_anketa)
    if message.text == text.skip:
        await message.answer(text.q_education, reply_markup=kb.individual_for_edit_anketa)
        await state.update_data(occupation="-")
        await state.set_state(edit_ank.education)
    else:
        if message.text == text.leave_it_as_it_was:
            await state.update_data(occupation=cursor.execute("""SELECT occupation FROM data_users WHERE id = ?""", (message.from_user.id,)).fetchone()[0])
            await message.answer(text.q_education, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.education)
        else:

            await state.update_data(occupation=message.text)
            await message.answer(text.q_education, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.education)


@router_edit.message(edit_ank.education)
async def get_education(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer(text.q_err_education, reply_markup=kb.individual_for_edit_anketa)
    if message.text == text.skip:
        await message.answer(text.q_about, reply_markup=kb.individual_for_edit_anketa)
        await state.update_data(education="-")
        await state.set_state(edit_ank.about)
    else:
        if message.text == text.leave_it_as_it_was:
            await state.update_data(education=cursor.execute("""SELECT education FROM data_users WHERE id = ?""", (message.from_user.id,)).fetchone()[0])
            await message.answer(text.q_about, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.about)
        else:

            await state.update_data(education=message.text)

            await message.answer(text.q_about, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.about)


@router_edit.message(edit_ank.about)
async def get_about(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer(text.q_err_about, reply_markup=kb.individual_for_edit_anketa)
    if message.text == text.skip:
        await message.answer(text.q_photo, reply_markup=kb.individual_for_edit_anketa)
        await state.update_data(about="-")
        await state.set_state(edit_ank.photo)
    else:
        if message.text == text.leave_it_as_it_was:
            await state.update_data(about=cursor.execute("""SELECT about FROM data_users WHERE id = ?""", (message.from_user.id,)).fetchone()[0])
            await message.answer(text.q_photo, reply_markup=kb.individual_for_edit_anketa)
            await state.set_state(edit_ank.photo)
        else:
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
            await message.answer(text.alotphoto, reply_markup=kb.back_to_main_kb2)
        else:
            if not message.media_group_id:
                flag_media_id = None
                await state.update_data(photo=message.photo[-1].file_id)
                data = await state.get_data()
                update_user(message.from_user.id, data)
                await state.clear()
                await message.answer(text.redacted, reply_markup=kb.after_reg_kb)
    elif message.text == text.skip:
        await state.update_data(photo=None)
        data = await state.get_data()
        update_user(message.from_user.id, data)
        await state.clear()
        await message.answer(text.redacted, reply_markup=kb.after_reg_kb)
    elif message.text == text.leave_it_as_it_was:
        await state.update_data(photo=cursor.execute("""SELECT photo FROM data_users WHERE id = ?""", (message.from_user.id,)).fetchone()[0])
        data = await state.get_data()
        update_user(message.from_user.id, data)
        await state.clear()
        await message.answer(text.redacted, reply_markup=kb.after_reg_kb)
    else:
        await message.answer(text.q_err_photo, reply_markup=kb.back_to_main_kb2)