import os

import discord
from dotenv import load_dotenv

from methods import (convert_pdf_to_combined_pdf, delete_files,
                     download_attachment_pdf, shape_file_name)

SUCCESS_MESSAGE = "success!"

load_dotenv()
Intents = discord.Intents.all()
Intents.members = True
client = discord.Client(intents=Intents)
@client.event
async def on_ready():
    delete_files()
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    try:
        if "combine" in message.content:
            download_attachment_pdf(message.attachments)
            convert_pdf_to_combined_pdf()
            if len(message.content.split(' ')) >1:
                file_name = shape_file_name(message.content.split(" ")[1])
                os.rename("./file/result.pdf", f"./file/{file_name}")
            else:
                file_name = "result.pdf"
            await message.channel.send(file=discord.File(f"./file/{file_name}"))
            delete_files()
    except Exception as e:
        await message.channel.send(str(e))

if __name__=="__main__":
    client.run(os.getenv('TOKEN'))
