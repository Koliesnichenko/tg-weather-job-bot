from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler, \
    CallbackQueryHandler, CallbackContext
from weather_three_day import get_three_day_weather
from config import BOT_TOKEN
from user_data import set_city, get_city, increment_weather_counter, get_profile
from weather import get_weather
from job_parser import get_jobs
from user_data import delete_profile
from weather import get_weather_by_coords


SET_CITY = 1# state for ConversationHandler


async def request_location(update: Update, context: CallbackContext):
    location_button = KeyboardButton(text="📍 Share Location", request_location=True)
    keyboard = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Please share your location:", reply_markup=keyboard)


async def handle_location(update: Update, context: CallbackContext):
    if update.message.location:
        lat = update.message.location.latitude
        lon = update.message.location.longitude
        weather_info = get_weather_by_coords(lat, lon)
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("❗ Could not get location")


# /start
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌤 Today", callback_data="weather_today")],
        [InlineKeyboardButton("📅 3-Day Forecast", callback_data="weather_3days")],
        [InlineKeyboardButton("💼 Jobs", callback_data="jobs")],
        [InlineKeyboardButton("📍 Set City", callback_data="set_city")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("🗑 Delete Profile", callback_data="delete_profile")],
        [InlineKeyboardButton("📍 Location", callback_data="location")]
    ])


async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("location", "Share your location"),
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hey! I'm your Dev-Bot. Choose option:",
        reply_markup=main_menu_keyboard()
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == "weather":
        city = get_city(user.id) or "Bucharest"
        weather_info = get_weather(city)
        increment_weather_counter(user.id)
        await query.edit_message_text(weather_info, reply_markup=main_menu_keyboard())

    elif query.data == "jobs":
        jobs = get_jobs()
        await query.edit_message_text(jobs, reply_markup=main_menu_keyboard())

    elif query.data == "location":
        await query.edit_message_text("To get weather by coordinates enter /location")

    elif query.data == "profile":
        profile = get_profile(user.id)
        if profile:
            text = (
                f"👤 {profile['name']}\n"
                f"📍 City: {profile.get('city', 'not set')}\n"
                f"🌤 Weather requests: {profile.get('weather_requests', 0)}"
            )
        else:
            text = "❗ Profile not found. Press 'Set City'"
        await query.edit_message_text(text, reply_markup=main_menu_keyboard())

    elif query.data == "delete_profile":
        if delete_profile(user.id):
            await query.edit_message_text("🗑 Profile deleted.", reply_markup=main_menu_keyboard())
        else:
            await query.edit_message_text("❗ Profile not found.", reply_markup=main_menu_keyboard())

    elif query.data == "set_city":
        context.user_data["set_city"] = True
        await query.edit_message_text("✍ Input city:")
        return

    elif query.data == "weather_today":
        city = get_city(user.id) or "Bucharest"
        weather_info = get_weather(city)
        increment_weather_counter(user.id)
        await query.edit_message_text(weather_info, reply_markup=main_menu_keyboard())

    elif query.data == "weather_3days":
        city = get_city(user.id) or "Bucharest"
        forecast = get_three_day_weather(city)
        await query.edit_message_text(forecast, reply_markup=main_menu_keyboard())


async def save_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    user = update.effective_user
    set_city(user.id, city, user.full_name)
    await update.message.reply_text(f"✅ City {city} saved!", reply_markup=main_menu_keyboard())


async def catch_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("set_city"):
        city = update.message.text
        user = update.effective_user
        set_city(user.id, city, user.full_name)
        context.user_data["set_city"] = False
        await update.message.reply_text(f"✅ City {city} saved!", reply_markup=main_menu_keyboard())

async def post_init(app):
    await set_commands(app)



if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Inline buttons
    app.add_handler(CallbackQueryHandler(handle_buttons))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, catch_text))

    app.add_handler(CommandHandler("location", request_location))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    app.post_init = post_init

    print("Bot started...")
    app.run_polling()
