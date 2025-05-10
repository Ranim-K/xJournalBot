import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)
from datetime import datetime

# === CONFIGURATION ===
BOT_TOKEN = "8065690612:AAE8wzvac0rqHom2Xrr8Tjrgw9J1ZtxUXMs"
YOUR_USER_ID = 5582563598
GROUP_CHAT_ID = -1002647932627
JOURNAL_TOPIC_ID = 2

# === LOGGING SETUP ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# === START / JOURNAL ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user already has an ongoing journal (if they completed one yesterday)
    if 'journal_step' in context.user_data:
        await resume_journal(update, context)
    else:
        await journal_prompt(update, context)

async def journal_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != YOUR_USER_ID:
        return

    context.user_data['journal_step'] = 1

    today = datetime.now().strftime('%A, %d %B %Y')
    keyboard = [
        [InlineKeyboardButton("📸 Yes, upload a photo", callback_data="photo")],
        [InlineKeyboardButton("⏩ Skip", callback_data="skip_photo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Hi! Let's start your journal for *{today}*.\n\nWould you like to add a photo?",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# === BUTTON CLICK HANDLER ===
async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != YOUR_USER_ID:
        return

    if query.data == "photo":
        context.user_data['journal_step'] = 2
        await query.edit_message_text("📸 Great! Please send me a photo for your journal.")

    elif query.data == "skip_photo":
        context.user_data['journal_step'] = 3
        await prompt_rating(query, context)

    elif query.data.startswith("rating_"):
        context.user_data['rating'] = int(query.data.split("_")[1])
        context.user_data['journal_step'] = 4
        await query.edit_message_text("✅ Got your rating!\nNow, please write your journal note.")

# === RATING PROMPT ===
async def prompt_rating(update_or_query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("⭐ 1", callback_data="rating_1"),
            InlineKeyboardButton("⭐ 2", callback_data="rating_2"),
            InlineKeyboardButton("⭐ 3", callback_data="rating_3"),
            InlineKeyboardButton("⭐ 4", callback_data="rating_4"),
            InlineKeyboardButton("⭐ 5", callback_data="rating_5")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update_or_query.edit_message_text(
        "🌟 On a scale from 1 to 5, how was your day?",
        reply_markup=reply_markup
    )

# === JOURNAL ENTRY HANDLER ===
async def handle_journal_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != YOUR_USER_ID:
        return

    step = context.user_data.get('journal_step', 1)

    if step == 2 and update.message.photo:
        context.user_data['photo'] = update.message.photo[-1].file_id
        context.user_data['journal_step'] = 3  # Move to rating step

        # Show rating buttons right away
        rating_keyboard = [
            [InlineKeyboardButton("⭐ 1", callback_data="rating_1"),
            InlineKeyboardButton("⭐ 2", callback_data="rating_2"),
            InlineKeyboardButton("⭐ 3", callback_data="rating_3"),
            InlineKeyboardButton("⭐ 4", callback_data="rating_4"),
            InlineKeyboardButton("⭐ 5", callback_data="rating_5")]
        ]
        reply_markup = InlineKeyboardMarkup(rating_keyboard)

        await update.message.reply_text("📸 Photo added! How would you rate your day (1–5)?", reply_markup=reply_markup)


    elif step == 3 and update.message.text:
        text = update.message.text.strip()
        if text.isdigit() and 1 <= int(text) <= 5:
            context.user_data['rating'] = int(text)
            context.user_data['journal_step'] = 4
            await update.message.reply_text("✅ Got it! Now, please write your journal note.")
        else:
            await update.message.reply_text("⚠️ Please enter a number between 1 and 5.")

    elif step == 4 and update.message.text:
        context.user_data['note'] = update.message.text.strip()
        await finalize_journal(update, context)

# === FINALIZE JOURNAL ENTRY ===
async def finalize_journal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now().strftime('%A, %d %B %Y')
    short_date = datetime.now().strftime('%d-%m-%Y')

    parts = [f"📔 *Daily Journal* — {today}"]

    if 'rating' in context.user_data:
        parts.append(f"\n🌟 *Today’s Rating*: {context.user_data['rating']} / 5")

    if 'note' in context.user_data:
        parts.append(f"📝 *Note*: {context.user_data['note']}")

    if 'photo' in context.user_data:
        parts.append("🖼️ *Photo*:  ✅")

    final_message = "\n".join(parts)

    if 'photo' in context.user_data:
        await context.bot.send_photo(
            chat_id=GROUP_CHAT_ID,
            photo=context.user_data['photo'],
            caption=final_message,
            message_thread_id=JOURNAL_TOPIC_ID,
            parse_mode="Markdown"
        )
    else:
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=final_message,
            message_thread_id=JOURNAL_TOPIC_ID,
            parse_mode="Markdown"
        )

    # Send confirmation message to user
    await update.message.reply_text("✅ Your journal has been posted! Great job today ✨")

    # Clear the user data for a fresh start
    context.user_data.clear()

# === RESUME JOURNAL ===
async def resume_journal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome back! You can continue your journaling process.")

# === MAIN ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button_click))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_journal_entry))

    print("🤖 LazyJournalBot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
