from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from database import cur, save
from utils import get_info_wallet

import datetime
from typing import Union
import asyncio

@Client.on_callback_query(filters.regex(r"^user_info$"))
async def user_info(c: Client, m: CallbackQuery):
    hora_atual = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))

    hora_atual_str = hora_atual.strftime('%H:%M:%S')

    data_atual = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))

    data_atual_str = data_atual.strftime('%d/%m/%Y')
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
             [
                 InlineKeyboardButton("❮ ❮", callback_data="start"),
             ],

        ]
    )
    link = f""
    await m.edit_message_text(
        f"""<b>{get_info_wallet(m.from_user.id)}""",
        reply_markup=kb,
    )


@Client.on_callback_query(filters.regex(r"^dev$"))
async def btc(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
      
            [
                InlineKeyboardButton("Menu", callback_data="start"),
            ],
        ]
    )
    await m.edit_message_text(
        f"""<b>🛠️ CONTATO DO CRIADOR DO BOT 🛠️

⚠️ ATENÇÃO ANTES DE CONTATA-LO ⚠️

O desenvolvedor não possui responsabilidade alguma sobre este Bot e nem sobre o adm do mesmo, caso entre em contato para reclamar sobre material ou pedir para chamar o adm deste Bot ou algo do tipo, será bloqueado de imediato... Apenas o Chame, caso queira conhecer nossos Bots.

⚠️ SE CHAMAR O DESENVOLVEDOR PRA TRATAR ASSUNTOS DE MATERIAL, PIX NAO TER CAIDO E ETC... ⚠️ VAI SER BLOQUEADO ⚠️

Vendedor: @gringomdz

ALUGEL BOT TELEGRAM:

💳| VENDAS DISPONIVEIS:

💳| INFO CCS / MIX
💳| CONSULTAVEIS / CONSULTADAS
💳| LOGINS / CONTAS PREMIUM  

🔸| PIX DISPONIVEIS:

NUBANK | PF/PJ
MERCADO PAGO | PF/PJ
GERENCIANET/EFI | PF/PJ
ASAAS | PJ
PIX MANUAL | PF/PJ


⚠️ SE CHAMAR O DESENVOLVEDOR PRA TRATAR ASSUNTOS DE MATERIAL, PIX NAO TER CAIDO E ETC... ⚠️ VAI SER BLOQUEADO ⚠️

VENDEDOR: @gringomdz

CANAL:
https://t.me/mdzup

ATENDIMENTO WHATSAPP:
http://wa.me/5555555555</b>""",
        reply_markup=kb,
    )  

@Client.on_callback_query(filters.regex(r"^history$"))
async def history(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
        
        [
        InlineKeyboardButton("💳 Historico de DOC", callback_data="buy_history"),],
       [ InlineKeyboardButton("💳 Historico de LOGINS", callback_data="buy_history_log")
        ],
        [ InlineKeyboardButton("💳 Historico de CONSUL", callback_data="buy_history_cons")
        ],
        [ InlineKeyboardButton("💳 Historico de VALES", callback_data="buy_history_vales")
        ],
            [
                InlineKeyboardButton("❮ ❮", callback_data="user_info"),
            ],
        ]
    )
    await m.edit_message_text(
        f"""⚠️ Selecione qual historico de compras você deseja ver.</b>""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^buy_history$"))
async def buy_history(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT nome, cpf, linkdoc, bought_date , level, score ,localidade FROM docs_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras</b>
<i>- Histórico de 50 últimas compras.</i>
NOME|CPF|LINK|COMPRADO|TIPO|SCORE|CIDADE

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^buy_history_log$"))
async def buy_history_log(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT tipo, email, senha, cidade bought_date FROM logins_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras</b>
<i>- Histórico de 50 últimas compras.</i>
TIPO|EMAIL|SENHA|CIDADE|COMPRADO

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^buy_history_vales$"))
async def buy_history_vales(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT tipo, email, senha, cpf,limite,cidade bought_date FROM vales_sold WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras</b>
<i>- Histórico de 50 últimas compras.</i>
TIPO|EMAIL|SENHA|CPF|LIMIE|CIDADE|COMPRADO

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^buy_history_cons$"))
async def buy_history_cons(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="history"),
            ],
        ]
    )
    history = cur.execute(
        "SELECT limite, preco, anjo, token,cc,bincc,senha,mes,ano,cvv,cpf,telefone,nome,nomebanco bought_date FROM consul_solds WHERE owner = ? ORDER BY bought_date DESC LIMIT 50",
        [m.from_user.id],
    ).fetchall()

    if not history:
        cards_txt = "<b>⚠️ Não há nenhuma compra nos registros.</b>"
    else:
        documentos = []
        print(documentos)
        for card in history:
            documentos.append("|".join([i for i in card]))
        cards_txt = "\n".join([f"<code>{cds}</code>" for cds in documentos])

    await m.edit_message_text(
        f"""<b>🛒 Histórico de compras de consul</b>
<i>- Histórico de 50 últimas compras.</i>

{cards_txt}""",
        reply_markup=kb,
    )

@Client.on_callback_query(filters.regex(r"^swap$"))
async def swap_points(c: Client, m: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="user_info"),
            ],
        ]
    )

    user_id = m.from_user.id
    balance, diamonds = cur.execute(
        "SELECT balance, balance_diamonds FROM users WHERE id=?", [user_id]
    ).fetchone()

    if diamonds >= 100:
        add_saldo = round((diamonds / 2), 2)
        new_balance = round((balance + add_saldo), 2)

        txt = f"⚜️ Seus <b>{diamonds}</b> pontos foram convertidos em R$ <b>{add_saldo}</b> de saldo."

        cur.execute(
            "UPDATE users SET balance = ?, balance_diamonds=?  WHERE id = ?",
            [new_balance, 0, user_id],
        )
        return await m.edit_message_text(txt, reply_markup=kb)

    await m.answer(
        "⚠️ Você não tem pontos suficientes para realizar a troca. O mínimo é 100 pontos.",
        show_alert=True,
    )


@Client.on_callback_query(filters.regex(r"^swap_info$"))
async def swap_info(c: Client, m: CallbackQuery):
    await m.message.delete()

    cpf = await m.message.ask(
        "<b>👤 CPF da lara (válido) da lara que irá pagar</b>",
        reply_markup=ForceReply(),
        timeout=120,
    )
    name = await m.message.ask(
        "<b>👤 Nome completo do pagador</b>", reply_markup=ForceReply(), timeout=120
    )
    email = await m.message.ask(
        "<b>📧 E-mail</b>", reply_markup=ForceReply(), timeout=120
    )
    cpf, name, email = cpf.text, name.text, email.text
    cur.execute(
        "UPDATE users SET cpf = ?, name = ?, email = ?  WHERE id = ?",
        [cpf, name, email, m.from_user.id],
    )
    save()

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("❮ ❮", callback_data="start"),
            ]
        ]
    )
    await m.message.reply_text(
        "<b>⚠️ Seus dados foram alterados com sucesso.</b>", reply_markup=kb
    )



