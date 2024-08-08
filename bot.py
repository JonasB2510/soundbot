import discord
from discord.ext import commands
import os
import threading
import tkinter as tk
from tkinter import messagebox

# Setze deinen Token hier sicher ein
DISCORD_TOKEN = ""

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.dm_messages = True

# Bot-Setup
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)
sound_files = {
    'test1': 'sounds/test1.mp3',
    'test2': 'sounds/test2.mp3',
    # Füge weitere Sounds hier hinzu
}

# Event, wenn der Bot bereit ist
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Funktion zum Betreten eines Sprachkanals
async def join_channel(guild_id, channel_id):
    try:
        guild = bot.get_guild(guild_id)
        channel = guild.get_channel(channel_id)
        await channel.connect()
    except Exception as e:
        print(f"Error joining channel: {e}")

# Funktion zum Verlassen eines Sprachkanals
async def leave_channel(guild_id):
    try:
        guild = bot.get_guild(guild_id)
        if guild.voice_client:
            await guild.voice_client.disconnect()
    except Exception as e:
        print(f"Error leaving channel: {e}")

# Funktion zum Abspielen eines Sounds
async def play_sound(guild_id, sound_name):
    try:
        guild = bot.get_guild(guild_id)
        if guild.voice_client and sound_name in sound_files:
            guild.voice_client.stop()
            source = discord.FFmpegPCMAudio(sound_files[sound_name])
            guild.voice_client.play(source)
        else:
            print(f"Sound {sound_name} not found or bot not connected to voice channel.")
    except Exception as e:
        print(f"Error playing sound: {e}")

class SoundboardApp:
    def __init__(self, master, bot):
        self.master = master
        self.bot = bot
        self.master.title("Discord Soundboard")
        
        self.guild_id = tk.StringVar()
        self.channel_id = tk.StringVar()
        
        # GUI-Elemente erstellen
        tk.Label(master, text="Guild ID:").grid(row=0)
        tk.Entry(master, textvariable=self.guild_id).grid(row=0, column=1)
        
        tk.Label(master, text="Channel ID:").grid(row=1)
        tk.Entry(master, textvariable=self.channel_id).grid(row=1, column=1)
        
        tk.Button(master, text="Join", command=self.join_channel).grid(row=2, column=0)
        tk.Button(master, text="Leave", command=self.leave_channel).grid(row=2, column=1)
        
        self.create_sound_buttons()

    def create_sound_buttons(self):
        row = 3
        for sound_name in sound_files:
            tk.Button(self.master, text=sound_name, command=lambda s=sound_name: self.play_sound(s)).grid(row=row, column=0, columnspan=2)
            row += 1

    def join_channel(self):
        try:
            guild_id = int(self.guild_id.get())
            channel_id = int(self.channel_id.get())
            bot.loop.create_task(join_channel(guild_id, channel_id))
        except ValueError:
            print("Invalid Guild ID or Channel ID")

    def leave_channel(self):
        try:
            guild_id = int(self.guild_id.get())
            bot.loop.create_task(leave_channel(guild_id))
        except ValueError:
            print("Invalid Guild ID")

    def play_sound(self, sound_name):
        try:
            guild_id = int(self.guild_id.get())
            bot.loop.create_task(play_sound(guild_id, sound_name))
        except ValueError:
            print("Invalid Guild ID")

# Starten der GUI in einem separaten Thread
def start_gui(bot):
    root = tk.Tk()
    app = SoundboardApp(root, bot)
    root.mainloop()

# Starten des Bots in einem separaten Thread
def start_bot():
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("Discord Token is not set. Please set the DISCORD_TOKEN environment variable.")

# Starten des Bots und der GUI
if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    start_gui(bot)
