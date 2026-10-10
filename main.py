import asyncio
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient, functions

# استخدام مفاتيح API الافتراضية الرسمية لكي يعمل تسجيل الدخول برقم الهاتف فوراً بدون تعقيد
API_ID = 611335
API_HASH = 'd52480d287ca3851ecfee7efc896956f'

# إنشاء جلسة العمل لحسابك الشخصي
client = TelegramClient('my_session', API_ID, API_HASH)

# تحديد توقيت العراق بدقة (UTC+3)
iraq_timezone = timezone(timedelta(hours=3))

async def update_live_time_loop():
    while True:
        try:
            # جلب الوقت الحالي بتوقيت العراق
            now = datetime.now(iraq_timezone)
            time_str = now.strftime("%I:%M %p") # تنسيق الساعة (مثلاً 02:15 م)
            
            # النص الحقيقي الذي سيظهر جنب الاسم أو في السيرة الذاتية (Bio)
            live_status = f"العراق 🕒 {time_str}"
            
            # أمر تحديث الحساب الشخصي المباشر
            await client(functions.account.UpdateProfileRequest(
                about=live_status
            ))
            print(f"[+] تم تحديث الساعة الحية بنجاح: {live_str}")
        except Exception as e:
            print(f"[-] خطأ أثناء تحديث الساعة: {e}")
            
        # الانتظار لمدة دقيقة واحدة بالضبط لتحديث الوقت التالي
        await asyncio.sleep(60)

async def main():
    print("جاري الاتصال بحسابك في تيليجرام...")
    # تسجيل الدخول التلقائي: سيطلب منك رقم الهاتف وكود التحقق في سجلات التشغيل (Logs) عند التشغيل لأول مرة
    await client.start()
    print("تم تسجيل الدخول بنجاح! وبدأت خدمة الوقت الحي في حسابك.")
    
    # تشغيل حلقة التحديث المستمرة
    await update_live_time_loop()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
