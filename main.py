import os
os.system('pip install python-telegram-bot flask')

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
  # Instead of putting your token directly

# Replace this with your actual bot token

# Step 1: Main questions
questions = {
    "start": {
        "question": "လျှောက်ထားသည့်တန်းခွဲရွေးပေးပါရန်",
        "options": [
            ("Batch-4 Morning Class", "Batch-4 Morning Class"),
            ("Batch-4 Evening Class", "Batch-4 Evening Class")
        ]
    },
    "Batch-4 Morning Class": {
        "question": "Morning Class Channel - https://t.me/+d9Pw-4tNgJY5MmY1\nမိမိတက်ရောက်မည့်အတန်းကိုရွေးပေးပါ",
        "options": [
            (f"Morning Grade-{i}", f"Morning Grade-{i}") for i in range(1, 13)
        ] + [("Morning KG", "Morning KG")]
    },
    "Batch-4 Evening Class": {
        "question": "Evening Class Channel - https://t.me/+2UQQusqCm0M1Mzg1\nမိမိတက်ရောက်မည့်အတန်းကိုရွေးပေးပါ",
        "options": [
            (f"Evening Grade-{i}", f"Evening Grade-{i}") for i in range(1, 13)
        ] + [("Evening KG", "Evening KG")]
    },
}

# Step 2: Group links for each class
grade_groups = {
    "Morning KG": "https://t.me/+-05jTDURsZs1ODdl",
    "Morning Grade-1": "https://t.me/+cfGLIsRZ6xBiMmJl",
    "Morning Grade-2": "https://t.me/+9GeHz6JvQ1EzOWVl",
    "Morning Grade-3": "https://t.me/+UaAQ111IAHUwMzA1",
    "Morning Grade-4": "https://t.me/+ffNbGFDGT-tmYmFl",
    "Morning Grade-5": "https://t.me/+lPbFuYXotX0zY2E1",
    "Morning Grade-6": "https://t.me/+IkfCwA0OhBdjNTQ1",
    "Morning Grade-7": "https://t.me/+uoBlLcrn5RtjODBl",
    "Morning Grade-8": "https://t.me/+1JKGvzZ75MRkYTc9",
    "Morning Grade-9": "https://t.me/+MydKQgpTAg80MThl",
    "Morning Grade-10": "https://t.me/+F4DXvgwWjXdlMjZl",
    "Morning Grade-11": "https://t.me/+VjPy1w1zZrdhMTJl",
    "Morning Grade-12": "https://t.me/+46oLfymCp7c0OGJl",
    "Evening KG": "https://t.me/+vrmsrNKFvS5kN2E1",
    "Evening Grade-1": "https://t.me/+WdK9kkNPQ-FmMDFl",
    "Evening Grade-2": "https://t.me/+a7MAFujuGaRlNGY1",
    "Evening Grade-3": "https://t.me/+hyE-o67q3Co3MzE1",
    "Evening Grade-4": "https://t.me/+-qt-NLhj6_c3OWU1",
    "Evening Grade-5": "https://t.me/+wxWEvWkXQsRlYjE1",
    "Evening Grade-6": "https://t.me/+1zIkSf6Q4tQwOWJl",
    "Evening Grade-7": "https://t.me/+72vW71ylM9c0YjQ1",
    "Evening Grade-8": "https://t.me/+suWAOulX95VlNzI1",
    "Evening Grade-9": "https://t.me/+caeWdiyCPIE1Yjc9",
    "Evening Grade-10": "https://t.me/+38R3pM4yrL01ZDM1",
    "Evening Grade-11": "https://t.me/+EzhZFucCQCg4YmFl",
    "Evening Grade-12": "https://t.me/+IArEquwM1q5hOTE9",
}

# Step 3: Student-ID form links for each class
student_id_forms = {
    "Morning KG": "https://docs.google.com/forms/d/1CIhaI6yiUe8rY26D7NPpQXqBnmVAYBJKVjE0CLjIqdQ/preview",
    "Morning Grade-1": "https://docs.google.com/forms/d/1tipVNWdoYMxp68SOk9FUllmaNJ3M1ZxyfEc5EpNGaoU/preview",
    "Morning Grade-2": "https://docs.google.com/forms/d/15wamd-8mtKnjwRXw669fYv6GRihu5M2gggUhw6O_t8E/preview",
    "Morning Grade-3": "https://docs.google.com/forms/d/1anFW6rO6P4J4FPs9A743LFgvKKhWr8SO4EEkcCl-VbU/preview",
    "Morning Grade-4": "https://docs.google.com/forms/d/1HtRM6aWa5sa08BvYWbwsSfFWRqPQA1wG4ml5LzFDfgc/preview",
    "Morning Grade-5": "https://docs.google.com/forms/d/1rBz_s1krZ9zRb2K6MsJF2NIFt0hxFerzEA3JWr27oJ8/preview",
    "Morning Grade-6": "https://docs.google.com/forms/d/1R8xYd69THv5EQNQsWNaR3-QZ9VioAvTsCMjq-u1zv9I/preview",
    "Morning Grade-7": "https://docs.google.com/forms/d/1zpLaD_rzTcQmNMH4qbyPeB4EvWqYl17PgOveVOS2fWc/preview",
    "Morning Grade-8": "https://docs.google.com/forms/d/1ZjX9oGq7MmQRFyDYrtIWcYLhMk8_qtdzAaOhV8ARm04/preview",
    "Morning Grade-9": "https://docs.google.com/forms/d/13HjGe926ONuUeq8e5SAq7Yn1cEG__UfMmzuThH-vMdY/preview",
    "Morning Grade-10": "https://docs.google.com/forms/d/1OzTDaDwsLTmlLsXodfNqIhYTY9GdWaHz3e1ZNGBT8cQ/preview",
    "Morning Grade-11": "https://docs.google.com/forms/d/1pKV4XnSuVTY6mD3a3_ROSieq4c0rXCutLbtwotiSNZo/preview",
    "Morning Grade-12": "https://docs.google.com/forms/d/1w20Mz7VJ7HDuo4dm3zUIxGDF115fz4c5148io4ZC2TI/preview",
    "Evening KG": "https://docs.google.com/forms/d/1rfAUPECAtpTtMsbPFz6VPn1bsa2_iV5-F6Ib8AajWDk/preview",
    "Evening Grade-1": "https://docs.google.com/forms/d/1Utb9vcYgTWcT8slen2PkPoXZEW7mK-39VlGwSfYcxuA/preview",
    "Evening Grade-2": "https://docs.google.com/forms/d/17ORJJPohna2oaEHe3doHA8ejcnZUmAxd8JJ4Student-IDeview",
    "Evening Grade-3": "https://docs.google.com/forms/d/1di_66vwwQLMha6qezziRUtm0z0XNutCBcy6rTXtf5ys/preview",
    "Evening Grade-4": "https://docs.google.com/forms/d/1lOTgoS4VqB2WqVZfMwj1_kA-Wmqlv0KtlQHjVfrQ8kE/preview",
    "Evening Grade-5": "https://docs.google.com/forms/d/1SRIXEYy3CB_cTQOFJ7pPcvehaT5RPFgBLf2FGmgbRYQ/preview",
    "Evening Grade-6": "https://docs.google.com/forms/d/13tIeXbSAmfgwEx7EU8Qpb3FP1N1xh9mME6tV_iR4G4k/preview",
    "Evening Grade-7": "https://docs.google.com/forms/d/1DUaoscDKrEqebwH67CeoTlV43U6YRlAi1IegsksGrgQ/preview",
    "Evening Grade-8": "https://docs.google.com/forms/d/15Ow1CQzjopjvTZEX9Bypka1DbvS7-a-z7rH7ZGrDdK4/preview",
    "Evening Grade-9": "https://docs.google.com/forms/d/1oM8MdXiDieUorHeKMZiauCKEyVaNOAgwNCJIueiaco0/preview",
    "Evening Grade-10": "https://docs.google.com/forms/d/1jgbagbhewmXz_2WE2KaWsypF4bduL-WNvnB1yd02yRw/preview",
    "Evening Grade-11": "https://docs.google.com/forms/d/1CrnOIe7MhihtayvWmsFTKHX4VE68J8P8_m_1fgU0Flc/preview",
    "Evening Grade-12": "https://docs.google.com/forms/d/1D9L207A3LHeFHJn6W6NPyEm76UY-5d501zCvtXbVA8s/preview",
}

# Step 4: Dynamically add follow-up questions to decision tree
for class_name, group_link in grade_groups.items():
    questions[class_name] = {
        "question": f"{class_name}: {group_link}\nGroup ထဲဝင်ထားပြီးပါပြီလား။",
        "options": [("ဝင်ထားပြီးပါပြီ", f"{class_name}-confirm"), ("မဝင်ရသေးပါ", class_name)]
    }
    questions[f"{class_name}-confirm"] = {
        "question": f"ကျေးဇူးပြု၍ Student-ID Form ကိုဖြည့်ပါ: {student_id_forms[class_name]}",
        "options": [("ဖြည့်ပြီးပါပြီ", "done"), ("မဖြည့်ရသေးပါ", class_name)]
    }

# Step 5: Track user state
user_state = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state[user_id] = "start"
    await send_question(update, context, "start")

# Send question function
async def send_question(update_or_query, context, key):
    q = questions.get(key)
    if not q:
        # Send the final message and end
        message = "Student-ID Form ပြီးပါက https://t.me/HFS1822 ကိုဆက်သွယ်၍ Student-ID တောင်းယူနိုင်ပါသည်။\nStudent-ID တောင်းယူရာတွင်\n၁။ အမည်\n၂။ လျှောက်ထားသည့်တန်းခွဲ (မနက်/ ည)\n၃။ လျှောက်ထားသည့်အတန်းများနှင့်အတူ အကြောင်းပြန်ပေးပါရန်"

        if hasattr(update_or_query, "message") and update_or_query.message:
            await update_or_query.message.reply_text(message)
        elif hasattr(update_or_query, "callback_query") and update_or_query.callback_query:
            await update_or_query.callback_query.message.reply_text(message)

        # End the conversation here
        return  # No further processing will happen after this return

    if hasattr(update_or_query, "callback_query") and update_or_query.callback_query:
        await update_or_query.callback_query.answer()
        update_or_query = update_or_query.callback_query

    buttons = [[InlineKeyboardButton(text, callback_data=data)] for text, data in q["options"]]
    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
    await update_or_query.message.reply_text(q["question"], reply_markup=reply_markup)

# Handle button presses
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    selected = query.data
    user_state[user_id] = selected
    await send_question(update, context, selected)

# Main function to start bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_answer))

    print("✅ Bot is running.")
    app.run_polling()

if __name__ == "__main__":
    main()
