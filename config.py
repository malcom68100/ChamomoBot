"""
config.py — Configuration file for Shampis Trial Key Bot
Edit this file before launching the bot.
"""

import discord

# ─────────────────────────────────────────────
# REQUIRED — Bot token from Discord Developer Portal
# https://discord.com/developers/applications
# ─────────────────────────────────────────────
BOT_TOKEN = "MTQwNTk5ODA4NTA5NTU1NTI1Ng.GqluF_.jefd2QoEccGs7hF0-R--N3LRsz6HO7A_1slljc"

# ─────────────────────────────────────────────
# Channel where the trial button will be posted
# The channel must already exist in your server
# ─────────────────────────────────────────────
TRIAL_CHANNEL_NAME = "free-trial-essai"

# ─────────────────────────────────────────────
# Button appearance
# ─────────────────────────────────────────────
BUTTON_LABEL = "External Cheat BO7"
BUTTON_EMOJI = "🎮"

# ─────────────────────────────────────────────
# Files
# ─────────────────────────────────────────────
KEYS_FILE = "keys.txt"        # One key per line
DATABASE_FILE = "database.json"  # Tracks who claimed a key

# ─────────────────────────────────────────────
# Embed message appearance
# ─────────────────────────────────────────────
EMBED_TITLE = "🎮 Free Trial — Chamomo Black Ops 7"
EMBED_DESCRIPTION = (
    "Want to try our **external cheat** for free?\n\n"
    "Click the button below to receive your **1-hour trial key** in DMs!\n\n"
    "⚠️ **Rules:**\n"
    "• 1 trial per Discord account\n"
    "• Make sure your DMs are open\n"
    "• Keys are valid for 1 hour\n\n"
    "🔑 Click below to claim your key!"
)
EMBED_COLOR = discord.Color.blue()


TOKEN = "MTQwNTk5ODA4NTA5NTU1NTI1Ng.GqluF_.jefd2QoEccGs7hF0-R--N3LRsz6HO7A_1slljc"   # entre guillemets
CHANNEL_NAME = "free-trial-essai"    # nom du salon où le bouton sera posté