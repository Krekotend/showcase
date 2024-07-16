import sql
import metric

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InputFile, InputMediaPhoto
from config import load_config

router: Router = Router()

admins: list = list(map(int, load_config().admins.admins.split(',')))


@router.message(F.photo, F.from_user.id.in_(admins), Command('add_image'))
async def add_image(message: Message, command):
    photo_id = f"{message.photo[-1].file_id}"
    data = command.args.split('_')
    photo_name = data[0]
    disc = data[1]
    if sql.write_media_table(photo_id=photo_id, photo_name=photo_name, disc=disc):
        await message.answer(text=f"Added to database")
    else:
        await message.answer(text="Change name")


@router.message(F.from_user.id.in_(admins), Command('list_items'))
async def models_list(message: Message, command):
    list_items = '\n'.join(sorted([f'{id_m}({model})' for id_m, model, age in sql.take_info_models()]))
    await message.answer(text=list_items)


@router.message(F.from_user.id.in_(admins), Command('add_item'))
async def add_item(message: Message, command):
    inf_item = command.args.split('_')
    sql.write_item(*inf_item)
    await message.answer(text='Item added')


@router.message(F.from_user.id.in_(admins), Command('add_desc'))
async def add_item_desc(message: Message, command):
    article = command.args.split('_')[0]
    desc_item = f"{' '.join(command.args.split('_')[1:])}"
    sql.add_desc_item(article, desc_item)
    await message.answer(text='Description written')


@router.message(F.from_user.id.in_(admins), Command('add_pay'))
async def add_pay(message: Message, command):
    article = command.args.split('_')[0]
    pay = list(map(int, f'''{command.args.split('_')[1]}'''.split(',')))
    sql.add_pay_item(article, pay)
    await message.answer(text='Price added')


@router.message(F.from_user.id.in_(admins), Command('add_img'))
async def add_image(message: Message, command):
    photo_id = f"{message.photo[-1].file_id}"
    article = command.args
    sql.add_photo_item(article, photo_id)
    await message.answer(text='Photo added')


@router.message(F.from_user.id.in_(admins), Command('del_item'))
async def del_item (message: Message, command):
    article = command.args
    sql.del_item(article)
    await message.answer(text='Item deleted')


@router.message(F.from_user.id.in_(admins), Command('users_day'))
async def count_users_day(message: Message, command):
    day = command.args
    users_day = metric.count_rows_day(day)
    await message.answer(text=users_day)

@router.message(F.from_user.id.in_(admins), Command('users_month'))
async def count_users_day(message: Message, command):
    month = command.args
    users_month = metric.count_rows_mon(month)
    await message.answer(text=users_month)
