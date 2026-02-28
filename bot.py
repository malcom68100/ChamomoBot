"""
Shampis Trial Key Bot
Discord bot for automatic trial key distribution
"""

import discord
from discord.ext import commands
from discord.ui import Button, View
import json
import os
import asyncio
from aiohttp import web
from datetime import datetime
from config import (
    BOT_TOKEN,
    TRIAL_CHANNEL_NAME,
    BUTTON_LABEL,
    BUTTON_EMOJI,
    KEYS_FILE,
    DATABASE_FILE,
    EMBED_TITLE,
    EMBED_DESCRIPTION,
    EMBED_COLOR
)

# ─────────────────────────────────────────────
# Bot setup
# ─────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ─────────────────────────────────────────────
# Database helpers (JSON)
# ─────────────────────────────────────────────
def load_database() -> dict:
    """Load the user database from JSON file with corruption protection."""
    if not os.path.exists(DATABASE_FILE):
        return {"users": {}}
    
    try:
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {"users": {}}
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Database error: {e}. Creating new one.")
        return {"users": {}}


def save_database(data: dict):
    """Save the user database to JSON file with UTF-8 encoding."""
    try:
        with open(DATABASE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"❌ Failed to save database: {e}")


def user_has_key(user_id: int) -> bool:
    """Check if a user already received a trial key."""
    db = load_database()
    return str(user_id) in db["users"]


def assign_key_to_user(user_id: int, username: str, key: str):
    """Assign a key to a user and save to database."""
    db = load_database()
    db["users"][str(user_id)] = {
        "username": username,
        "key": key,
        "assigned_at": datetime.utcnow().isoformat()
    }
    save_database(db)


# ─────────────────────────────────────────────
# Keys file helpers
# ─────────────────────────────────────────────
def load_keys() -> list:
    """Load available keys from the keys file, ignoring comments and empty lines."""
    if not os.path.exists(KEYS_FILE):
        print(f"⚠️ Warning: {KEYS_FILE} not found!")
        return []
    try:
        with open(KEYS_FILE, "r", encoding="utf-8") as f:
            # Filter matches: not empty and doesn't start with #
            keys = [
                line.strip() for line in f.readlines() 
                if line.strip() and not line.strip().startswith("#")
            ]
        return keys
    except IOError as e:
        print(f"❌ Error reading {KEYS_FILE}: {e}")
        return []


def pop_key() -> str | None:
    """Get and remove the first available key."""
    keys = load_keys()
    if not keys:
        return None
    key = keys[0]
    remaining = keys[1:]
    with open(KEYS_FILE, "w") as f:
        f.write("\n".join(remaining))
    return key


def keys_remaining() -> int:
    """Return the number of available keys."""
    return len(load_keys())


# ─────────────────────────────────────────────
# Button View
# ─────────────────────────────────────────────
class TrialKeyView(View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view

    @discord.ui.button(
        label=BUTTON_LABEL,
        emoji=BUTTON_EMOJI,
        style=discord.ButtonStyle.primary,
        custom_id="claim_trial_key"
    )
    async def claim_key(self, interaction: discord.Interaction, button: Button):
        user = interaction.user

        # Check if user already has a key
        if user_has_key(user.id):
            await interaction.response.send_message(
                "❌ You have already claimed your free trial key!\n"
                "Each account is limited to **1 trial key**.",
                ephemeral=True
            )
            return

        # Check if keys are available
        key = pop_key()
        if key is None:
            await interaction.response.send_message(
                "😔 Sorry, all trial keys have been claimed!\n"
                "Please check back later or contact an admin.",
                ephemeral=True
            )
            return

        # Try to send DM
        try:
            dm_embed = discord.Embed(
                title="🎮 Your Trial Key — Shampis BO7",
                description=(
                    f"Hey **{user.display_name}**! Here is your **1-hour trial key**:\n\n"
                    f"```\n{key}\n```\n"
                    "**How to use:**\n"
                    "1. Launch the loader\n"
                    "2. Enter your key when prompted\n"
                    "3. Enjoy! 🎯\n\n"
                    "> ⚠️ This key is valid for **1 hour** and can only be used **once**."
                ),
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            dm_embed.set_footer(text="Shampis — Black Ops 7 External")

            await user.send(embed=dm_embed)

            # Save to database only after successful DM
            assign_key_to_user(user.id, str(user), key)

            await interaction.response.send_message(
                "✅ Your trial key has been sent to your **DMs**!\n"
                "Check your private messages 📬",
                ephemeral=True
            )

        except discord.Forbidden:
            # DMs are disabled — put the key back
            keys = load_keys()
            keys.insert(0, key)
            with open(KEYS_FILE, "w") as f:
                f.write("\n".join(keys))

            await interaction.response.send_message(
                "❌ I couldn't send you a DM!\n"
                "Please **enable Direct Messages** from server members:\n"
                "> User Settings → Privacy & Safety → Allow DMs from server members ✅\n"
                "Then click the button again.",
                ephemeral=True
            )


# ─────────────────────────────────────────────
# Bot events
# ─────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ Bot connected as {bot.user} (ID: {bot.user.id})")
    print(f"🔑 Keys available: {keys_remaining()}")

    # Register persistent view
    bot.add_view(TrialKeyView())

    # Set bot status
    await bot.change_presence(
        activity=discord.Game(name="Black Ops 7 🎮")
    )

    # Start simple web server for keep-alive
    async def handle_ping(request):
        return web.Response(text="Bot is ALIVE! 🟢")

    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    
    try:
        await site.start()
        print("🌐 Keep-alive server started on port 8080")
    except Exception as e:
        print(f"⚠️ Could not start web server: {e}")


# ─────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────
@bot.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup(ctx):
    """
    Admin command to post the trial key message in the configured channel.
    Usage: !setup
    """
    channel = discord.utils.get(ctx.guild.text_channels, name=TRIAL_CHANNEL_NAME)

    if channel is None:
        await ctx.send(
            f"❌ Channel `#{TRIAL_CHANNEL_NAME}` not found!\n"
            f"Please create it first or update `TRIAL_CHANNEL_NAME` in config.py",
            delete_after=10
        )
        return

    embed = discord.Embed(
        title=EMBED_TITLE,
        description=EMBED_DESCRIPTION,
        color=EMBED_COLOR,
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text="Shampis — 1 trial per account")

    view = TrialKeyView()
    await channel.send(embed=embed, view=view)
    await ctx.send(f"✅ Setup complete! Message posted in #{TRIAL_CHANNEL_NAME}", delete_after=5)


@bot.command(name="keys")
@commands.has_permissions(administrator=True)
async def check_keys(ctx):
    """Admin command to check remaining keys."""
    count = keys_remaining()
    await ctx.send(f"🔑 **{count}** trial key(s) remaining.", delete_after=10)


@bot.command(name="addkeys")
@commands.has_permissions(administrator=True)
async def add_keys(ctx, *, keys_text: str):
    """
    Admin command to add new keys.
    Usage: !addkeys KEY1\nKEY2\nKEY3
    """
    new_keys = [k.strip() for k in keys_text.split("\n") if k.strip()]
    existing = load_keys()
    all_keys = existing + new_keys

    with open(KEYS_FILE, "w") as f:
        f.write("\n".join(all_keys))

    await ctx.send(
        f"✅ Added **{len(new_keys)}** key(s). Total: **{len(all_keys)}** keys.",
        delete_after=10
    )


@bot.command(name="resetuser")
@commands.has_permissions(administrator=True)
async def reset_user(ctx, user: str):
    """
    Admin command to reset a user's trial (allow them to claim again).
    Usage: !resetuser @user OR !resetuser USER_ID
    """
    db = load_database()
    
    # Try to extract ID from mention if provided
    user_id = user.replace("<@", "").replace(">", "").replace("!", "")
    
    if user_id not in db["users"]:
        await ctx.send(f"❌ User with ID `{user_id}` has not claimed a key yet.", delete_after=10)
        return

    username = db["users"][user_id].get("username", "Unknown")
    del db["users"][user_id]
    save_database(db)
    
    await ctx.send(f"✅ Reset trial for user **{username}** (ID: `{user_id}`). They can claim again.", delete_after=10)


# ─────────────────────────────────────────────
# Run bot
# ─────────────────────────────────────────────
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
