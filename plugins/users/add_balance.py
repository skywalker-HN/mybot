import math
from typing import Union

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import ADMIN_CHAT
from config import GRUPO_PUB
from database import cur, save
from config import BOT_LINK
from config import BOT_LINK_SUPORTE

from utils import create_mention, get_lara_info, get_support_user, insert_sold_balance


@Client.on_callback_query(filters.regex(r"^add_saldo$"))
async def add_saldo(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    "Pix Automático", callback_data="add_saldo_auto"
                ),
                InlineKeyboardButton("Pix Manual", callback_data="add_saldo_manual"),
                
            ],
            [
                InlineKeyboardButton("❮ ❮", callback_data="start"),
            ],
        ]
    )

    await m.edit_message_text(
        """<b>Qual forma de pagamento deseja adicionar Saldo?</b>""",
        reply_markup=kb,
    )


@Client.on_callback_query(filters.regex(r"^add_saldo_manual$"))
async def add_saldo_manual(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="add_saldo"),
            ],
        ]
    )

    pix_name, pix_key = get_lara_info()

    support_user = get_support_user()
    valor_min = 10
    details = (
        f"\n\n⚠️ <i>Não envie um valor menor que R${valor_min}, pois se você enviar perderá seu Dinheiro.</i>"
        if valor_min
        else ""
    )
    await m.edit_message_text(
        f"""<b>👤 Dados da Conta</b>

<b>Nome:</b> <code>{pix_name}</code>
<b>Pix:</b> <code>{pix_key}</code>

<b>⚠️ <i>Se você já fez o pagamento, envie o comprovante para</i> @AstaCarder
{details}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^btc$"))
async def btc(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("⚠️", callback_data="add_saldo"),
            ],
        ]
    )

    pix_name, pix_key = get_lara_info()

    support_user = BOT_LINK_SUPORTE
    valor_min = 20
    details = (
        f"\n\n⚠️ Não envie um valor menor que R${valor_min}, pois se você enviar perderá seu Dinheiro!"
        if valor_min
        else ""
    )
    await m.edit_message_text(
        f"""<b>💰Bitcoin Manual</b>\n\n
Para adicionar saldo via Bitcoin, envie a quantia que desejar para nosso endereço Bitcoin, segue o endereço:\n\n

<code>Endereço aqui</code>\n\n

Após enviar, chame {support_user} e mande o link da transação.
Será adicionado exatamente o valor que chegar à carteira.
{details}""",
        reply_markup=kb,
    )        


@Client.on_message(filters.regex(r"/resgatar (?P<gift>\w+)$"))
@Client.on_callback_query(filters.regex(r"^resgatar (?P<gift>\w+)$"))
async def resgatar_gift(c: Client, m: Union[CallbackQuery, Message]):
    user_id = m.from_user.id
    gift = m.matches[0]["gift"]

    if isinstance(m, Message):
        send = m.reply_text
    else:
        send = m.edit_message_text

    try:
        value = cur.execute(
            "SELECT value from gifts WHERE token = ?", [gift]
        ).fetchone()[0]
    except:
        return await send("<b>⚠️ Gift Card não existente ou já resgatado, digite</b> <i>/pix<i> </b>para adicionar saldo no Bot!</b>")

    cur.execute("DELETE FROM gifts WHERE token = ?", [gift])

    cur.execute(
        "UPDATE users SET balance = balance + ? WHERE id = ?", [value, user_id]
    ).fetchone()

    new_balance = cur.execute(
        "SELECT balance FROM users WHERE id = ?", [user_id]
    ).fetchone()[0]

    mention = create_mention(m.from_user)
    insert_sold_balance(value, user_id, "manual")
    base = f"""🎁 <code>{mention}</code> <b>Resgatou um Gift Card de<b> <b>R${value}</b>
    
💸 <b>Novo Saldo:</b> <b>R${new_balance}</b>
🎟️ <b>Gift Card:</b> <code>{gift}</code>"""

    await c.send_message(ADMIN_CHAT, base)
    
    kb = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="💳 Compre as melhores GG's",url="https://t.me/CloverStoreOfcBot"
                            ),
                        ],
                    ]
                )
    mention = m.from_user.first_name
    base = f"""🎁 <code>{mention}</code> <b>Resgatou um Gift Card de</b> <b>R${value}</b>
    
🎉 <b>Parabéns</b> <code>{mention}</code> <b>por ter resgatado o Gift!</b>

🎟️ <b>Gift Card:</b> <code>{gift[0:6]}</code>\n</a>"""
    await c.send_message(GRUPO_PUB, base, reply_markup=kb)

    if isinstance(m, CallbackQuery):
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        "🛒 Voltar ao bot",
                        url=f"https://t.me/{c.me.username}?start=start",
                    ),
                ],
            ]
        )
        await send(
            f"<b>🎁 {m.from_user.first_name} </b>resgatou</b> R${value} </b>no Bot.</b>",
            reply_markup=kb,
        )
    else:
        await send(
            f"<b> 🎉 Parabéns! foi adicionado</b> <b>R${value}</b> <b>em sua conta no Bot!</b>"
        )

    save()
