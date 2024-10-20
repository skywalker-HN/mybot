from typing import Union

from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database import cur, save
from utils import create_mention, get_info_wallet

GROUP_ID = -1002114686028

async def check_user_in_group(c: Client, user_id: int):
    try:
        await c.get_chat_member(GROUP_ID, user_id)
        return True, None  
    except Exception as e:
        if "USER_NOT_PARTICIPANT" in str(e):
            message = "<b>⚠️ Para acessar esse bot é obrigatório que se inscreva no canal clicando no botão abaixo para poder começar a usar o Bot!</b>"
            return False, message
        else:
            print("Error checking user in group: ", e)
            return False, '<b>⚠️ Ocorreu um erro ao verificar sua participação no grupo. Tente novamente mais tarde.</b>'

kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🤖 Registre-se", url="t.me/CloverStoreOfcBot"),
        ],
    ]
)

@Client.on_message(filters.command(["start", "menu"]) & filters.private)
@Client.on_callback_query(filters.regex("^start$") & filters.private)
async def start(c: Client, m: Union[Message, CallbackQuery]):
    user_id = m.from_user.id
    user_name = m.from_user.first_name

    is_in_group, message = await check_user_in_group(c, user_id)
    if not is_in_group:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton("⭐ Entre no Canal", url="https://t.me/CloverStoreCanal")]]
        )
        await m.reply_text(message, reply_markup=keyboard)
        return

    if isinstance(m, Message):
        refer = (
            int(m.command[1])
            if (len(m.command) == 2)
            and (m.command[1]).isdigit()
            and int(m.command[1]) != user_id
            else None
        )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("💳 Comprar", callback_data="shop")],
            [
                
                InlineKeyboardButton("💵 Adicionar Saldo", callback_data="add_saldo"),
                InlineKeyboardButton("👤 Informações", callback_data="user_info"),
            ],
         
        ]
    )

    bot_logo, news_channel, support_user = cur.execute(
        "SELECT main_img, channel_user, support_user FROM bot_config WHERE ROWID = 0"
    ).fetchone()

    start_message = f"""‌<a href='{bot_logo}'>&#8204</a><b><b> Olá</b> <i><code>{m.from_user.first_name}</code></i>, <b>Seja Bem-Vindo(a) à Clover Store!</b>"""

    if isinstance(m, CallbackQuery):
        send = m.edit_message_text
    else:
        send = m.reply_text
    save()
    await send(start_message, reply_markup=kb)
