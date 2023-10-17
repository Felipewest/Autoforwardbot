import nest_asyncio
nest_asyncio.apply()
import asyncio
import logging
import pymongo
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery  # Corrected import
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

# Initialize the Pyrogram client
api_id = "24317766"
api_hash = "04032b32b0547bbf9ea81a844545ef4f"
bot_token = "6365158055:AAFem5DZN2EBVWGQa5K9v2NTT6Bzbv0FpdY"
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Initialize MongoDB connection
mongo_client = pymongo.MongoClient("mongodb+srv://autoforwardbot:yuvraj178@cluster0.k6xfpbz.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["autoforwardbot"]
status_collection = db["status"]

# Enable logging
logging.basicConfig(level=logging.INFO)

# Dictionary to store last processed message IDs
last_message_ids = {}

# Define a filter to check if the user is a bot admin
def is_admin(chat_id, user_id):
    try:
        chat = app.get_chat_member(chat_id, user_id)
        return chat.status == "administrator" or chat.status == "creator"
    except Exception as e:
        return False

# Start command handler
@app.on_message(filters.command("start"))
async def start_command(client, message):
    user = message.from_user
    user_name = user.first_name
    if user.last_name:
        user_name += " " + user.last_name
    user_link = f"[{user_name}](tg://user?id={user.id})"

    message_text = (
        f"ʜɪ 👋 {user_link}\n\nɪ'ᴍ ᴀ 👑ᴀᴅᴠᴀɴᴄᴇᴅ ᴀᴜᴛᴏ ꜰᴏʀᴡᴀʀᴅ ʙᴏᴛ👑\n"
        "ɪ ᴄᴀɴ ꜰᴏʀᴡᴀʀᴅ ᴀʟʟ ᴍᴇssᴀɢᴇ ꜰʀᴏᴍ ᴏɴᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴄʜᴀɴᴇʟ\n\n"
        f"ᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ\n"
    )

    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Help", callback_data="help")],
            [
                InlineKeyboardButton("Support group", url="https://t.me/+vrOa7OsSUKZiMjZl"),
                InlineKeyboardButton("Update channel", url="https://t.me/+vrOa7OsSUKZiMjZl"),
            ],
            [InlineKeyboardButton("Donate", callback_data="donate")],
        ]
    )

    await message.reply(message_text, reply_markup=reply_markup)
    
# Define a function to handle the "donate" callback_data
async def handle_donate_button(client, callback_query):
    chat_id = callback_query.message.chat.id

    donate_message = (
        "if you liked me ❤️, consider making a donation to support my developer 👦\n"
        "UPI ID - `krishna527062@oksbi`"
    )

    # Create an inline keyboard with a "Back" button
    back_button = InlineKeyboardButton("Back", callback_data="back")
    reply_markup = InlineKeyboardMarkup([[back_button]])

    # Edit the message with the donation message and the "Back" button
    await callback_query.message.edit_text(
        donate_message,
        reply_markup=reply_markup,
    )

# Register the callback handler for "donate" callback_data
@app.on_callback_query(filters.regex(r"^donate$"))
async def donate_button(client, callback_query):
    await handle_donate_button(client, callback_query)
    
# Define a list to store back_button_counter as its first element
back_button_counter = [1]

# Callback handler for "Back" button
@app.on_callback_query(filters.regex(r"^back$"))
async def back_button(client, callback_query):
    user = callback_query.from_user  # Get user info
    user_name = user.first_name
    if user.last_name:
        user_name += " " + user.last_name
    user_link = f"[{user_name}](tg://user?id={user.id})"

    # Create a unique callback data for the "back" button
    back_button_counter[0] += 1
    back_button_callback_data = f"back_{back_button_counter[0]}"

    # Create the inline keyboard for the previous menu
    previous_menu_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Help", callback_data="help")],
            [
                InlineKeyboardButton("Support group", url="https://t.me/+vrOa7OsSUKZiMjZl"),
                InlineKeyboardButton("Update channel", url="https://t.me/+vrOa7OsSUKZiMjZl"),
            ],
            [InlineKeyboardButton("Donate", callback_data="donate")],
        ]
    )

    await callback_query.message.edit_text(
        f"ʜɪ 👋 {user_link}\n\nɪ'ᴍ ᴀ 👑ᴀᴅᴠᴀɴᴄᴇᴅ ᴀᴜᴛᴏ ꜰᴏʀᴡᴀʀᴅ ʙᴏᴛ👑\n"
        "ɪ ᴄᴀɴ ꜰᴏʀᴡᴀʀᴅ ᴀʟʟ ᴍᴇssᴀɢᴇ ꜰʀᴏᴍ ᴏɴᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴄʜᴀɴᴇʟ\n\n"
        f"ᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ\n",
        reply_markup=previous_menu_keyboard
    )
    
    # Define a function to handle the "help" callback_data
async def handle_help_button(client, callback_query):
    chat_id = callback_query.message.chat.id

    help_message = (
        "🔆 HELP\n\n"
        "📚 Available commands:\n"
        "⏣ /start - check I'm alive\n"
        "⏣ /forward - forward messages\n"
        "⏣ /private_forward - forward messages from private chat\n"
        "⏣ /unequify - delete duplicate media messages in chats\n"
        "⏣ /settings - configure your settings\n"
        "⏣ /stop - stop your ongoing tasks\n"
        "⏣ /reset - reset your settings\n\n"
        "💢 Features:\n"
        "► Forward message from public channel to your channel without admin permission. if the channel is private need admin permission\n"
        "► Forward message from private channel to your channel by using userbot (user must be a member in there)\n"
        "► Custom caption\n"
        "► Custom button\n"
        "► Support restricted chats\n"
        "► Skip duplicate messages\n"
        "► Filter type of messages\n"
        "► Skip messages based on extensions & keywords & size"
    )

    # Create inline keyboard with the requested buttons
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("How to use me?", callback_data="how_to_use")],
            [
             InlineKeyboardButton("Settings", callback_data="settings"),
             InlineKeyboardButton("Status", callback_data="status"),
            ],
            [
             InlineKeyboardButton("About", callback_data="about"),
             InlineKeyboardButton("Back", callback_data="back"),
            ]
        ]
    )

    # Edit the message with the help message and inline keyboard
    await callback_query.message.edit_text(
        help_message,
        reply_markup=keyboard,
    )

# Register the callback handler for "help" callback_data
@app.on_callback_query(filters.regex(r"^help$"))
async def help_button(client, callback_query):
    await handle_help_button(client, callback_query)
    
   # Callback handler for the "How to use me?" button
@app.on_callback_query(filters.regex(r"^how_to_use$"))
async def how_to_use_button(client, callback_query):
    user = callback_query.from_user
    user_name = user.first_name
    if user.last_name:
        user_name += " " + user.last_name
    user_link = f"[{user_name}](tg://user?id={user.id})"
    
    how_to_use_message = (
        "⚠️ Before Forwarding:\n"
        "► First add a bot or userbot\n"
        "► Add at least one target channel (your bot/userbot must be an admin there)\n"
        "► You can add chats or bots by using /settings\n"
        "► If the Source Channel is private, your userbot must be a member there, or your bot must have admin permission there\n"
        "► Then use /forward to forward messages"
    )

    # Create the inline keyboard with a "Back" button
    back_button = InlineKeyboardButton("Back", callback_data="back_2")
    reply_markup = InlineKeyboardMarkup([[back_button]])

    await callback_query.message.edit_text(
        f"🔆 HOW TO USE ME?\n\n{how_to_use_message}",
        reply_markup=reply_markup
    )
    
    # Callback handler for "Back" button with a counter of 2
@app.on_callback_query(filters.regex(r"^back_2$"))
async def back_button_2(client, callback_query):
    user = callback_query.from_user
    user_name = user.first_name
    if user.last_name:
        user_name += " " + user.last_name
    user_link = f"[{user_name}](tg://user?id={user.id})"

    # Create the inline keyboard for the previous menu
    previous_menu_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("How to use me?", callback_data="how_to_use")],
            [
             InlineKeyboardButton("Settings", callback_data="settings"),
             InlineKeyboardButton("Status", callback_data="status"),
            ],
            [
             InlineKeyboardButton("About", callback_data="about"),
             InlineKeyboardButton("Back", callback_data="back"),
            ]
        ]
    )

    await callback_query.message.edit_text(
        f"🔆 HELP\n\n📚 Available commands:\n⏣ /start - check I'm alive\n⏣ /forward - forward messages\n⏣ /private_forward - forward messages from private chat\n⏣ /unequify - delete duplicate media messages in chats\n⏣ /settings - configure your settings\n⏣ /stop - stop your ongoing tasks\n⏣ /reset - reset your settings\n\n💢 Features:\n► Forward message from public channel to your channel without admin permission. if the channel is private need admin permission\n► Forward message from private channel to your channel by using userbot (user must be a member there)\n► custom caption\n► custom button\n► support restricted chats\n► skip duplicate messages\n► filter type of messages\n► skip messages based on extensions & keywords & size",
        reply_markup=previous_menu_keyboard
    )
   

# Function to fetch and format status information
async def get_status_info():
    while True:
        # Fetch status information from MongoDB (adjust document structure accordingly)
        status_doc = status_collection.find_one({"_id": 1})
        total_users = status_doc.get("total_users", 0)
        total_bots = status_doc.get("total_bots", 0)
        total_forwardings = status_doc.get("total_forwardings", 0)
        total_unequifyings = status_doc.get("total_unequifyings", 0)
        
        # Format the status message
        status_message = f" ╔════❰ ʙᴏᴛ sᴛᴀᴛᴜs  ❱═❍⊱❁۪۪\n"\
                        f"║╭━━━━━━━━━━━━━━━➣\n"\
                        f"║┣⪼👱 ᴛᴏᴛᴀʟ ᴜsᴇʀs: {total_users}\n"\
                        f"║┃\n"\
                        f"║┣⪼🤖 ᴛᴏᴛᴀʟ ʙᴏᴛ: {total_bots}\n"\
                        f"║┃\n"\
                        f"║┣⪼🔃 ғᴏʀᴡᴀʀᴅɪɴɢs: {total_forwardings}\n"\
                        f"║┃\n"\
                        f"║┣⪼🔍 ᴜɴᴇǫᴜɪꜰʏɪɴɢs: {total_unequifyings}\n"\
                        f"║╰━━━━━━━━━━━━━━━➣\n"\
                        f"╚══════════════════❍⊱❁۪۪"

        # Update the status message in the database every second
        await status_collection.update_one({"_id": 1}, {"$set": {"message": status_message}}, upsert=True)
        await asyncio.sleep(1)

# Start the status update loop
asyncio.create_task(get_status_info())

# Create a "Back" button
back_button = InlineKeyboardButton("Back", callback_data="back")

# Create an InlineKeyboardMarkup for the "Back" button
back_button_keyboard = InlineKeyboardMarkup([[back_button]])

# Define the callback for the "Status" button
@bot.on_callback_query(filters.regex("status"))
async def status_button_handler(client, callback_query):
    # Fetch the status message from the database
    status_doc = status_collection.find_one({"_id": 1})
    status_message = status_doc.get("message", "Status information not available.")
    
    # Edit the message with the status information
    await callback_query.message.edit_text(status_message, reply_markup=back_button_keyboard)

# Define the callback for the "Back" button
@bot.on_callback_query(filters.regex("back"))
async def back_button_handler(client, callback_query):
    # Edit the message to navigate back to the main menu (you can adjust this as needed)
    main_menu_message = "🔆 MAIN MENU"
    await callback_query.message.edit_text(main_menu_message, reply_markup=main_menu_keyboard)


    # Define the "about" message
about_message = (
    "╔════❰ ғᴏʀᴡᴀʀᴅ ʙᴏᴛ ❱═❍⊱❁۪۪\n"
    "║╭━━━━━━━━━━━━━━━➣\n"
    "║┣⪼📃ʙᴏᴛ : ғᴏʀᴡᴀʀᴅ ʙᴏᴛ\n"
    "║┣⪼👦ᴄʀᴇᴀᴛᴏʀ : ᴍadhu\n"
    "║┣⪼📡ʜᴏsᴛᴇᴅ ᴏɴ : Render\n"
    "║┣⪼🗣️ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ3\n"
    "║┣⪼📚ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄɪᴏ 2.0.0\n"
    "║┣⪼🗒️ᴠᴇʀsɪᴏɴ : 1.0.0\n"
    "║╰━━━━━━━━━━━━━━━➣\n"
    "╚══════════════════❍⊱❁۪۪"
)

# Callback handler for "about" button
@app.on_callback_query(filters.regex(r"^about$"))
async def about_button(client, callback_query):
    user = callback_query.from_user
    user_name = user.first_name
    if user.last_name:
        user_name += " " + user.last_name
    user_link = f"[{user_name}](tg://user?id={user.id})"

    # Create the inline keyboard with a "Back" button
    back_button = InlineKeyboardButton("Back", callback_data="back_3")
    reply_markup = InlineKeyboardMarkup([[back_button]])

    await callback_query.message.edit_text(
        f"🔆 ABOUT\n\n{about_message}",
        reply_markup=reply_markup
    )

# Modify the "Back" button callback handler to handle the "about" button and go back to the main help menu
@app.on_callback_query(filters.regex(r"^back_3$"))
async def back_button_3(client, callback_query):
    user = callback_query.from_user
    user_name = user.first_name
    if user.last_name:
        user_name += " " + user.last_name
    user_link = f"[{user_name}](tg://user?id={user.id})"

    # Create the inline keyboard for the previous menu (main help menu)
    previous_menu_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("How to use me?", callback_data="how_to_use")],
            [
                InlineKeyboardButton("Settings", callback_data="settings"),
                InlineKeyboardButton("Status", callback_data="status"),
            ],
            [
                InlineKeyboardButton("About", callback_data="about"),
                InlineKeyboardButton("Back", callback_data="back"),
            ]
        ]
    )

    await callback_query.message.edit_text(
        f"🔆 HELP\n\n📚 Available commands:\n⏣ /start - check I'm alive\n⏣ /forward - forward messages\n⏣ /private_forward - forward messages from private chat\n⏣ /unequify - delete duplicate media messages in chats\n⏣ /settings - configure your settings\n⏣ /stop - stop your ongoing tasks\n⏣ /reset - reset your settings\n\n💢 Features:\n► Forward message from public channel to your channel without admin permission. if the channel is private need admin permission\n► Forward message from private channel to your channel by using userbot (user must be a member there)\n► custom caption\n► custom button\n► support restricted chats\n► skip duplicate messages\n► filter type of messages\n► skip messages based on extensions & keywords & size",
        reply_markup=previous_menu_keyboard
    )
    
   # Callback handler for "settings" button
@app.on_callback_query(filters.regex(r"^settings$"))
async def settings_button(client, callback_query):
    # Create inline keyboard with the requested buttons
    keyboard = InlineKeyboardMarkup(
        [
            [
              InlineKeyboardButton("Bots", callback_data="settings_bots"),
              InlineKeyboardButton("Channels", callback_data="settings_channels")
            ],
            [
              InlineKeyboardButton("Caption", callback_data="settings_caption"),
              InlineKeyboardButton("Database", callback_data="settings_database")
            ],
            [
              InlineKeyboardButton("Filters", callback_data="settings_filters"),
              InlineKeyboardButton("Back", callback_data="back_5")
            ],
        ]
    )

    await callback_query.message.edit_text(
        "🔆 SETTINGS\n\nChange your settings as you wish.",
        reply_markup=keyboard,
    )

# Callback handler for "Back" button with a counter of 5
@app.on_callback_query(filters.regex(r"^back_5$"))
async def back_button_5(client, callback_query):
    user = callback_query.from_user
    user_name = user.first_name
    if user.last_name:
        user_name += " " + user.last_name
    user_link = f"[{user_name}](tg://user?id={user.id})"

    # Create the inline keyboard for the previous menu (main help menu)
    previous_menu_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("How to use me?", callback_data="how_to_use")],
            [
                InlineKeyboardButton("Settings", callback_data="settings"),
                InlineKeyboardButton("Status", callback_data="status"),
            ],
            [
                InlineKeyboardButton("About", callback_data="about"),
                InlineKeyboardButton("Back", callback_data="back"),
            ]
        ]
    )

    await callback_query.message.edit_text(
        f"🔆 HELP\n\n📚 Available commands:\n⏣ /start - check I'm alive\n⏣ /forward - forward messages\n⏣ /private_forward - forward messages from private chat\n⏣ /unequify - delete duplicate media messages in chats\n⏣ /settings - configure your settings\n⏣ /stop - stop your ongoing tasks\n⏣ /reset - reset your settings\n\n💢 Features:\n► Forward message from public channel to your channel without admin permission. if the channel is private need admin permission\n► Forward message from private channel to your channel by using userbot (user must be a member there)\n► custom caption\n► custom button\n► support restricted chats\n► skip duplicate messages\n► filter type of messages\n► skip messages based on extensions & keywords & size",
        reply_markup=previous_menu_keyboard
    )
    
    
 # Callback handler for "settings_bots" button
@app.on_callback_query(filters.regex(r"^settings_bots$"))
async def settings_bots_button(client, callback_query):
    # Create inline keyboard with the requested buttons
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Add bot", callback_data="settings_add_bot")],
            [InlineKeyboardButton("Add userbot", callback_data="settings_add_userbot")],
            [InlineKeyboardButton("Back", callback_data="settings_back")],
        ]
    )

    await callback_query.message.edit_text(
        "🤖 Bots\n\nYou can manage your bots here.",
        reply_markup=keyboard,
    )

# Callback handler for "Add bot" button
@app.on_callback_query(filters.regex(r"^settings_add_bot$"))
async def settings_add_bot_button(client, callback_query):
    pass  # This is an empty implementation, and it won't perform any actions.

# Callback handler for "Add userbot" button
@app.on_callback_query(filters.regex(r"^settings_add_userbot$"))
async def settings_add_userbot_button(client, callback_query):
    pass  # This is an empty implementation, and it won't perform any actions.

# Callback handler for "Back" button in the Bots menu
@app.on_callback_query(filters.regex(r"^settings_back$"))
async def settings_back_button(client, callback_query):
    # Navigate back to the Settings menu
    user = callback_query.from_user
    user_name = user.first_name
    if user.last_name:
        user_name += " " + user.last_name
    user_link = f"[{user_name}](tg://user?id={user.id})"

    # Create the inline keyboard for the Settings menu
    settings_menu_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Bots", callback_data="settings_bots"),
             InlineKeyboardButton("Channels", callback_data="settings_channels")],
            [InlineKeyboardButton("Caption", callback_data="settings_caption"),
             InlineKeyboardButton("Database", callback_data="settings_database")],
            [InlineKeyboardButton("Filters", callback_data="settings_filters"),
              InlineKeyboardButton("Back", callback_data="back_5")],
        ]
    )

    await callback_query.message.edit_text(
        f"🔆 SETTINGS\n\nChange your settings as you wish.",
        reply_markup=settings_menu_keyboard,
    )
    
    # Callback handler for "Channels" button in the Settings menu
@app.on_callback_query(filters.regex(r"^settings_channels$"))
async def settings_channels_button(client, callback_query):
    # Create inline keyboard with the requested buttons
    channels_menu_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Add Source Channel", callback_data="settings_add_source_channel")],
            [InlineKeyboardButton("Add Destination Channel", callback_data="settings_add_destination_channel")],
            [InlineKeyboardButton("Back", callback_data="settings_back")],
        ]
    )

    await callback_query.message.edit_text(
        "📡 Channels\n\nYou can manage your channels here.",
        reply_markup=channels_menu_keyboard,
    )
    
    # Callback handler for "Caption" button in the Settings menu
@app.on_callback_query(filters.regex(r"^settings_caption$"))
async def settings_caption_button(client, callback_query):
    # Create inline keyboard with the requested buttons
    caption_menu_keyboard = InlineKeyboardMarkup(
        [
            [
              InlineKeyboardButton("Replace all texts", callback_data="settings_replace_all_texts"),
              InlineKeyboardButton("Replace all links", callback_data="settings_replace_all_links")
            ],
            [
              InlineKeyboardButton("Delete all links", callback_data="settings_delete_all_links"),
              InlineKeyboardButton("Delete all media captions", callback_data="settings_delete_all_captions")
            ],
            [
              InlineKeyboardButton("Add custom caption", callback_data="settings_add_custom_caption"),
              InlineKeyboardButton("Back", callback_data="settings_back")
            ]
        ]
    )

    await callback_query.message.edit_text(
        "🖋️ Caption\n\nYou can add your custom caption here and also delete/replace all links/texts.",
        reply_markup=caption_menu_keyboard,
    )
    
    # Callback handler for "Database" button in the Settings menu
@app.on_callback_query(filters.regex(r"^settings_database$"))
async def settings_database_button(client, callback_query):
    # Create inline keyboard with the requested buttons
    database_menu_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Add MongoDB database", callback_data="settings_add_mongodb_database")],
            [InlineKeyboardButton("Back", callback_data="settings_back")],
        ]
    )

    await callback_query.message.edit_text(
        "🗃️ Database\n\nA database is necessary to store your duplicate messages and for the de-duplication process.",
        reply_markup=database_menu_keyboard,
    )
    
    



# Define the Filters collection for storing user filter configurations
filters_collection = db["user_filters"]


# Dictionary to store user filter settings
user_filters = {}

# Callback handler for "Filters" button in the Settings menu
@app.on_callback_query(filters.regex(r"^settings_filters$"))
async def settings_filters_button(client, callback_query):
    user_id = callback_query.from_user.id
    # Load user filter settings from MongoDB
    user_filter_doc = filters_collection.find_one({"user_id": user_id})
    if user_filter_doc:
        user_filters = user_filter_doc.get("filters", {})

    # Create inline keyboard with the requested buttons
    filters_menu_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Forward tag", callback_data="settings_forward_tag"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "forward_tag") else "Off", callback_data="settings_forward_tag_toggle")],
            [InlineKeyboardButton("Texts", callback_data="settings_texts"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "texts") else "Off", callback_data="settings_texts_toggle")],
            [InlineKeyboardButton("Documents", callback_data="settings_documents"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "documents") else "Off", callback_data="settings_documents_toggle")],
            [InlineKeyboardButton("Videos", callback_data="settings_videos"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "videos") else "Off", callback_data="settings_videos_toggle")],
            [InlineKeyboardButton("Photos", callback_data="settings_photos"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "photos") else "Off", callback_data="settings_photos_toggle")],
            [InlineKeyboardButton("Audios", callback_data="settings_audios"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "audios") else "Off", callback_data="settings_audios_toggle")],
            [InlineKeyboardButton("Voices", callback_data="settings_voices"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "voices") else "Off", callback_data="settings_voices_toggle")],
            [InlineKeyboardButton("Animations", callback_data="settings_animations"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "animations") else "Off", callback_data="settings_animations_toggle")],
            [InlineKeyboardButton("Stickers", callback_data="settings_stickers"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "stickers") else "Off", callback_data="settings_stickers_toggle")],
            [InlineKeyboardButton("Skip duplicate", callback_data="settings_skip_duplicate"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "skip_duplicate") else "Off", callback_data="settings_skip_duplicate_toggle")],
            [InlineKeyboardButton("Back", callback_data="settings_back_6"),
             InlineKeyboardButton("Next", callback_data="settings_next")],
        ]
    )

    await callback_query.message.edit_text(
        "🌟 Custom Filters\n\nConfigure the type of messages you want to forward.",
        reply_markup=filters_menu_keyboard,
    )

# Callback handler for toggling filter settings
@app.on_callback_query(filters.regex(r"^settings_(\w+)_toggle$"))
async def settings_filter_toggle_button(client, callback_query):
    filter_key = callback_query.matches[0].group(1)  # Extract the filter key
    user_id = callback_query.from_user.id

    if filter_key in user_filters:
        # Toggle the filter setting for the user
        user_filters[filter_key] = not user_filters[filter_key]
    else:
        # Initialize the filter setting for the user
        user_filters[filter_key] = True

    # Update user filter settings in MongoDB
    filters_collection.update_one(
        {"user_id": user_id},
        {"$set": {"filters": user_filters}},
        upsert=True  # Insert a new document if it doesn't exist
    )

    await settings_filters_button(client, callback_query)  # Re-display the filters menu

# Callback handler for "Back" button in the Filters menu
@app.on_callback_query(filters.regex(r"^settings_back_6$"))
async def settings_back_6_button(client, callback_query):
    await settings_button(client, callback_query)  # Navigate back to the Settings menu


# Function to check if a user has enabled a specific filter
def has_filter_enabled(user_id, filter_key):
    return user_filters.get(filter_key, False)

# Callback handler for the "Next" button in the Filters menu
@app.on_callback_query(filters.regex(r"^settings_next$"))
async def settings_next_button(client, callback_query):
    user_id = callback_query.from_user.id
    user_filter_doc = filters_collection.find_one({"user_id": user_id})
    if user_filter_doc:
        user_filters = user_filter_doc.get("filters", {})

    # Create inline keyboard with the requested buttons for the "Next" menu
    next_menu_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Poll", callback_data="settings_poll"),
             InlineKeyboardButton("On" if has_filter_enabled(user_id, "poll") else "Off", callback_data="settings_poll_toggle")],
            [InlineKeyboardButton("Back", callback_data="settings_back_next")]
        ]
    )

    await callback_query.message.edit_text(
        "🌟 Custom Filters\n\nConfigure the type of messages you want to forward.",
        reply_markup=next_menu_keyboard,
    )

# Callback handler for toggling the "Poll" filter setting
@app.on_callback_query(filters.regex(r"^settings_poll_toggle$"))
async def settings_poll_toggle_button(client, callback_query):
    user_id = callback_query.from_user.id
    if "poll" in user_filters:
        user_filters["poll"] = not user_filters["poll"]
    else:
        user_filters["poll"] = True

    filters_collection.update_one(
        {"user_id": user_id},
        {"$set": {"filters": user_filters}},
        upsert=True
    )

    await settings_next_button(client, callback_query)

# Callback handler for the "Back" button in the "Next" menu
@app.on_callback_query(filters.regex(r"^settings_back_next$"))
async def settings_back_next_button(client, callback_query):
    await settings_filters_button(client, callback_query)  # Navigate back to the Filters menu

# Function to check if a user has enabled the "Poll" filter
def has_filter_enabled(user_id, filter_key):
    return user_filters.get(filter_key, False)
    

    
# Run the bot
if __name__ == "__main__":
    app.run()
    
