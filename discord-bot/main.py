import disnake
import datetime
import requests
import json
import asyncio
from disnake.ext import commands
import os


bot = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all(),
                   activity=disnake.Game(name="Работаем во благо роботов"),
                   test_guilds=[1231205097711734887])

if not os.path.exists('registered_users.json'):
    with open('registered_users.json', 'w') as file:
        json.dump({}, file)

registered_users = json.load(open('registered_users.json')) if os.path.exists('registered_users.json') else {}

if os.path.exists('transportations.json'):
    with open('transportations.json', 'r') as file:
        datas = json.load(file)


@bot.event
async def on_ready():
    print(f"Бот {bot.user} везёт груз 200!!")


@bot.event
async def on_member_join(member):
    role = await disnake.utils.get(guild_id=member.guild.id, id=770246760177467392)
    channel = member.guild.system_channel

    embed = disnake.Embed(
        title="Новый пассажир!",
        description=f"{member.name}#{member.descriminator}",
        color=0xffffff
    )

    await member.add_role(role)
    await channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения команды.")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=disnake.Embed(
            title=f"Команда: '{ctx.prefix}{ctx.command.name}'",
            description=f"Правильное написание команды: '{ctx.prefix}{ctx.command.name}' ({ctx.command.brief})"
                        f"\nExample: {ctx.prefix}{ctx.command.usage} ",
            color=0xd3fc86
        ))


@bot.command(name="help", brief="Вывод всего списка команд.", usage="!help", help="Выводит весь список команд")
async def help(ctx):
    embed = disnake.Embed(
        title='Список команд',
        description='Список всех доступных команд',
        color=0x04860e
    )

    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)

    await ctx.send(embed=embed)


@bot.command(name="status", brief="Статус сервера", usage="!status", help="Отображает информацию о сервере")
@commands.has_permissions(administrator=True)
async def status(ctx):
    url = "http://45.141.76.200:1212/status"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            await ctx.send('Сервер доступен!')
        else:
            await ctx.send('Сервер не доступен!')
    except requests.exceptions.RequestException:
        await ctx.send(embed=disnake.Embed(
            title=f"Ошибка!",
            description=f"Ошибка при попытке подключении к серверу! Сообщите администратору о проблеме.",
            color=0x8B0000
        ))
        await asyncio.sleep(60)


@bot.command(name="timeout", brief="Тайм-Аут",
             usage="!timeout <@user>(@Пользователь#0000), Время = Время мута, Причина = Причина мута",
             help="Добавляет тайм-аут игроку(задаётся в минутах)")
@commands.has_permissions(administrator=True)
async def timeout(ctx, member: disnake.Member, time: str, reason: str):
    time = datetime.datetime.now() + datetime.timedelta(minutes=int(time))
    await member.timeout(reason=reason, until=time)
    await ctx.send(embed=disnake.Embed(
        title="Тайм-Аут!",
        description=f"Великий {ctx.author.mention} замутил {member.mention}!",
        color=0x9ACD32
    ))


@bot.command(name="untimeout", brief="Окончание Тайм-Аута", usage="!untimeout <@user>(@Пользователь#0000)",
             help="Убирает тайм-аут с игрока")
@commands.has_permissions(administrator=True)
async def untimeout(ctx, member: disnake.Member):
    await member.timeout(reason=None, until=None)
    await ctx.send(embed=disnake.Embed(
        title="Окончание Тайм-Аута!",
        description=f"Великий {ctx.author.mention} размутил {member.mention}!",
        color=0x9ACD32
    ))


@bot.command(name="kick", brief="Кикнуть пользователя", usage="!kick <@user> <reason = None>",
             help="Кикает пользователя с сервера")
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason="падла"):
    await ctx.send(embed=disnake.Embed(
        title="Кикнут!",
        description=f"Великий {ctx.author.mention} кикнул {member.mention} по причине {reason}!",
        color=0xFF4500
    ))
    await member.kick(reason=reason)
    await ctx.message.delete()


@bot.command(name="ban", brief="Забанить пользователя", usage="!ban <@user> <reason = None>",
             help="Банит игрока на сервере")
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason="падла"):
    await ctx.send(embed=disnake.Embed(
        title="Забанен!",
        description=f"Великий {ctx.author.mention} забанил {member.mention} по причине {reason}!",
        color=0xFF0000
    ))
    await member.ban(reason=reason)
    await ctx.message.delete()


# блок регистрации
@bot.command(name="reg", brief="Регистрирует вас на сайте Последний путь",
             usage="!reg Никнейм Пароль(никнейм только английскими буквами)", help="Регистрация на сайте")
async def reg(ctx, username: str, password: str):
    data = {username: password}

    with open('registered_users.json', 'r') as file:
        try:
            registered_users = json.load(file)
        except json.JSONDecodeError:
            registered_users = {}

    if username in registered_users:
        await ctx.send(embed=disnake.Embed(
            title="Под данным именем уже зарегистрированы!",
            description=f"Попробуйте повторить!(Пример !рег Никнейм Пароль)",
            color=0x800020
        ))
    else:
        registered_users.update(data)
        await ctx.send(embed=disnake.Embed(
            title="Успешно зарегистрирован!",
            description=f"Можно переходить на сайт https://example.com",
            color=0x228b22
        ))

    with open('registered_users.json', 'w') as file:
        json.dump(registered_users, file, indent=4)


@bot.command()
async def request(ctx, *, message: str):
    if isinstance(ctx.channel, disnake.DMChannel):
        guild = bot.get_guild(1231205097711734887)
        if guild:
            support_channel = await guild.create_text_channel(name=f'Запрос от {ctx.author}', topic='Техподдержка')
            await support_channel.send(f'**Новый запрос:**\n{message}')
            response = await bot.wait_for('message', check=lambda m: m.channel == support_channel)
            await ctx.send(f'**Ответ от техподдержки:**\n{response.content}')
            await support_channel.delete()
        else:
            await ctx.send('Не удалось найти сервер техподдержки. Обратитесь к администратору.')


@bot.command(name='order')
async def order(ctx, *args):
    if len(args) != 3:
        await ctx.send('Пожалуйста, укажите команду в формате !order Транспорт Пункт_назначения Логин.')
        return

    transport, destination, login = args

    if login not in registered_users:
        await ctx.send('Данный логин не зарегистрирован.')
        return

    data = {
        'date': str(datetime.datetime.now().strftime('%d.%m.%y')),
        'transport': transport,
        'destination': destination,
        'user_id': login
    }

    datas.append(data)

    with open('transportations.json', 'w') as file:
        json.dump(datas, file, indent=4)
        file.write('\n')

    await ctx.send(f'Данные успешно сохранены для пользователя {login}.')


bot.run('MTA4NzM3NDM5NTkxMzI3NzQ3MQ.GRfw88.bv-OzyCkxf6LQz260Omsy4CYj0G9U_XdOv9zV4')