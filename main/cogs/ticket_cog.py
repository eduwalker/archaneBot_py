import discord
from discord.ext import commands


# Definindo a lista suspensa
class TicketDropdown(discord.ui.Select):
    def __init__(self):
        # Defina as opções que aparecerão na lista suspensa
        options = [
            discord.SelectOption(label="Gamer", description="Adentrar ao templo como PLAYER", emoji="👾"),
            discord.SelectOption(label="Dev", description="Adentrar ao templo como DESENVOLVEDOR", emoji="🤖"),
            discord.SelectOption(label="Estudante", description="Adentrar ao templo como ESTUDANTE (FASIPE)", emoji="📗"),
            discord.SelectOption(label="Viajante", description="Apenas de passagem pelo templo", emoji="🛣️"),
            discord.SelectOption(label="Cancelar", description="Cancele a abertura de um ticket", emoji="🚫")
            # Você pode adicionar mais opções conforme necessário
        ]
        super().__init__(placeholder="Escolha uma opção...", min_values=1, max_values=1, options=options)

    # Esta função é chamada quando o usuário seleciona uma opção
    async def callback(self, interaction: discord.Interaction):
        # Você pode adicionar a lógica com base na opção escolhida
        if self.values[0] == "Criar Ticket":
            # Aqui você pode adicionar a lógica para criar um ticket
            await interaction.response.send_message(f"Ticket criado!", ephemeral=True)
        elif self.values[0] == "Cancelar":
            await interaction.response.send_message(f"Cancelado.", ephemeral=True)


# Definindo a view que contém a lista suspensa
class TicketDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TicketDropdown())


# Definindo o cog
class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando para enviar o Embed com a lista suspensa
    @commands.command(name="ticket")
    async def ticket(self, ctx):
        # Criando o Embed
        embed = discord.Embed(title="SAUDAÇÕES VIAJANTE..."
                              ,
                              description="Selecione uma opção abaixo para definir seu caminho Arcano.",
                              color=discord.Color.blue())

        embed.set_image(url='https://files.oaiusercontent.com/file-1jhTIwsdtKsMJ8cWlSe0inq8?se=2023-12-23T16%3A15%3A26Z&sp=r&sv=2021-08-06&sr=b&rscc=max-age%3D31536000%2C%20immutable&rscd=attachment%3B%20filename%3D6d7540b8-a904-4f24-9ac8-8977bdf33805.webp&sig=ClP2wCTPBPuTcDXrM005pSlMa5Ts4SvHJYfZN5WqdTc%3D')

        # Enviando a mensagem com o Embed e a lista suspensa anexada
        await ctx.send(embed=embed, view=TicketDropdownView())


async def setup(bot):
    await bot.add_cog(TicketCog(bot))
