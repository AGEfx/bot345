from  telebot import types as t


btn_add = t.KeyboardButton('Добавить')
btn_day = t.KeyboardButton('План на день')
btn_ready = t.KeyboardButton('Есть. Выполнено')
btn_award = t.KeyboardButton('Награда')
btn_location = t.KeyboardButton('Отправить свою локацию 🗺️', request_location=True)

markup = t.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup.row(btn_add,btn_day)

markup1 = t.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup1.row(btn_day)
markup1.row(btn_ready)
markup1.row(btn_award)
