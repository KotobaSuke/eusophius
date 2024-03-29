import re
import username as usrn
import inflection as infl
import bili_video as bili
import hellenize as hln
import greeting, fortune, sml, eld, daijisen, krdict
import mancala as mcl
import con_four as con4
import robot_app as app
import handict as han

from datetime import datetime, timezone, timedelta
from bilibili_api import video
from latindict import latinDict
from errors import ArgMissingError, EmptyMsgError, OptConflictError, OptError, OverlengthError
from shuxuemi import generateModel as miModel

app_box: app.AppBox = app.AppBox()


class Command(object):

    def __init__(self, raw: str) -> None:
        tokens = re.split(r" +", raw)
        self.head = tokens[0].lstrip('$').lstrip('#')
        self.opts = set()
        self.args = []
        if len(tokens) > 1:
            if tokens[1].startswith('-'):
                self.opts = set(list(tokens[1].lstrip('-')))
                self.args = tokens[2:]
            else:
                self.args = tokens[1:]

    def __len__(self):
        return len(self.args)



CMD_FORMATS = {
    "alea": "$alea [NVM_LTR(4~65535)]",
    "bv": "$bv CODEX_BV/AV(\"av...\")",
    "fortuna": "$fortuna",
    "graece": "$graece [-ip] LTR_LTN; $graece -a",
    "mancala": "$mancala [-prEL] [NVM_LPD NVM_PVT]",
    "mi": "$mi INITIVM",
    "nomenmihi": "$nomenmihi NOMEN; $nomenmihi -d",
    "robota": "$robota [-v]",
    "salve": "$salve",
    "sml": "$sml(=lms) [-[A|R|V]vm] AREA; $sml -c CODEX",
}


def getNowTime() -> datetime:
    return datetime.now(timezone(timedelta(hours=8)))


def checkExcessiveOpts(cmd: Command, legalOpts: str) -> list:
    opts = cmd.opts.copy()
    for o in legalOpts:
        if o in opts:
            opts.remove(o)
    return list(set(list(opts)))


def checkCmdFormat(cmd: Command,
                   argNum: int,
                   argOptNum: int = 0,
                   legalOpts: str = "",
                   conflictOpts: list[tuple[str, str]] = []):
    if len(cmd) > argNum + argOptNum:
        raise OverlengthError()
    elif len(cmd) < argNum:
        raise ArgMissingError()
    exOpts = checkExcessiveOpts(cmd, legalOpts)
    if exOpts:
        raise OptError(exOpts)
    if conflictOpts:
        for c, o in conflictOpts:
            if c in cmd.opts:
                for s in o:
                    if s in cmd.opts:
                        raise OptConflictError(c, s)


async def warn(text: str, msg) -> str:
    await msg.channel.send("**MONITIO**: {}".format(text))


async def robotReport(cmd: Command, msg, bootTime: datetime):
    try:
        checkCmdFormat(cmd, 0, legalOpts='v')
    except BaseException as e:
        raise e

    nowTime = getNowTime()
    await msg.channel.send("Εὐσοφίος adsum. Tempus nunc est {} Pekini.".format(
        str(nowTime)[:19]))
    timeInterval = (nowTime - bootTime).seconds
    minutes = timeInterval // 60
    if minutes == 0:
        await msg.channel.send("Operari modo coepi.")
    elif minutes < 60:
        await msg.channel.send("Bene operor per {} minut{}.".format(
            minutes, "um" if minutes == 1 else "a"))
    else:
        hours = minutes // 60
        minutes %= 60
        if hours < 24:
            await msg.channel.send(
                "Bene operor per {} hora{} et {} minut{}.".format(
                    hours, "m" if hours == 1 else "s", minutes,
                    "um" if minutes == 1 else "a"))
        else:
            days = hours // 24
            hours %= 24
            await msg.channel.send("Bene operor per {}d{}h{}min.".format(
                days, hours, minutes))

    if 'v' in cmd.opts:
        await msg.channel.send("Operor a tempore: {}.".format(
            str(bootTime)[:19]))


async def robotGreet(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0)
    except BaseException as e:
        raise e
    await msg.channel.send("Salve, {}!".format(
        infl.vocativize(usrn.getUserName(msg.author.name))))
    await msg.channel.send("{}".format(greeting.greet(getNowTime().hour)))


async def fortuneLot(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0)
    except BaseException as e:
        raise e
    authorTag = int(str(msg.author.id)[-4:])
    await msg.channel.send(
        "Fortuna hodie tibi est: {}.\n--------------------".format(
            fortune.countFortune(authorTag)))
    await msg.channel.send("**Agendum:**\n  {}\n**Vitandum:**\n  {}".format(
        *fortune.doAndDont(authorTag)))


async def throwDie(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0, 1)
    except BaseException as e:
        raise e

    async def runThrowDie(sideNum: int = 6):
        sideNum = int(sideNum)
        await msg.channel.send("Aleam {} laterum jecisti.".format(sideNum))
        await msg.channel.send("Eventus est: **{}**.".format(
            fortune.dice(sideNum)))

    try:
        await runThrowDie(*cmd.args)
    except:
        raise TypeError()


async def showBiliVideo(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 1)
    except BaseException as e:
        raise e

    try:
        if cmd.args[0].startswith(("av", "Av", "AV")):
            v = video.Video(aid=int(cmd.args[0][2:]))
        else:
            v = video.Video(bvid="BV{}".format(cmd.args[0]))
        info = await v.get_info()
        text = bili.formatVideoInfo(info)
        await msg.channel.send(text)
    except:
        await warn("*Codex BV/av pravus.*", msg)


async def showSmlInfo(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0, 1, legalOpts="cvmARV")
    except BaseException as e:
        raise e

    if 'c' in cmd.opts:
        try:
            checkCmdFormat(cmd, 1, legalOpts='c')
        except BaseException as e:
            raise e

        try:
            bv = await sml.query(cmd.args[0])
            await showBiliVideo(Command("$bv {}".format(bv[2:])), msg)
        except:
            await warn("*Codex pravus.*", msg)
    else:
        try:
            checkCmdFormat(cmd,
                           0,
                           1,
                           legalOpts="vmARV",
                           conflictOpts=[('A', "RV"), ('R', "AV"),
                                         ('V', "AR")])
        except BaseException as e:
            raise e

        range = cmd.args[0] if len(cmd) > 0 else ""
        if 'A' in cmd.opts: mode = 'A'
        elif 'R' in cmd.opts: mode = 'R'
        elif 'V' in cmd.opts: mode = 'V'
        else: mode = 'N'

        text = await sml.getDataList(mode, range, 'm' in cmd.opts, 'v'
                                     in cmd.opts)
        await msg.channel.send("{}".format(text))


async def greekTranscript(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0, 65536, legalOpts="aip")
    except BaseException as e:
        raise e

    if 'a' in cmd.opts:
        try:
            checkCmdFormat(cmd, 0, legalOpts="a")
        except BaseException as e:
            raise e

        await msg.channel.send("{}".format(hln.help()))
    else:
        try:
            checkCmdFormat(cmd, 1, 65536, legalOpts="ip")
        except BaseException as e:
            raise e

        text = hln.latinToGreek(' '.join(cmd.args), not 'p' in cmd.opts, 'i'
                                in cmd.opts)
        await msg.channel.send("{}".format(text))
    try:
        checkCmdFormat(cmd, 1)
    except BaseException as e:
        raise e


async def manageUserName(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0, 65536, legalOpts="d")
    except BaseException as e:
        raise e

    if 'd' in cmd.opts:
        try:
            checkCmdFormat(cmd, 0, legalOpts="d")
        except BaseException as e:
            raise e

        usrn.delUserName(msg.author.name)
    else:
        try:
            checkCmdFormat(cmd, 1, 65536)
        except BaseException as e:
            raise e

        name = ' '.join(cmd.args)
        usrn.setUserName(msg.author.name, name)

    await msg.channel.send("Nunc nomen tibi est: **{}**".format(
        usrn.getUserName(msg.author.name)))


async def showNowWork(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0)
    except BaseException as e:
        raise e

    if app_box:
        workName = app_box.app.getName()
    else:
        workName = "nihil"
    await msg.channel.send("Opus nunc est : *{}*".format(workName))


async def lookupDictionary(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0, 65536, legalOpts="irR")
    except BaseException as e:
        raise e

    DICT_LIST = {
        "eld":
        "*An __E__lementary __L__atin __D__ictionary*, la>en",
        "djs":
        "*__D__ai__j__i__s__en* (デジタル大辞泉), ja>ja",
        "han":
        "*Index Pronunciationalis Multilingualis Litterarum Sinicarum*",
        "llt":
        "*__L__exicon __L__atinum __T__rilianum*, la>en, cum {} vocabulis".
        format(latinDict.getVolume()),
        "wjk":
        "*Weblio Lexicon Japono-Coreanum* (Weblio 日韓辞典), ja>ko",
    }

    if 'i' in cmd.opts:
        try:
            checkCmdFormat(cmd, 0, legalOpts='i')
        except BaseException as e:
            raise e

        await msg.channel.send("{}".format('\n'.join(
            ["`{}`:    {}".format(k, v) for (k, v) in DICT_LIST.items()])))
    else:
        try:
            checkCmdFormat(cmd, 2, 65536, legalOpts='rR')
        except BaseException as e:
            raise e

        dictName = cmd.args[0]
        entry = ' '.join(cmd.args[1:])

        if dictName not in DICT_LIST:
            await warn("*Lexicon nondum sustendum vel nomen pravum.*", msg)

        try:
            if dictName == "llt":
                try:
                    checkCmdFormat(cmd, 2, 65536, legalOpts='rR')
                except BaseException as e:
                    raise e
                if entry == '?':
                    text = latinDict.getInfo()
                elif entry == '~':
                    text = latinDict.getRandomEntry().toText()
                else:
                    if 'r' in cmd.opts:
                        try:
                            checkCmdFormat(cmd, 2, 65536, legalOpts='r')
                        except BaseException as e:
                            raise e

                        if entry.startswith('*'):
                            entries = latinDict.getEntryByDef(
                                entry.lstrip('*'), True)
                        else:
                            entries = latinDict.getEntryByDef(entry)
                        if len(entries) > 10:
                            text = '\n\n'.join(
                                list(map(lambda x: x.toText(),
                                         entries[:10]))) + "\n... ..."
                        else:
                            text = '\n\n'.join(
                                list(map(lambda x: x.toText(), entries)))
                    else:
                        entries = latinDict.getEntry(entry)
                        text = '\n\n'.join(
                            list(map(lambda x: x.toText(), entries)))
                if not text:
                    raise EmptyMsgError()
                await msg.channel.send("{}".format(text))
            elif dictName == "han":
                try:
                    checkCmdFormat(cmd, 2, 2)
                except BaseException as e:
                    raise e

                text = han.getEntry(entry)
                if not text:
                    raise EmptyMsgError()
                await msg.channel.send("{}".format(text))
            else:
                try:
                    checkCmdFormat(cmd, 2, 65536)
                except BaseException as e:
                    raise e
                if dictName == "eld":
                    text = ""
                    for i in [""] + list(range(1, 5)):
                        rs = eld.mainSearch(entry + str(i))
                        if rs:
                            if text: text += "——————————\n"
                            text += rs
                    await msg.channel.send("{}".format(text))
                elif dictName == "djs":
                    text = daijisen.mainSearch(entry)
                    await msg.channel.send("{}".format(text))
                elif dictName == "wjk":
                    text = krdict.mainSearch(entry)
                    await msg.channel.send("{}".format(text))
        except BaseException as e:
            print(e)
            raise EmptyMsgError()


async def echo(cmd: Command, msg):
    authorTag = int(str(msg.author.id)[-4:])
    if authorTag not in [3544]:
        raise PermissionError()

    try:
        checkCmdFormat(cmd, 1, 65536)
    except BaseException as e:
        raise e

    await msg.channel.send("{}".format(' '.join(cmd.args)))


async def cmdEval(cmd: Command, msg):
    authorTag = int(str(msg.author.id)[-4:])
    if authorTag not in [3544]:
        raise PermissionError()

    try:
        checkCmdFormat(cmd, 1, 65536)
    except BaseException as e:
        raise e

    expr = ' '.join(cmd.args).strip('`')
    try:
        rs = eval(expr)
    except:
        rs = "ERROR"
    await msg.channel.send("Valor expressionis `{}`:\n\t__`{}`__".format(
        expr, rs))


async def cmdHelp(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 1)
    except BaseException as e:
        raise e

    if cmd.args[0] in CMD_FORMATS:
        await msg.channel.send("`{}`".format(CMD_FORMATS[cmd.args[0]]))
    else:
        await msg.channel.send("*Jussum ignotum sive sine auxilio.*")


async def showDataBase(cmd: Command, msg):
    authorTag = int(str(msg.author.id)[-4:])
    if authorTag not in [3544]:
        raise PermissionError()

    try:
        checkCmdFormat(cmd, 0, 2, legalOpts="rv")
    except BaseException as e:
        raise e

    db = None #
    scope = db
    if len(cmd) == 2:
        if cmd.args[1] in db:
            scope = db[cmd.args[1]]
        else:
            raise EmptyMsgError()

    def dbDictUnpack(v):
        rs = []
        try:
            for k, v2 in v.items():
                rs.append("\"{}\": \"{}\"".format(k, v2))
            return "; ".join(rs)
        except:
            return str(v)

    rs = []
    if len(cmd) == 0 or ('r' not in cmd.opts and cmd.args[0] == '/'):
        for k, v in scope.items():
            rs.append("\"{}\":    \"{}\"".format(k, dbDictUnpack(v)))
    else:
        entry = cmd.args[0].strip('`')
        for k, v in scope.items():
            pattern = str(v) if 'v' in cmd.opts else str(k)
            if 'r' not in cmd.opts and pattern == entry:
                rs.append("\"{}\":    \"{}\"".format(k, dbDictUnpack(v)))
            elif 'r' in cmd.opts and re.match(entry, pattern):
                rs.append("\"{}\":    \"{}\"".format(k, dbDictUnpack(v)))
    if rs:
        await msg.channel.send('\n'.join(rs))
    else:
        raise EmptyMsgError()


async def runMancala(cmd: Command, msg, bot):
    try:
        checkCmdFormat(cmd, 0, 2, legalOpts="prEL")
    except BaseException as e:
        raise e

    if len(cmd) == 0:
        app_box.setApp(mcl.MancalaBoard())
    else:
        try:
            app_box.setApp(mcl.MancalaBoard(*cmd.args))
        except BaseException as e:
            raise e

    if 'p' in cmd.opts:
        app_box.app.handicap = False

    if 'r' in cmd.opts:
        app_box.app.shuffle = True

    if 'E' in cmd.opts:
        await msg.channel.send(
            "Ludus Mancala agitandus est. Dic __`$intersim`__ ut ludo intersis."
        )
        if await app_box.app.joinGame(bot, msg, isRobot=True) == 1:
            await mcl.aiReceiveSemaphore(app_box.app, msg)
    else:
        await msg.channel.send(
            "Ludus Mancala agitandus est. Dic __`$intersim`__ ut ludo intersis, aut __`$interes`__ ut me ad ludum invites."
        )
    if 'L' in cmd.opts:
        await msg.channel.send("come")


async def joinMancala(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0)
    except BaseException as e:
        raise e

    if await app_box.app.joinGame(msg.author, msg) == 1:
        await mcl.aiReceiveSemaphore(app_box.app, msg)


async def callBotToMancala(cmd: Command, msg, bot):
    try:
        checkCmdFormat(cmd, 0)
    except BaseException as e:
        raise e

    if bot in app_box.app.users:
        await msg.channel.send("Jam ludo intersim.")
    elif await app_box.app.joinGame(bot, msg, isRobot=True) == 1:
        await mcl.aiReceiveSemaphore(app_box.app, msg)


async def operateMancala(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 1)
    except BaseException as e:
        raise e

    if app_box.app.users[app_box.app.nowUser] == msg.author:
        if len(app_box.app.users) == 2:
            try:
                rs = await app_box.app.runRoutine(msg, int(cmd.args[0]))
                print("mv", rs)
                if rs == 0:
                    app_box.delApp()
                elif rs == 1:
                    await mcl.aiReceiveSemaphore(app_box.app, msg)
            except BaseException as e:
                await msg.channel.send("ERROR.")
                print(e)
        else:
            await msg.channel.send("Nondum praesto sunt lusores.")


async def runConnectFour(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0)
    except BaseException as e:
        raise e

    app_box.setApp(con4.ConFourBoard())
    await msg.channel.send(
        "Ludus Con4 agitandus est. Dic __`$intersim`__ ut ludo intersis.")


async def joinConnectFour(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0)
    except BaseException as e:
        raise e

    if len(app_box.app.users) < 2:
        app_box.app.users.append(msg.author)
        await msg.channel.send("Ludo Con4 interes.")
        if len(app_box.app.users) == 2:
            await msg.channel.send("Ludus Con4 agitatus est.")
            await msg.channel.send(str(app_box.app))
    else:
        await msg.channel.send("Jam duo lusores intersunt.")


async def operateConnectFour(cmd: Command, msg):
    if app_box.app.users[app_box.app.nowUser] == msg.author:
        if len(app_box.app.users) == 2:
            try:
                rs = await app_box.app.runRoutine(msg, int(cmd.args[0]))
                if rs == 0:
                    app_box.delApp()
            except:
                await msg.channel.send("ERROR.")
        else:
            await msg.channel.send("Nondum praesto sunt lusores.")


async def endApp(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 0)
    except BaseException as e:
        raise e

    try:
        appName = app_box.app.getName()
    except:
        appName = ""
    app.cleanApp(app_box)
    await msg.channel.send("Ludus {} desitus est.".format(appName))


async def autoCleanApp():
    app.cleanApp(app_box, isAuto=True)


async def imitateMi(cmd: Command, msg):
    try:
        checkCmdFormat(cmd, 1)
    except BaseException as e:
        raise e

    await msg.channel.send(miModel(cmd.args[0]))


pass