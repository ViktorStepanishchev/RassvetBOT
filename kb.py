from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import text

back_to_main_kb = [[InlineKeyboardButton(text = text.back, callback_data="back_to_main")]]


back_to_main_kb2 = [[InlineKeyboardButton(text = text.back, callback_data="back_to_main2")]]


back_to_main_after_done_anketa_kb = [[InlineKeyboardButton(text = text.redacting_anketa, callback_data="edit_ank")],
                                     [InlineKeyboardButton(text=text.back, callback_data="back_to_main_after_done_anketa")]]

rofl_kb = [[InlineKeyboardButton(text = text.back, callback_data="back_to_main_after_done_anketa")]]


start_kb = [
[InlineKeyboardButton(text = text.more_detailed, callback_data="discription"), InlineKeyboardButton(text = text.feedback, url="tg://resolve?domain=EfimovNM")],
[InlineKeyboardButton(text = text.join, callback_data="join")]
           ]


start_if_reg_user = [
[InlineKeyboardButton(text = text.more_detailed, callback_data="discription"), InlineKeyboardButton(text = text.feedback, url="tg://resolve?domain=EfimovNM")],
[InlineKeyboardButton(text = text.anketa, callback_data="user_anketa1")],
[InlineKeyboardButton(text = text.get_chat, callback_data="get_chat")]
                    ]


after_reg_kb = [
[InlineKeyboardButton(text = text.get_chat, callback_data="get_chat"), InlineKeyboardButton(text = text.anketa, callback_data="user_anketa1")],
[InlineKeyboardButton(text = text.back, callback_data="back_to_main")]
               ]


anketa_choice_kb = [[InlineKeyboardButton(text = text.view_anketa, callback_data="user_anketa"),
                     InlineKeyboardButton(text = text.redacting_anketa, callback_data="edit_ank")],
                    [InlineKeyboardButton(text = text.delete_anketa, callback_data="delete_ank")]]


individual_for_get_chat_kb = [
[InlineKeyboardButton(text = text.info_about_users, callback_data="info_users")],
[InlineKeyboardButton(text = text.back, callback_data="back_to_main")]
                             ]


individual_for_edit_anketa = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.leave_it_as_it_was)],
        [KeyboardButton(text=text.skip)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

skiper = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.skip)]
    ],
        resize_keyboard=True
)



back_to_main_kb_descr = [[InlineKeyboardButton(text = text.back, callback_data="back_to_main")],
                         [InlineKeyboardButton(text = text.join, callback_data="join")]]


start_kb = InlineKeyboardMarkup(inline_keyboard=start_kb)
back_to_main_kb = InlineKeyboardMarkup(inline_keyboard=back_to_main_kb)
back_to_main_kb2 = InlineKeyboardMarkup(inline_keyboard=back_to_main_kb2)
back_to_main_after_done_anketa_kb = InlineKeyboardMarkup(inline_keyboard=back_to_main_after_done_anketa_kb)
start_if_reg_user = InlineKeyboardMarkup(inline_keyboard=start_if_reg_user)
after_reg_kb = InlineKeyboardMarkup(inline_keyboard=after_reg_kb)
anketa_choice_kb = InlineKeyboardMarkup(inline_keyboard=anketa_choice_kb)
individual_for_get_chat_kb = InlineKeyboardMarkup(inline_keyboard=individual_for_get_chat_kb)
back_to_main_kb_descr = InlineKeyboardMarkup(inline_keyboard=back_to_main_kb_descr)
rofl_kb = InlineKeyboardMarkup(inline_keyboard=rofl_kb)


