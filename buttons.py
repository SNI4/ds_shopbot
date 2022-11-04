import uuid
import discord
from configparser import ConfigParser
from discord.ui import Button

import config as cfg

config = ConfigParser()
config.read('settings.ini')


class ReviewsButton(Button):
    def __init__(self):
        super().__init__(label=cfg.ReviewsButtonName, url=cfg.ReviewsButtonLink)


class StartButton(Button):
    def __init__(self):
        super().__init__(label=cfg.StartMessage, style=discord.ButtonStyle.green)

    async def callback(self, interaction):
        config.read('settings.ini')

        authorName = interaction.user.name
        authorId = interaction.user.id

        inactiveChannel = await interaction.guild.create_text_channel(
            name=f'{authorName}-{str(uuid.uuid4().fields[-1])[:5]}',
            category=discord.utils.get(interaction.guild.categories,
                                       id=config.getint('inactive_orders', 'inactive_orders_category_id')))

        await interaction.response.send_message(inactiveChannel.mention, file=discord.File(cfg.PrivatePictureFilePath),
                                                ephemeral=True)
        await inactiveChannel.send(f'{interaction.user.mention}', file=discord.File(cfg.ChooseCategoryPictureFilePath))