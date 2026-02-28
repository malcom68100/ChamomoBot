# 🤖 Chamomo Trial Key Bot

Discord bot designed for automatic trial key distribution for Black Ops 7. 

## 🚀 Deployment & Installation

### 1. Prerequisites
- Python 3.8 or higher
- A Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))

### 2. Installation
Clone or upload the bot files to your server and run:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Edit `config.py` with your bot token and adjust the channel names/settings.
- `BOT_TOKEN`: Your secret bot token.
- `TRIAL_CHANNEL_NAME`: The name of the channel where you want the setup to post.

### 4. Keys Setup
- Put your keys in `keys.txt` (one key per line).
- Lines starting with `#` are ignored (comments allowed).
- Empty lines are automatically skipped.

### 5. Launching
```bash
python bot.py
```

## 🛠 Admin Commands
- `!setup`: Post the trial key claim button in the configured channel.
- `!keys`: Check the number of remaining trial keys.
- `!addkeys`: Add multiple keys at once.
- `!resetuser @user`: Allow a user to claim a trial key again.

## 🌐 Hosting (fps.ms / Keep-alive)
The bot includes a built-in web server on port `8080`. This helps keep the bot active on hosting platforms that require an open port to prevent process hibernation.
