import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from VacciDate_bot.get_data import get_state_list, get_district_list
from VacciDate_bot.record_data import store_data
from utils.api_call import get_instant_details
from datetime import datetime

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def instant_check(update, context):
    update.message.reply_text(
        "Hi, I am VacciBot.\n I'll help you to get the vaccination slot.\n Please provide your District name in below format\ndistrict-<DISTRICT ID>-<AGE GROUP>\n For Example: district-123-18"
    )


def new_reg(update, context):
    update.message.reply_text(
        "Hi, I am VacciBot.\n I'll help you to get the vaccination slot.\n Please provide your State and District name?"
    )
    state_text = get_state_list()
    update.message.reply_text(state_text)


def get_district(update, context):
    state_id = update.message.text
    if state_id.split("-")[0] == "district":
        today = datetime.now()
        start_date = today.strftime("%d-%m-%Y")
        dist_id = state_id.split("-")[1]
        age_group = state_id.split("-")[2]
        av_slots = get_instant_details(dist_id, start_date, int(age_group))
        if len(av_slots) == 0:
            update.message.reply_text(
                "Sorry no slot available in your area. Please try after some time, or register to our telegram channel , and get a notification once slots are available in your area.\nsend /register to register to the channel"
            )
        else:
            for message in av_slots:
                update.message.reply_text(message)
    elif int(state_id) <= 36:
        dist_text = get_district_list(state_id=state_id)
        update.message.reply_text(dist_text)
    else:
        res = store_data(disctrict_id=state_id)
        update.message.reply_text(
            "Thankyou for registering.\nPlease join the channel to get latest update on vaccine slot:https://t.me/joinchat/HtLv30uoSl82ZDc1"
        )


def main():
    """Start the bot."""
    updater = Updater(
        "1726606541:AAEhx3O4XsHlxlhX8u9_1E_38dS3tgnHlu8", use_context=True
    )
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("register", new_reg))
    dp.add_handler(CommandHandler("get_district_id", new_reg))
    dp.add_handler(CommandHandler("instant", instant_check))
    dp.add_handler(MessageHandler(Filters.text, get_district))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()