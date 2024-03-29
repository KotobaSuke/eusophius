from math import log

def scoring(info: dict):
    like = info["like"]
    view = info["view"]
    dm = info["danmaku"]
    coin = info["coin"]
    fav = info["favorite"]
    share = info["share"]
    if view == 0: return 0
    else:
        scale = lambda x: log(x) * 25
        return scale(like * (1 + 0.1 * (fav / 5 + dm + share / 5 + coin / 2)) / (view**0.5))


def formatVideoInfo(info: dict):
    return '\n'.join([
        "__{}__ ({} / av{})".format(info["title"], info["bvid"], info["aid"]),
        ":link: **Nexus**: https://www.bilibili.com/video/{}".format(
            info["bvid"]),
        ":pencil: **Auctor**: {}".format(info["owner"]["name"]),
        ":arrow_forward: **Visa**: {}".format(info["stat"]["view"]),
        ":satellite: **Danmaku**: {}".format(info["stat"]["danmaku"]),
        ":speech_balloon: **Responsa**: {}".format(info["stat"]["reply"]),
        ":+1: **Approbata**: {}".format(info["stat"]["like"]),
        ":coin: **Nummi**: {}".format(info["stat"]["coin"]),
        ":star: **Collecta**: {}".format(info["stat"]["favorite"]),
        ":loudspeaker: **Consociata**: {}".format(info["stat"]["share"]),
        ":triangular_ruler: **Ratio**: {:.2f}".format(scoring(info["stat"]))
    ])
