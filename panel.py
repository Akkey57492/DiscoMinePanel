import nextcord
import yaml
import os

from nextcord.ext import commands
from rcon import Client

class Panel(nextcord.ui.View):
    def __init__(self):
        super().__init__()
    
    @nextcord.ui.button(label="起動", style=nextcord.ButtonStyle.green, custom_id="on")
    async def on(self, button: nextcord.Button, interaction: nextcord.Interaction):
        allow_users = config["discord"]["users"]
        for uid in allow_users:
            if uid == interaction.user.id:
                ps1_fullpath = config["minecraft"]["start"]
                os.system('powershell -Command' + ' ' +\
                    f'powershell -ExecutionPolicy RemoteSigned {ps1_fullpath}')
                await interaction.response.edit_message(
                    content="起動中です。\n起動までお待ちください。",
                    view=None
                )
                return
            else:
                pass
        await interaction.response.edit_message(
            content="申し訳ありません。\nこの操作パネルは指定されたユーザーのみが操作できます。",
            view=None
        )

    @nextcord.ui.button(label="停止", style=nextcord.ButtonStyle.red, custom_id="off")
    async def off(self, button: nextcord.Button, interaction: nextcord.Interaction):
        allow_users = config["discord"]["users"]
        for uid in allow_users:
            if uid == interaction.user.id:
                rcon_address = config["minecraft"]["ip"]
                rcon_port = config["minecraft"]["port"]
                rcon_pass = config["minecraft"]["password"]
                rcon_stop_cmd = config["minecraft"]["stop"]
                with Client(str(rcon_address), int(rcon_port), passwd=str(rcon_pass)) as client:
                    client.run(str(rcon_stop_cmd))
                await interaction.response.edit_message(
                    content="停止中です。\n完全停止までお待ちください。",
                    view=None
                )
                return
            else:
                pass
        await interaction.response.edit_message(
            content="申し訳ありません。\nこの操作パネルは指定されたユーザーのみが操作できます。",
            view=None
        )

with open("config.yml", "r", encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)

bot = commands.Bot(command_prefix=";", intents=nextcord.Intents.all(), help_command=None)

@bot.command()
async def panel(panel):
    allow_users = config["discord"]["users"]
    for uid in allow_users:
        if int(uid) == int(panel.author.id):
            btn_view = Panel()
            await panel.send("行う動作をボタンで選択してください。", view=btn_view)
        else:
            await panel.send("申し訳ありません。\nこのコマンドは指定されたユーザーのみが操作できます。")

@bot.command()
async def addpl(addpl):
    allow_users = config["discord"]["users"]
    for uid in allow_users:
        if int(uid) == int(panel.author.id):
            addpl_msg = await addpl.send("プラグインを追加中です。\nお待ちください。")
            channel = bot.get_channel(int(addpl.channel.id))
            message = await channel.fetch_message(int(addpl.message.id))
            attachments_filename = message.attachments[0].filename
            plugins_path = config["minecraft"]["plugins"]
            await message.attachments[0].save(plugins_path + f"\\{attachments_filename}")
            await addpl_msg.edit("プラグインを追加しました。")
        else:
            await panel.send("申し訳ありません。\nこのコマンドは指定されたユーザーのみが操作できます。")

bot.run(token=config["discord"]["token"])