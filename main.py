import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, \
    CallbackQueryHandler, CallbackContext

from scrapers.djinni_selenium import get_djinni_jobs_selenium
from telegram.error import TelegramError
from db import set_city, get_city, increment_weather_counter, get_profile, delete_profile
from weather_three_day import get_three_day_weather
from config import BOT_TOKEN
from weather import get_weather
from job_parser import get_jobs
from weather import get_weather_by_coords
from datetime import datetime, timedelta


SET_CITY = 1# state for ConversationHandler

djinni_cache = {
    "data": None,
    "expires_at": datetime.min
}


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


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
        [InlineKeyboardButton("💼 Djinni Jobs", callback_data="djinni_jobs")],
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
    text = (
        "👋 <b>Welcome to Dev-Bot!</b>\n\n"
        "📍 <i>Set your city via '📍 Set City' to personalize your experience</i>\n"
        "🌍 Default city is <b>Bucharest</b>\n\n"
        "I'm here to help with:\n"
        "🌤 <b>Weather forecast</b>\n"
        "📅 <b>3-day outlook</b>\n"
        "💼 <b>Python job offers</b> from:\n"
        "   └ 🇺🇦 <b>Djinni</b>\n"
        "   └ 🌍 <b>Python.org</b>\n\n"
        "<i>Built by Koliesnichenko_</i>"
    )
    await update.message.reply_text(text, reply_markup=main_menu_keyboard(), parse_mode="HTML")


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

    elif query.data == "djinni_jobs":

        now = datetime.now()
        if djinni_cache["data"] and now < djinni_cache["expires_at"]:
            jobs = djinni_cache["data"]
        else:
            await query.edit_message_text("🔎 Searching Djinni jobs...")
            jobs = get_djinni_jobs_selenium()
            djinni_cache["data"] = jobs
            djinni_cache["expires_at"] = now + timedelta(minutes=10)

        await query.edit_message_text(jobs, reply_markup=main_menu_keyboard())


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


async def error_handler(update, context):
    logging.error(f"‼️ Error: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("🚫 Unexpected error occurred.")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ I'm alive!")


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Inline buttons
    app.add_handler(CallbackQueryHandler(handle_buttons))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, catch_text))

    app.add_handler(CommandHandler("location", request_location))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    app.add_error_handler(error_handler)

    app.add_handler(CommandHandler("ping", ping))

    app.post_init = post_init

    logging.info("Bot started...")
    app.run_polling()
