import sql

from aiogram import Router, F, Dispatcher, types, utils
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InputFile, InputMediaPhoto
from lexsicon import translations as trsl
from keyboards import (main_keyb, info_keyb, items_keyb,
                       card_item_keyb, rews_keyb, lang_menu)

router: Router = Router()


class PhotoStates(StatesGroup):
    current_index = State()
    rews_index = State()


@router.message(CommandStart())
async def process_start_command(message: Message):
    photo = str(sql.take_media('lang'))
    await message.answer_photo(photo=photo,
                               caption=' ',
                               reply_markup=lang_menu)


@router.callback_query(F.data == 'lang')
async def lang(callback: CallbackQuery):
    await process_start_command(callback.message)


@router.callback_query(F.data.in_(['en', 'ru']))
async def main_menu(callback: CallbackQuery):
    tg_id = callback.from_user.id
    name = callback.from_user.username
    lang_data = callback.data
    sql.write_users_table(name=name, tg_id=tg_id, lang=lang_data)
    lang = sql.get_lang(tg_id)
    photo = str(sql.take_media('mainwall'))
    caption_main = trsl[lang]['caption_main']
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_main),
                                      reply_markup=main_keyb(lang),
                                      parse_mode='MarkdownV2')
    await callback.answer()


@router.callback_query(F.data == 'info')
async def shows_info(callback: CallbackQuery):
    lang = sql.get_lang(callback.from_user.id)
    caption_info = trsl[lang]['caption_info']
    photo = str(sql.take_media('info'))
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_info),
                                      reply_markup=info_keyb(lang),
                                      parse_mode='MarkdownV2' )
    await callback.answer()


@router.callback_query(F.data == 'back')
async def back_to_main(callback: CallbackQuery):
    lang = sql.get_lang(callback.from_user.id)
    photo = str(sql.take_media('mainwall'))
    caption_main = trsl[lang]['caption_main']
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_main),
                                      reply_markup=main_keyb(lang),
                                      parse_mode='MarkdownV2')
    await callback.answer()


@router.callback_query(F.data == 'items')
async def show_items(callback: CallbackQuery):
    lang = sql.get_lang(callback.from_user.id)
    caption_all_mod = trsl[lang]['caption_all_mod']
    photo = str(sql.take_media('mainwall'))
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_all_mod),
                                      reply_markup=items_keyb(lang),
                                      parse_mode='MarkdownV2')
    await callback.answer()


@router.callback_query(F.data.in_([str(i) for i in range(1, 99)]))
async def show_item(callback: CallbackQuery, state: FSMContext):
    lang = sql.get_lang(callback.from_user.id)
    all_info = sql.take_item(callback.data)[0]
    photo = all_info[4][0]
    pay = all_info[3]
    caption = (f'''{all_info[0]}  articl {all_info[1]}   \n\n'''v
               f'Discription: \n{all_info[2]}\n\n'
               f'Singl price - {pay[0]} €\n'
               f'if more 5  - {pay[1]} €\n\n'               
               f'contact the operator for details')

    await state.update_data(item_now=callback.data, current_index=0, caption=caption)

    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption),
                                      reply_markup=card_item_keyb(lang),
                                      parse_mode='MarkdownV2')
    await callback.answer()


@router.callback_query(F.data == "next_photo")
async def next_photo(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = sql.get_lang(callback.from_user.id)

    current_index = data.get('current_index', 0)
    item = data.get('item_now', 0)
    caption = data.get('caption', '')
    all_photo = sql.take_item(item)[0][4]
    next_index = (current_index + 1) % len(all_photo)
    photo = all_photo[next_index]

    if current_index == next_index:
        await callback.answer()
        return

    await state.update_data(current_index=next_index)

    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption),
                                      reply_markup=card_item_keyb(lang))
    await callback.answer()


@router.callback_query(F.data == 'reviews')
async def show_items(callback: CallbackQuery, state: FSMContext):
    lang = sql.get_lang(callback.from_user.id)
    photos = sql.take_rews()
    caption_rews = trsl[lang]['caption_rews']

    await state.update_data(photos=photos, rews_index=0, caption=caption_rews)

    await callback.message.edit_media(InputMediaPhoto(media=photos[0],
                                                      caption=caption_rews),
                                      reply_markup=rews_keyb(lang),
                                      parse_mode='MarkdownV2')
    await callback.answer()


@router.callback_query(F.data == "next_rews")
async def next_photo(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = sql.get_lang(callback.from_user.id)

    rews_index = data.get('rews_index', 0)
    caption = data.get('caption', '')
    all_photo = data.get('photos')
    next_index = (rews_index + 1) % len(all_photo)
    photo = all_photo[next_index]

    if rews_index == next_index:
        await callback.answer()
        return

    await state.update_data(rews_index=next_index)

    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption),
                                      reply_markup=rews_keyb(lang))
    await callback.answer()


@router.message(Command(commands=['dice']))
async def cmd_dice_in_group(message: Message):
    await message.answer_dice(emoji="🎲")


@router.message()
async def other(message: Message):
    lang = sql.get_lang(message.from_user.id)
    caption_other = trsl[lang]['caption_other']
    await message.reply(text=caption_other)
