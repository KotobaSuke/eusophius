import discord
import sml
import robot_cmd as rcmd
import mancala as mcl, con_four as con4

import base64
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timezone, timedelta
from robot_cmd import Command
from keep_alive import keep_alive
from latindict import latinDict
from handict import loadDatabase as loadHan
from errors import ArgMissingError, EmptyMsgError, OptConflictError, OptError, OverlengthError, UnsupportedGameError

TOKEN = base64.b64decode("TVRBM01UUTJNalF6TkRrMk9USXpNVE00TUEuRzJHTVctLnRvbnJ6Mm1tLWxqM2lLWk8yY1VyejlQMWJITVNXeVZDQ3RjWXZ3").decode()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
boot_time = None

JOURNAL_CNL = None
ROBOT_CNL = None
POTATO_CNL = None

now_time = datetime.now(timezone(timedelta(hours=8)))


async def sendJournal():
    await client.wait_until_ready()
    text = await sml.getDataList('R', '', True, False)

    await JOURNAL_CNL.send(""" :newspaper2:  **ACTA HODIERNA**     {}
————————————————————
STATVS SOCIETATIS MVSICAE LAGRAMMATIS

{}""".format(str(now_time)[:10], text))


async def sendTodayWord():
    await client.wait_until_ready()
    text = latinDict.getRandomEntry().toText()
    await POTATO_CNL.send(""" :label:  **VOCABVLVM HODIERNVM**     {}\n
{}""".format(str(now_time)[:10], text))


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    global boot_time
    boot_time = datetime.now(timezone(timedelta(hours=8)))

    try:
        await sml.updateAll()
    except:
        print("SML Update Failed.")

    global JOURNAL_CNL
    JOURNAL_CNL = client.get_channel(1074055996013543514)
    global ROBOT_CNL
    ROBOT_CNL = client.get_channel(754022821763612702)
    global POTATO_CNL
    POTATO_CNL = client.get_channel(1074290154992312380)
    global stat
    LATIN_DICT_SRC = "latindictsrc.py"
    latinDict.scan(LATIN_DICT_SRC)
    print(
        "Latin Dictionary has been loaded, with {} entries identified.".format(
            latinDict.getVolume()))
    loadHan()
    print("Hanzi Dictionary has been loaded.")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(sendJournal, CronTrigger(hour='0', minute='0', second='0'))
    scheduler.add_job(sendTodayWord,
                      CronTrigger(hour='0', minute='0', second='5'))
    scheduler.add_job(
        rcmd.autoCleanApp,
        CronTrigger(second="0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55"))
    scheduler.start()


async def dealCmd(cmd: str, msg):
    abbrMap = {
        "lms": "sml",
        "mcl": "mancala",
        "tf": "transfer",
        "?": "juva",
    }
    try:
        if cmd.head in abbrMap:
            head = abbrMap[cmd.head]
        else:
            head = cmd.head

        if head == "alea": await rcmd.throwDie(cmd, msg)
        elif head == "bv": await rcmd.showBiliVideo(cmd, msg)
        elif head == "echo": await rcmd.echo(cmd, msg)
        elif head == "eval": await rcmd.cmdEval(cmd, msg)
        elif head == "dt": await rcmd.showDataBase(cmd, msg)
        elif head == "fortuna": await rcmd.fortuneLot(cmd, msg)
        elif head == "graece": await rcmd.greekTranscript(cmd, msg)
        elif head == "juva": await rcmd.cmdHelp(cmd, msg)
        elif head == "nomenmihi": await rcmd.manageUserName(cmd, msg)
        elif head == "opus": await rcmd.showNowWork(cmd, msg)
        elif head == "robota": await rcmd.robotReport(cmd, msg, boot_time)
        elif head == "salve": await rcmd.robotGreet(cmd, msg)
        elif head == "sml": await rcmd.showSmlInfo(cmd, msg)
        elif head == "transfer": await rcmd.translate(cmd, msg)
        elif head == "mi": await rcmd.imitateMi(cmd, msg)

        nowApp = rcmd.app_box.app

        if not nowApp:
            if head == "con4": await rcmd.runConnectFour(cmd, msg)
            elif head == "mancala":
                await rcmd.runMancala(cmd, msg, client.user)
        else:
            if head == "desine": await rcmd.endApp(cmd, msg)
            else:
                if isinstance(nowApp, mcl.MancalaBoard):
                    if head == "intersim": await rcmd.joinMancala(cmd, msg)
                    if head == "interes":
                        await rcmd.callBotToMancala(cmd, msg, client.user)
                    if head == "mv": await rcmd.operateMancala(cmd, msg)
                elif isinstance(nowApp, con4.ConFourBoard):
                    if head == "intersim": await rcmd.joinConnectFour(cmd, msg)
                    if head == "interes": raise UnsupportedGameError()
                    if head == "p": await rcmd.operateConnectFour(cmd, msg)

    except OverlengthError as e:
        print(e)
        try:
            await rcmd.warn(
                "*Nimis multa argumenta.* (`{}`)".format(
                    rcmd.CMD_FORMATS[head]), msg)
        except:
            await rcmd.warn("*Nimis multa argumenta.*", msg)
    except ArgMissingError as e:
        print(e)
        try:
            await rcmd.warn(
                "*Parum multa argumenta.* (`{}`)".format(
                    rcmd.CMD_FORMATS[head]), msg)
        except:
            await rcmd.warn("*Parum multa argumenta.*", msg)
    except OptError as e:
        print(e)
        if len(e.opts) == 1:
            await rcmd.warn("*Ignota optio:* `{}`.".format(', '.join(e.opts)),
                            msg)
        else:
            await rcmd.warn(
                "*Ignotae optiones:* `{}`.".format(', '.join(e.opts)), msg)
    except OptConflictError as e:
        print(e)
        await rcmd.warn(
            "*Optiones interse repugnantes:* `{}` cum `{}`.".format(
                e.cause, ', '.join(e.conf)), msg)
    except UnsupportedGameError as e:
        print(e)
        await msg.channel.send("*Eusophius nondum hôc ludo ludere possum.*")
    except EmptyMsgError:
        await msg.channel.send("*nihil*")
    except TypeError as e:
        print(e)
        try:
            await rcmd.warn(
                "*Typus pravus.* (`{}`)".format(rcmd.CMD_FORMATS[cmd.head]),
                msg)
        except:
            await rcmd.warn("*Typus pravus.*", msg)
    except ValueError as e:
        print(e)
        try:
            await rcmd.warn(
                "*Valor pravus.* (`{}`)".format(rcmd.CMD_FORMATS[cmd.head]),
                msg)
        except:
            await rcmd.warn("*Valor pravus.*", msg)
    except PermissionError as e:
        print(e)
        await rcmd.warn("*Tibi non licet hoc agere.*", msg)
    pass


@client.event
async def on_message(msg):

    if msg.content.startswith('$'):
        if msg.author == client.user and not msg.content.startswith("$#"):
            return

        cmd = Command(msg.content)
        await dealCmd(cmd, msg)


keep_alive()
client.run(TOKEN)
