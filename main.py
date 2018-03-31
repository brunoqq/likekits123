import discord
import asyncio
import time

client = discord.Client()
version = "Beta 1.0.0"

def toint(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


@client.event
async def on_ready():
    print("=================================")
    print("Bot iniciado com sucesso!")
    print (client.user.name)
    print (client.user.id)
    print(f"Bot Versão: {version}")
    print("=================================")

@client.event
async def on_message(message):

#INFO DO SERVIDOR
    if message.content.lower().startswith('!serverinfo'):
        server = message.server
        embedserver = discord.Embed(
            title='Informaçoes do Servidor',
            color=0x551A8B,
            descripition='Essas são as informaçoes\n')
        embedserver = discord.Embed(name="{} Server ".format(message.server.name), color=0x551A8B)
        embedserver.add_field(name="Nome:", value=message.server.name, inline=True)
        embedserver.add_field(name="Dono:", value=message.server.owner.mention)
        embedserver.add_field(name="ID:", value=message.server.id, inline=True)
        embedserver.add_field(name="Cargos:", value=len(message.server.roles), inline=True)
        embedserver.add_field(name="Membros:", value=len(message.server.members), inline=True)
        embedserver.add_field(name="Criado em:", value=message.server.created_at.strftime("%d %b %Y %H:%M"))
        embedserver.add_field(name="Emojis:", value=f"{len(message.server.emojis)}/100")
        embedserver.add_field(name="Região:", value=str(message.server.region).title())
        embedserver.set_thumbnail(url=message.server.icon_url)
        embedserver.set_footer(text="By: @brunoqq_")
        await client.send_message(message.channel, embed=embedserver)

#PEGA INFORMAÇÕES DO USUÁRIO
    if message.content.startswith('!user'):
        try:
            user = message.mentions[0]
            userjoinedat = str(user.joined_at).split('.', 1)[0]
            usercreatedat = str(user.created_at).split('.', 1)[0]

            userembed = discord.Embed(
                title="Nome:",
                description=user.name,
                color=0xe67e22
            )
            userembed.set_author(
                name="Informações do usuário"
            )
            userembed.add_field(
                name="Entrou no servidor em:",
                value=userjoinedat
            )
            userembed.add_field(
                name="Criou seu Discord em:",
                value=usercreatedat
            )
            userembed.add_field(
                name="TAG:",
                value=user.discriminator
            )
            userembed.add_field(
                name="ID:",
                value=user.id
            )

            await client.send_message(message.channel, embed=userembed)
        except IndexError:
            await client.send_message(message.channel, "Usuário não encontrado!")
        except:
            await client.send_message(message.channel, "Erro, desculpe. ")
        finally:
            pass

#APLICAR
    if message.content.lower().startswith('!aplicar'):
        embed = discord.Embed(
            title="Faça parte de nossa equipe:",
            color=0xe67e22,
            description="\n"
                        "***🎓 Ajudante (Trial-Mod)*** » https://pastebin.com/Eh4nGJ0J\n"
                        "***🔨 Construtor*** » https://pastebin.com/1xurYZtC"
        )
        embed.set_author(
            name="",
            icon_url="",
            url="https://twitter.com/brunoqq_"
        )
        embed.set_footer(
            text="Copyright © 2018 LikeKits",
            icon_url="https://cdn.discordapp.com/attachments/429409764590747660/429419629325189140/logolike.png"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/429409764590747660/429419629325189140/logolike.png"
        )

        await client.send_message(message.channel, embed=embed)

#APAGA DE 1 A 100 MENSAGENS
    if message.content.lower().startswith('!apagar'):
        qntdd = message.content.strip('!apagar ')
        qntdd = toint(qntdd)

        cargo = discord.utils.find(lambda r: r.name == "MEMBRO", message.server.roles)

        if message.author.top_role.position >= cargo.position:
            if qntdd <= 100:
                msg_author = message.author.mention
                await client.delete_message(message)
                # await asyncio.sleep(1)
                deleted = await client.purge_from(message.channel, limit=qntdd)
                botmsgdelete = await client.send_message(message.channel,
                                                         '{} mensagens foram excluidas com sucesso, {}.'.format(
                                                             len(deleted), msg_author))
                await asyncio.sleep(5)
                await client.delete_message(botmsgdelete)

            else:
                botmsgdelete = await client.send_message(message.channel,
                                                         'Utilize o comando digitando !apagar <numero de 1 a 100>.')
                await asyncio.sleep(5)
                await client.delete_message(message)
                await client.delete_message(botmsgdelete)

        else:
            await client.send_message(message.channel, 'Você não tem permissão para utilizar este comando.')

#TESTE
    if message.content.lower().startswith('!teste'):
            await client.send_message(message.channel, "aaa")

#VEJA O MS DE CONEXÃO DO BOT
    if message.content.lower().startswith('!ping'):
      timep = time.time()
      emb = discord.Embed(title='Aguarde', color=0x565656)
      pingm0 = await client.send_message(message.channel, embed=emb)
      ping = time.time() - timep
      pingm1 = discord.Embed(title='Pong!', description=':ping_pong: Ping - %.01f segundos' % ping, color=0x15ff00)
      await client.edit_message(pingm0, embed=pingm1)


#BOT AVISA O QUE FOI DITO
    if message.content.lower().startswith("!alert"):
        msg = message.content[7:2000]
        await client.send_message(message.channel, msg)
        await client.delete_message(message)

#INICIA UMA VOTAÇÃO COM REAÇÃO DE LIKE E DESLIKE
    elif message.content.lower().startswith('!votar'):
        msg = message.content[7:2000]
        botmsg = await client.send_message(message.channel, msg)
        await client.add_reaction(botmsg, '👍')
        await client.add_reaction(botmsg, '👎')
        await client.delete_message(message)

#GERA UM CONVITE E ENVIA NO PRIVADO DE QUEM EXECUTOU O COMANDO
    if message.content.lower().startswith('!convite'):
        invite = await client.create_invite(message.channel, max_uses=1, xkcd=True)
        await client.send_message(message.author, "Seu convite é {}".format(invite.url))
        await client.send_message(message.channel, "Olá {}, acabei de enviar um convite na sua direct.".format(message.author.mention))

#BANE UM MEMBRO
    elif message.content.lower().startswith('!ban'):
        membro = message.mentions[0]
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, "❌ {} Você nao possui permissão para executar este comando!".format(message.author.mention))

        await client.send_message(message.channel, "✔ O staff {} Baniu o membro {}!".format(message.author.mention, message.mentions[0].mention))
        await client.ban(membro)

#KICKA UM MEMBRO
    elif message.content.lower().startswith('!kick'):
        member = message.mentions[0]
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, "❌ {} Você nao possui permissão para executar este comando!".format(message.author.mention))

        await client.send_message(message.channel, "✔ O staff {} expulsou o membro {}!".format(message.author.mention, message.mentions[0].mention))
        await client.kick(member)

#MUTA UM MEMBRO
    elif message.content.lower().startswith('!mute'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        mention = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='Mutado')
        await client.add_roles(mention, cargo)
        await client.send_message(message.channel, '✔ O membro {} foi mutado com sucesso!'.format(mention))

#DESMUTA UM MEMBRO
    elif message.content.lower().startswith('!unmute'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        mention = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='Mutado')
        await client.remove_roles(mention, cargo)
        await client.send_message(message.channel, '✔ O membro {} foi desmutado com sucesso!'.format(mention))

#AO ENTRAR ELE ENVIA MENSAGEM NO PRIVADO, SETA ROLE MEMBRO E ENVIA MENSAGEM NO CANAL DO DISCORD
@client.event
async def on_member_join(member):
      grupo = discord.utils.find(lambda g: g.name == "💭 Membros", member.server.roles)
      await client.add_roles(member, grupo)
      channel = client.get_channel('429413097988554774')
      serverchannel = member.server.default_channel
      msg = "{0} entrou no servidor!".format(member.mention)
      await client.send_message(channel, msg)


# MENSAGEM QUANDO ALGUÉM SAI DO SERVIDOR
@client.event
async def on_member_remove(member):
    channel = client.get_channel('429413097988554774')
    serverchannel = member.server.default_channel
    msg = "{0} saiu do servidor!".format(member.name)
    await client.send_message(channel, msg)

client.run('NDI5NDIxMzMwMDQwMDk0NzIw.DaBZ8A.5rX99nbE7S56hePwXolk4nM1Fsw')