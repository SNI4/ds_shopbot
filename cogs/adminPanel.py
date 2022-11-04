from discord.ext import commands
from discord.ui import View

from buttons import *

import config as cfg
from configparser import ConfigParser

config = ConfigParser()


class AdminPanel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def ss(self, ctx):

        if ctx.author.id == cfg.TOTAL_ADMIN_ID:

            try:
                config.read('settings.ini')
                orderChannel = self.client.get_channel(config.getint('order', 'order_channel_id'))

                await orderChannel.send(file=discord.File(cfg.StartPictureFilePath),
                                        view=View().add_item(StartButton()).add_item(ReviewsButton()))

            except Exception as e:

                await ctx.send(f'i got troubles...\n:[ADMIN-PANEL]: {e}')


async def setup(client):
    await client.add_cog(AdminPanel(client))
