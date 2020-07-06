import discord
import logging
import os
import shutil
import tempfile
from mediapart_parser import MediapartParser
from discord.ext import tasks
from tinydb import TinyDB
from tinydb import Query

discord_client = discord.Client()

# Resolve directories
articles_tmp_folder = tempfile.gettempdir() + "/mediapart_bot/articles"
logs_file = tempfile.gettempdir() + "/mediapart_bot/logs.app"

# Environment variables
bot_fetch_time_hours = int(os.environ['BOT_FETCH_TIME_HOURS'])
mediapart_channel_id = int(os.environ['CHANNEL_ID'])
discord_token = os.environ['DISCORD_BOT_TOKEN']

bot_started = False


@discord_client.event
async def on_ready():
    logging.info('Bot is connected. Ready to start.')
    start_bot()


@discord_client.event
async def on_message(message):
    global bot_started

    is_direct_message_bool = is_message_from_direct_messages(message)

    if not is_direct_message_bool:
        return

    if message.author == discord_client.user:
        return

    # check is the bot is alive
    if message.content == "!is-alive":
        logging.debug("Received !is-alive command.")
        await message.channel.send("I'am Alive :D")

    # get bot logs
    if message.content == "!logs":
        logging.debug("Received !logs command.")
        await message.channel.send(
            content="See logs in attachement.",
            file=discord.File(logs_file, filename="logs.txt"))

    # force fetching last articles
    if message.content == "!fetch-articles":
        logging.debug("Received !fetch-articles command.")
        await message.channel.send(
            "Fetching last articles in the channel "
            + str(discord_client.get_channel(mediapart_channel_id)))
        await get_last_articles()


@tasks.loop(hours=bot_fetch_time_hours)
async def update():
    logging.debug('Fetching lastest articles.')
    await get_last_articles()


async def get_last_articles():
    mediapart_channel = discord_client.get_channel(mediapart_channel_id)

    try:
        parser = get_mediapart_parser()
        all_article_links = parser.get_last_french_articles_links()

        # if no new articles, exit method
        new_articles_number = resolve_new_articles_numbers(all_article_links)
        if new_articles_number == 0:
            logging.debug("No new articles to fetch.")
            return

        logging.debug("Fetching %s new articles", str(new_articles_number))

        all_article_titles = parser.get_last_articles_titles()
        all_articles_categories = parser.get_last_articles_categories()

        User = Query()

        for article_number in range(len(all_article_titles)):

            # resolve article id
            article_link = all_article_links[article_number]
            article_id = parser.get_article_id(article_link)

            # check if article id is found in the database
            result = mediapart_database.search(User.articleId == article_id)

            # if the article id is not already in the database
            if not result:
                article_title = all_article_titles[article_number]
                article_category = all_articles_categories[article_number]
                article_file_name = resolve_article_file_name(article_id)
                final_file_path = articles_tmp_folder + "/" \
                                  + article_file_name + ".pdf"

                parser.download_article(article_id, final_file_path)

                await mediapart_channel.send(
                    # category
                    content="[" + article_category + "] "
                            # article title
                            + article_title,
                    # attachment
                    file=discord.File(
                        final_file_path,
                        filename=article_title + ".pdf"))

                mediapart_database.insert({"articleId": article_id})

        clean_temp_folder()

    except Exception as e:
        clean_temp_folder()
        logging.error(str(e), exc_info=True)


def is_message_from_mediapart_channel(message):
    if str(message.channel.id) == str(mediapart_channel_id):
        return True
    else:
        return False


def is_message_from_direct_messages(message):
    if message.guild is None and message.author != discord_client.user:
        return True
    else:
        return False


def resolve_new_articles_numbers(all_article_links):
    User = Query()
    parser = get_mediapart_parser()

    new_articles_number = 0

    for article_link in all_article_links:
        article_id = parser.get_article_id(article_link)

        result = mediapart_database.search(User.articleId == article_id)

        if not result:
            new_articles_number = new_articles_number + 1
    return new_articles_number


def start_bot():
    global bot_started

    if not bot_started:
        bot_started = True
        mediapart_channel = discord_client.get_channel(mediapart_channel_id)
        logging.debug('Resolved mediapart channel is %s', mediapart_channel)
        update.start()


def get_mediapart_parser():
    mediapart_user = os.environ['MEDIAPART_USER']
    mediapart_password = os.environ['MEDIAPART_PWD']

    return MediapartParser(mediapart_user, mediapart_password)


def resolve_article_file_name(article_id):
    base_name = "article"
    file_name = base_name + "_" + article_id
    return file_name


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def clean_temp_folder():
    for filename in os.listdir(articles_tmp_folder):
        file_path = os.path.join(articles_tmp_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


# clean and prepare folders
create_folder(articles_tmp_folder)
clean_temp_folder()

# Configure database
mediapart_database = TinyDB(tempfile.gettempdir()
                            + "/mediapart_bot/mediapart_database.json")

# Configure logger
logging.basicConfig(
    filename=logs_file,
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# run the bot
discord_client.run(discord_token)
