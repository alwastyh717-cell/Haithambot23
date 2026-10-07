import asyncio
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient, functions

# استخدام مفاتيح API افتراضية عامة مسموحة لكي يعمل تسجيل الدخول برقم الهاتف فوراً
API_ID = 611335                # مفتاح افتراضي معتمد لتليجرام ديسكอป
API_HASH = 'd52480d287ca3851ecfee7efc896956f'

# إنشاء الجلسة تلقائياً باسم my_session
client = TelegramClient('my_session', API_ID, API_HASH)

# تحديد توقيت العراق (UTC+3)
iraq_timezone = timezone(timedelta(hours=3))

async def update_time_loop():
    while True:
        try:
            now = datetime.now(iraq_timezone)
            time_str = now.strftime("%I:%M %p") # تنسيق الوقت (مثلاً 06:15 م)
            
            # النص الذي سيظهر في البايو الخاص بحسابك
            new_bio = f"الساعة الآن في العراق 🕒 {time_str}"
            
            await client(functions.account.UpdateProfileRequest(
                about=new_bio
            ))
            print(f"تم تحديث الوقت في البايو بنجاح: {time_str}")
        except Exception as e:
            print(f"خطأ أثناء تحديث الوقت: {e}")
            
        # الانتظار لمدة دقيقة واحدة قبل التحديث القادم
        await asyncio.sleep(60)

async def main():
    print("جاري الاتصال بتليجرام... يرجى إدخال بيانات الحساب في الأسفل إن طلب ذلك.")
    # هذه الدالة ستطلب منك رقم الهاتف (Phone) ثم كود التحقق (Code) تلقائياً في السجلات (Logs)
    await client.start()
    print("تم تسجيل الدخول بنجاح وبدأ تحديث الوقت في حسابك!")
    await update_time_loop()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
