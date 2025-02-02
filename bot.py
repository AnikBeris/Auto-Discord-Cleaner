import json
import nextcord
from nextcord.ext import commands

# Загружаем инфу из config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN = config['TOKEN']
GUILD_ID = int(config['GUILD_ID'])

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} успешно подключился к Discord!")

    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("❌ Ошибка: сервер не найден!")
        return

    await clear_channels(guild)
    await clear_roles(guild)

async def clear_channels(guild):
    """Удаляет все текстовые и голосовые каналы."""
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"🗑️ Удалён канал: {channel.name}")
        except Exception as e:
            print(f"❌ Ошибка при удалении {channel.name}: {e}")

async def clear_roles(guild):
    """Удаляет все роли, кроме @everyone."""
    for role in guild.roles:
        if role.name != "@everyone":  # Не удаляем стандартную роль
            try:
                await role.delete()
                print(f"🗑️ Удалена роль: {role.name}")
            except Exception as e:
                print(f"❌ Ошибка при удалении роли {role.name}: {e}")

# Запускаем бота
bot.run(TOKEN)