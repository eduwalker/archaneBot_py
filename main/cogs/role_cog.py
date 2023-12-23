import discord
from discord.ext import commands


class RoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_message = (
            "Olá pequeno gafanhoto! Para iniciarmos nossa jornada, "
            "preciso que me diga qual classe de aprendiz de feiticeiro você participará...."
        )
        try:
            await member.send(welcome_message, view=self.QuestionarioView(member))
        except discord.Forbidden:
            print(f"Não foi possível enviar uma DM para {member.name}.")

    class QuestionarioView(discord.ui.View):
        def __init__(self, member):
            super().__init__()
            self.member = member

        async def interaction_check(self, interaction):
            return interaction.user == self.member

        ROLE_IDS = {
            "Player": 1038901971953930241,
            "Dev": 1021606072164827177,
            "Estudante": 1135385830031106089,
            "Visitante": 1021877429372985454
        }

        async def handle_role_assignment(self, role_name, interaction):
            role_id = self.ROLE_IDS.get(role_name)
            if role_id:
                role = self.member.guild.get_role(role_id)
                await self.member.add_roles(role)
                await interaction.response.send_message(f"Classe '{role_name}' atribuída com sucesso!", ephemeral=True)
            else:
                await interaction.response.send_message("Classe não encontrada. Por favor, contate um administrador.",
                                                        ephemeral=True)

        @discord.ui.button(label="Player (Games)", style=discord.ButtonStyle.primary)
        async def player_button(self, button, interaction):
            await self.handle_role_assignment("Player", interaction)

        @discord.ui.button(label='Dev (Desenvolvedor)', style=discord.ButtonStyle.primary)
        async def dev_button(self, button, interaction):
            await self.handle_role_assignment('Dev', interaction)

        @discord.ui.button(label='Estudante (Fasipe)', style=discord.ButtonStyle.primary)
        async def est_button(self, button, interaction):
            await self.handle_role_assignment('Estudante', interaction)

        @discord.ui.button(label='Visitante (Apenas de passagem...)', style=discord.ButtonStyle.primary)
        async def visit_button(self, button, interaction):
            await self.handle_role_assignment('Visitante', interaction)


async def setup(bot):
    await bot.add_cog(RoleCog(bot))
