# -*- coding: utf-8 -*-

from .hbo_now import HBONow as _HBONow
from .hbo_max import HBOMax as _HBOMax
from .bahamute_anime import BahamuteAnime as _BahamuteAnime
from .bilibili import BilibiliHKMOTW as _BilibiliHKMOTW
from .bilibili import BilibiliTWOnly as _BilibiliTWOnly
from .abematv import AbemaTV as _AbemaTV
from .cygames import PCRJP as _PCRJP, UmaJP as _UmaJP
from .kadokawa import KanColle as _KanColle
from .bbc import BBC as _BBC
from .netflix import NetflixSelenium as _NetflixSelenium, NetflixV2 as _NetflixV2
from .dazn import Dazn as _Dazn
from .hulu import HuluJP as _HuluJP
from .disney_plus import DisneyPlus as _DisneyPlus
from .viu_com import ViuCom as _ViuCom
from .tver_jp import TVerJP as _TVerJP
from .line_tv import LineTV as _LineTV
from .abc import ABCCom as _ABCCom
from .mytvsuper import MyTVSuper as _MyTVSuper
from .paravi import Paravi as _Paravi
from .niconico import Niconico as _Niconico

Medias = {
    "HBO Now": _HBONow,
    "HBO Max": _HBOMax,
    "Bahamute Anime": _BahamuteAnime,
    "Bilibili HK/MO/TW": _BilibiliHKMOTW,
    "Bilibili TW Only": _BilibiliTWOnly,
    "AbemaTV": _AbemaTV,
    "PCR JP": _PCRJP,
    "UMA JP": _UmaJP,
    "KanColle": _KanColle,
    "BBC": _BBC,
    "Netflix": _NetflixV2,
    "Netflix Selenium": _NetflixSelenium,
    "Dazn": _Dazn,
    "Hulu JP": _HuluJP,
    "Disney Plus": _DisneyPlus,
    "Viu.com": _ViuCom,
    "TVer JP": _TVerJP,
    "Line TV": _LineTV,
    "ABC": _ABCCom,
    "MyTVSuper": _MyTVSuper,
    "Paravi": _Paravi,
    "Niconico": _Niconico
}
