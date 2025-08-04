import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Список вопросов
questions = [
    "Ваше любимое блюдо?",
    "Где бы вы хотели побывать?",
    "Какой ваш любимый фильм?",
    "Что вы делаете в свободное время?",
    "Если бы у вас была суперсила, какой бы она была?"
]

# Храним состояние для каждого пользователя
user_states = {}

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {'step': 0, 'answers': []}
    await update.message.reply_text("Привет! Давайте начнём опрос. Отвечайте на вопросы.")
    await update.message.reply_text(questions[0])

# Обработчик ответов
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_states:
        await update.message.reply_text("Начните опрос с помощью команды /start")
        return

    state = user_states[user_id]
    answer = update.message.text
    state['answers'].append(answer)
    state['step'] += 1

    if state['step'] < len(questions):
        await update.message.reply_text(questions[state['step']])
    else:
        # Опрос окончен
        await update.message.reply_text("Спасибо за участие в опросе! Ваши ответы:")
        for i, ans in enumerate(state['answers'], 1):
            await update.message.reply_text(f"{i}. {ans}")
        del user_states[user_id]

def main():
    TOKEN = "8166924304:AAFH2axLZOJ-smTBCH1SoIYD48w-z5wzqGo"  # Замените на ваш токен от BotFather
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()


