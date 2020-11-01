from telebot import types
ADD_TO_QUEUE, WATCH_QUEUE, SKIP_QUEUE, SET_WASHING, WASHING_FINISHED, LEAVE_QUEUE = (
    'Записатися у чергу',
    'Переглянути чергу',
    'Пропустити чергу',
    'Закласти прання',
    'Прання завершилось',
    'Покинути чергу'
)
IN_QUEUE_KEYBOARD = types.ReplyKeyboardMarkup()
IN_QUEUE_KEYBOARD.row(ADD_TO_QUEUE)
IN_QUEUE_KEYBOARD.row(WATCH_QUEUE)

WASHING_KEYBOARD = types.ReplyKeyboardMarkup()
WASHING_KEYBOARD.row(SET_WASHING, WATCH_QUEUE, LEAVE_QUEUE)

WAITING_KEYBOARD=types.ReplyKeyboardMarkup()
WAITING_KEYBOARD.row(WATCH_QUEUE)

REGIME_OF_WASHING_KEYBOARD=types.ReplyKeyboardMarkup()
item1=types.KeyboardButton("1 година")
item2=types.KeyboardButton("2 години")
item3=types.KeyboardButton("30 хвилин")
REGIME_OF_WASHING_KEYBOARD.add(item1, item2, item3)

