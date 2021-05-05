import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from VacciDate_bot.get_data import get_state_list, get_district_list
from VacciDate_bot.record_data import store_data, update_age_group, remove_record
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
    logger.warning(update)
    update.message.reply_text(
        "Hi, I am VacciBot.\n\nI'll help you get the vaccination slot.\n\nPlease provide your District code and Age Group (18 or 45) in below format\n\nFor Example : district-<DISTRICT CODE>-<AGE GROUP>\n\ndistrict-123-18"
    )


def start(update, context):
    update.message.reply_text(
        "Welcome!!!\n\nHere is a list of task I can help you with:\n\n1. Register for regular updates on slot availability: /register\n\n2. Get instant slot availability: /instant"
    )


def new_reg(update, context):
    update.message.reply_text(
        "Hi, I am VacciBot.\n\nI'll help you to get the vaccination slot."
    )
    state_text = get_state_list()
    update.message.reply_text(state_text)
    update.message.reply_text("Please provide your State code from the list above.")


def get_district(update, context):
    state_id = update.message.text
    logger.warning(state_id)
    if state_id.split("-")[0].lower() == "district":
        logger.warning("Instant status check")
        today = datetime.now()
        start_date = today.strftime("%d-%m-%Y")
        dist_id = state_id.split("-")[1]
        logger.warning("Instant status check")
        age_group = state_id.split("-")[2]
        logger.warning("Instant status check")
        av_slots = get_instant_details(dist_id, start_date, int(age_group))
        if len(av_slots) == 0:
            update.message.reply_text(
                "Sorry no slot available in your area.\n\nPlease try after some time, or register to our telegram channel and get a notification once slots are available in your area.\n\nPress /register to register to the channel"
            )
        else:
            for message in av_slots:
                update.message.reply_text(message)
            update.message.reply_text("These are top 5 results in your area.")
    elif state_id == "18+" or state_id == "45+":
        logger.warning("Age Group selected")
        logger.warning("Updating user data")
        res = update_age_group(age_group=state_id, user_data=update)
        update.message.reply_text(
            "Thankyou for registering.\n\nPlease join the channel to get latest update on vaccine slot.\n\nhttps://t.me/joinchat/HtLv30uoSl82ZDc1"
        )
    elif state_id == "Y":
        logger.warning("User de-registeration")
        remove_record(update)
        update.message.reply_text(
            "User de-registered.\n\nThank You for using VacciDate"
        )
    elif state_id == "N":
        update.message.reply_text("User de-registeration CANCELLED")
    elif int(state_id) <= 36:
        logger.warning("State selected")
        logger.warning("getting district data")
        dist_text = get_district_list(state_id=state_id)
        update.message.reply_text(dist_text)
        update.message.reply_text(
            "Please provide your District code from the list above."
        )
    else:
        logger.warning("District selected")
        logger.warning("calling store data")
        res = store_data(district_id=state_id, user_data=update)
        update.message.reply_text(
            "Please select the Age Group you want notifications for.\n\nEnter '18+' if your age is between 18 and 45 years\n\nEnter '45+' if your age is more than 45 years"
        )


def deregister(update, context):
    update.message.reply_text(
        "Are you sure you want to de-register from VacciDate Bot?\n\nOnce you deregister, you won't receive any notification for vaccination slot.\n\nPress Y to confirm\n\nPress N to cancel"
    )


def main():
    """Start the bot."""
    updater = Updater(
        "1726606541:AAEhx3O4XsHlxlhX8u9_1E_38dS3tgnHlu8", use_context=True
    )
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", new_reg))
    dp.add_handler(CommandHandler("get_district_id", new_reg))
    dp.add_handler(CommandHandler("instant", instant_check))
    dp.add_handler(CommandHandler("deregister", deregister))
    dp.add_handler(MessageHandler(Filters.text, get_district))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()