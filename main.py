import os
import discord
from discord.ext import commands
from discord.ui import View

import config as cfg
from configparser import ConfigParser
from buttons import StartButton, ReviewsButton

cogs = ['cogs.adminPanel']

config = ConfigParser()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=cfg.PREFIX, intents=intents)


@client.event
async def on_ready():
    global inactiveOrdersCategory, orderChannel
    print(f'ПОШЕЛ НАХУЙ {client.user}')

    try:

        for extension in cogs:
            await client.load_extension('cogs.adminPanel')
            print(f'{extension} has loaded!')

    except Exception as e:
        print(e)

    guild = client.get_guild(cfg.GUILD_ID)

    if 'settings.ini' not in os.listdir():
        startMessage = await guild.system_channel.send("bot start's first time, setting up...")

        try:
            orderCategory = await guild.create_category(name=cfg.OrderCategoryName)
            inactiveOrdersCategory = await guild.create_category(name=cfg.InactiveCategoryName)

            await inactiveOrdersCategory.edit(overwrites={
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False,
                                                                connect=False, speak=False)
            })
            orderChannel = await guild.create_text_channel(name=cfg.OrderChannelName, category=orderCategory)
            await orderChannel.send(file=discord.File(cfg.StartPictureFilePath),
                                    view=View().add_item(StartButton()).add_item(ReviewsButton()))

        except Exception as e:
            await guild.system_channel.send(f'i got troubles...\n[CREATE-CHANNELS]: {e}')

        try:
            config.read('settings.ini')
            config.add_section('order')
            config.add_section('inactive_orders')

            config.set('order', 'order_category_id', str(orderChannel.category_id))
            config.set('order', 'order_channel_id', str(orderChannel.id))
            config.set('inactive_orders', 'inactive_orders_category_id', str(inactiveOrdersCategory.id))

            with open('settings.ini', 'w') as configfile:
                config.write(configfile)

            await startMessage.edit(content='all finished! enjoyable use')

        except Exception as e:

            await guild.system_channel.send(f'i got troubles...\n[INI-CONFIG]: {e}')


client.run(cfg.BOT_TOKEN)
