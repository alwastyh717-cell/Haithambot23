import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8643244738:AAGMF6yW7uhTkel2sXktrliTNxaYrDxa7F4"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


class VerificationState(StatesGroup):
  waiting_for_answer = State()


user_verification = {}


def main_menu_keyboard():
  return InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(text="شراء رقم", callback_data="buy_number"),
              InlineKeyboardButton(
                  text="شراء أرقام SMS", callback_data="buy_sms"
              ),
          ],
          [
              InlineKeyboardButton(
                  text="رصيدك الحالي", callback_data="my_balance"
              ),
              InlineKeyboardButton(
                  text="الشحن التلقائي", callback_data="auto_charge"
              ),
          ],
          [
              InlineKeyboardButton(
                  text="دعوة صديق", callback_data="invite_friend"
              ),
              InlineKeyboardButton(
                  text="الوكيل الرسمي", callback_data="official_agent"
              ),
          ],
      ]
  )


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  num1 = random.randint(1, 5)
  num2 = random.randint(1, 5)
  correct_answer = num1 + num2

  user_verification[user_id] = correct_answer
  await state.set_state(VerificationState.waiting_for_answer)

  verify_kb = InlineKeyboardMarkup(inline_keyboard=[
      [
          InlineKeyboardButton(
              text="🔄 إعادة المحاولة", callback_data="retry_verify"
          )
      ]
  ])

  await message.answer(
      f"للتحقق من أنك لست روبوت، الرجاء حل المعادلة التالية:\n\n"
      f"<b>{num1} + {num2} = ?</b>\n\n"
      f"📍 أرسل الإجابة كرقم فقط:",
      reply_markup=verify_kb,
      parse_mode="HTML",
  )


@dp.message(VerificationState.waiting_for_answer)
async def process_verification(message: types.Message, state: FSMContext):
  user_id = message.from_user.id
  text = message.text.strip()

  if not text.isdigit():
    await message.answer("❌ الرجاء إرسال رقم صحيح فقط لإجابة المعادلة.")
    return

  user_answer = int(text)
  correct_answer = user_verification.get(user_id)

  if user_answer == correct_answer:
    await state.clear()
    welcome_text = (
        f"أهلاً بك في بوت بيع حسابات تيليجرام!\n\n"
        f"🆔 أيديك: <code>{user_id}</code>\n"
        f"💰 نقاطك: 0.0\n\n"
        f"✨ يختص هذا البوت في بيع حسابات تيليجرام.\n"
        f"🚀 استخدم الأزرار أدناه للتحكم."
    )
    await message.answer(
        welcome_text, reply_markup=main_menu_keyboard(), parse_mode="HTML"
    )
  else:
    await message.answer(
        "❌ الإجابة خاطئة. حاول مرة أخرى أو اضغط على إعادة المحاولة."
    )


@dp.callback_query(F.data == "retry_verify")
async def retry_verification(callback: types.CallbackQuery, state: FSMContext):
  await callback.message.delete()
  await cmd_start(callback.message, state)
  await callback.answer()


@dp.callback_query(
    F.data.in_({
        "buy_number",
        "buy_sms",
        "my_balance",
        "auto_charge",
        "invite_friend",
        "official_agent",
    })
)
async def menu_callbacks(callback: types.CallbackQuery):
  action = callback.data
  if action == "buy_number":
    await callback.answer(
        "قسم شراء رقم (قريبًا ربط القسم)", show_alert=True
    )
  elif action == "buy_sms":
    await callback.answer(
        "قسم شراء أرقام SMS (قريبًا ربط القسم)", show_alert=True
    )
  elif action == "my_balance":
    await callback.answer("رصيدك الحالي هو: 0.0 نقطة", show_alert=True)
  elif action == "auto_charge":
    await callback.answer(
        "قسم الشحن التلقائي (قريبًا ربط القسم)", show_alert=True
    )
  elif action == "invite_friend":
    await callback.answer(
        "رابط الإحالة الخاص بك قيد التفعيل", show_alert=True
    )
  elif action == "official_agent":
    await callback.answer("تواصل مع الوكيل الرسمي عبر البوت", show_alert=True)


async def main():
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
