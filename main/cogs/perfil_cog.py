import discord
from discord.ext import commands


class PerfilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def perfil(self, ctx):
        user = ctx.author  # O membro cujo perfil está sendo solicitado

        # Criar uma embed para o cartão de perfil
        embed = discord.Embed(title=f"Perfil de {user.name}", color=user.color)
        embed.set_thumbnail(url=user.avatar.url)  # Adiciona a foto de perfil do usuário

        # Adicionar a data de ingresso no servidor
        join_date = user.joined_at.strftime("%d/%m/%Y")
        embed.add_field(name="Ingressou no servidor em", value=join_date, inline=False)

        # Adicionar os cargos do usuário
        roles = " \n ".join(
            [role.name for role in user.roles if role.name != "@everyone"])  # Ignora o cargo padrão @everyone
        if roles:
            embed.add_field(name="Cargos", value=roles, inline=False)

        # Adicionar outras informações que você desejar
        # ...

        # Enviar a embed no canal atual
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PerfilCog(bot))
