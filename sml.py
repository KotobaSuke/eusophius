import asyncio
from bilibili_api import user, video, Credential
from bili_video import scoring

CRED = Credential(sessdata="dd8cf581%2C1725339251%2C7d71e%2A31CjBWUfA_zm4zZTS3SdUU6m7benh4DrJZyM4tP3kjhadC6QLf4sd5pxDMvo5pNBBphhcSVkhsMy1xQ2dmanQzeTVabUd5bXI0SzNDZ1BoZmJDUEtsTXdvU0dnR3RxWHpic0tabEJFbjR6ay1RS2ZVY3BkOGhlc2ltWGVNekR2RnB3SC1RT0F3enJnIIEC", bili_jct="57e21ed07913a21089cf868d7108f963", buvid3="464E723E-A0A4-B2B5-6829-4E92162A9D8C42908infoc")


def monospace(text: str):
    mapping = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿")
    return text.translate(mapping)


class Member():

    def __init__(self, uid, head, translate_table=None):
        self.uid = uid
        self.head = head
        self.translate_table = translate_table
        self.videos = dict()

    def extractCodename(self, title):
        codename_begin = title.find(self.head) + len(self.head)
        codename_end = min(title.find('】', codename_begin),
                           title.find(' ', codename_begin))
        codename = title[codename_begin:codename_end]
        if self.translate_table != None:
            codename = codename.translate(self.translate_table)
        return codename

    async def update(self):
        u = user.User(self.uid, credential=CRED)
        resp = await u.get_videos()
        videos = resp["list"]["vlist"]
        self.videos.clear()
        for video in filter(lambda v: self.head in v["title"], videos):
            codename = self.extractCodename(video["title"])
            bvid = video["bvid"]
            self.videos[codename] = bvid


CHRONYETE = Member(12037123, "ce #")
KOTOBA = Member(
    5088042, "𝙺𝚃 #",
    str.maketrans("𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
                  "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))


async def updateAll():
    await CHRONYETE.update()
    await KOTOBA.update()


async def query(codename):
    u = None
    if codename[0:1].isupper():
        u = KOTOBA
    else:
        u = CHRONYETE
    if not codename in u.videos:
        await updateAll()
    return u.videos[codename]


async def getDataList(mode: str, range: str, isMixed: bool, isReversed: bool):
    lines = []
    videos = {KOTOBA: [], CHRONYETE: []}
    ordering = "NAVR"
    genitives = {KOTOBA: "Kotobae Trilii", CHRONYETE: "Chronyetae"}
    
    for m in [KOTOBA, CHRONYETE]:
        for code, bv in m.videos.items():
            if (not range) or (range == "#k" and m == KOTOBA) or (range == "#c" and m == CHRONYETE) or (not range.startswith('#') and code[0] in range):
                vd = video.Video(bvid="{}".format(bv))
                info = await vd.get_info()
                like = info["stat"]["like"]
                view = info["stat"]["view"]
                score = scoring(info["stat"])
                videos[m].append((code, like, view, score))
        if not isMixed:
            if videos[m]:
                if lines:
                    lines.append("——————————")
                lines.append("**{}:**".format(genitives[m]))
            videos[m] = sorted(videos[m], key=lambda x: x[ordering.find(mode)], reverse=((mode == 'N') == isReversed))
            lines += arrange(videos[m])
    if isMixed:
        lines.append("**Societatis Musicae Lagrammatis:**")
        mixList = videos[KOTOBA] + videos[CHRONYETE]
        mixList = sorted(mixList, key=lambda x: x[ordering.find(mode)], reverse=((mode == 'N') == isReversed))
        lines += arrange(mixList)
    
    if lines:
        return '\n'.join(lines)
    else:
        return "*nihil*"

def arrange(dataList: list[tuple[str, int, int, float]]):
    rs = []
    tformat = lambda rc: monospace("{}:    {} / {}    ⇒ {:.2f}".format(*rc))
    
    for rc in dataList:
        text = tformat(rc)
        rs.append(text)
    return rs