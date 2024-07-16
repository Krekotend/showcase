from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from sql import take_info_items as t_i_m
from lexsicon import translations as trsl
from config import load_config

link_oper: str = load_config().operator.operator


def add_oper(keyboard: InlineKeyboardMarkup, text: str):
    return keyboard.inline_keyboard.append([InlineKeyboardButton(text=text,
                                                                 url=f'tg://user?id={link_oper}')])


def create_inline_kb(width: int = 0,
                     adj: list = [0],
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            print(button)
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    if width:
        kb_builder.row(*buttons, width=width)
    if adj != [0]:
        kb_builder.row(*buttons)
        kb_builder.adjust(*adj)

    return kb_builder.as_markup()


lang_buttons = {'en': '🇺🇸Eng', 'ru': '🇷🇺Рус'}
lang_menu = create_inline_kb(3, **lang_buttons)


def main_keyb(lang):
    main_m_buttons = {'items': f'''{trsl[lang]['items']}''',
                      'info': f'''{trsl[lang]['info']}'''}
    main_m_menu = create_inline_kb(1, **main_m_buttons)
    add_oper(main_m_menu, trsl[lang]['operator'])
    return main_m_menu


def info_keyb(lang):
    info_buttons = {'back': f'''{trsl[lang]['back']}''',
                    'reviews': f'''{trsl[lang]['reviews']}''',
                    'lang': f'''{trsl[lang]['lang']}'''}
    info_menu = create_inline_kb(2, **info_buttons)
    add_oper(info_menu, trsl[lang]['operator'])
    return info_menu


def items_keyb(lang):
    items_buttons = {str(article): (f'{name})') for article, name in t_i_m()}
    count = len(items_buttons.keys())
    count_m = [2 for i in range(count // 2)] + [1]
    items_buttons.setdefault('back', f'''{trsl[lang]['back']}''')
    items_menu = create_inline_kb(adj=count_m, **items_buttons)
    return items_menu


def card_item_keyb(lang):
    card_item_buttons = {'items': f'''{trsl[lang]['items']}''',
                          'next_photo': f'''{trsl[lang]['next_photo']}'''}
    card_item_menu = create_inline_kb(2, **card_item_buttons)
    add_oper(card_item_menu, f'''{trsl[lang]['operator']}''')
    return card_item_menu


def rews_keyb(lang):
    rews_buttons = {'next_rews': f'''{trsl[lang]['next_rews']}''',
                    'back': f'''{trsl[lang]['back']}'''}
    rews_menu = create_inline_kb(1, **rews_buttons)
    return rews_menu
