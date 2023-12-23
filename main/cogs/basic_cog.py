import discord
from discord.ext import commands


class BasicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        user = ctx.author
        bot_latency = round(self.bot.latency * 1000)
        magic = f'{bot_latency} ms ✨'
        embed = discord.Embed(title=f'🧙‍ Conexão Mágica', color=user.color)
        embed.add_field(name='Latência com Magia dos Deuses', value=magic, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)  # Garante que apenas usuários com permissão podem usar
    async def clear(self, ctx, num: int = 500):

        # Limita o número de mensagens a serem apagadas para evitar abuso
        num = min(max(1, num), 1000)

        # Apaga as mensagens
        deleted = await ctx.channel.purge(limit=num)
        confirm_message = await ctx.send(f'🧹 Limpei {len(deleted)} mensagens!', delete_after=5)
        await confirm_message.delete(delay=5)


async def setup(bot):
    await bot.add_cog(BasicCog(bot))
