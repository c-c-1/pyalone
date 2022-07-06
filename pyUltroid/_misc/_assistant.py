# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import inspect
import re

from telethon import Button
from telethon.events import CallbackQuery, InlineQuery, NewMessage
from telethon.tl.types import InputWebDocument

from .. import LOGS, asst, ultroid_bot
from ..functions.admins import admin_check
from . import append_or_update, owner_and_sudos

OWNER = ultroid_bot.full_name

MSG = f"""
** الى ماذا تَنْظُر؟ الى رجُلٍ عَبَثَ بالتِاريخ وعاش بيّن صفّحاتِه بطل ..**
- 𝑴𝒂𝒔𝒕𝒆𝒓 ⁦♪ : @C_C_1
- 𝑪𝒉𝒂𝒏𝒏𝒆𝒍 ♪ : @NvvvC
➖➖➖➖➖➖➖➖➖➖
"""

IN_BTTS = [
    [
        Button.url(
            "𝑪𝒉𝒂𝒏𝒏𝒆𝒍",
            url="t.me/NvvvM",
        ),
        Button.url("𝑴𝒂𝒔𝒕𝒆𝒓", url="t.me/C_C_1"),
    ]
]


# decorator for assistant


def asst_cmd(pattern=None, load=None, owner=False, **kwargs):
    """Decorator for assistant's command"""
    name = inspect.stack()[1].filename.split("/")[-1].replace(".py", "")
    kwargs["forwards"] = False

    def ult(func):
        if pattern:
            kwargs["pattern"] = re.compile("^/" + pattern)
        if owner:
            kwargs["from_users"] = owner_and_sudos
        asst.add_event_handler(func, NewMessage(**kwargs))
        if load is not None:
            append_or_update(load, func, name, kwargs)

    return ult


def callback(data=None, from_users=[], admins=False, owner=False, **kwargs):
    """Assistant's callback decorator"""
    if "me" in from_users:
        from_users.remove("me")
        from_users.append(ultroid_bot.uid)

    def ultr(func):
        async def wrapper(event):
            if admins and not await admin_check(event):
                return
            if from_users and event.sender_id not in from_users:
                return await event.answer("Not for You!", alert=True)
            if owner and event.sender_id not in owner_and_sudos():
                return await event.answer(f"This is {OWNER}'s bot!!")
            try:
                await func(event)
            except Exception as er:
                LOGS.exception(er)

        asst.add_event_handler(wrapper, CallbackQuery(data=data, **kwargs))

    return ultr


def in_pattern(pattern=None, owner=False, **kwargs):
    """Assistant's inline decorator."""

    def don(func):
        async def wrapper(event):
            if owner and event.sender_id not in owner_and_sudos():
                res = [
                    await event.builder.article(
                        title="• 𝑩𝒚 𝑨𝒍𝒐𝒏𝒆",
                        url="https://t.me/NvvvC",
                        description="- @NvvvM ~ @NvvvC",
                        text=MSG,
                        thumb=InputWebDocument(
                            "https://telegra.ph/file/e0a4c22e0faa158de7add.jpg",
                            0,
                            "image/jpeg",
                            [],
                        ),
                        buttons=IN_BTTS,
                    )
                ]
                return await event.answer(
                    res,
                    switch_pm=f"- 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒐𝒇 𝑨𝒍𝒐𝒏𝒆",
                    switch_pm_param="start",
                )
            try:
                await func(event)
            except Exception as er:
                LOGS.exception(er)

        asst.add_event_handler(wrapper, InlineQuery(pattern=pattern, **kwargs))

    return don
