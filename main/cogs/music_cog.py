import discord
import pytube
from discord.ext import commands
from discord.ui import View, Button
from collections import deque
from pytube import YouTube
import datetime
import asyncio

ffmpeg_path = 'C:/Program Files/ffmpeg/bin/ffmpeg.exe'
music_down_path = 'C:/Users/dudz_/OneDrive/Documents/Projects/ArchaneBot_py/main/music'


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


class MusicQueue:
    def __init__(self):
        self.queue = deque()
        self.history = deque()
        self.current = None

    def add_to_queue(self, ytdl_source):
        self.queue.append(ytdl_source)

    def get_next_song(self):
        if self.queue:
            self.history.append(self.current)
            self.current = self.queue.popleft()
            return self.current
        else:
            return None  # Retornar None se a fila estiver vazia

    def get_previous_song(self):
        if self.history:
            self.queue.appendleft(self.current)
            self.current = self.history.pop()
            return self.current
        else:
            return None  # Retornar None se não houver histórico


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.title

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        download_path = stream.download(output_path=music_down_path)
        return cls(discord.FFmpegPCMAudio(executable=ffmpeg_path, source=download_path), data=yt)


class MusicControls(View):
    def __init__(self, ctx, voice_client, music_queue):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.voice_client = voice_client
        self.music_queue = music_queue

    @discord.ui.button(label="Return", style=discord.ButtonStyle.grey, emoji="⏮️")
    async def return_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        previous_song = self.music_queue.get_previous_song()
        if previous_song:
            self.voice_client.stop()
            self.voice_client.play(previous_song, after=lambda e: print(f'Player error: {e}') if e else None)
            await interaction.response.send_message(f"Voltando para a música anterior: {previous_song.title}",
                                                    ephemeral=True)
        else:
            await interaction.response.send_message("Não há música anterior na fila.", ephemeral=True)

    @discord.ui.button(label="Play/Pause", style=discord.ButtonStyle.grey, emoji="⏯️")
    async def toggle_playback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.voice_client.is_playing():
            self.voice_client.pause()
            await interaction.response.send_message("Música pausada.", ephemeral=True)
        else:
            self.voice_client.resume()
            await interaction.response.send_message("Reprodução retomada.", ephemeral=True)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.grey, emoji="⏭️")
    async def skip_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        next_song = self.music_queue.get_next_song()
        if next_song:
            self.voice_client.stop()
            self.voice_client.play(next_song, after=lambda e: print(f'Player error: {e}') if e else None)
            await interaction.response.send_message(f"Pulando para a próxima música: {next_song.title}", ephemeral=True)
        else:
            await interaction.response.send_message("Não há próxima música na fila.", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red, emoji="⏹️")
    async def stop_playback(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.voice_client.stop()
        await interaction.response.send_message("Música parada e canal de voz será desconectado.", ephemeral=True)
        await self.voice_client.disconnect()

    @discord.ui.button(label="clear Playlist", style=discord.ButtonStyle.grey, emoji="🗑️")
    async def clear_queue(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.music_queue.queue.clear()
        await interaction.response.send_message("A fila de músicas foi limpa.", ephemeral=True)


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_queues = {}

    @commands.command()
    async def play(self, ctx, *, url):
        # Verifica se o usuário está em um canal de voz
        if not ctx.author.voice:
            await ctx.send("Você não está em um canal de voz.")
            return

        # Obtém ou cria um cliente de voz para o servidor
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()

        # Cria ou obtém a fila de música para o servidor
        music_queue = self.music_queues.get(ctx.guild.id, MusicQueue())
        self.music_queues[ctx.guild.id] = music_queue

        # Carrega a música e adiciona à fila
        try:
            ytdl_source = await YTDLSource.from_url(url, loop=self.bot.loop)
            music_queue.add_to_queue(ytdl_source)
    # ... resto do código ...
        except pytube.exceptions.AgeRestrictedError:
            embedE = discord.Embed(
                title="🚫  Música com Restrição de Idade  🚫",
                description="Desculpe, não posso reproduzir músicas/vídeos com restrições de idade.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embedE)
            return  # Encerra a execução do comando aqui
        except Exception as e:
            await ctx.send(f"Ocorreu um erro ao processar sua solicitação: {e}")
            return

        # Toca a próxima música da fila se necessário
        if not voice_client.is_playing():
            next_song = music_queue.get_next_song()
            if next_song:
                voice_client.play(next_song, after=lambda e: print(f'Player error: {e}') if e else None)

            try:
                await ctx.message.delete()
            except discord.Forbidden:
                await ctx.send("Não tenho permissão para apagar mensagens.")
            except discord.HTTPException:
                await ctx.send("Falha ao tentar apagar a mensagem.")

        # Envia uma mensagem embed para mostrar o que está tocando
        embed = discord.Embed(
            title="Adicionada à lista 🎶",
            description=f"[{ytdl_source.title}]({url})",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=ytdl_source.data.thumbnail_url)
        embed.add_field(name="Pedido por", value=ctx.author.mention)
        embed.add_field(name="Duração", value=str(datetime.timedelta(seconds=ytdl_source.data.length)))

        # Envia a mensagem com os controles de música
        view = MusicControls(ctx, voice_client, music_queue)
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
