import os
import discord
import Extract_Apex
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
Discord_tok = os.getenv('Discord_tok')

def free_mem_folder(folder):
    os.rmdir(folder)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='&', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event    
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Try &helps1')
    else:
        # Handle other errors
        print(f"Error: {error}")
@bot.command()
async def Apex(ctx, *, args):
    # 'args' will contain any additional words after the command
    #print(args)
    try:
        tok = args.split(' ')
        plat = tok[0]
        player_name = tok[1]
        player_info = Extract_Apex.Extract_Apex_func(plat,player_name)
        await ctx.send(file=discord.File(f'images/{player_name}_combined_image.png'))
        await ctx.send(player_info)
    except:
        await ctx.send('Try &helps2')
@bot.command()
async def Helps(ctx):
    help_info = "Games Supported: Apex,\nPlatforms: PC,PS4,X1,SWITCH\nFormat: &<game> <platform> <profile name>\nFor example type: ```&Apex PC MrAzn69```\n"
    await ctx.send(help_info)
    
bot.run(Discord_tok)

#print(Extract_Apex('PC','MrAzn69'))