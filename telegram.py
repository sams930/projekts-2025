import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

user_tasks = {}
user_answers = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("uzraksti /task vai /task2 ")

async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num1 = random.randint(1, 50)
    num2 = random.randint(1, 50)
    op = random.choice(["+", "-", "*"])
    example = f"{num1} {op} {num2}"
    user_tasks[update.effective_user.id] = eval(example)
    await update.message.reply_text(f"risini: {example}")


async def task2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = random.randint(-10, 10)
    r = random.randint(1, 10)
    x = -k / r
    user_answers[update.effective_user.id] = round(x, 2)
    line2 = f"{r}x + {k} = 0   x = ?"
    await update.message.reply_text(line2)


async def task_checker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text.replace(",", ".")


    if user_id in user_answers:# task2
        try:
            user_input = float(message_text)
            correct = user_answers[user_id]
            if round(user_input, 2) == correct:# ja atbilde ir pariz uzraksti paeizi
                await update.message.reply_text("Pareizi!")
            else: # raksta ka nepareiza atbilde un dot pareizo
                await update.message.reply_text(f"nepareizi. pareizi ir: {correct}")
            del user_answers[user_id]
        except:# ja ir cits prasa uzrakstīt ciparus
            await update.message.reply_text("ciparus raksti")
        return


    elif user_id in user_tasks:#task
        try:
            answer = int(message_text)
            correct = user_tasks[user_id]
            if answer == correct:# ja atbilde ir pariz uzraksti paeizi
                await update.message.reply_text("Pareizi!")
            else: # raksta ka nepareiza atbilde un dot pareizo
                await update.message.reply_text(f"nepareizi. pareizi ir: {correct}")
            del user_tasks[user_id]
        except: # ja ir cits prasa uzrakstīt ciparus
            await update.message.reply_text("ciparus raksti")
        return
    else:
        await update.message.reply_text("uzraksti /task vai /task2 ")

if __name__ == "__main__":
    app = ApplicationBuilder().token('7917201612:AAGViUvNuhK_m8bJFpTOOTZkhbyzpu1zDhc').build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", task))
    app.add_handler(CommandHandler("task2", task2))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, task_checker))

    app.run_polling()

#python bot.py
#testi 1.kods palaižas 2.dod izvelni task vai task2
#liet. testi 1.uarakstot /task dod uzdevumus 2. uzrakstot /task2 dod uzdevumus ar x
# 3.uzakstot atbildi tas dod pareizas atbildes 4. uzakstot nepaeizi tas dod paeizo tabildi
# robež scenāriji. 1.uzakstot paeizo atbildi kopā a citie burtiem("asd3") tas prasa uzrakstīt tikai cipaus 2. izjot no programas un ieejot atpakļ, uzdevumu laikā, pareizo atbildi var uzakstīt.
