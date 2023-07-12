from telebot.types import InlineKeyboardButton, KeyboardButton
type_person01 = [0, "men talabaman", "Men ota-onaman", "maktabda o'qiyman", "kasbimni o'zgartirmoqchiman"]
text01 = {
    'id': 1,

    "name": "Davom etamiz, siz IT olamiga yaqinlashmoqdasiz. Ismingizni kiriting",

    "contact": "Super, endi telefon raqamingizni kiriting. "
               "Buni pastdagi tugma yordamida amalga oshirish mumkin yoki 998XXXXXXXX formatida habar yuboring.",

    "who_you": "Yakuniy urinish. Sizga eng aniq ma'lumotni berishimiz uchun shulardan birini tanlang",

    "action": "Mana boshlab ham oldik, biz sizni ochiq master-klassga yozishimiz mumkin "
              "yoki siz qo'ng'iroq qilish uchun ariza qoldirishingiz mumkin, bizning mutaxassisimiz siz bilan "
              "'it mutaxassis'so'zini aytishizga ulgurmasizdanoq siz bilan bog'lanishadi.",

    "call_back": "Ajoyib. Qachon suhbatlashish qulay bo'ladi?",

    "called": "Bizning mutaxassisimiz allaqachon sizga yordam berishga shoshilmoqda. "
              "Siz belgilagan vaqtda qo'ng'iroq qiladilar",

    "call_friend": "Birgalikda o'rganish har doim qiziqarliroq! "
                   "Do'stini olib kelgan har bir kishi dars ohirida yoqimli bonusga ega bo'ladi.",

    "message_friend": "IT mutaxassisi bo'lishning oson yo'li, bepul sinov darsiga keling.",

    "webinar": "Ajoyib! Keling, master-klassning sanasi va vaqtini aniqlaylik?",

    "alert": "Nimadir hato ketdi. Katta ehtimol bilan raqam noto'g'ri. Iltimos, "
             "raqamni tekshiring va qayta urinib ko'ring😊",

    "vebinar_date": "Keling, master-klassning sanasi va vaqtini aniqlaylik??",

    "super": "Ajoyib!",

    "sorry": "Uzr so'raymiz, hozirda bizda veb-seminarlar mavjud emas. Ammo biz sizga telefon orqali mamnuniyat bilan "
             "maslahat beramiz. Iltimos, qayta qo'ng'iroq qilish uchun ariza qoldiring.  "
             "Kun, oy va sizga qulay vaqtni yozib qoldiring.Shunda ko'rsatilgan vaqtda menejerlarimiz "
             "siz bilan bog'lanishadi."


}

actions01 = {
    "sign_up": "Konsultatsiyaga yozilish",
    "sign_up_webinar": "Vebinarga yozilish"
}

buttons01 = {
    'btn3': KeyboardButton(text='Konsultatsiyaga yozilish'),
    'btn4': KeyboardButton(text='Vebinarga yozilish'),
    'btn5': KeyboardButton(text='Men ota-onaman'),
    'btn6': KeyboardButton(text="maktabda o'qiyman"),
    'btn7': KeyboardButton(text='men talabaman'),
    'btn8': KeyboardButton(text="kasbimni o'zgartirmoqchiman"),
    'btn9': KeyboardButton(text='Raqamni yuborish', request_contact=True),
    'btn10': InlineKeyboardButton(text="Do'stimga jonatish", switch_inline_query=f" - "
                                                                                 f"IT mutaxassisi bo'lishning oson "
                                                                                 f"yo'li, bizning bepul sinov "
                                                                                 f"darsimizga qatnasish.")


}
