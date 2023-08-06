# coding: UTF-8
import sys
bstack1ll1_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack1l1_opy_ (bstack11l_opy_):
    global bstack1ll_opy_
    stringNr = ord (bstack11l_opy_ [-1])
    bstack111_opy_ = bstack11l_opy_ [:-1]
    bstack1_opy_ = stringNr % len (bstack111_opy_)
    bstack1l_opy_ = bstack111_opy_ [:bstack1_opy_] + bstack111_opy_ [bstack1_opy_:]
    if bstack1ll1_opy_:
        bstack1l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack1lll_opy_ + stringNr) % bstackl_opy_) for bstack1lll_opy_, char in enumerate (bstack1l_opy_)])
    else:
        bstack1l1l_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack1lll_opy_ + stringNr) % bstackl_opy_) for bstack1lll_opy_, char in enumerate (bstack1l_opy_)])
    return eval (bstack1l1l_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack111l11l1_opy_ = {
	bstack1l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstack1l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstack1l1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstack1l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstack1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstack1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstack1l1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstack1l1_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstack1l1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstack1l1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstack1l1_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstack1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstack1l1_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstack1l1_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstack1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstack1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstack1l1_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstack1l1_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstack1l1_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstack1l1_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstack1l1_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstack1l1_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstack1l1_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstack1l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstack1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstack1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstack1l1_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstack1l1_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstack1l1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstack1l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstack1l1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstack1l1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstack1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack11llll1l_opy_ = [
  bstack1l1_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstack1l1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstack1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstack1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstack1l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstack1l1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack11ll111l_opy_ = {
  bstack1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstack1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstack1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstack1l1_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstack1l1_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstack1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack11l1llll1_opy_ = {
  bstack1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstack1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstack1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstack1l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstack1l1_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstack1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstack1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack1l1l1ll1l_opy_ = {
  bstack1l1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstack1l1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstack1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstack1l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstack1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstack1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstack1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstack1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstack1l1_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstack1l1_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstack1l1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstack1l1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack1lll1ll11_opy_ = [
  bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstack1l1_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstack1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstack1l1_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstack1l1_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstack1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstack1l1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstack1l1_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstack1l1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack11111l11_opy_ = [
  bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstack1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstack1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstack1l1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstack1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack1l1l1111l_opy_ = [
  bstack1l1_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstack1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstack1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstack1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstack1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstack1l1_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstack1l1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstack1l1_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstack1l1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstack1l1_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstack1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstack1l1_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstack1l1_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstack1l1_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstack1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstack1l1_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstack1l1_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstack1l1_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstack1l1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstack1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstack1l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstack1l1_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstack1l1_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstack1l1_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstack1l1_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstack1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstack1l1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstack1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstack1l1_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstack1l1_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstack1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstack1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstack1l1_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstack1l1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstack1l1_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstack1l1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstack1l1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstack1l1_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstack1l1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstack1l1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstack1l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstack1l1_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstack1l1_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstack1l1_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstack1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstack1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstack1l1_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstack1l1_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstack1l1_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstack1l1_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstack1l1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstack1l1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstack1l1_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstack1l1_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstack1l1_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstack1l1_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstack1l1_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstack1l1_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstack1l1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstack1l1_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstack1l1_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstack1l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstack1l1_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstack1l1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstack1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstack1l1_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstack1l1_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstack1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstack1l1_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstack1l1_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstack1l1_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstack1l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstack1l1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstack1l1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstack1l1_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstack1l1_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstack1l1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstack1l1_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstack1l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstack1l1_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstack1l1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstack1l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstack1l1_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstack1l1_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstack1l1_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstack1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstack1l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstack1l1_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstack1l1_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstack1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstack1l1_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstack1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstack1l1_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1l111111l_opy_ = {
  bstack1l1_opy_ (u"࠭ࡶࠨच"): bstack1l1_opy_ (u"ࠧࡷࠩछ"),
  bstack1l1_opy_ (u"ࠨࡨࠪज"): bstack1l1_opy_ (u"ࠩࡩࠫझ"),
  bstack1l1_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstack1l1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstack1l1_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstack1l1_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstack1l1_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstack1l1_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstack1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstack1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstack1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstack1l1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstack1l1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstack1l1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstack1l1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstack1l1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstack1l1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstack1l1_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstack1l1_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstack1l1_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstack1l1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstack1l1_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstack1l1_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstack1l1_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstack1l1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstack1l1_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstack1l1_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack11lll11l_opy_ = bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack11ll1lll1_opy_ = bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack1l1111l1l_opy_ = bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack111l111l_opy_ = {
  bstack1l1_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstack1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstack1l1_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstack1l1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstack1l1_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack1ll11_opy_ = bstack111l111l_opy_[bstack1l1_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack11lll111_opy_ = bstack1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack1llll11l_opy_ = bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack111ll1l_opy_ = bstack1l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1lllll111_opy_ = bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack111l1_opy_ = [bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstack1l1_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack1l1l11ll1_opy_ = [bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstack1l1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack11l1111l1_opy_ = [
  bstack1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstack1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstack1l1_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstack1l1_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstack1l1_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstack1l1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstack1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstack1l1_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstack1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstack1l1_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstack1l1_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstack1l1_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstack1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstack1l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstack1l1_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstack1l1_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstack1l1_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstack1l1_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstack1l1_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstack1l1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstack1l1_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstack1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstack1l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstack1l1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstack1l1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstack1l1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstack1l1_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstack1l1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstack1l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstack1l1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstack1l1_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstack1l1_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstack1l1_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstack1l1_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstack1l1_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstack1l1_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstack1l1_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstack1l1_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstack1l1_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstack1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstack1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstack1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstack1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstack1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstack1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstack1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstack1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstack1l1_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstack1l1_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstack1l1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstack1l1_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstack1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstack1l1_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstack1l1_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstack1l1_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstack1l1_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstack1l1_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstack1l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstack1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstack1l1_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstack1l1_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstack1l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstack1l1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstack1l1_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstack1l1_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstack1l1_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstack1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstack1l1_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstack1l1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstack1l1_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstack1l1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstack1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstack1l1_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstack1l1_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstack1l1_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstack1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstack1l1_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstack1l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstack1l1_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstack1l1_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstack1l1_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstack1l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstack1l1_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstack1l1_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstack1l1_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstack1l1_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstack1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstack1l1_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstack1l1_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstack1l1_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstack1l1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstack1l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstack1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstack1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstack1l1_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstack1l1_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstack1l1_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstack1l1_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstack1l1_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstack1l1_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstack1l1_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstack1l1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstack1l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstack1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstack1l1_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstack1l1_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstack1l1_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstack1l1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstack1l1_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstack1l1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstack1l1_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstack1l1_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstack1l1_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstack1l1_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstack1l1_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstack1l1_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstack1l1_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstack1l1_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstack1l1_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstack1l1_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstack1l1_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstack1l1_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstack1l1_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstack1l1_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstack1l1_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstack1l1_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstack1l1_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstack1l1_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstack1l1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstack1l1_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstack1l1_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstack1l1_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstack1l1_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstack1l1_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstack1l1_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstack1l1_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstack1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstack1l1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstack1l1_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstack1l1_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstack1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstack1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstack1l1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack11lll1_opy_ = bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack1lll1l1l_opy_ = [bstack1l1_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstack1l1_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstack1l1_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack1l1l11l_opy_ = [bstack1l1_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstack1l1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstack1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstack1l1_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack11ll1l_opy_ = {
  bstack1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstack1l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstack1l1_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstack1l1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstack1l1_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstack1l1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstack1l1_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstack1l1_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstack1l1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstack1l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack1l1111_opy_ = [
  bstack1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstack1l1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstack1l1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstack1l1_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstack1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack1l11ll11l_opy_ = bstack11111l11_opy_ + bstack1l1l1111l_opy_ + bstack11l1111l1_opy_
bstack11111lll_opy_ = [
  bstack1l1_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstack1l1_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstack1l1_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstack1l1_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstack1l1_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstack1l1_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstack1l1_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstack1l1_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack11l1ll1_opy_ = bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack11l11l11l_opy_ = bstack1l1_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack1llll1l1l_opy_ = [ bstack1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack1l11ll111_opy_ = [ bstack1l1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack1ll1l111l_opy_ = [ bstack1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack11ll1ll11_opy_ = bstack1l1_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack11ll1l11_opy_ = bstack1l1_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack111111l1_opy_ = bstack1l1_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack1lll1l1l1_opy_ = bstack1l1_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack11l1llll_opy_ = [
  bstack1l1_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstack1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstack1l1_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstack1l1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstack1l1_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstack1l1_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstack1l1_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstack1l1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstack1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstack1l1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstack1l1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstack1l1_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstack1l1_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstack1l1_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstack1l1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstack1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstack1l1_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstack1l1_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstack1l1_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstack1l1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstack1l1_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
bstack1l1l11l11_opy_ = bstack1l1_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧਧ")
def bstack1ll1ll1ll_opy_():
  global CONFIG
  headers = {
        bstack1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩਨ"): bstack1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ਩"),
      }
  proxies = bstack1lllll_opy_(CONFIG, bstack1l1111l1l_opy_)
  try:
    response = requests.get(bstack1l1111l1l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11ll1l1l1_opy_ = response.json()[bstack1l1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪਪ")]
      logger.debug(bstack111lll1l_opy_.format(response.json()))
      return bstack11ll1l1l1_opy_
    else:
      logger.debug(bstack1ll11ll1l_opy_.format(bstack1l1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧਫ")))
  except Exception as e:
    logger.debug(bstack1ll11ll1l_opy_.format(e))
def bstack1ll11l11l_opy_(hub_url):
  global CONFIG
  url = bstack1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤਬ")+  hub_url + bstack1l1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣਭ")
  headers = {
        bstack1l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨਮ"): bstack1l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ਯ"),
      }
  proxies = bstack1lllll_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l111l1l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1lll11ll1_opy_.format(hub_url, e))
def bstack1ll11l11_opy_():
  try:
    global bstack1llll1lll_opy_
    bstack11ll1l1l1_opy_ = bstack1ll1ll1ll_opy_()
    bstack11l11l1l_opy_ = []
    results = []
    for bstack1lll1_opy_ in bstack11ll1l1l1_opy_:
      bstack11l11l1l_opy_.append(bstack11l1l1l1_opy_(target=bstack1ll11l11l_opy_,args=(bstack1lll1_opy_,)))
    for t in bstack11l11l1l_opy_:
      t.start()
    for t in bstack11l11l1l_opy_:
      results.append(t.join())
    bstack1l111l11l_opy_ = {}
    for item in results:
      hub_url = item[bstack1l1_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬਰ")]
      latency = item[bstack1l1_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭਱")]
      bstack1l111l11l_opy_[hub_url] = latency
    bstack1ll1l1l1l_opy_ = min(bstack1l111l11l_opy_, key= lambda x: bstack1l111l11l_opy_[x])
    bstack1llll1lll_opy_ = bstack1ll1l1l1l_opy_
    logger.debug(bstack1ll1llll1_opy_.format(bstack1ll1l1l1l_opy_))
  except Exception as e:
    logger.debug(bstack111l1l1l_opy_.format(e))
bstack11l1l111l_opy_ = bstack1l1_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࡿࢂ࠭ਲ")
bstack1l1ll1l11_opy_ = bstack1l1_opy_ (u"ࠧࡄࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡷࡪࡺࡵࡱࠣࠪਲ਼")
bstack1l11lll_opy_ = bstack1l1_opy_ (u"ࠨࡒࡤࡶࡸ࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪ਴")
bstack1l111ll11_opy_ = bstack1l1_opy_ (u"ࠩࡖࡥࡳ࡯ࡴࡪࡼࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧਵ")
bstack1l1lll1l_opy_ = bstack1l1_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧਸ਼")
bstack1l1ll_opy_ = bstack1l1_opy_ (u"ࠫࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࡽࢀࠫ਷")
bstack11lllllll_opy_ = bstack1l1_opy_ (u"ࠬࡘࡥࡤࡧ࡬ࡺࡪࡪࠠࡪࡰࡷࡩࡷࡸࡵࡱࡶ࠯ࠤࡪࡾࡩࡵ࡫ࡱ࡫ࠬਸ")
bstack1lll11lll_opy_ = bstack1l1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫਹ")
bstack1l111ll1l_opy_ = bstack1l1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡣࡱࡨࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬ਺")
bstack1ll11ll11_opy_ = bstack1l1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡵࡳࡧࡵࡴ࠭ࠢࡳࡥࡧࡵࡴࠡࡣࡱࡨࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡬ࡪࡤࡵࡥࡷࡿࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡷࡳࠥࡸࡵ࡯ࠢࡵࡳࡧࡵࡴࠡࡶࡨࡷࡹࡹࠠࡪࡰࠣࡴࡦࡸࡡ࡭࡮ࡨࡰ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠭ࡱࡣࡥࡳࡹࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࡮࡬ࡦࡷࡧࡲࡺࡢࠪ਻")
bstack1l1l1_opy_ = bstack1l1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡦࡪ࡮ࡡࡷࡧࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡥࡩ࡭ࡧࡶࡦࡢ਼ࠪ")
bstack111l1ll1_opy_ = bstack1l1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡦࡶࡰࡪࡷࡰ࠱ࡨࡲࡩࡦࡰࡷࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡅࡵࡶࡩࡶ࡯࠰ࡔࡾࡺࡨࡰࡰ࠰ࡇࡱ࡯ࡥ࡯ࡶࡣࠫ਽")
bstack11111_opy_ = bstack1l1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡥ࠭ਾ")
bstack1l1l1llll_opy_ = bstack1l1_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡨ࡬ࡲࡩࠦࡥࡪࡶ࡫ࡩࡷࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡱࡵࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡸࡦࡲ࡬ࠡࡶ࡫ࡩࠥࡸࡥ࡭ࡧࡹࡥࡳࡺࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡸࡷ࡮ࡴࡧࠡࡲ࡬ࡴࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠬਿ")
bstack1l11l1l1l_opy_ = bstack1l1_opy_ (u"࠭ࡈࡢࡰࡧࡰ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡰࡴࡹࡥࠨੀ")
bstack1ll1l1ll_opy_ = bstack1l1_opy_ (u"ࠧࡂ࡮࡯ࠤࡩࡵ࡮ࡦࠣࠪੁ")
bstack1ll11l1ll_opy_ = bstack1l1_opy_ (u"ࠨࡅࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࠠࡢࡶࠣࡥࡳࡿࠠࡱࡣࡵࡩࡳࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡳ࡫ࠦࠢࡼࡿࠥ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡤ࡮ࡸࡨࡪࠦࡡࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠡࡨ࡬ࡰࡪࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡵࡧࡶࡸࡸ࠴ࠧੂ")
bstack1ll1lll1l_opy_ = bstack1l1_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡵࡩࡩ࡫࡮ࡵ࡫ࡤࡰࡸࠦ࡮ࡰࡶࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡸ࡭࡫࡭ࠡ࡫ࡱࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩࠥࡧࡳࠡࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦࠥࡧ࡮ࡥࠢࠥࡥࡨࡩࡥࡴࡵࡎࡩࡾࠨࠠࡰࡴࠣࡷࡪࡺࠠࡵࡪࡨࡱࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠼ࠣࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧࠦࡡ࡯ࡦࠣࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠢࠨ੃")
bstack1l1l1ll1_opy_ = bstack1l1_opy_ (u"ࠪࡑࡦࡲࡦࡰࡴࡰࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠧࢁࡽࠣࠩ੄")
bstack1l11l11ll_opy_ = bstack1l1_opy_ (u"ࠫࡊࡴࡣࡰࡷࡱࡸࡪࡸࡥࡥࠢࡨࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࠤ࠲ࠦࡻࡾࠩ੅")
bstack111llll11_opy_ = bstack1l1_opy_ (u"࡙ࠬࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰࠬ੆")
bstack11ll11_opy_ = bstack1l1_opy_ (u"࠭ࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱ࠭ੇ")
bstack1l1111111_opy_ = bstack1l1_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰࠥ࡯ࡳࠡࡰࡲࡻࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠧࠧੈ")
bstack111l1111_opy_ = bstack1l1_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࠣࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡏࡳࡨࡧ࡬࠻ࠢࡾࢁࠬ੉")
bstack11l1lllll_opy_ = bstack1l1_opy_ (u"ࠩࡖࡸࡦࡸࡴࡪࡰࡪࠤࡱࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡻ࡮ࡺࡨࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࡿࢂ࠭੊")
bstack1l1ll11ll_opy_ = bstack1l1_opy_ (u"࡙ࠪࡵࡪࡡࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠫੋ")
bstack1ll1l111_opy_ = bstack1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠪੌ")
bstack1l11l1lll_opy_ = bstack1l1_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࠦࡡ࡯ࠢࡤࡴࡵࡸ࡯ࡱࡴ࡬ࡥࡹ࡫ࠠࡇ࡙ࠣࠬࡷࡵࡢࡰࡶ࠲ࡴࡦࡨ࡯ࡵࠫࠣ࡭ࡳࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠰ࠥࡹ࡫ࡪࡲࠣࡸ࡭࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡯ࡪࡿࠠࡪࡰࠣࡧࡴࡴࡦࡪࡩࠣ࡭࡫ࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡴ࡫ࡰࡴࡱ࡫ࠠࡱࡻࡷ࡬ࡴࡴࠠࡴࡥࡵ࡭ࡵࡺࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡣࡱࡽࠥࡌࡗ࠯੍ࠩ")
bstack1l11111ll_opy_ = bstack1l1_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡩࡶࡷࡴࡕࡸ࡯ࡹࡻ࠲࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠠࡪࡵࠣࡲࡴࡺࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡳࡳࠦࡣࡶࡴࡵࡩࡳࡺ࡬ࡺࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࡯ࡧࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤ࠭ࢁࡽࠪ࠮ࠣࡴࡱ࡫ࡡࡴࡧࠣࡹࡵ࡭ࡲࡢࡦࡨࠤࡹࡵࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࡀࡀ࠸࠳࠶࠮࠱ࠢࡲࡶࠥࡸࡥࡧࡧࡵࠤࡹࡵࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡰࡪࡴࡩࡶ࡯࠲ࡶࡺࡴ࠭ࡵࡧࡶࡸࡸ࠳ࡢࡦࡪ࡬ࡲࡩ࠳ࡰࡳࡱࡻࡽࠨࡶࡹࡵࡪࡲࡲࠥ࡬࡯ࡳࠢࡤࠤࡼࡵࡲ࡬ࡣࡵࡳࡺࡴࡤ࠯ࠩ੎")
bstack1ll1ll1l_opy_ = bstack1l1_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡽࡲࡲࠠࡧ࡫࡯ࡩ࠳࠴ࠧ੏")
bstack1l11l1l_opy_ = bstack1l1_opy_ (u"ࠨࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡨࡧࡱࡩࡷࡧࡴࡦࡦࠣࡸ࡭࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠦ࠭੐")
bstack1ll11l1l1_opy_ = bstack1l1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥ࠯ࠢࡾࢁࠬੑ")
bstack11l1l1l_opy_ = bstack1l1_opy_ (u"ࠪࡉࡽࡶࡥࡤࡶࡨࡨࠥࡧࡴࠡ࡮ࡨࡥࡸࡺࠠ࠲ࠢ࡬ࡲࡵࡻࡴ࠭ࠢࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࠵࠭੒")
bstack1ll11lll_opy_ = bstack1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡨࡺࡸࡩ࡯ࡩࠣࡅࡵࡶࠠࡶࡲ࡯ࡳࡦࡪ࠮ࠡࡽࢀࠫ੓")
bstack11l1l_opy_ = bstack1l1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡰࡴࡧࡤࠡࡃࡳࡴ࠳ࠦࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࢁࡽ࠯ࠩ੔")
bstack11l1111ll_opy_ = bstack1l1_opy_ (u"࠭ࡋࡦࡻࡶࠤࡨࡧ࡮࡯ࡱࡷࠤࡨࡵ࠭ࡦࡺ࡬ࡷࡹࠦࡡࡴࠢࡤࡴࡵࠦࡶࡢ࡮ࡸࡩࡸ࠲ࠠࡶࡵࡨࠤࡦࡴࡹࠡࡱࡱࡩࠥࡶࡲࡰࡲࡨࡶࡹࡿࠠࡧࡴࡲࡱࠥࢁࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡵࡧࡴࡩ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿ࡿ࠯ࠤࡴࡴ࡬ࡺࠢࠥࡴࡦࡺࡨࠣࠢࡤࡲࡩࠦࠢࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠥࠤࡨࡧ࡮ࠡࡥࡲ࠱ࡪࡾࡩࡴࡶࠣࡸࡴ࡭ࡥࡵࡪࡨࡶ࠳࠭੕")
bstack1llllll1_opy_ = bstack1l1_opy_ (u"ࠧ࡜ࡋࡱࡺࡦࡲࡩࡥࠢࡤࡴࡵࠦࡰࡳࡱࡳࡩࡷࡺࡹ࡞ࠢࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠢࡤࡶࡪࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠲ࠥࡌ࡯ࡳࠢࡰࡳࡷ࡫ࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡲ࡯ࡩࡦࡹࡥࠡࡸ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡱ࡫ࡸࡱ࠴ࡹࡥࡵ࠯ࡸࡴ࠲ࡺࡥࡴࡶࡶ࠳ࡸࡶࡥࡤ࡫ࡩࡽ࠲ࡧࡰࡱࠩ੖")
bstack11llllll1_opy_ = bstack1l1_opy_ (u"ࠨ࡝ࡌࡲࡻࡧ࡬ࡪࡦࠣࡥࡵࡶࠠࡱࡴࡲࡴࡪࡸࡴࡺ࡟ࠣࡗࡺࡶࡰࡰࡴࡷࡩࡩࠦࡶࡢ࡮ࡸࡩࡸࠦ࡯ࡧࠢࡤࡴࡵࠦࡡࡳࡧࠣࡳ࡫ࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠲ࠥࡌ࡯ࡳࠢࡰࡳࡷ࡫ࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡲ࡯ࡩࡦࡹࡥࠡࡸ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡱ࡫ࡸࡱ࠴ࡹࡥࡵ࠯ࡸࡴ࠲ࡺࡥࡴࡶࡶ࠳ࡸࡶࡥࡤ࡫ࡩࡽ࠲ࡧࡰࡱࠩ੗")
bstack111l1l_opy_ = bstack1l1_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡥࡵࡶࠠࡪࡦࠣࡿࢂࠦࡦࡰࡴࠣ࡬ࡦࡹࡨࠡ࠼ࠣࡿࢂ࠴ࠧ੘")
bstack1l1111l11_opy_ = bstack1l1_opy_ (u"ࠪࡅࡵࡶࠠࡖࡲ࡯ࡳࡦࡪࡥࡥࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠢࡌࡈࠥࡀࠠࡼࡿࠪਖ਼")
bstack1ll11lll1_opy_ = bstack1l1_opy_ (u"࡚ࠫࡹࡩ࡯ࡩࠣࡅࡵࡶࠠ࠻ࠢࡾࢁ࠳࠭ਗ਼")
bstack11ll1l111_opy_ = bstack1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡲࡶࠥࡼࡡ࡯࡫࡯ࡰࡦࠦࡰࡺࡶ࡫ࡳࡳࠦࡴࡦࡵࡷࡷ࠱ࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥࡶࡡࡳࡣ࡯ࡰࡪࡲࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠤࡂࠦ࠱ࠨਜ਼")
bstack11l11l1_opy_ = bstack1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࠿ࠦࡻࡾࠩੜ")
bstack1l111l1ll_opy_ = bstack1l1_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡧࡱࡵࡳࡦࠢࡥࡶࡴࡽࡳࡦࡴ࠽ࠤࢀࢃࠧ੝")
bstack1l1l111ll_opy_ = bstack1l1_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤ࡬࡫ࡴࠡࡴࡨࡥࡸࡵ࡮ࠡࡨࡲࡶࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫࠮ࠡࡽࢀࠫਫ਼")
bstack1ll1111_opy_ = bstack1l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡࡣࡳ࡭ࠥࡩࡡ࡭࡮࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ੟")
bstack111lll1_opy_ = bstack1l1_opy_ (u"࡙ࠪࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡩࡱࡺࠤࡧࡻࡩ࡭ࡦ࡙ࠣࡗࡒࠬࠡࡣࡶࠤࡧࡻࡩ࡭ࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠠࡪࡵࠣࡲࡴࡺࠠࡶࡵࡨࡨ࠳࠭੠")
bstack1l11l1l11_opy_ = bstack1l1_opy_ (u"ࠫࡘ࡫ࡲࡷࡧࡵࠤࡸ࡯ࡤࡦࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ࠭ࢁࡽࠪࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡥࡲ࡫ࠠࡢࡵࠣࡧࡱ࡯ࡥ࡯ࡶࠣࡷ࡮ࡪࡥࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠬࢀࢃࠩࠨ੡")
bstack1ll111l1_opy_ = bstack1l1_opy_ (u"ࠬ࡜ࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡲࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡩࡧࡳࡩࡤࡲࡥࡷࡪ࠺ࠡࡽࢀࠫ੢")
bstack1l1lll11_opy_ = bstack1l1_opy_ (u"࠭ࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡤࡧࡨ࡫ࡳࡴࠢࡤࠤࡵࡸࡩࡷࡣࡷࡩࠥࡪ࡯࡮ࡣ࡬ࡲ࠿ࠦࡻࡾࠢ࠱ࠤࡘ࡫ࡴࠡࡶ࡫ࡩࠥ࡬࡯࡭࡮ࡲࡻ࡮ࡴࡧࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡱࠤࡾࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠽ࠤࡡࡴ࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰ࠤࡡࡴࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯࠾ࠥࡺࡲࡶࡧࠣࡠࡳ࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯ࠪ੣")
bstack1l1l1l1l_opy_ = bstack1l1_opy_ (u"ࠧࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡪࡩࡹࡥ࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࡣࡪࡸࡲࡰࡴࠣ࠾ࠥࢁࡽࠨ੤")
bstack1l11ll1l_opy_ = bstack1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠࡣࡰࡴࡱ࡯ࡴࡶࡦࡨࡣࡪࡼࡥ࡯ࡶࠣࡪࡴࡸࠠࡔࡆࡎࡗࡪࡺࡵࡱࠢࡾࢁࠧ੥")
bstack11l11111_opy_ = bstack1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏ࡙࡫ࡳࡵࡃࡷࡸࡪࡳࡰࡵࡧࡧࠤࢀࢃࠢ੦")
bstack11l11ll_opy_ = bstack1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥ࡯ࡦࡢࡥࡲࡶ࡬ࡪࡶࡸࡨࡪࡥࡥࡷࡧࡱࡸࠥ࡬࡯ࡳࠢࡖࡈࡐ࡚ࡥࡴࡶࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠦࡻࡾࠤ੧")
bstack11111l1l_opy_ = bstack1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡴࡨࡣࡷ࡫ࡱࡶࡧࡶࡸࠥࢁࡽࠣ੨")
bstack111l11_opy_ = bstack1l1_opy_ (u"ࠧࡖࡏࡔࡖࠣࡉࡻ࡫࡮ࡵࠢࡾࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠ࠻ࠢࡾࢁࠧ੩")
bstack11lllll1l_opy_ = bstack1l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡶࡲࡰࡺࡼࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ੪")
bstack111lll1l_opy_ = bstack1l1_opy_ (u"ࠧࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠ࠰ࡰࡨࡼࡹࡥࡨࡶࡤࡶࠤࢀࢃࠧ੫")
bstack1ll11ll1l_opy_ = bstack1l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤ࠴ࡴࡥࡹࡶࡢ࡬ࡺࡨࡳ࠻ࠢࡾࢁࠬ੬")
bstack1ll1llll1_opy_ = bstack1l1_opy_ (u"ࠩࡑࡩࡦࡸࡥࡴࡶࠣ࡬ࡺࡨࠠࡢ࡮࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡸࡀࠠࡼࡿࠪ੭")
bstack111l1l1l_opy_ = bstack1l1_opy_ (u"ࠪࡉࡗࡘࡏࡓࠢࡌࡒࠥࡇࡌࡍࡑࡆࡅ࡙ࡋࠠࡉࡗࡅࠤࢀࢃࠧ੮")
bstack11l111l1l_opy_ = bstack1l1_opy_ (u"ࠫࡑࡧࡴࡦࡰࡦࡽࠥࡵࡦࠡࡪࡸࡦ࠿ࠦࡻࡾࠢ࡬ࡷ࠿ࠦࡻࡾࠩ੯")
bstack1lll11ll1_opy_ = bstack1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡ࡮ࡤࡸࡪࡴࡣࡺࠢࡩࡳࡷࠦࡻࡾࠢ࡫ࡹࡧࡀࠠࡼࡿࠪੰ")
bstack11l11ll1_opy_ = bstack1l1_opy_ (u"࠭ࡈࡶࡤࠣࡹࡷࡲࠠࡤࡪࡤࡲ࡬࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡱࡳࡸ࡮ࡳࡡ࡭ࠢ࡫ࡹࡧࡀࠠࡼࡿࠪੱ")
bstack1ll1lll11_opy_ = bstack1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡳࡵࡺࡩ࡮ࡣ࡯ࠤ࡭ࡻࡢࠡࡷࡵࡰ࠿ࠦࡻࡾࠩੲ")
bstack11l11ll1l_opy_ = bstack1l1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡯࡭ࡸࡺࡳ࠻ࠢࡾࢁࠬੳ")
bstack1lll1llll_opy_ = bstack1l1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳ࠻ࠢࡾࢁࠬੴ")
bstack1l11111l_opy_ = bstack1l1_opy_ (u"࡙ࠪࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡶࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡼࡿ࠱ࠤࡊࡸࡲࡰࡴࠣ࠱ࠥࢁࡽࠨੵ")
bstack1l1l1l111_opy_ = bstack1l1_opy_ (u"ࠫࠥࠦ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࠤࠥ࡯ࡦࠩࡲࡤ࡫ࡪࠦ࠽࠾࠿ࠣࡺࡴ࡯ࡤࠡ࠲ࠬࠤࢀࡢ࡮ࠡࠢࠣࡸࡷࡿࡻ࡝ࡰࠣࡧࡴࡴࡳࡵࠢࡩࡷࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩ࡞ࠪࡪࡸࡢࠧࠪ࠽࡟ࡲࠥࠦࠠࠡࠢࡩࡷ࠳ࡧࡰࡱࡧࡱࡨࡋ࡯࡬ࡦࡕࡼࡲࡨ࠮ࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫࠰ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡰࡠ࡫ࡱࡨࡪࡾࠩࠡ࠭ࠣࠦ࠿ࠨࠠࠬࠢࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࠩࡣࡺࡥ࡮ࡺࠠ࡯ࡧࡺࡔࡦ࡭ࡥ࠳࠰ࡨࡺࡦࡲࡵࡢࡶࡨࠬࠧ࠮ࠩࠡ࠿ࡁࠤࢀࢃࠢ࠭ࠢ࡟ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦ࡬࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡧࡷࡥ࡮ࡲࡳࠣࡿ࡟ࠫ࠮࠯ࠩ࡜ࠤ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠧࡣࠩࠡ࠭ࠣࠦ࠱ࡢ࡜࡯ࠤࠬࡠࡳࠦࠠࠡࠢࢀࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࢁ࡜࡯ࠢࠣࠤࠥࢃ࡜࡯ࠢࠣࢁࡡࡴࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠫ੶")
bstack111l_opy_ = bstack1l1_opy_ (u"ࠬࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡴࡦࡺࡨࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷ࡢࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡳࡣ࡮ࡴࡤࡦࡺࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠸࡝࡝ࡰࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰ࡶࡰ࡮ࡩࡥࠩ࠲࠯ࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹ࠩ࡝ࡰࡦࡳࡳࡹࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࠪ࠽࡟ࡲ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡱࡧࡵ࡯ࡥ࡫ࠤࡂࠦࡡࡴࡻࡱࡧࠥ࠮࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸ࠯ࠠ࠾ࡀࠣࡿࡡࡴ࡬ࡦࡶࠣࡧࡦࡶࡳ࠼࡞ࡱࡸࡷࡿࠠࡼ࡞ࡱࡧࡦࡶࡳࠡ࠿ࠣࡎࡘࡕࡎ࠯ࡲࡤࡶࡸ࡫ࠨࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷ࠮ࡢ࡮ࠡࠢࢀࠤࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࠠࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࡸࡥࡵࡷࡵࡲࠥࡧࡷࡢ࡫ࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬࠰ࡦ࡬ࡷࡵ࡭ࡪࡷࡰ࠲ࡨࡵ࡮࡯ࡧࡦࡸ࠭ࢁ࡜࡯ࠢࠣࠤࠥࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ࠼ࠣࡤࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂࠪࡻࡦࡰࡦࡳࡩ࡫ࡕࡓࡋࡆࡳࡲࡶ࡯࡯ࡧࡱࡸ࠭ࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡣࡢࡲࡶ࠭࠮ࢃࡠ࠭࡞ࡱࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵ࡟ࡲࠥࠦࡽࠪ࡞ࡱࢁࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࠫ੷")
from ._version import __version__
bstack1l1l111l_opy_ = None
CONFIG = {}
bstack11llll1l1_opy_ = {}
bstack111111_opy_ = {}
bstack1l11lll1_opy_ = None
bstack1l1ll1l1l_opy_ = None
bstack11llll11l_opy_ = None
bstack11111111_opy_ = -1
bstack11l1l11_opy_ = bstack1ll11_opy_
bstack1l11l11_opy_ = 1
bstack11l111111_opy_ = False
bstack1ll1l1ll1_opy_ = False
bstack1111l11_opy_ = bstack1l1_opy_ (u"࠭ࠧ੸")
bstack1llllll11_opy_ = bstack1l1_opy_ (u"ࠧࠨ੹")
bstack1111l1l1_opy_ = False
bstack11ll1lll_opy_ = True
bstack1lll1l11_opy_ = bstack1l1_opy_ (u"ࠨࠩ੺")
bstack1ll11l111_opy_ = []
bstack1llll1lll_opy_ = bstack1l1_opy_ (u"ࠩࠪ੻")
bstack11lllll_opy_ = False
bstack111111ll_opy_ = None
bstack1l1ll11_opy_ = -1
bstack1l1ll111_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠪࢂࠬ੼")), bstack1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੽"), bstack1l1_opy_ (u"ࠬ࠴ࡲࡰࡤࡲࡸ࠲ࡸࡥࡱࡱࡵࡸ࠲࡮ࡥ࡭ࡲࡨࡶ࠳ࡰࡳࡰࡰࠪ੾"))
bstack1l1lll_opy_ = []
bstack1lll1lll1_opy_ = False
bstack11ll_opy_ = None
bstack1lll1l_opy_ = None
bstack111llllll_opy_ = None
bstack11lll1ll_opy_ = None
bstack11ll1llll_opy_ = None
bstack11l111ll1_opy_ = None
bstack11l1ll11l_opy_ = None
bstack1llll1ll_opy_ = None
bstack111l1ll_opy_ = None
bstack1lllll11l_opy_ = None
bstack11llll_opy_ = None
bstack1l1l1ll_opy_ = None
bstack111llll_opy_ = None
bstack1ll111l1l_opy_ = None
bstack11111l_opy_ = None
bstack11l1lll_opy_ = bstack1l1_opy_ (u"ࠨࠢ੿")
class bstack11l1l1l1_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack11l1l1l1_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l1l11_opy_,
                    format=bstack1l1_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬ઀"),
                    datefmt=bstack1l1_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪઁ"))
def bstack1l11ll11_opy_():
  global CONFIG
  global bstack11l1l11_opy_
  if bstack1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫં") in CONFIG:
    bstack11l1l11_opy_ = bstack111l111l_opy_[CONFIG[bstack1l1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬઃ")]]
    logging.getLogger().setLevel(bstack11l1l11_opy_)
def bstack1l11l111l_opy_():
  global CONFIG
  global bstack1lll1lll1_opy_
  bstack11l11l_opy_ = bstack1l1ll1l_opy_(CONFIG)
  if(bstack1l1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭઄") in bstack11l11l_opy_ and str(bstack11l11l_opy_[bstack1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧઅ")]).lower() == bstack1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫઆ")):
    bstack1lll1lll1_opy_ = True
def bstack11lll1111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lllll1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111ll111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1_opy_ (u"ࠢ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡤࡱࡱࡪ࡮࡭ࡦࡪ࡮ࡨࠦઇ") == args[i].lower() or bstack1l1_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡳ࡬ࡩࡨࠤઈ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lll1l11_opy_
      bstack1lll1l11_opy_ += bstack1l1_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪࠦࠧઉ") + path
      return path
  return None
def bstack1lll111l_opy_():
  bstack11l1l11l1_opy_ = bstack111ll111_opy_()
  if bstack11l1l11l1_opy_ and os.path.exists(os.path.abspath(bstack11l1l11l1_opy_)):
    fileName = bstack11l1l11l1_opy_
  if bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧઊ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨઋ")])) and not bstack1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧઌ") in locals():
    fileName = os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪઍ")]
  if bstack1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩ઎") in locals():
    bstack1l111l11_opy_ = os.path.abspath(fileName)
  else:
    bstack1l111l11_opy_ = bstack1l1_opy_ (u"ࠨࠩએ")
  bstack11l1l1l11_opy_ = os.getcwd()
  bstack11l1l11l_opy_ = bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬઐ")
  bstack11lll11l1_opy_ = bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧઑ")
  while (not os.path.exists(bstack1l111l11_opy_)) and bstack11l1l1l11_opy_ != bstack1l1_opy_ (u"ࠦࠧ઒"):
    bstack1l111l11_opy_ = os.path.join(bstack11l1l1l11_opy_, bstack11l1l11l_opy_)
    if not os.path.exists(bstack1l111l11_opy_):
      bstack1l111l11_opy_ = os.path.join(bstack11l1l1l11_opy_, bstack11lll11l1_opy_)
    if bstack11l1l1l11_opy_ != os.path.dirname(bstack11l1l1l11_opy_):
      bstack11l1l1l11_opy_ = os.path.dirname(bstack11l1l1l11_opy_)
    else:
      bstack11l1l1l11_opy_ = bstack1l1_opy_ (u"ࠧࠨઓ")
  if not os.path.exists(bstack1l111l11_opy_):
    bstack11l111l11_opy_(
      bstack1ll11l1ll_opy_.format(os.getcwd()))
  with open(bstack1l111l11_opy_, bstack1l1_opy_ (u"࠭ࡲࠨઔ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack11l111l11_opy_(bstack1l1l1ll1_opy_.format(str(exc)))
def bstack11111ll1_opy_(config):
  bstack1lll1lll_opy_ = bstack1lll1ll1_opy_(config)
  for option in list(bstack1lll1lll_opy_):
    if option.lower() in bstack1l111111l_opy_ and option != bstack1l111111l_opy_[option.lower()]:
      bstack1lll1lll_opy_[bstack1l111111l_opy_[option.lower()]] = bstack1lll1lll_opy_[option]
      del bstack1lll1lll_opy_[option]
  return config
def bstack11ll11l_opy_():
  global bstack111111_opy_
  for key, bstack111l111_opy_ in bstack11ll111l_opy_.items():
    if isinstance(bstack111l111_opy_, list):
      for var in bstack111l111_opy_:
        if var in os.environ:
          bstack111111_opy_[key] = os.environ[var]
          break
    elif bstack111l111_opy_ in os.environ:
      bstack111111_opy_[key] = os.environ[bstack111l111_opy_]
  if bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩક") in os.environ:
    bstack111111_opy_[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬખ")] = {}
    bstack111111_opy_[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ગ")][bstack1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬઘ")] = os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ઙ")]
def bstack1111llll_opy_():
  global bstack11llll1l1_opy_
  global bstack1lll1l11_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack1l1_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨચ").lower() == val.lower():
      bstack11llll1l1_opy_[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪછ")] = {}
      bstack11llll1l1_opy_[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫજ")][bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪઝ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1lll1111_opy_ in bstack11l1llll1_opy_.items():
    if isinstance(bstack1lll1111_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lll1111_opy_:
          if idx<len(sys.argv) and bstack1l1_opy_ (u"ࠩ࠰࠱ࠬઞ") + var.lower() == val.lower() and not key in bstack11llll1l1_opy_:
            bstack11llll1l1_opy_[key] = sys.argv[idx+1]
            bstack1lll1l11_opy_ += bstack1l1_opy_ (u"ࠪࠤ࠲࠳ࠧટ") + var + bstack1l1_opy_ (u"ࠫࠥ࠭ઠ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack1l1_opy_ (u"ࠬ࠳࠭ࠨડ") + bstack1lll1111_opy_.lower() == val.lower() and not key in bstack11llll1l1_opy_:
          bstack11llll1l1_opy_[key] = sys.argv[idx+1]
          bstack1lll1l11_opy_ += bstack1l1_opy_ (u"࠭ࠠ࠮࠯ࠪઢ") + bstack1lll1111_opy_ + bstack1l1_opy_ (u"ࠧࠡࠩણ") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack11l1ll1l1_opy_(config):
  bstack1l1lllll_opy_ = config.keys()
  for bstack1l11ll1l1_opy_, bstack11l1l1111_opy_ in bstack111l11l1_opy_.items():
    if bstack11l1l1111_opy_ in bstack1l1lllll_opy_:
      config[bstack1l11ll1l1_opy_] = config[bstack11l1l1111_opy_]
      del config[bstack11l1l1111_opy_]
  for bstack1l11ll1l1_opy_, bstack11l1l1111_opy_ in bstack1l1l1ll1l_opy_.items():
    if isinstance(bstack11l1l1111_opy_, list):
      for bstack1l11l_opy_ in bstack11l1l1111_opy_:
        if bstack1l11l_opy_ in bstack1l1lllll_opy_:
          config[bstack1l11ll1l1_opy_] = config[bstack1l11l_opy_]
          del config[bstack1l11l_opy_]
          break
    elif bstack11l1l1111_opy_ in bstack1l1lllll_opy_:
        config[bstack1l11ll1l1_opy_] = config[bstack11l1l1111_opy_]
        del config[bstack11l1l1111_opy_]
  for bstack1l11l_opy_ in list(config):
    for bstack11lll1l1_opy_ in bstack1l11ll11l_opy_:
      if bstack1l11l_opy_.lower() == bstack11lll1l1_opy_.lower() and bstack1l11l_opy_ != bstack11lll1l1_opy_:
        config[bstack11lll1l1_opy_] = config[bstack1l11l_opy_]
        del config[bstack1l11l_opy_]
  bstack1111lll1_opy_ = []
  if bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫત") in config:
    bstack1111lll1_opy_ = config[bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬથ")]
  for platform in bstack1111lll1_opy_:
    for bstack1l11l_opy_ in list(platform):
      for bstack11lll1l1_opy_ in bstack1l11ll11l_opy_:
        if bstack1l11l_opy_.lower() == bstack11lll1l1_opy_.lower() and bstack1l11l_opy_ != bstack11lll1l1_opy_:
          platform[bstack11lll1l1_opy_] = platform[bstack1l11l_opy_]
          del platform[bstack1l11l_opy_]
  for bstack1l11ll1l1_opy_, bstack11l1l1111_opy_ in bstack1l1l1ll1l_opy_.items():
    for platform in bstack1111lll1_opy_:
      if isinstance(bstack11l1l1111_opy_, list):
        for bstack1l11l_opy_ in bstack11l1l1111_opy_:
          if bstack1l11l_opy_ in platform:
            platform[bstack1l11ll1l1_opy_] = platform[bstack1l11l_opy_]
            del platform[bstack1l11l_opy_]
            break
      elif bstack11l1l1111_opy_ in platform:
        platform[bstack1l11ll1l1_opy_] = platform[bstack11l1l1111_opy_]
        del platform[bstack11l1l1111_opy_]
  for bstack1ll111lll_opy_ in bstack11ll1l_opy_:
    if bstack1ll111lll_opy_ in config:
      if not bstack11ll1l_opy_[bstack1ll111lll_opy_] in config:
        config[bstack11ll1l_opy_[bstack1ll111lll_opy_]] = {}
      config[bstack11ll1l_opy_[bstack1ll111lll_opy_]].update(config[bstack1ll111lll_opy_])
      del config[bstack1ll111lll_opy_]
  for platform in bstack1111lll1_opy_:
    for bstack1ll111lll_opy_ in bstack11ll1l_opy_:
      if bstack1ll111lll_opy_ in list(platform):
        if not bstack11ll1l_opy_[bstack1ll111lll_opy_] in platform:
          platform[bstack11ll1l_opy_[bstack1ll111lll_opy_]] = {}
        platform[bstack11ll1l_opy_[bstack1ll111lll_opy_]].update(platform[bstack1ll111lll_opy_])
        del platform[bstack1ll111lll_opy_]
  config = bstack11111ll1_opy_(config)
  return config
def bstack1lllll1l1_opy_(config):
  global bstack1llllll11_opy_
  if bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧદ") in config and str(config[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨધ")]).lower() != bstack1l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫન"):
    if not bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ઩") in config:
      config[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫપ")] = {}
    if not bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪફ") in config[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭બ")]:
      bstack11l1l11ll_opy_ = datetime.datetime.now()
      bstack1l1l1l11_opy_ = bstack11l1l11ll_opy_.strftime(bstack1l1_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧભ"))
      hostname = socket.gethostname()
      bstack11ll11ll_opy_ = bstack1l1_opy_ (u"ࠫࠬમ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l1_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧય").format(bstack1l1l1l11_opy_, hostname, bstack11ll11ll_opy_)
      config[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪર")][bstack1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ઱")] = identifier
    bstack1llllll11_opy_ = config[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬલ")][bstack1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫળ")]
  return config
def bstack111lllll_opy_():
  if (
    isinstance(os.getenv(bstack1l1_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠨ઴")), str) and len(os.getenv(bstack1l1_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠩવ"))) > 0
  ) or (
    isinstance(os.getenv(bstack1l1_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠫશ")), str) and len(os.getenv(bstack1l1_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠬષ"))) > 0
  ):
    return os.getenv(bstack1l1_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭સ"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠨࡅࡌࠫહ"))).lower() == bstack1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ઺") and str(os.getenv(bstack1l1_opy_ (u"ࠪࡇࡎࡘࡃࡍࡇࡆࡍࠬ઻"))).lower() == bstack1l1_opy_ (u"ࠫࡹࡸࡵࡦ઼ࠩ"):
    return os.getenv(bstack1l1_opy_ (u"ࠬࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠨઽ"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"࠭ࡃࡊࠩા"))).lower() == bstack1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬિ") and str(os.getenv(bstack1l1_opy_ (u"ࠨࡖࡕࡅ࡛ࡏࡓࠨી"))).lower() == bstack1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧુ"):
    return os.getenv(bstack1l1_opy_ (u"ࠪࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩૂ"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠫࡈࡏࠧૃ"))).lower() == bstack1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪૄ") and str(os.getenv(bstack1l1_opy_ (u"࠭ࡃࡊࡡࡑࡅࡒࡋࠧૅ"))).lower() == bstack1l1_opy_ (u"ࠧࡤࡱࡧࡩࡸ࡮ࡩࡱࠩ૆"):
    return 0 # bstack1l1ll1l1_opy_ bstack1l1ll1ll_opy_ not set build number env
  if os.getenv(bstack1l1_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠫે")) and os.getenv(bstack1l1_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠬૈ")):
    return os.getenv(bstack1l1_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬૉ"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠫࡈࡏࠧ૊"))).lower() == bstack1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪો") and str(os.getenv(bstack1l1_opy_ (u"࠭ࡄࡓࡑࡑࡉࠬૌ"))).lower() == bstack1l1_opy_ (u"ࠧࡵࡴࡸࡩ્ࠬ"):
    return os.getenv(bstack1l1_opy_ (u"ࠨࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭૎"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠩࡆࡍࠬ૏"))).lower() == bstack1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨૐ") and str(os.getenv(bstack1l1_opy_ (u"ࠫࡘࡋࡍࡂࡒࡋࡓࡗࡋࠧ૑"))).lower() == bstack1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪ૒"):
    return os.getenv(bstack1l1_opy_ (u"࠭ࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠩ૓"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠧࡄࡋࠪ૔"))).lower() == bstack1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭૕") and str(os.getenv(bstack1l1_opy_ (u"ࠩࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠬ૖"))).lower() == bstack1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨ૗"):
    return os.getenv(bstack1l1_opy_ (u"ࠫࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠧ૘"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠬࡉࡉࠨ૙"))).lower() == bstack1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫ૚") and str(os.getenv(bstack1l1_opy_ (u"ࠧࡃࡗࡌࡐࡉࡑࡉࡕࡇࠪ૛"))).lower() == bstack1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭૜"):
    return os.getenv(bstack1l1_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫ૝"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠪࡘࡋࡥࡂࡖࡋࡏࡈࠬ૞"))).lower() == bstack1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩ૟"):
    return os.getenv(bstack1l1_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬૠ"), 0)
  return -1
def bstack11l1l1ll1_opy_(bstack111ll_opy_):
  global CONFIG
  if not bstack1l1_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨૡ") in CONFIG[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩૢ")]:
    return
  CONFIG[bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪૣ")] = CONFIG[bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૤")].replace(
    bstack1l1_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬ૥"),
    str(bstack111ll_opy_)
  )
def bstack1llllll_opy_():
  global CONFIG
  if not bstack1l1_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪ૦") in CONFIG[bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૧")]:
    return
  bstack11l1l11ll_opy_ = datetime.datetime.now()
  bstack1l1l1l11_opy_ = bstack11l1l11ll_opy_.strftime(bstack1l1_opy_ (u"࠭ࠥࡥ࠯ࠨࡦ࠲ࠫࡈ࠻ࠧࡐࠫ૨"))
  CONFIG[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")] = CONFIG[bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૪")].replace(
    bstack1l1_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨ૫"),
    bstack1l1l1l11_opy_
  )
def bstack1ll11l1_opy_():
  global CONFIG
  if bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૬") in CONFIG and not bool(CONFIG[bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૭")]):
    del CONFIG[bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮")]
    return
  if not bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯") in CONFIG:
    CONFIG[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૰")] = bstack1l1_opy_ (u"ࠨࠥࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫ૱")
  if bstack1l1_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨ૲") in CONFIG[bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૳")]:
    bstack1llllll_opy_()
    os.environ[bstack1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ૴")] = CONFIG[bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૵")]
  if not bstack1l1_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨ૶") in CONFIG[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૷")]:
    return
  bstack111ll_opy_ = bstack1l1_opy_ (u"ࠨࠩ૸")
  bstack11l1l1l1l_opy_ = bstack111lllll_opy_()
  if bstack11l1l1l1l_opy_ != -1:
    bstack111ll_opy_ = bstack1l1_opy_ (u"ࠩࡆࡍࠥ࠭ૹ") + str(bstack11l1l1l1l_opy_)
  if bstack111ll_opy_ == bstack1l1_opy_ (u"ࠪࠫૺ"):
    bstack1l111_opy_ = bstack1l1111ll1_opy_(CONFIG[bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧૻ")])
    if bstack1l111_opy_ != -1:
      bstack111ll_opy_ = str(bstack1l111_opy_)
  if bstack111ll_opy_:
    bstack11l1l1ll1_opy_(bstack111ll_opy_)
    os.environ[bstack1l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩૼ")] = CONFIG[bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૽")]
def bstack1111lll_opy_(bstack1lll11_opy_, bstack11l11_opy_, path):
  bstack1l1llll11_opy_ = {
    bstack1l1_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૾"): bstack11l11_opy_
  }
  if os.path.exists(path):
    bstack111lll_opy_ = json.load(open(path, bstack1l1_opy_ (u"ࠨࡴࡥࠫ૿")))
  else:
    bstack111lll_opy_ = {}
  bstack111lll_opy_[bstack1lll11_opy_] = bstack1l1llll11_opy_
  with open(path, bstack1l1_opy_ (u"ࠤࡺ࠯ࠧ଀")) as outfile:
    json.dump(bstack111lll_opy_, outfile)
def bstack1l1111ll1_opy_(bstack1lll11_opy_):
  bstack1lll11_opy_ = str(bstack1lll11_opy_)
  bstack1ll1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠪࢂࠬଁ")), bstack1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଂ"))
  try:
    if not os.path.exists(bstack1ll1ll_opy_):
      os.makedirs(bstack1ll1ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠬࢄࠧଃ")), bstack1l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭଄"), bstack1l1_opy_ (u"ࠧ࠯ࡤࡸ࡭ࡱࡪ࠭࡯ࡣࡰࡩ࠲ࡩࡡࡤࡪࡨ࠲࡯ࡹ࡯࡯ࠩଅ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1_opy_ (u"ࠨࡹࠪଆ")):
        pass
      with open(file_path, bstack1l1_opy_ (u"ࠤࡺ࠯ࠧଇ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1_opy_ (u"ࠪࡶࠬଈ")) as bstack1llll1111_opy_:
      bstack11l111l_opy_ = json.load(bstack1llll1111_opy_)
    if bstack1lll11_opy_ in bstack11l111l_opy_:
      bstack1lll11111_opy_ = bstack11l111l_opy_[bstack1lll11_opy_][bstack1l1_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨଉ")]
      bstack11llll1_opy_ = int(bstack1lll11111_opy_) + 1
      bstack1111lll_opy_(bstack1lll11_opy_, bstack11llll1_opy_, file_path)
      return bstack11llll1_opy_
    else:
      bstack1111lll_opy_(bstack1lll11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11l11l1_opy_.format(str(e)))
    return -1
def bstack111l11ll_opy_(config):
  if not config[bstack1l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧଊ")] or not config[bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩଋ")]:
    return True
  else:
    return False
def bstack1lll1111l_opy_(config):
  if bstack1l1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ଌ") in config:
    del(config[bstack1l1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ଍")])
    return False
  if bstack1lllll1ll_opy_() < version.parse(bstack1l1_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨ଎")):
    return False
  if bstack1lllll1ll_opy_() >= version.parse(bstack1l1_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩଏ")):
    return True
  if bstack1l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫଐ") in config and config[bstack1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ଑")] == False:
    return False
  else:
    return True
def bstack11ll11l1_opy_(config, index = 0):
  global bstack1111l1l1_opy_
  bstack1ll111l11_opy_ = {}
  caps = bstack11111l11_opy_ + bstack1lll1ll11_opy_
  if bstack1111l1l1_opy_:
    caps += bstack11l1111l1_opy_
  for key in config:
    if key in caps + [bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଒")]:
      continue
    bstack1ll111l11_opy_[key] = config[key]
  if bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଓ") in config:
    for bstack11111ll_opy_ in config[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଔ")][index]:
      if bstack11111ll_opy_ in caps + [bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧକ"), bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫଖ")]:
        continue
      bstack1ll111l11_opy_[bstack11111ll_opy_] = config[bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଗ")][index][bstack11111ll_opy_]
  bstack1ll111l11_opy_[bstack1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧଘ")] = socket.gethostname()
  if bstack1l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧଙ") in bstack1ll111l11_opy_:
    del(bstack1ll111l11_opy_[bstack1l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨଚ")])
  return bstack1ll111l11_opy_
def bstack11l11l111_opy_(config):
  global bstack1111l1l1_opy_
  bstack11ll111ll_opy_ = {}
  caps = bstack1lll1ll11_opy_
  if bstack1111l1l1_opy_:
    caps+= bstack11l1111l1_opy_
  for key in caps:
    if key in config:
      bstack11ll111ll_opy_[key] = config[key]
  return bstack11ll111ll_opy_
def bstack1ll1llll_opy_(bstack1ll111l11_opy_, bstack11ll111ll_opy_):
  bstack1ll1ll11l_opy_ = {}
  for key in bstack1ll111l11_opy_.keys():
    if key in bstack111l11l1_opy_:
      bstack1ll1ll11l_opy_[bstack111l11l1_opy_[key]] = bstack1ll111l11_opy_[key]
    else:
      bstack1ll1ll11l_opy_[key] = bstack1ll111l11_opy_[key]
  for key in bstack11ll111ll_opy_:
    if key in bstack111l11l1_opy_:
      bstack1ll1ll11l_opy_[bstack111l11l1_opy_[key]] = bstack11ll111ll_opy_[key]
    else:
      bstack1ll1ll11l_opy_[key] = bstack11ll111ll_opy_[key]
  return bstack1ll1ll11l_opy_
def bstack1l1111ll_opy_(config, index = 0):
  global bstack1111l1l1_opy_
  caps = {}
  bstack11ll111ll_opy_ = bstack11l11l111_opy_(config)
  bstack1ll1l1lll_opy_ = bstack1lll1ll11_opy_
  bstack1ll1l1lll_opy_ += bstack1l1111_opy_
  if bstack1111l1l1_opy_:
    bstack1ll1l1lll_opy_ += bstack11l1111l1_opy_
  if bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଛ") in config:
    if bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧଜ") in config[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଝ")][index]:
      caps[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଞ")] = config[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଟ")][index][bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଠ")]
    if bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨଡ") in config[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଢ")][index]:
      caps[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪଣ")] = str(config[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ତ")][index][bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଥ")])
    bstack1lll11l1l_opy_ = {}
    for bstack1ll111_opy_ in bstack1ll1l1lll_opy_:
      if bstack1ll111_opy_ in config[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଦ")][index]:
        if bstack1ll111_opy_ == bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨଧ"):
          bstack1lll11l1l_opy_[bstack1ll111_opy_] = str(config[bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪନ")][index][bstack1ll111_opy_] * 1.0)
        else:
          bstack1lll11l1l_opy_[bstack1ll111_opy_] = config[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index][bstack1ll111_opy_]
        del(config[bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬପ")][index][bstack1ll111_opy_])
    bstack11ll111ll_opy_ = update(bstack11ll111ll_opy_, bstack1lll11l1l_opy_)
  bstack1ll111l11_opy_ = bstack11ll11l1_opy_(config, index)
  for bstack1l11l_opy_ in bstack1lll1ll11_opy_ + [bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଫ"), bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬବ")]:
    if bstack1l11l_opy_ in bstack1ll111l11_opy_:
      bstack11ll111ll_opy_[bstack1l11l_opy_] = bstack1ll111l11_opy_[bstack1l11l_opy_]
      del(bstack1ll111l11_opy_[bstack1l11l_opy_])
  if bstack1lll1111l_opy_(config):
    bstack1ll111l11_opy_[bstack1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬଭ")] = True
    caps.update(bstack11ll111ll_opy_)
    caps[bstack1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧମ")] = bstack1ll111l11_opy_
  else:
    bstack1ll111l11_opy_[bstack1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧଯ")] = False
    caps.update(bstack1ll1llll_opy_(bstack1ll111l11_opy_, bstack11ll111ll_opy_))
    if bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ର") in caps:
      caps[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ଱")] = caps[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଲ")]
      del(caps[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଳ")])
    if bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭଴") in caps:
      caps[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨଵ")] = caps[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨଶ")]
      del(caps[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଷ")])
  return caps
def bstack111111l_opy_():
  global bstack1llll1lll_opy_
  if bstack1lllll1ll_opy_() <= version.parse(bstack1l1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩସ")):
    if bstack1llll1lll_opy_ != bstack1l1_opy_ (u"ࠪࠫହ"):
      return bstack1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ଺") + bstack1llll1lll_opy_ + bstack1l1_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤ଻")
    return bstack11ll1lll1_opy_
  if  bstack1llll1lll_opy_ != bstack1l1_opy_ (u"଼࠭ࠧ"):
    return bstack1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤଽ") + bstack1llll1lll_opy_ + bstack1l1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤା")
  return bstack11lll11l_opy_
def bstack11lll1l1l_opy_(options):
  return hasattr(options, bstack1l1_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪି"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1111ll1_opy_(options, bstack11l111l1_opy_):
  for bstack1l1llll1_opy_ in bstack11l111l1_opy_:
    if bstack1l1llll1_opy_ in [bstack1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨୀ"), bstack1l1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨୁ")]:
      next
    if bstack1l1llll1_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1llll1_opy_]= update(options._experimental_options[bstack1l1llll1_opy_], bstack11l111l1_opy_[bstack1l1llll1_opy_])
    else:
      options.add_experimental_option(bstack1l1llll1_opy_, bstack11l111l1_opy_[bstack1l1llll1_opy_])
  if bstack1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪୂ") in bstack11l111l1_opy_:
    for arg in bstack11l111l1_opy_[bstack1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫୃ")]:
      options.add_argument(arg)
    del(bstack11l111l1_opy_[bstack1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬୄ")])
  if bstack1l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ୅") in bstack11l111l1_opy_:
    for ext in bstack11l111l1_opy_[bstack1l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭୆")]:
      options.add_extension(ext)
    del(bstack11l111l1_opy_[bstack1l1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧେ")])
def bstack11l111ll_opy_(options, bstack1lllll11_opy_):
  if bstack1l1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪୈ") in bstack1lllll11_opy_:
    for bstack11llllll_opy_ in bstack1lllll11_opy_[bstack1l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୉")]:
      if bstack11llllll_opy_ in options._preferences:
        options._preferences[bstack11llllll_opy_] = update(options._preferences[bstack11llllll_opy_], bstack1lllll11_opy_[bstack1l1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ୊")][bstack11llllll_opy_])
      else:
        options.set_preference(bstack11llllll_opy_, bstack1lllll11_opy_[bstack1l1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ୋ")][bstack11llllll_opy_])
  if bstack1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ୌ") in bstack1lllll11_opy_:
    for arg in bstack1lllll11_opy_[bstack1l1_opy_ (u"ࠩࡤࡶ࡬ࡹ୍ࠧ")]:
      options.add_argument(arg)
def bstack1l1lll1l1_opy_(options, bstack1111111l_opy_):
  if bstack1l1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ୎") in bstack1111111l_opy_:
    options.use_webview(bool(bstack1111111l_opy_[bstack1l1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬ୏")]))
  bstack1111ll1_opy_(options, bstack1111111l_opy_)
def bstack111lllll1_opy_(options, bstack1l1lll111_opy_):
  for bstack1l1ll11l_opy_ in bstack1l1lll111_opy_:
    if bstack1l1ll11l_opy_ in [bstack1l1_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩ୐"), bstack1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫ୑")]:
      next
    options.set_capability(bstack1l1ll11l_opy_, bstack1l1lll111_opy_[bstack1l1ll11l_opy_])
  if bstack1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬ୒") in bstack1l1lll111_opy_:
    for arg in bstack1l1lll111_opy_[bstack1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୓")]:
      options.add_argument(arg)
  if bstack1l1_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭୔") in bstack1l1lll111_opy_:
    options.use_technology_preview(bool(bstack1l1lll111_opy_[bstack1l1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ୕")]))
def bstack1llll11_opy_(options, bstack1l1111lll_opy_):
  for bstack111ll1ll_opy_ in bstack1l1111lll_opy_:
    if bstack111ll1ll_opy_ in [bstack1l1_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨୖ"), bstack1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪୗ")]:
      next
    options._options[bstack111ll1ll_opy_] = bstack1l1111lll_opy_[bstack111ll1ll_opy_]
  if bstack1l1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ୘") in bstack1l1111lll_opy_:
    for bstack11ll11l11_opy_ in bstack1l1111lll_opy_[bstack1l1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୙")]:
      options.add_additional_option(
          bstack11ll11l11_opy_, bstack1l1111lll_opy_[bstack1l1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ୚")][bstack11ll11l11_opy_])
  if bstack1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୛") in bstack1l1111lll_opy_:
    for arg in bstack1l1111lll_opy_[bstack1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଡ଼")]:
      options.add_argument(arg)
def bstack1111ll_opy_(options, caps):
  if not hasattr(options, bstack1l1_opy_ (u"ࠫࡐࡋ࡙ࠨଢ଼")):
    return
  if options.KEY == bstack1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୞") and options.KEY in caps:
    bstack1111ll1_opy_(options, caps[bstack1l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫୟ")])
  elif options.KEY == bstack1l1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬୠ") and options.KEY in caps:
    bstack11l111ll_opy_(options, caps[bstack1l1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ୡ")])
  elif options.KEY == bstack1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪୢ") and options.KEY in caps:
    bstack111lllll1_opy_(options, caps[bstack1l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫୣ")])
  elif options.KEY == bstack1l1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ୤") and options.KEY in caps:
    bstack1l1lll1l1_opy_(options, caps[bstack1l1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୥")])
  elif options.KEY == bstack1l1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ୦") and options.KEY in caps:
    bstack1llll11_opy_(options, caps[bstack1l1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୧")])
def bstack1l11111l1_opy_(caps):
  global bstack1111l1l1_opy_
  if bstack1111l1l1_opy_:
    if bstack11lll1111_opy_() < version.parse(bstack1l1_opy_ (u"ࠨ࠴࠱࠷࠳࠶ࠧ୨")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ୩")
    if bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ୪") in caps:
      browser = caps[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ୫")]
    elif bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭୬") in caps:
      browser = caps[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ୭")]
    browser = str(browser).lower()
    if browser == bstack1l1_opy_ (u"ࠧࡪࡲ࡫ࡳࡳ࡫ࠧ୮") or browser == bstack1l1_opy_ (u"ࠨ࡫ࡳࡥࡩ࠭୯"):
      browser = bstack1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ୰")
    if browser == bstack1l1_opy_ (u"ࠪࡷࡦࡳࡳࡶࡰࡪࠫୱ"):
      browser = bstack1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ୲")
    if browser not in [bstack1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ୳"), bstack1l1_opy_ (u"࠭ࡥࡥࡩࡨࠫ୴"), bstack1l1_opy_ (u"ࠧࡪࡧࠪ୵"), bstack1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ୶"), bstack1l1_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ୷")]:
      return None
    try:
      package = bstack1l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࢀ࠲ࡴࡶࡴࡪࡱࡱࡷࠬ୸").format(browser)
      name = bstack1l1_opy_ (u"ࠫࡔࡶࡴࡪࡱࡱࡷࠬ୹")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11lll1l1l_opy_(options):
        return None
      for bstack1l11l_opy_ in caps.keys():
        options.set_capability(bstack1l11l_opy_, caps[bstack1l11l_opy_])
      bstack1111ll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l11ll11_opy_(options, bstack1l1l111l1_opy_):
  if not bstack11lll1l1l_opy_(options):
    return
  for bstack1l11l_opy_ in bstack1l1l111l1_opy_.keys():
    if bstack1l11l_opy_ in bstack1l1111_opy_:
      next
    if bstack1l11l_opy_ in options._caps and type(options._caps[bstack1l11l_opy_]) in [dict, list]:
      options._caps[bstack1l11l_opy_] = update(options._caps[bstack1l11l_opy_], bstack1l1l111l1_opy_[bstack1l11l_opy_])
    else:
      options.set_capability(bstack1l11l_opy_, bstack1l1l111l1_opy_[bstack1l11l_opy_])
  bstack1111ll_opy_(options, bstack1l1l111l1_opy_)
  if bstack1l1_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫ୺") in options._caps:
    if options._caps[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ୻")] and options._caps[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୼")].lower() != bstack1l1_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ୽"):
      del options._caps[bstack1l1_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨ୾")]
def bstack1111l_opy_(proxy_config):
  if bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ୿") in proxy_config:
    proxy_config[bstack1l1_opy_ (u"ࠫࡸࡹ࡬ࡑࡴࡲࡼࡾ࠭஀")] = proxy_config[bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஁")]
    del(proxy_config[bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஂ")])
  if bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪஃ") in proxy_config and proxy_config[bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ஄")].lower() != bstack1l1_opy_ (u"ࠩࡧ࡭ࡷ࡫ࡣࡵࠩஅ"):
    proxy_config[bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ஆ")] = bstack1l1_opy_ (u"ࠫࡲࡧ࡮ࡶࡣ࡯ࠫஇ")
  if bstack1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡅࡺࡺ࡯ࡤࡱࡱࡪ࡮࡭ࡕࡳ࡮ࠪஈ") in proxy_config:
    proxy_config[bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩஉ")] = bstack1l1_opy_ (u"ࠧࡱࡣࡦࠫஊ")
  return proxy_config
def bstack1ll1l1l11_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ஋") in config:
    return proxy
  config[bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ஌")] = bstack1111l_opy_(config[bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ஍")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪஎ")])
  return proxy
def bstack1l1l1l1ll_opy_(self):
  global CONFIG
  global bstack111l1ll_opy_
  try:
    proxy = bstack1l1ll1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪஏ")):
        proxies = bstack1l111ll_opy_(proxy, bstack111111l_opy_())
        if len(proxies) > 0:
          protocol, bstack111l1lll_opy_ = proxies.popitem()
          if bstack1l1_opy_ (u"ࠨ࠺࠰࠱ࠥஐ") in bstack111l1lll_opy_:
            return bstack111l1lll_opy_
          else:
            return bstack1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ஑") + bstack111l1lll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧஒ").format(str(e)))
  return bstack111l1ll_opy_(self)
def bstack11l11lll1_opy_():
  global CONFIG
  return bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬஓ") in CONFIG or bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧஔ") in CONFIG
def bstack1l1ll1_opy_(config):
  if not bstack11l11lll1_opy_():
    return
  if config.get(bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧக")):
    return config.get(bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ஖"))
  if config.get(bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ஗")):
    return config.get(bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ஘"))
def bstack1llll1l_opy_(url):
  try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
  except:
      return False
def bstack1ll1l1l_opy_(bstack1lll1l1ll_opy_, bstack1ll1l1l1_opy_):
  from pypac import get_pac
  from pypac import PACSession
  from pypac.parser import PACFile
  import socket
  if os.path.isfile(bstack1lll1l1ll_opy_):
    with open(bstack1lll1l1ll_opy_) as f:
      pac = PACFile(f.read())
  elif bstack1llll1l_opy_(bstack1lll1l1ll_opy_):
    pac = get_pac(url=bstack1lll1l1ll_opy_)
  else:
    raise Exception(bstack1l1_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨங").format(bstack1lll1l1ll_opy_))
  session = PACSession(pac)
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((bstack1l1_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥச"), 80))
    bstack11ll1l1ll_opy_ = s.getsockname()[0]
    s.close()
  except:
    bstack11ll1l1ll_opy_ = bstack1l1_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫ஛")
  proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1l1l1_opy_, bstack11ll1l1ll_opy_)
  return proxy_url
def bstack1l111ll_opy_(bstack1lll1l1ll_opy_, bstack1ll1l1l1_opy_):
  proxies = {}
  global bstack1ll1lll1_opy_
  if bstack1l1_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧஜ") in globals():
    return bstack1ll1lll1_opy_
  try:
    proxy = bstack1ll1l1l_opy_(bstack1lll1l1ll_opy_,bstack1ll1l1l1_opy_)
    if bstack1l1_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧ஝") in proxy:
      proxies = {}
    elif bstack1l1_opy_ (u"ࠨࡈࡕࡖࡓࠦஞ") in proxy or bstack1l1_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨட") in proxy or bstack1l1_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢ஠") in proxy:
      bstack11l11l11_opy_ = proxy.split(bstack1l1_opy_ (u"ࠤࠣࠦ஡"))
      if bstack1l1_opy_ (u"ࠥ࠾࠴࠵ࠢ஢") in bstack1l1_opy_ (u"ࠦࠧண").join(bstack11l11l11_opy_[1:]):
        proxies = {
          bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫத"): bstack1l1_opy_ (u"ࠨࠢ஥").join(bstack11l11l11_opy_[1:])
        }
      else:
        proxies = {
          bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭஦") : str(bstack11l11l11_opy_[0]).lower()+ bstack1l1_opy_ (u"ࠣ࠼࠲࠳ࠧ஧") + bstack1l1_opy_ (u"ࠤࠥந").join(bstack11l11l11_opy_[1:])
        }
    elif bstack1l1_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤன") in proxy:
      bstack11l11l11_opy_ = proxy.split(bstack1l1_opy_ (u"ࠦࠥࠨப"))
      if bstack1l1_opy_ (u"ࠧࡀ࠯࠰ࠤ஫") in bstack1l1_opy_ (u"ࠨࠢ஬").join(bstack11l11l11_opy_[1:]):
        proxies = {
          bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭஭"): bstack1l1_opy_ (u"ࠣࠤம").join(bstack11l11l11_opy_[1:])
        }
      else:
        proxies = {
          bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨய"): bstack1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦர") + bstack1l1_opy_ (u"ࠦࠧற").join(bstack11l11l11_opy_[1:])
        }
    else:
      proxies = {
        bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫல"): proxy
      }
  except Exception as e:
    logger.error(bstack1l11111l_opy_.format(bstack1lll1l1ll_opy_, str(e)))
  bstack1ll1lll1_opy_ = proxies
  return proxies
def bstack1lllll_opy_(config, bstack1ll1l1l1_opy_):
  proxy = bstack1l1ll1_opy_(config)
  proxies = {}
  if config.get(bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩள")) or config.get(bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫழ")):
    if proxy.endswith(bstack1l1_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭வ")):
      proxies = bstack1l111ll_opy_(proxy,bstack1ll1l1l1_opy_)
    else:
      proxies = {
        bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨஶ"): proxy
      }
  return proxies
def bstack11l1111l_opy_():
  return bstack11l11lll1_opy_() and bstack1lllll1ll_opy_() >= version.parse(bstack1lll1l1l1_opy_)
def bstack1lll1ll1_opy_(config):
  bstack1lll1lll_opy_ = {}
  if bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧஷ") in config:
    bstack1lll1lll_opy_ =  config[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨஸ")]
  if bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫஹ") in config:
    bstack1lll1lll_opy_ = config[bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ஺")]
  proxy = bstack1l1ll1_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ஻")) and os.path.isfile(proxy):
      bstack1lll1lll_opy_[bstack1l1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ஼")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ஽")):
        proxies = bstack1lllll_opy_(config, bstack111111l_opy_())
        if len(proxies) > 0:
          protocol, bstack111l1lll_opy_ = proxies.popitem()
          if bstack1l1_opy_ (u"ࠥ࠾࠴࠵ࠢா") in bstack111l1lll_opy_:
            parsed_url = urlparse(bstack111l1lll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l1_opy_ (u"ࠦ࠿࠵࠯ࠣி") + bstack111l1lll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1lll1lll_opy_[bstack1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨீ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1lll1lll_opy_[bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩு")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1lll1lll_opy_[bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪூ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1lll1lll_opy_[bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ௃")] = str(parsed_url.password)
  return bstack1lll1lll_opy_
def bstack1l1ll1l_opy_(config):
  if bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧ௄") in config:
    return config[bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ௅")]
  return {}
def bstack1111l1_opy_(caps):
  global bstack1llllll11_opy_
  if bstack1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬெ") in caps:
    caps[bstack1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ே")][bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬை")] = True
    if bstack1llllll11_opy_:
      caps[bstack1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ௉")][bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪொ")] = bstack1llllll11_opy_
  else:
    caps[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧோ")] = True
    if bstack1llllll11_opy_:
      caps[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫௌ")] = bstack1llllll11_opy_
def bstack1l1ll11l1_opy_():
  global CONFIG
  if bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ்") in CONFIG and CONFIG[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௎")]:
    bstack1lll1lll_opy_ = bstack1lll1ll1_opy_(CONFIG)
    bstack1l111l_opy_(CONFIG[bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ௏")], bstack1lll1lll_opy_)
def bstack1l111l_opy_(key, bstack1lll1lll_opy_):
  global bstack1l1l111l_opy_
  logger.info(bstack111llll11_opy_)
  try:
    bstack1l1l111l_opy_ = Local()
    bstack1ll11ll1_opy_ = {bstack1l1_opy_ (u"ࠧ࡬ࡧࡼࠫௐ"): key}
    bstack1ll11ll1_opy_.update(bstack1lll1lll_opy_)
    logger.debug(bstack11l1lllll_opy_.format(str(bstack1ll11ll1_opy_)))
    bstack1l1l111l_opy_.start(**bstack1ll11ll1_opy_)
    if bstack1l1l111l_opy_.isRunning():
      logger.info(bstack1l1111111_opy_)
  except Exception as e:
    bstack11l111l11_opy_(bstack111l1111_opy_.format(str(e)))
def bstack11llll111_opy_():
  global bstack1l1l111l_opy_
  if bstack1l1l111l_opy_.isRunning():
    logger.info(bstack11ll11_opy_)
    bstack1l1l111l_opy_.stop()
  bstack1l1l111l_opy_ = None
def bstack1l11l1l1_opy_(bstack1llll1l11_opy_=[]):
  global CONFIG
  bstack1111111_opy_ = []
  bstack1lll111ll_opy_ = [bstack1l1_opy_ (u"ࠨࡱࡶࠫ௑"), bstack1l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ௒"), bstack1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ௓"), bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௔"), bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ௕"), bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ௖")]
  try:
    for err in bstack1llll1l11_opy_:
      bstack1llllll1l_opy_ = {}
      for k in bstack1lll111ll_opy_:
        val = CONFIG[bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪௗ")][int(err[bstack1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ௘")])].get(k)
        if val:
          bstack1llllll1l_opy_[k] = val
      bstack1llllll1l_opy_[bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺࡳࠨ௙")] = {
        err[bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ௚")]: err[bstack1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ௛")]
      }
      bstack1111111_opy_.append(bstack1llllll1l_opy_)
  except Exception as e:
    logger.debug(bstack1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡱࡵࡱࡦࡺࡴࡪࡰࡪࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸ࠿ࠦࠧ௜") +str(e))
  finally:
    return bstack1111111_opy_
def bstack11ll1111_opy_():
  global bstack11l1lll_opy_
  global bstack1ll11l111_opy_
  global bstack1l1lll_opy_
  if bstack11l1lll_opy_:
    logger.warning(bstack1l1lll11_opy_.format(str(bstack11l1lll_opy_)))
  logger.info(bstack1l11l1l1l_opy_)
  global bstack1l1l111l_opy_
  if bstack1l1l111l_opy_:
    bstack11llll111_opy_()
  try:
    for driver in bstack1ll11l111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll1l1ll_opy_)
  bstack1l111lll_opy_()
  if len(bstack1l1lll_opy_) > 0:
    message = bstack1l11l1l1_opy_(bstack1l1lll_opy_)
    bstack1l111lll_opy_(message)
  else:
    bstack1l111lll_opy_()
def bstack11llll11_opy_(self, *args):
  logger.error(bstack11lllllll_opy_)
  bstack11ll1111_opy_()
  sys.exit(1)
def bstack11l111l11_opy_(err):
  logger.critical(bstack1l11l11ll_opy_.format(str(err)))
  bstack1l111lll_opy_(bstack1l11l11ll_opy_.format(str(err)))
  atexit.unregister(bstack11ll1111_opy_)
  sys.exit(1)
def bstack11lllll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l111lll_opy_(message)
  atexit.unregister(bstack11ll1111_opy_)
  sys.exit(1)
def bstack1l1lll11l_opy_():
  global CONFIG
  global bstack11llll1l1_opy_
  global bstack111111_opy_
  global bstack11ll1lll_opy_
  CONFIG = bstack1lll111l_opy_()
  bstack11ll11l_opy_()
  bstack1111llll_opy_()
  CONFIG = bstack11l1ll1l1_opy_(CONFIG)
  update(CONFIG, bstack111111_opy_)
  update(CONFIG, bstack11llll1l1_opy_)
  CONFIG = bstack1lllll1l1_opy_(CONFIG)
  if bstack1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ௝") in CONFIG and str(CONFIG[bstack1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ௞")]).lower() == bstack1l1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ௟"):
    bstack11ll1lll_opy_ = False
  if (bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ௠") in CONFIG and bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௡") in bstack11llll1l1_opy_) or (bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௢") in CONFIG and bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௣") not in bstack111111_opy_):
    if os.getenv(bstack1l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ௤")):
      CONFIG[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௥")] = os.getenv(bstack1l1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ௦"))
    else:
      bstack1ll11l1_opy_()
  elif (bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ௧") not in CONFIG and bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ௨") in CONFIG) or (bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௩") in bstack111111_opy_ and bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௪") not in bstack11llll1l1_opy_):
    del(CONFIG[bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ௫")])
  if bstack111l11ll_opy_(CONFIG):
    bstack11l111l11_opy_(bstack1ll1lll1l_opy_)
  bstack11lll1lll_opy_()
  bstack11lllll11_opy_()
  if bstack1111l1l1_opy_:
    CONFIG[bstack1l1_opy_ (u"ࠧࡢࡲࡳࠫ௬")] = bstack11l1111_opy_(CONFIG)
    logger.info(bstack1ll11lll1_opy_.format(CONFIG[bstack1l1_opy_ (u"ࠨࡣࡳࡴࠬ௭")]))
def bstack11lllll11_opy_():
  global CONFIG
  global bstack1111l1l1_opy_
  if bstack1l1_opy_ (u"ࠩࡤࡴࡵ࠭௮") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11lllll1_opy_(e, bstack111l1ll1_opy_)
    bstack1111l1l1_opy_ = True
def bstack11l1111_opy_(config):
  bstack1l11ll1_opy_ = bstack1l1_opy_ (u"ࠪࠫ௯")
  app = config[bstack1l1_opy_ (u"ࠫࡦࡶࡰࠨ௰")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lll1l1l_opy_:
      if os.path.exists(app):
        bstack1l11ll1_opy_ = bstack1111ll1l_opy_(config, app)
      elif bstack1l1l11lll_opy_(app):
        bstack1l11ll1_opy_ = app
      else:
        bstack11l111l11_opy_(bstack11l1l_opy_.format(app))
    else:
      if bstack1l1l11lll_opy_(app):
        bstack1l11ll1_opy_ = app
      elif os.path.exists(app):
        bstack1l11ll1_opy_ = bstack1111ll1l_opy_(app)
      else:
        bstack11l111l11_opy_(bstack11llllll1_opy_)
  else:
    if len(app) > 2:
      bstack11l111l11_opy_(bstack11l1111ll_opy_)
    elif len(app) == 2:
      if bstack1l1_opy_ (u"ࠬࡶࡡࡵࡪࠪ௱") in app and bstack1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ௲") in app:
        if os.path.exists(app[bstack1l1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ௳")]):
          bstack1l11ll1_opy_ = bstack1111ll1l_opy_(config, app[bstack1l1_opy_ (u"ࠨࡲࡤࡸ࡭࠭௴")], app[bstack1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ௵")])
        else:
          bstack11l111l11_opy_(bstack11l1l_opy_.format(app))
      else:
        bstack11l111l11_opy_(bstack11l1111ll_opy_)
    else:
      for key in app:
        if key in bstack1l1l11l_opy_:
          if key == bstack1l1_opy_ (u"ࠪࡴࡦࡺࡨࠨ௶"):
            if os.path.exists(app[key]):
              bstack1l11ll1_opy_ = bstack1111ll1l_opy_(config, app[key])
            else:
              bstack11l111l11_opy_(bstack11l1l_opy_.format(app))
          else:
            bstack1l11ll1_opy_ = app[key]
        else:
          bstack11l111l11_opy_(bstack1llllll1_opy_)
  return bstack1l11ll1_opy_
def bstack1l1l11lll_opy_(bstack1l11ll1_opy_):
  import re
  bstack1l1llll_opy_ = re.compile(bstack1l1_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ௷"))
  bstack111lll11_opy_ = re.compile(bstack1l1_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ௸"))
  if bstack1l1_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬ௹") in bstack1l11ll1_opy_ or re.fullmatch(bstack1l1llll_opy_, bstack1l11ll1_opy_) or re.fullmatch(bstack111lll11_opy_, bstack1l11ll1_opy_):
    return True
  else:
    return False
def bstack1111ll1l_opy_(config, path, bstack1ll1lllll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1_opy_ (u"ࠧࡳࡤࠪ௺")).read()).hexdigest()
  bstack1l1lll1ll_opy_ = bstack1llll1_opy_(md5_hash)
  bstack1l11ll1_opy_ = None
  if bstack1l1lll1ll_opy_:
    logger.info(bstack111l1l_opy_.format(bstack1l1lll1ll_opy_, md5_hash))
    return bstack1l1lll1ll_opy_
  bstack11l1ll_opy_ = MultipartEncoder(
    fields={
        bstack1l1_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭௻"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1_opy_ (u"ࠩࡵࡦࠬ௼")), bstack1l1_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧ௽")),
        bstack1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ௾"): bstack1ll1lllll_opy_
    }
  )
  response = requests.post(bstack11lll1_opy_, data=bstack11l1ll_opy_,
                         headers={bstack1l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ௿"): bstack11l1ll_opy_.content_type}, auth=(config[bstack1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨఀ")], config[bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪఁ")]))
  try:
    res = json.loads(response.text)
    bstack1l11ll1_opy_ = res[bstack1l1_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩం")]
    logger.info(bstack1l1111l11_opy_.format(bstack1l11ll1_opy_))
    bstack11l1l1ll_opy_(md5_hash, bstack1l11ll1_opy_)
  except ValueError as err:
    bstack11l111l11_opy_(bstack1ll11lll_opy_.format(str(err)))
  return bstack1l11ll1_opy_
def bstack11lll1lll_opy_():
  global CONFIG
  global bstack1l11l11_opy_
  bstack1l11ll1ll_opy_ = 0
  bstack1l111l1l_opy_ = 1
  if bstack1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩః") in CONFIG:
    bstack1l111l1l_opy_ = CONFIG[bstack1l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪఄ")]
  if bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఅ") in CONFIG:
    bstack1l11ll1ll_opy_ = len(CONFIG[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఆ")])
  bstack1l11l11_opy_ = int(bstack1l111l1l_opy_) * int(bstack1l11ll1ll_opy_)
def bstack1llll1_opy_(md5_hash):
  bstack11l11l1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"࠭ࡾࠨఇ")), bstack1l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧఈ"), bstack1l1_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩఉ"))
  if os.path.exists(bstack11l11l1ll_opy_):
    bstack11l11111l_opy_ = json.load(open(bstack11l11l1ll_opy_,bstack1l1_opy_ (u"ࠩࡵࡦࠬఊ")))
    if md5_hash in bstack11l11111l_opy_:
      bstack1l1l11111_opy_ = bstack11l11111l_opy_[md5_hash]
      bstack11l1l1lll_opy_ = datetime.datetime.now()
      bstack11l111lll_opy_ = datetime.datetime.strptime(bstack1l1l11111_opy_[bstack1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ఋ")], bstack1l1_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨఌ"))
      if (bstack11l1l1lll_opy_ - bstack11l111lll_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1l11111_opy_[bstack1l1_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ఍")]):
        return None
      return bstack1l1l11111_opy_[bstack1l1_opy_ (u"࠭ࡩࡥࠩఎ")]
  else:
    return None
def bstack11l1l1ll_opy_(md5_hash, bstack1l11ll1_opy_):
  bstack1ll1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠧࡿࠩఏ")), bstack1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨఐ"))
  if not os.path.exists(bstack1ll1ll_opy_):
    os.makedirs(bstack1ll1ll_opy_)
  bstack11l11l1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠩࢁࠫ఑")), bstack1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪఒ"), bstack1l1_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬఓ"))
  bstack1llllllll_opy_ = {
    bstack1l1_opy_ (u"ࠬ࡯ࡤࠨఔ"): bstack1l11ll1_opy_,
    bstack1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩక"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫఖ")),
    bstack1l1_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭గ"): str(__version__)
  }
  if os.path.exists(bstack11l11l1ll_opy_):
    bstack11l11111l_opy_ = json.load(open(bstack11l11l1ll_opy_,bstack1l1_opy_ (u"ࠩࡵࡦࠬఘ")))
  else:
    bstack11l11111l_opy_ = {}
  bstack11l11111l_opy_[md5_hash] = bstack1llllllll_opy_
  with open(bstack11l11l1ll_opy_, bstack1l1_opy_ (u"ࠥࡻ࠰ࠨఙ")) as outfile:
    json.dump(bstack11l11111l_opy_, outfile)
def bstack1ll11111_opy_(self):
  return
def bstack1ll1ll1l1_opy_(self):
  return
def bstack1l1l1l1l1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1ll111ll_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l11lll1_opy_
  global bstack11111111_opy_
  global bstack11llll11l_opy_
  global bstack11l111111_opy_
  global bstack1ll1l1ll1_opy_
  global bstack1111l11_opy_
  global bstack11ll_opy_
  global bstack1ll11l111_opy_
  global bstack1l1ll11_opy_
  CONFIG[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭చ")] = str(bstack1111l11_opy_) + str(__version__)
  command_executor = bstack111111l_opy_()
  logger.debug(bstack1l1lll1l_opy_.format(command_executor))
  proxy = bstack1ll1l1l11_opy_(CONFIG, proxy)
  bstack1l1l1lll_opy_ = 0 if bstack11111111_opy_ < 0 else bstack11111111_opy_
  if bstack11l111111_opy_ is True:
    bstack1l1l1lll_opy_ = int(multiprocessing.current_process().name)
  if bstack1ll1l1ll1_opy_ is True:
    bstack1l1l1lll_opy_ = int(threading.current_thread().name)
  bstack1l1l111l1_opy_ = bstack1l1111ll_opy_(CONFIG, bstack1l1l1lll_opy_)
  logger.debug(bstack1l11lll_opy_.format(str(bstack1l1l111l1_opy_)))
  if bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩఛ") in CONFIG and CONFIG[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪజ")]:
    bstack1111l1_opy_(bstack1l1l111l1_opy_)
  if desired_capabilities:
    bstack11l1lll1l_opy_ = bstack11l1ll1l1_opy_(desired_capabilities)
    bstack11l1lll1l_opy_[bstack1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧఝ")] = bstack1lll1111l_opy_(CONFIG)
    bstack1ll11ll_opy_ = bstack1l1111ll_opy_(bstack11l1lll1l_opy_)
    if bstack1ll11ll_opy_:
      bstack1l1l111l1_opy_ = update(bstack1ll11ll_opy_, bstack1l1l111l1_opy_)
    desired_capabilities = None
  if options:
    bstack11l11ll11_opy_(options, bstack1l1l111l1_opy_)
  if not options:
    options = bstack1l11111l1_opy_(bstack1l1l111l1_opy_)
  if proxy and bstack1lllll1ll_opy_() >= version.parse(bstack1l1_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨఞ")):
    options.proxy(proxy)
  if options and bstack1lllll1ll_opy_() >= version.parse(bstack1l1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨట")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1lllll1ll_opy_() < version.parse(bstack1l1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩఠ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l1l111l1_opy_)
  logger.info(bstack1l1ll1l11_opy_)
  if bstack1lllll1ll_opy_() >= version.parse(bstack1l1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫడ")):
    bstack11ll_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lllll1ll_opy_() >= version.parse(bstack1l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫఢ")):
    bstack11ll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lllll1ll_opy_() >= version.parse(bstack1l1_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ణ")):
    bstack11ll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11ll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack1lllll1l_opy_ = bstack1l1_opy_ (u"ࠧࠨత")
    if bstack1lllll1ll_opy_() >= version.parse(bstack1l1_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩథ")):
      bstack1lllll1l_opy_ = self.caps.get(bstack1l1_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤద"))
    else:
      bstack1lllll1l_opy_ = self.capabilities.get(bstack1l1_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥధ"))
    if bstack1lllll1l_opy_:
      if bstack1lllll1ll_opy_() <= version.parse(bstack1l1_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫన")):
        self.command_executor._url = bstack1l1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ఩") + bstack1llll1lll_opy_ + bstack1l1_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥప")
      else:
        self.command_executor._url = bstack1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤఫ") + bstack1lllll1l_opy_ + bstack1l1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤబ")
      logger.debug(bstack11l11ll1_opy_.format(bstack1lllll1l_opy_))
    else:
      logger.debug(bstack1ll1lll11_opy_.format(bstack1l1_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥభ")))
  except Exception as e:
    logger.debug(bstack1ll1lll11_opy_.format(e))
  if bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩమ") in bstack1111l11_opy_:
    bstack11l1ll1l_opy_(bstack11111111_opy_, bstack1l1ll11_opy_)
  bstack1l11lll1_opy_ = self.session_id
  bstack1ll11l111_opy_.append(self)
  if bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧయ") in CONFIG and bstack1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪర") in CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఱ")][bstack1l1l1lll_opy_]:
    bstack11llll11l_opy_ = CONFIG[bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪల")][bstack1l1l1lll_opy_][bstack1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ళ")]
  logger.debug(bstack1l1ll_opy_.format(bstack1l11lll1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1ll1l11_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11lllll_opy_
      if(bstack1l1_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦఴ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠪࢂࠬవ")), bstack1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫశ"), bstack1l1_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧష")), bstack1l1_opy_ (u"࠭ࡷࠨస")) as fp:
          fp.write(bstack1l1_opy_ (u"ࠢࠣహ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ఺")))):
          with open(args[1], bstack1l1_opy_ (u"ࠩࡵࠫ఻")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l1_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰఼ࠪࠩ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1l1l111_opy_)
            lines.insert(1, bstack111l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l1_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨఽ")), bstack1l1_opy_ (u"ࠬࡽࠧా")) as bstack1llll11ll_opy_:
              bstack1llll11ll_opy_.writelines(lines)
        CONFIG[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨి")] = str(bstack1111l11_opy_) + str(__version__)
        bstack1l1l1lll_opy_ = 0 if bstack11111111_opy_ < 0 else bstack11111111_opy_
        if bstack11l111111_opy_ is True:
          bstack1l1l1lll_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack1l1_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢీ")] = False
        CONFIG[bstack1l1_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢు")] = True
        bstack1l1l111l1_opy_ = bstack1l1111ll_opy_(CONFIG, bstack1l1l1lll_opy_)
        logger.debug(bstack1l11lll_opy_.format(str(bstack1l1l111l1_opy_)))
        if CONFIG[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ూ")]:
          bstack1111l1_opy_(bstack1l1l111l1_opy_)
        if bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ృ") in CONFIG and bstack1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩౄ") in CONFIG[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౅")][bstack1l1l1lll_opy_]:
          bstack11llll11l_opy_ = CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩె")][bstack1l1l1lll_opy_][bstack1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬే")]
        args.append(os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠨࢀࠪై")), bstack1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ౉"), bstack1l1_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬొ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l1l111l1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l1_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨో"))
      bstack11lllll_opy_ = True
      return bstack1l1l1ll_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l1111l1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l11lll1_opy_
    global bstack11111111_opy_
    global bstack11llll11l_opy_
    global bstack11l111111_opy_
    global bstack1111l11_opy_
    global bstack11ll_opy_
    CONFIG[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧౌ")] = str(bstack1111l11_opy_) + str(__version__)
    bstack1l1l1lll_opy_ = 0 if bstack11111111_opy_ < 0 else bstack11111111_opy_
    if bstack11l111111_opy_ is True:
      bstack1l1l1lll_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack1l1_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ్ࠧ")] = True
    bstack1l1l111l1_opy_ = bstack1l1111ll_opy_(CONFIG, bstack1l1l1lll_opy_)
    logger.debug(bstack1l11lll_opy_.format(str(bstack1l1l111l1_opy_)))
    if CONFIG[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ౎")]:
      bstack1111l1_opy_(bstack1l1l111l1_opy_)
    if bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౏") in CONFIG and bstack1l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ౐") in CONFIG[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౑")][bstack1l1l1lll_opy_]:
      bstack11llll11l_opy_ = CONFIG[bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ౒")][bstack1l1l1lll_opy_][bstack1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ౓")]
    import urllib
    import json
    bstack1l111l1_opy_ = bstack1l1_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ౔") + urllib.parse.quote(json.dumps(bstack1l1l111l1_opy_))
    browser = self.connect(bstack1l111l1_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1l1l1_opy_():
    global bstack11lllll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1111l1_opy_
        bstack11lllll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1l11_opy_
      bstack11lllll_opy_ = True
    except Exception as e:
      pass
def bstack11l1ll111_opy_(context, bstack1ll11l_opy_):
  try:
    context.page.evaluate(bstack1l1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽౕࠣ"), bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ౖࠬ")+ json.dumps(bstack1ll11l_opy_) + bstack1l1_opy_ (u"ࠤࢀࢁࠧ౗"))
  except Exception as e:
    logger.debug(bstack1l1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣౘ"), e)
def bstack1l11lll11_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧౙ"), bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪౚ") + json.dumps(message) + bstack1l1_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩ౛") + json.dumps(level) + bstack1l1_opy_ (u"ࠧࡾࡿࠪ౜"))
  except Exception as e:
    logger.debug(bstack1l1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦౝ"), e)
def bstack11ll1ll1l_opy_(context, status, message = bstack1l1_opy_ (u"ࠤࠥ౞")):
  try:
    if(status == bstack1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ౟")):
      context.page.evaluate(bstack1l1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧౠ"), bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿࠭ౡ") + json.dumps(bstack1l1_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠࠣౢ") + str(message)) + bstack1l1_opy_ (u"ࠧ࠭ࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠫౣ") + json.dumps(status) + bstack1l1_opy_ (u"ࠣࡿࢀࠦ౤"))
    else:
      context.page.evaluate(bstack1l1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ౥"), bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠫ౦") + json.dumps(status) + bstack1l1_opy_ (u"ࠦࢂࢃࠢ౧"))
  except Exception as e:
    logger.debug(bstack1l1_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠤ౨"), e)
def bstack11ll1ll_opy_(self, url):
  global bstack11llll_opy_
  try:
    bstack1l1l11_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1l1l1l_opy_.format(str(err)))
  try:
    bstack11llll_opy_(self, url)
  except Exception as e:
    try:
      bstack11ll111_opy_ = str(e)
      if any(err_msg in bstack11ll111_opy_ for err_msg in bstack11l1llll_opy_):
        bstack1l1l11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1l1l1l_opy_.format(str(err)))
    raise e
def bstack1l111111_opy_(self):
  global bstack111111ll_opy_
  bstack111111ll_opy_ = self
  return
def bstack1ll111l_opy_(self, test):
  global CONFIG
  global bstack111111ll_opy_
  global bstack1l11lll1_opy_
  global bstack1l1ll1l1l_opy_
  global bstack11llll11l_opy_
  global bstack1lll1l_opy_
  global bstack111llllll_opy_
  global bstack1ll11l111_opy_
  try:
    if not bstack1l11lll1_opy_:
      with open(os.path.join(os.path.expanduser(bstack1l1_opy_ (u"࠭ࡾࠨ౩")), bstack1l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ౪"), bstack1l1_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ౫"))) as f:
        bstack1ll11111l_opy_ = json.loads(bstack1l1_opy_ (u"ࠤࡾࠦ౬") + f.read().strip() + bstack1l1_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬ౭") + bstack1l1_opy_ (u"ࠦࢂࠨ౮"))
        bstack1l11lll1_opy_ = bstack1ll11111l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll11l111_opy_:
    for driver in bstack1ll11l111_opy_:
      if bstack1l11lll1_opy_ == driver.session_id:
        if test:
          bstack1111_opy_ = str(test.data)
        if not bstack1lll1lll1_opy_ and bstack1111_opy_:
          bstack111l11l_opy_ = {
            bstack1l1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ౯"): bstack1l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ౰"),
            bstack1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ౱"): {
              bstack1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭౲"): bstack1111_opy_
            }
          }
          bstack11l1l1_opy_ = bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ౳").format(json.dumps(bstack111l11l_opy_))
          driver.execute_script(bstack11l1l1_opy_)
        if bstack1l1ll1l1l_opy_:
          bstack11lll_opy_ = {
            bstack1l1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ౴"): bstack1l1_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭౵"),
            bstack1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ౶"): {
              bstack1l1_opy_ (u"࠭ࡤࡢࡶࡤࠫ౷"): bstack1111_opy_ + bstack1l1_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ౸"),
              bstack1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ౹"): bstack1l1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ౺")
            }
          }
          bstack111l11l_opy_ = {
            bstack1l1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ౻"): bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ౼"),
            bstack1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ౽"): {
              bstack1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭౾"): bstack1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ౿")
            }
          }
          if bstack1l1ll1l1l_opy_.status == bstack1l1_opy_ (u"ࠨࡒࡄࡗࡘ࠭ಀ"):
            bstack1l11_opy_ = bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧಁ").format(json.dumps(bstack11lll_opy_))
            driver.execute_script(bstack1l11_opy_)
            bstack11l1l1_opy_ = bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨಂ").format(json.dumps(bstack111l11l_opy_))
            driver.execute_script(bstack11l1l1_opy_)
          elif bstack1l1ll1l1l_opy_.status == bstack1l1_opy_ (u"ࠫࡋࡇࡉࡍࠩಃ"):
            reason = bstack1l1_opy_ (u"ࠧࠨ಄")
            bstack11ll1ll1_opy_ = bstack1111_opy_ + bstack1l1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠧಅ")
            if bstack1l1ll1l1l_opy_.message:
              reason = str(bstack1l1ll1l1l_opy_.message)
              bstack11ll1ll1_opy_ = bstack11ll1ll1_opy_ + bstack1l1_opy_ (u"ࠧࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࠧಆ") + reason
            bstack11lll_opy_[bstack1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಇ")] = {
              bstack1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨಈ"): bstack1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩಉ"),
              bstack1l1_opy_ (u"ࠫࡩࡧࡴࡢࠩಊ"): bstack11ll1ll1_opy_
            }
            bstack111l11l_opy_[bstack1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨಋ")] = {
              bstack1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ಌ"): bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ಍"),
              bstack1l1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨಎ"): reason
            }
            bstack1l11_opy_ = bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧಏ").format(json.dumps(bstack11lll_opy_))
            driver.execute_script(bstack1l11_opy_)
            bstack11l1l1_opy_ = bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨಐ").format(json.dumps(bstack111l11l_opy_))
            driver.execute_script(bstack11l1l1_opy_)
  elif bstack1l11lll1_opy_:
    try:
      data = {}
      bstack1111_opy_ = None
      if test:
        bstack1111_opy_ = str(test.data)
      if not bstack1lll1lll1_opy_ and bstack1111_opy_:
        data[bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ಑")] = bstack1111_opy_
      if bstack1l1ll1l1l_opy_:
        if bstack1l1ll1l1l_opy_.status == bstack1l1_opy_ (u"ࠬࡖࡁࡔࡕࠪಒ"):
          data[bstack1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ಓ")] = bstack1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧಔ")
        elif bstack1l1ll1l1l_opy_.status == bstack1l1_opy_ (u"ࠨࡈࡄࡍࡑ࠭ಕ"):
          data[bstack1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩಖ")] = bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪಗ")
          if bstack1l1ll1l1l_opy_.message:
            data[bstack1l1_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫಘ")] = str(bstack1l1ll1l1l_opy_.message)
      user = CONFIG[bstack1l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧಙ")]
      key = CONFIG[bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩಚ")]
      url = bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠳ࢀࢃ࠮࡫ࡵࡲࡲࠬಛ").format(user, key, bstack1l11lll1_opy_)
      headers = {
        bstack1l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧಜ"): bstack1l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬಝ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll1l111_opy_.format(str(e)))
  if bstack111111ll_opy_:
    bstack111llllll_opy_(bstack111111ll_opy_)
  bstack1lll1l_opy_(self, test)
def bstack1lllllll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11lll1ll_opy_
  bstack11lll1ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1ll1l1l_opy_
  bstack1l1ll1l1l_opy_ = self._test
def bstack11lll111l_opy_():
  global bstack1l1ll111_opy_
  try:
    if os.path.exists(bstack1l1ll111_opy_):
      os.remove(bstack1l1ll111_opy_)
  except Exception as e:
    logger.debug(bstack1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ಞ") + str(e))
def bstack111l1l11_opy_():
  global bstack1l1ll111_opy_
  bstack111lll_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1ll111_opy_):
      with open(bstack1l1ll111_opy_, bstack1l1_opy_ (u"ࠫࡼ࠭ಟ")):
        pass
      with open(bstack1l1ll111_opy_, bstack1l1_opy_ (u"ࠧࡽࠫࠣಠ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1ll111_opy_):
      bstack111lll_opy_ = json.load(open(bstack1l1ll111_opy_, bstack1l1_opy_ (u"࠭ࡲࡣࠩಡ")))
  except Exception as e:
    logger.debug(bstack1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩࡦࡪࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩಢ") + str(e))
  finally:
    return bstack111lll_opy_
def bstack11l1ll1l_opy_(platform_index, item_index):
  global bstack1l1ll111_opy_
  try:
    bstack111lll_opy_ = bstack111l1l11_opy_()
    bstack111lll_opy_[item_index] = platform_index
    with open(bstack1l1ll111_opy_, bstack1l1_opy_ (u"ࠣࡹ࠮ࠦಣ")) as outfile:
      json.dump(bstack111lll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡼࡸࡩࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧತ") + str(e))
def bstack111l1l1_opy_(bstack1lllllll1_opy_):
  global CONFIG
  bstack1ll1ll111_opy_ = bstack1l1_opy_ (u"ࠪࠫಥ")
  if not bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧದ") in CONFIG:
    logger.info(bstack1l1_opy_ (u"ࠬࡔ࡯ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠤࡵࡧࡳࡴࡧࡧࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡵࡩࡵࡵࡲࡵࠢࡩࡳࡷࠦࡒࡰࡤࡲࡸࠥࡸࡵ࡯ࠩಧ"))
  try:
    platform = CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩನ")][bstack1lllllll1_opy_]
    if bstack1l1_opy_ (u"ࠧࡰࡵࠪ಩") in platform:
      bstack1ll1ll111_opy_ += str(platform[bstack1l1_opy_ (u"ࠨࡱࡶࠫಪ")]) + bstack1l1_opy_ (u"ࠩ࠯ࠤࠬಫ")
    if bstack1l1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ಬ") in platform:
      bstack1ll1ll111_opy_ += str(platform[bstack1l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧಭ")]) + bstack1l1_opy_ (u"ࠬ࠲ࠠࠨಮ")
    if bstack1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪಯ") in platform:
      bstack1ll1ll111_opy_ += str(platform[bstack1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫರ")]) + bstack1l1_opy_ (u"ࠨ࠮ࠣࠫಱ")
    if bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫಲ") in platform:
      bstack1ll1ll111_opy_ += str(platform[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬಳ")]) + bstack1l1_opy_ (u"ࠫ࠱ࠦࠧ಴")
    if bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪವ") in platform:
      bstack1ll1ll111_opy_ += str(platform[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫಶ")]) + bstack1l1_opy_ (u"ࠧ࠭ࠢࠪಷ")
    if bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩಸ") in platform:
      bstack1ll1ll111_opy_ += str(platform[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪಹ")]) + bstack1l1_opy_ (u"ࠪ࠰ࠥ࠭಺")
  except Exception as e:
    logger.debug(bstack1l1_opy_ (u"ࠫࡘࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡹࡸࡩ࡯ࡩࠣࡪࡴࡸࠠࡳࡧࡳࡳࡷࡺࠠࡨࡧࡱࡩࡷࡧࡴࡪࡱࡱࠫ಻") + str(e))
  finally:
    if bstack1ll1ll111_opy_[len(bstack1ll1ll111_opy_) - 2:] == bstack1l1_opy_ (u"ࠬ࠲ࠠࠨ಼"):
      bstack1ll1ll111_opy_ = bstack1ll1ll111_opy_[:-2]
    return bstack1ll1ll111_opy_
def bstack1lll111l1_opy_(path, bstack1ll1ll111_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1lll111_opy_ = ET.parse(path)
    bstack1ll1ll1_opy_ = bstack1lll111_opy_.getroot()
    bstack1l11l11l1_opy_ = None
    for suite in bstack1ll1ll1_opy_.iter(bstack1l1_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬಽ")):
      if bstack1l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧಾ") in suite.attrib:
        suite.attrib[bstack1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಿ")] += bstack1l1_opy_ (u"ࠩࠣࠫೀ") + bstack1ll1ll111_opy_
        bstack1l11l11l1_opy_ = suite
    bstack1l1l1111_opy_ = None
    for robot in bstack1ll1ll1_opy_.iter(bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩು")):
      bstack1l1l1111_opy_ = robot
    bstack11l1lll1_opy_ = len(bstack1l1l1111_opy_.findall(bstack1l1_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪೂ")))
    if bstack11l1lll1_opy_ == 1:
      bstack1l1l1111_opy_.remove(bstack1l1l1111_opy_.findall(bstack1l1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫೃ"))[0])
      bstack1ll1l1_opy_ = ET.Element(bstack1l1_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬೄ"), attrib={bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ೅"):bstack1l1_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࡳࠨೆ"), bstack1l1_opy_ (u"ࠩ࡬ࡨࠬೇ"):bstack1l1_opy_ (u"ࠪࡷ࠵࠭ೈ")})
      bstack1l1l1111_opy_.insert(1, bstack1ll1l1_opy_)
      bstack1ll1l11l_opy_ = None
      for suite in bstack1l1l1111_opy_.iter(bstack1l1_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ೉")):
        bstack1ll1l11l_opy_ = suite
      bstack1ll1l11l_opy_.append(bstack1l11l11l1_opy_)
      bstack111llll1l_opy_ = None
      for status in bstack1l11l11l1_opy_.iter(bstack1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬೊ")):
        bstack111llll1l_opy_ = status
      bstack1ll1l11l_opy_.append(bstack111llll1l_opy_)
    bstack1lll111_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠫೋ") + str(e))
def bstack1ll111111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11111l_opy_
  global CONFIG
  if bstack1l1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦೌ") in options:
    del options[bstack1l1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬್ࠧ")]
  bstack1l1llll11_opy_ = bstack111l1l11_opy_()
  for bstack11ll11ll1_opy_ in bstack1l1llll11_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࡠࡴࡨࡷࡺࡲࡴࡴࠩ೎"), str(bstack11ll11ll1_opy_), bstack1l1_opy_ (u"ࠪࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠧ೏"))
    bstack1lll111l1_opy_(path, bstack111l1l1_opy_(bstack1l1llll11_opy_[bstack11ll11ll1_opy_]))
  bstack11lll111l_opy_()
  return bstack11111l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack111ll11_opy_(self, ff_profile_dir):
  global bstack11ll1llll_opy_
  if not ff_profile_dir:
    return None
  return bstack11ll1llll_opy_(self, ff_profile_dir)
def bstack1111l1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1llllll11_opy_
  bstack111lll1ll_opy_ = []
  if bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ೐") in CONFIG:
    bstack111lll1ll_opy_ = CONFIG[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೑")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢ೒")],
      pabot_args[bstack1l1_opy_ (u"ࠢࡷࡧࡵࡦࡴࡹࡥࠣ೓")],
      argfile,
      pabot_args.get(bstack1l1_opy_ (u"ࠣࡪ࡬ࡺࡪࠨ೔")),
      pabot_args[bstack1l1_opy_ (u"ࠤࡳࡶࡴࡩࡥࡴࡵࡨࡷࠧೕ")],
      platform[0],
      bstack1llllll11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࡫࡯࡬ࡦࡵࠥೖ")] or [(bstack1l1_opy_ (u"ࠦࠧ೗"), None)]
    for platform in enumerate(bstack111lll1ll_opy_)
  ]
def bstack1l1l1l11l_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1l1l11l1l_opy_=bstack1l1_opy_ (u"ࠬ࠭೘")):
  global bstack11l1ll11l_opy_
  self.platform_index = platform_index
  self.bstack11ll1l1l_opy_ = bstack1l1l11l1l_opy_
  bstack11l1ll11l_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1l11l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1llll1ll_opy_
  global bstack1lll1l11_opy_
  if not bstack1l1_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ೙") in item.options:
    item.options[bstack1l1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ೚")] = []
  for v in item.options[bstack1l1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ೛")]:
    if bstack1l1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ೜") in v:
      item.options[bstack1l1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬೝ")].remove(v)
    if bstack1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫೞ") in v:
      item.options[bstack1l1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ೟")].remove(v)
  item.options[bstack1l1_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨೠ")].insert(0, bstack1l1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝ࡀࡻࡾࠩೡ").format(item.platform_index))
  item.options[bstack1l1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪೢ")].insert(0, bstack1l1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩೣ").format(item.bstack11ll1l1l_opy_))
  if bstack1lll1l11_opy_:
    item.options[bstack1l1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ೤")].insert(0, bstack1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖ࠾ࢀࢃࠧ೥").format(bstack1lll1l11_opy_))
  return bstack1llll1ll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l1ll111l_opy_(command, item_index):
  global bstack1lll1l11_opy_
  if bstack1lll1l11_opy_:
    command[0] = command[0].replace(bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ೦"), bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ೧") + str(item_index) + bstack1lll1l11_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭೨"), bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ೩") + str(item_index), 1)
def bstack1lll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l111ll1_opy_
  bstack1l1ll111l_opy_(command, item_index)
  return bstack11l111ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11ll11l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l111ll1_opy_
  bstack1l1ll111l_opy_(command, item_index)
  return bstack11l111ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l111ll1_opy_
  bstack1l1ll111l_opy_(command, item_index)
  return bstack11l111ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11ll1_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1l11l1_opy_
  bstack1lll1l111_opy_ = bstack1l1l11l1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1l1_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡤࡧࡲࡳࠩ೪")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1_opy_ (u"ࠪࡩࡽࡩ࡟ࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࡢࡥࡷࡸࠧ೫")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll1l111_opy_
def bstack1111l111_opy_(self, name, context, *args):
  global bstack1lllll1_opy_
  if name in [bstack1l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ೬"), bstack1l1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ೭")]:
    bstack1lllll1_opy_(self, name, context, *args)
  if name == bstack1l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ೮"):
    try:
      if(not bstack1lll1lll1_opy_):
        bstack1ll11l_opy_ = str(self.feature.name)
        bstack11l1ll111_opy_(context, bstack1ll11l_opy_)
        context.browser.execute_script(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ೯") + json.dumps(bstack1ll11l_opy_) + bstack1l1_opy_ (u"ࠨࡿࢀࠫ೰"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1l1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩೱ").format(str(e)))
  if name == bstack1l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬೲ"):
    try:
      if not hasattr(self, bstack1l1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ೳ")):
        self.driver_before_scenario = True
      if(not bstack1lll1lll1_opy_):
        bstack1ll1l1111_opy_ = args[0].name
        bstack1l11l1111_opy_ = bstack1ll11l_opy_ = str(self.feature.name)
        bstack1ll11l_opy_ = bstack1l11l1111_opy_ + bstack1l1_opy_ (u"ࠬࠦ࠭ࠡࠩ೴") + bstack1ll1l1111_opy_
        if self.driver_before_scenario:
          bstack11l1ll111_opy_(context, bstack1ll11l_opy_)
          context.browser.execute_script(bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ೵") + json.dumps(bstack1ll11l_opy_) + bstack1l1_opy_ (u"ࠧࡾࡿࠪ೶"))
    except Exception as e:
      logger.debug(bstack1l1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ೷").format(str(e)))
  if name == bstack1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ೸"):
    try:
      bstack11111l1_opy_ = args[0].status.name
      if str(bstack11111l1_opy_).lower() == bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ೹"):
        bstack1111l1ll_opy_ = bstack1l1_opy_ (u"ࠫࠬ೺")
        bstack1l1ll1lll_opy_ = bstack1l1_opy_ (u"ࠬ࠭೻")
        bstack1ll1l11ll_opy_ = bstack1l1_opy_ (u"࠭ࠧ೼")
        try:
          import traceback
          bstack1111l1ll_opy_ = self.exception.__class__.__name__
          bstack111ll11l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1l1ll1lll_opy_ = bstack1l1_opy_ (u"ࠧࠡࠩ೽").join(bstack111ll11l_opy_)
          bstack1ll1l11ll_opy_ = bstack111ll11l_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l1l111ll_opy_.format(str(e)))
        bstack1111l1ll_opy_ += bstack1ll1l11ll_opy_
        bstack1l11lll11_opy_(context, json.dumps(str(args[0].name) + bstack1l1_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ೾") + str(bstack1l1ll1lll_opy_)), bstack1l1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ೿"))
        if self.driver_before_scenario:
          bstack11ll1ll1l_opy_(context, bstack1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥഀ"), bstack1111l1ll_opy_)
        context.browser.execute_script(bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩഁ") + json.dumps(str(args[0].name) + bstack1l1_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦം") + str(bstack1l1ll1lll_opy_)) + bstack1l1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ഃ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧഄ") + json.dumps(bstack1l1_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧഅ") + str(bstack1111l1ll_opy_)) + bstack1l1_opy_ (u"ࠩࢀࢁࠬആ"))
      else:
        bstack1l11lll11_opy_(context, bstack1l1_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦഇ"), bstack1l1_opy_ (u"ࠦ࡮ࡴࡦࡰࠤഈ"))
        if self.driver_before_scenario:
          bstack11ll1ll1l_opy_(context, bstack1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧഉ"))
        context.browser.execute_script(bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫഊ") + json.dumps(str(args[0].name) + bstack1l1_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦഋ")) + bstack1l1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧഌ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡴࡦࡹࡳࡦࡦࠥࢁࢂ࠭഍"))
    except Exception as e:
      logger.debug(bstack1l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬഎ").format(str(e)))
  if name == bstack1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫഏ"):
    try:
      if context.failed is True:
        bstack11lll1l_opy_ = []
        bstack1l111ll1_opy_ = []
        bstack1ll1lll_opy_ = []
        bstack11l11l1l1_opy_ = bstack1l1_opy_ (u"ࠬ࠭ഐ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack11lll1l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack111ll11l_opy_ = traceback.format_tb(exc_tb)
            bstack1l1l1ll11_opy_ = bstack1l1_opy_ (u"࠭ࠠࠨ഑").join(bstack111ll11l_opy_)
            bstack1l111ll1_opy_.append(bstack1l1l1ll11_opy_)
            bstack1ll1lll_opy_.append(bstack111ll11l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1l111ll_opy_.format(str(e)))
        bstack1111l1ll_opy_ = bstack1l1_opy_ (u"ࠧࠨഒ")
        for i in range(len(bstack11lll1l_opy_)):
          bstack1111l1ll_opy_ += bstack11lll1l_opy_[i] + bstack1ll1lll_opy_[i] + bstack1l1_opy_ (u"ࠨ࡞ࡱࠫഓ")
        bstack11l11l1l1_opy_ = bstack1l1_opy_ (u"ࠩࠣࠫഔ").join(bstack1l111ll1_opy_)
        if not self.driver_before_scenario:
          bstack1l11lll11_opy_(context, bstack11l11l1l1_opy_, bstack1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤക"))
          bstack11ll1ll1l_opy_(context, bstack1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦഖ"), bstack1111l1ll_opy_)
          context.browser.execute_script(bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪഗ") + json.dumps(bstack11l11l1l1_opy_) + bstack1l1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ഘ"))
          context.browser.execute_script(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧങ") + json.dumps(bstack1l1_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨച") + str(bstack1111l1ll_opy_)) + bstack1l1_opy_ (u"ࠩࢀࢁࠬഛ"))
      else:
        if not self.driver_before_scenario:
          bstack1l11lll11_opy_(context, bstack1l1_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨജ") + str(self.feature.name) + bstack1l1_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨഝ"), bstack1l1_opy_ (u"ࠧ࡯࡮ࡧࡱࠥഞ"))
          bstack11ll1ll1l_opy_(context, bstack1l1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨട"))
          context.browser.execute_script(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬഠ") + json.dumps(bstack1l1_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦഡ") + str(self.feature.name) + bstack1l1_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦഢ")) + bstack1l1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩണ"))
          context.browser.execute_script(bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧࡶࡡࡴࡵࡨࡨࠧࢃࡽࠨത"))
    except Exception as e:
      logger.debug(bstack1l1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧഥ").format(str(e)))
  if name in [bstack1l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ദ"), bstack1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨധ")]:
    bstack1lllll1_opy_(self, name, context, *args)
    if (name == bstack1l1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩന") and self.driver_before_scenario) or (name == bstack1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩഩ") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack11lll1l11_opy_(config, startdir):
  return bstack1l1_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣപ").format(bstack1l1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥഫ"))
class Notset:
  def __repr__(self):
    return bstack1l1_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢബ")
notset = Notset()
def bstack11lll11ll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack111llll_opy_
  if str(name).lower() == bstack1l1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ഭ"):
    return bstack1l1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨമ")
  else:
    return bstack111llll_opy_(self, name, default, skip)
def bstack11ll1111l_opy_(item, when):
  global bstack1ll111l1l_opy_
  try:
    bstack1ll111l1l_opy_(item, when)
  except Exception as e:
    pass
def bstack1lll11l_opy_():
  return
def bstack11l1ll11_opy_(framework_name):
  global bstack1111l11_opy_
  global bstack11lllll_opy_
  bstack1111l11_opy_ = framework_name
  logger.info(bstack11l1l111l_opy_.format(bstack1111l11_opy_.split(bstack1l1_opy_ (u"ࠨ࠯ࠪയ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack1ll11111_opy_
    Service.stop = bstack1ll1ll1l1_opy_
    webdriver.Remote.__init__ = bstack1ll111ll_opy_
    webdriver.Remote.get = bstack11ll1ll_opy_
    WebDriver.close = bstack1l1l1l1l1_opy_
    bstack11lllll_opy_ = True
  except Exception as e:
    pass
  bstack1l1l1l1_opy_()
  if not bstack11lllll_opy_:
    bstack11lllll1_opy_(bstack1l1_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦര"), bstack1l1l1llll_opy_)
  if bstack11l1111l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l1l1l1ll_opy_
    except Exception as e:
      logger.error(bstack11lllll1l_opy_.format(str(e)))
  if (bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩറ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack111ll11_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l111111_opy_
      except Exception as e:
        logger.warn(bstack1ll11ll11_opy_ + str(e))
    except Exception as e:
      bstack11lllll1_opy_(e, bstack1ll11ll11_opy_)
    Output.end_test = bstack1ll111l_opy_
    TestStatus.__init__ = bstack1lllllll_opy_
    QueueItem.__init__ = bstack1l1l1l11l_opy_
    pabot._create_items = bstack1111l1l_opy_
    try:
      from pabot import __version__ as bstack11l11lll_opy_
      if version.parse(bstack11l11lll_opy_) >= version.parse(bstack1l1_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫല")):
        pabot._run = bstack1llll1l1_opy_
      elif version.parse(bstack11l11lll_opy_) >= version.parse(bstack1l1_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬള")):
        pabot._run = bstack11ll11l1l_opy_
      else:
        pabot._run = bstack1lll1l11l_opy_
    except Exception as e:
      pabot._run = bstack1lll1l11l_opy_
    pabot._create_command_for_execution = bstack1ll1l11l1_opy_
    pabot._report_results = bstack1ll111111_opy_
  if bstack1l1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ഴ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11lllll1_opy_(e, bstack1l1l1_opy_)
    Runner.run_hook = bstack1111l111_opy_
    Step.run = bstack11ll1_opy_
  if bstack1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧവ") in str(framework_name).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      from _pytest import runner
      pytest_selenium.pytest_report_header = bstack11lll1l11_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1lll11l_opy_
      Config.getoption = bstack11lll11ll_opy_
      runner._update_current_test_var = bstack11ll1111l_opy_
    except Exception as e:
      pass
def bstack1l1ll1111_opy_():
  global CONFIG
  if bstack1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨശ") in CONFIG and int(CONFIG[bstack1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩഷ")]) > 1:
    logger.warn(bstack11ll1l111_opy_)
def bstack1l11ll_opy_(arg):
  arg.append(bstack1l1_opy_ (u"ࠥ࠱࠲ࡩࡡࡱࡶࡸࡶࡪࡃࡳࡺࡵࠥസ"))
  arg.append(bstack1l1_opy_ (u"ࠦ࠲࡝ࠢഹ"))
  arg.append(bstack1l1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣഺ"))
  global CONFIG
  bstack11l1ll11_opy_(bstack1lllll111_opy_)
  os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋ഻ࠧ")] = CONFIG[bstack1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦ഼ࠩ")]
  os.environ[bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫഽ")] = CONFIG[bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬാ")]
  from _pytest.config import main as bstack1l11l1ll1_opy_
  bstack1l11l1ll1_opy_(arg)
def bstack1l11lllll_opy_(arg):
  bstack11l1ll11_opy_(bstack111ll1l_opy_)
  from behave.__main__ import main as bstack1ll1ll11_opy_
  bstack1ll1ll11_opy_(arg)
def bstack1l1ll1ll1_opy_():
  logger.info(bstack1ll1ll1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩി"), help=bstack1l1_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࠬീ"))
  parser.add_argument(bstack1l1_opy_ (u"ࠬ࠳ࡵࠨു"), bstack1l1_opy_ (u"࠭࠭࠮ࡷࡶࡩࡷࡴࡡ࡮ࡧࠪൂ"), help=bstack1l1_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪ࠭ൃ"))
  parser.add_argument(bstack1l1_opy_ (u"ࠨ࠯࡮ࠫൄ"), bstack1l1_opy_ (u"ࠩ࠰࠱ࡰ࡫ࡹࠨ൅"), help=bstack1l1_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠫെ"))
  parser.add_argument(bstack1l1_opy_ (u"ࠫ࠲࡬ࠧേ"), bstack1l1_opy_ (u"ࠬ࠳࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪൈ"), help=bstack1l1_opy_ (u"࡙࠭ࡰࡷࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൉"))
  bstack11ll1l11l_opy_ = parser.parse_args()
  try:
    bstack1l111llll_opy_ = bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡰࡨࡶ࡮ࡩ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫൊ")
    if bstack11ll1l11l_opy_.framework and bstack11ll1l11l_opy_.framework not in (bstack1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨോ"), bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪൌ")):
      bstack1l111llll_opy_ = bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦ്ࠩ")
    bstack1llll1ll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l111llll_opy_)
    bstack1l1lll1_opy_ = open(bstack1llll1ll1_opy_, bstack1l1_opy_ (u"ࠫࡷ࠭ൎ"))
    bstack1l1111l_opy_ = bstack1l1lll1_opy_.read()
    bstack1l1lll1_opy_.close()
    if bstack11ll1l11l_opy_.username:
      bstack1l1111l_opy_ = bstack1l1111l_opy_.replace(bstack1l1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ൏"), bstack11ll1l11l_opy_.username)
    if bstack11ll1l11l_opy_.key:
      bstack1l1111l_opy_ = bstack1l1111l_opy_.replace(bstack1l1_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ൐"), bstack11ll1l11l_opy_.key)
    if bstack11ll1l11l_opy_.framework:
      bstack1l1111l_opy_ = bstack1l1111l_opy_.replace(bstack1l1_opy_ (u"࡚ࠧࡑࡘࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ൑"), bstack11ll1l11l_opy_.framework)
    file_name = bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ൒")
    file_path = os.path.abspath(file_name)
    bstack1l1l111_opy_ = open(file_path, bstack1l1_opy_ (u"ࠩࡺࠫ൓"))
    bstack1l1l111_opy_.write(bstack1l1111l_opy_)
    bstack1l1l111_opy_.close()
    logger.info(bstack1l11l1l_opy_)
    try:
      os.environ[bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬൔ")] = bstack11ll1l11l_opy_.framework if bstack11ll1l11l_opy_.framework != None else bstack1l1_opy_ (u"ࠦࠧൕ")
      config = yaml.safe_load(bstack1l1111l_opy_)
      config[bstack1l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬൖ")] = bstack1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡳࡦࡶࡸࡴࠬൗ")
      bstack1l11l1ll_opy_(bstack11ll1ll11_opy_, config)
    except Exception as e:
      logger.debug(bstack1l11ll1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll11l1l1_opy_.format(str(e)))
def bstack1l11l1ll_opy_(bstack1l11llll1_opy_, config, bstack11lll11_opy_ = {}):
  global bstack11ll1lll_opy_
  if not config:
    return
  bstack1l11llll_opy_ = bstack1ll1l111l_opy_ if not bstack11ll1lll_opy_ else ( bstack1l11ll111_opy_ if bstack1l1_opy_ (u"ࠧࡢࡲࡳࠫ൘") in config else bstack1llll1l1l_opy_ )
  data = {
    bstack1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ൙"): config[bstack1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ൚")],
    bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭൛"): config[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ൜")],
    bstack1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ൝"): bstack1l11llll1_opy_,
    bstack1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ൞"): {
      bstack1l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬൟ"): str(config[bstack1l1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨൠ")]) if bstack1l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩൡ") in config else bstack1l1_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦൢ"),
      bstack1l1_opy_ (u"ࠫࡷ࡫ࡦࡦࡴࡵࡩࡷ࠭ൣ"): bstack11ll111l1_opy_(os.getenv(bstack1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢ൤"), bstack1l1_opy_ (u"ࠨࠢ൥"))),
      bstack1l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ൦"): bstack1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ൧"),
      bstack1l1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ൨"): bstack1l11llll_opy_,
      bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭൩"): config[bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ൪")]if config[bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ൫")] else bstack1l1_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ൬"),
      bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ൭"): str(config[bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ൮")]) if bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൯") in config else bstack1l1_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ൰"),
      bstack1l1_opy_ (u"ࠫࡴࡹࠧ൱"): sys.platform,
      bstack1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ൲"): socket.gethostname()
    }
  }
  update(data[bstack1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ൳")], bstack11lll11_opy_)
  try:
    response = bstack1l11111_opy_(bstack1l1_opy_ (u"ࠧࡑࡑࡖࡘࠬ൴"), bstack11l11l11l_opy_, data, config)
    if response:
      logger.debug(bstack111l11_opy_.format(bstack1l11llll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11111l1l_opy_.format(str(e)))
def bstack1l11111_opy_(type, url, data, config):
  bstack1lll1ll_opy_ = bstack11l1ll1_opy_.format(url)
  proxies = bstack1lllll_opy_(config, bstack1lll1ll_opy_)
  if type == bstack1l1_opy_ (u"ࠨࡒࡒࡗ࡙࠭൵"):
    response = requests.post(bstack1lll1ll_opy_, json=data,
                    headers={bstack1l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ൶"): bstack1l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭൷")}, auth=(config[bstack1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭൸")], config[bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ൹")]), proxies=proxies)
  return response
def bstack11ll111l1_opy_(framework):
  return bstack1l1_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥൺ").format(str(framework), __version__) if framework else bstack1l1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣൻ").format(__version__)
def bstack1ll1111l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1l1lll11l_opy_()
    logger.debug(bstack1l111ll11_opy_.format(str(CONFIG)))
    bstack1l11ll11_opy_()
    bstack1l11l111l_opy_()
  except Exception as e:
    logger.error(bstack1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧർ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1111ll11_opy_
  atexit.register(bstack11ll1111_opy_)
  signal.signal(signal.SIGINT, bstack11llll11_opy_)
  signal.signal(signal.SIGTERM, bstack11llll11_opy_)
def bstack1111ll11_opy_(exctype, value, traceback):
  global bstack1ll11l111_opy_
  try:
    for driver in bstack1ll11l111_opy_:
      driver.execute_script(
        bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩൽ") + json.dumps(bstack1l1_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨൾ") + str(value)) + bstack1l1_opy_ (u"ࠫࢂࢃࠧൿ"))
  except Exception:
    pass
  bstack1l111lll_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l111lll_opy_(message = bstack1l1_opy_ (u"ࠬ࠭඀")):
  global CONFIG
  try:
    if message:
      bstack11lll11_opy_ = {
        bstack1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬඁ"): str(message)
      }
      bstack1l11l1ll_opy_(bstack111111l1_opy_, CONFIG, bstack11lll11_opy_)
    else:
      bstack1l11l1ll_opy_(bstack111111l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l11ll_opy_.format(str(e)))
def bstack1111l11l_opy_(bstack1lll11l1_opy_, size):
  bstack11l1lll11_opy_ = []
  while len(bstack1lll11l1_opy_) > size:
    bstack1l111l1l1_opy_ = bstack1lll11l1_opy_[:size]
    bstack11l1lll11_opy_.append(bstack1l111l1l1_opy_)
    bstack1lll11l1_opy_   = bstack1lll11l1_opy_[size:]
  bstack11l1lll11_opy_.append(bstack1lll11l1_opy_)
  return bstack11l1lll11_opy_
def run_on_browserstack(bstack1l111l111_opy_=None, bstack1lll1ll1l_opy_=None):
  global CONFIG
  global bstack1llll1lll_opy_
  bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠧࠨං")
  if bstack1l111l111_opy_:
    CONFIG = bstack1l111l111_opy_[bstack1l1_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨඃ")]
    bstack1llll1lll_opy_ = bstack1l111l111_opy_[bstack1l1_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ඄")]
    bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪඅ")
  if len(sys.argv) <= 1:
    logger.critical(bstack11l1l1l_opy_)
    return
  if sys.argv[1] == bstack1l1_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧආ")  or sys.argv[1] == bstack1l1_opy_ (u"ࠬ࠳ࡶࠨඇ"):
    logger.info(bstack1l1_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭ඈ").format(__version__))
    return
  if sys.argv[1] == bstack1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ඉ"):
    bstack1l1ll1ll1_opy_()
    return
  args = sys.argv
  bstack1ll1111l_opy_()
  global bstack1l11l11_opy_
  global bstack11l111111_opy_
  global bstack1ll1l1ll1_opy_
  global bstack11111111_opy_
  global bstack1llllll11_opy_
  global bstack1lll1l11_opy_
  global bstack1l1lll_opy_
  if not bstack1l1llll1l_opy_:
    if args[1] == bstack1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨඊ") or args[1] == bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪඋ"):
      bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪඌ")
      args = args[2:]
    elif args[1] == bstack1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪඍ"):
      bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫඎ")
      args = args[2:]
    elif args[1] == bstack1l1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬඏ"):
      bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ඐ")
      args = args[2:]
    elif args[1] == bstack1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩඑ"):
      bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪඒ")
      args = args[2:]
    elif args[1] == bstack1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඓ"):
      bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫඔ")
      args = args[2:]
    elif args[1] == bstack1l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬඕ"):
      bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඖ")
      args = args[2:]
    else:
      if not bstack1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ඗") in CONFIG or str(CONFIG[bstack1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ඘")]).lower() in [bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ඙"), bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫක")]:
        bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫඛ")
        args = args[1:]
      elif str(CONFIG[bstack1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨග")]).lower() == bstack1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඝ"):
        bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ඞ")
        args = args[1:]
      elif str(CONFIG[bstack1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫඟ")]).lower() == bstack1l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨච"):
        bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩඡ")
        args = args[1:]
      elif str(CONFIG[bstack1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧජ")]).lower() == bstack1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬඣ"):
        bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ඤ")
        args = args[1:]
      elif str(CONFIG[bstack1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඥ")]).lower() == bstack1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨඦ"):
        bstack1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩට")
        args = args[1:]
      else:
        os.environ[bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬඨ")] = bstack1l1llll1l_opy_
        bstack11l111l11_opy_(bstack1l11l1lll_opy_)
  global bstack1l1l1ll_opy_
  if bstack1l111l111_opy_:
    try:
      os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ඩ")] = bstack1l1llll1l_opy_
      bstack1l11l1ll_opy_(bstack11ll1l11_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack11l11ll_opy_.format(str(e)))
  global bstack11ll_opy_
  global bstack1lll1l_opy_
  global bstack111llllll_opy_
  global bstack11lll1ll_opy_
  global bstack11ll1llll_opy_
  global bstack11l111ll1_opy_
  global bstack11l1ll11l_opy_
  global bstack1llll1ll_opy_
  global bstack1lllll11l_opy_
  global bstack1lllll1_opy_
  global bstack1l1l11l1_opy_
  global bstack11llll_opy_
  global bstack111l1ll_opy_
  global bstack111llll_opy_
  global bstack1ll111l1l_opy_
  global bstack11111l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll_opy_ = webdriver.Remote.__init__
    bstack1lllll11l_opy_ = WebDriver.close
    bstack11llll_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1l1ll_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack11l11lll1_opy_():
    if bstack1lllll1ll_opy_() < version.parse(bstack1lll1l1l1_opy_):
      logger.error(bstack1l11111ll_opy_.format(bstack1lllll1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack111l1ll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11lllll1l_opy_.format(str(e)))
  if bstack1l1llll1l_opy_ != bstack1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬඪ") or (bstack1l1llll1l_opy_ == bstack1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ණ") and not bstack1l111l111_opy_):
    bstack1ll11l11_opy_()
  if (bstack1l1llll1l_opy_ in [bstack1l1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ඬ"), bstack1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧත"), bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪථ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack111ll11_opy_
        bstack111llllll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll11ll11_opy_ + str(e))
    except Exception as e:
      bstack11lllll1_opy_(e, bstack1ll11ll11_opy_)
    if bstack1l1llll1l_opy_ != bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫද"):
      bstack11lll111l_opy_()
    bstack1lll1l_opy_ = Output.end_test
    bstack11lll1ll_opy_ = TestStatus.__init__
    bstack11l111ll1_opy_ = pabot._run
    bstack11l1ll11l_opy_ = QueueItem.__init__
    bstack1llll1ll_opy_ = pabot._create_command_for_execution
    bstack11111l_opy_ = pabot._report_results
  if bstack1l1llll1l_opy_ == bstack1l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫධ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11lllll1_opy_(e, bstack1l1l1_opy_)
    bstack1lllll1_opy_ = Runner.run_hook
    bstack1l1l11l1_opy_ = Step.run
  if bstack1l1llll1l_opy_ == bstack1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬන"):
    try:
      from _pytest.config import Config
      bstack111llll_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll111l1l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l111ll1l_opy_)
  if bstack1l1llll1l_opy_ == bstack1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭඲"):
    bstack11l111111_opy_ = True
    if bstack1l111l111_opy_:
      bstack1llllll11_opy_ = CONFIG.get(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫඳ"), {}).get(bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪප"))
      bstack11l1ll11_opy_(bstack11lll111_opy_)
      sys.path.append(os.path.dirname(os.path.abspath(bstack1l111l111_opy_[bstack1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬඵ")])))
      mod_globals = globals()
      mod_globals[bstack1l1_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬබ")] = bstack1l1_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭භ")
      mod_globals[bstack1l1_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧම")] = os.path.abspath(bstack1l111l111_opy_[bstack1l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඹ")])
      global bstack1ll11l111_opy_
      try:
        exec(open(bstack1l111l111_opy_[bstack1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪය")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l1_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨර").format(str(e)))
          for driver in bstack1ll11l111_opy_:
            bstack1lll1ll1l_opy_.append({
              bstack1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ඼"): bstack1l111l111_opy_[bstack1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ල")],
              bstack1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ඾"): str(e),
              bstack1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ඿"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡧࡣ࡬ࡰࡪࡪࠢ࠭ࠢࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠥ࠭ව") + json.dumps(bstack1l1_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥශ") + str(e)) + bstack1l1_opy_ (u"ࠨࡿࢀࠫෂ"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll11l111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      bstack1l1ll11l1_opy_()
      bstack1l1ll1111_opy_()
      if bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬස") in CONFIG:
        bstack1l1l1lll1_opy_ = {
          bstack1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭හ"): args[0],
          bstack1l1_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫළ"): CONFIG,
          bstack1l1_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ෆ"): bstack1llll1lll_opy_
        }
        bstack11l11llll_opy_ = []
        manager = multiprocessing.Manager()
        bstack11lll1ll1_opy_ = manager.list()
        for index, platform in enumerate(CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෇")]):
          bstack1l1l1lll1_opy_[bstack1l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭෈")] = index
          bstack11l11llll_opy_.append(multiprocessing.Process(name=str(index),
                                        target=run_on_browserstack, args=(bstack1l1l1lll1_opy_, bstack11lll1ll1_opy_)))
        for t in bstack11l11llll_opy_:
          t.start()
        for t in bstack11l11llll_opy_:
          t.join()
        bstack1l1lll_opy_ = list(bstack11lll1ll1_opy_)
      else:
        bstack11l1ll11_opy_(bstack11lll111_opy_)
        sys.path.append(os.path.dirname(os.path.abspath(args[0])))
        mod_globals = globals()
        mod_globals[bstack1l1_opy_ (u"ࠨࡡࡢࡲࡦࡳࡥࡠࡡࠪ෉")] = bstack1l1_opy_ (u"ࠩࡢࡣࡲࡧࡩ࡯ࡡࡢ්ࠫ")
        mod_globals[bstack1l1_opy_ (u"ࠪࡣࡤ࡬ࡩ࡭ࡧࡢࡣࠬ෋")] = os.path.abspath(args[0])
        exec(open(args[0]).read(), mod_globals)
  elif bstack1l1llll1l_opy_ == bstack1l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ෌") or bstack1l1llll1l_opy_ == bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ෍"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack11lllll1_opy_(e, bstack1ll11ll11_opy_)
    bstack1l1ll11l1_opy_()
    bstack11l1ll11_opy_(bstack1llll11l_opy_)
    if bstack1l1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ෎") in args:
      i = args.index(bstack1l1_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬා"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l11l11_opy_))
    args.insert(0, str(bstack1l1_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ැ")))
    pabot.main(args)
  elif bstack1l1llll1l_opy_ == bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪෑ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11lllll1_opy_(e, bstack1ll11ll11_opy_)
    for a in args:
      if bstack1l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩි") in a:
        bstack11111111_opy_ = int(a.split(bstack1l1_opy_ (u"ࠫ࠿࠭ී"))[1])
      if bstack1l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩු") in a:
        bstack1llllll11_opy_ = str(a.split(bstack1l1_opy_ (u"࠭࠺ࠨ෕"))[1])
      if bstack1l1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧූ") in a:
        bstack1lll1l11_opy_ = str(a.split(bstack1l1_opy_ (u"ࠨ࠼ࠪ෗"))[1])
    bstack111ll1l1_opy_ = None
    if bstack1l1_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨෘ") in args:
      i = args.index(bstack1l1_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩෙ"))
      args.pop(i)
      bstack111ll1l1_opy_ = args.pop(i)
    if bstack111ll1l1_opy_ is not None:
      global bstack1l1ll11_opy_
      bstack1l1ll11_opy_ = bstack111ll1l1_opy_
    bstack11l1ll11_opy_(bstack1llll11l_opy_)
    run_cli(args)
  elif bstack1l1llll1l_opy_ == bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫේ"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack1l1l11ll_opy_ = importlib.find_loader(bstack1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧෛ"))
    except Exception as e:
      logger.warn(e, bstack1l111ll1l_opy_)
    bstack1l1ll11l1_opy_()
    try:
      if bstack1l1_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨො") in args:
        i = args.index(bstack1l1_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩෝ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫෞ") in args:
        i = args.index(bstack1l1_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬෟ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1_opy_ (u"ࠪ࠱ࡵ࠭෠") in args:
        i = args.index(bstack1l1_opy_ (u"ࠫ࠲ࡶࠧ෡"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭෢") in args:
        i = args.index(bstack1l1_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ෣"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1_opy_ (u"ࠧ࠮ࡰࠪ෤") in args:
        i = args.index(bstack1l1_opy_ (u"ࠨ࠯ࡱࠫ෥"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1llll111_opy_ = config.args
    bstack1l11l111_opy_ = config.invocation_params.args
    bstack1l11l111_opy_ = list(bstack1l11l111_opy_)
    bstack111ll1_opy_ = []
    for arg in bstack1l11l111_opy_:
      for spec in bstack1llll111_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack111ll1_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l1_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪ෦"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1llll111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l111lll1_opy_)))
                    for bstack1l111lll1_opy_ in bstack1llll111_opy_]
    if (bstack1lll1lll1_opy_):
      bstack111ll1_opy_.append(bstack1l1_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ෧"))
      bstack111ll1_opy_.append(bstack1l1_opy_ (u"࡙ࠫࡸࡵࡦࠩ෨"))
    bstack111ll1_opy_.append(bstack1l1_opy_ (u"ࠬ࠳ࡰࠨ෩"))
    bstack111ll1_opy_.append(bstack1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫ෪"))
    bstack111ll1_opy_.append(bstack1l1_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩ෫"))
    bstack111ll1_opy_.append(bstack1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ෬"))
    bstack1l11l11l_opy_ = []
    for spec in bstack1llll111_opy_:
      bstack11ll11111_opy_ = []
      bstack11ll11111_opy_.append(spec)
      bstack11ll11111_opy_ += bstack111ll1_opy_
      bstack1l11l11l_opy_.append(bstack11ll11111_opy_)
    bstack1ll1l1ll1_opy_ = True
    bstack1l1lllll1_opy_ = 1
    if bstack1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ෭") in CONFIG:
      bstack1l1lllll1_opy_ = CONFIG[bstack1l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ෮")]
    bstack1l11lll1l_opy_ = int(bstack1l1lllll1_opy_)*int(len(CONFIG[bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෯")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ෰")]):
      for bstack11ll11111_opy_ in bstack1l11l11l_opy_:
        item = {}
        item[bstack1l1_opy_ (u"࠭ࡡࡳࡩࠪ෱")] = bstack11ll11111_opy_
        item[bstack1l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ෲ")] = index
        execution_items.append(item)
    bstack11l111_opy_ = bstack1111l11l_opy_(execution_items, bstack1l11lll1l_opy_)
    for execution_item in bstack11l111_opy_:
      bstack11l11llll_opy_ = []
      for item in execution_item:
        bstack11l11llll_opy_.append(bstack11l1l1l1_opy_(name=str(item[bstack1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧෳ")]),
                                            target=bstack1l11ll_opy_,
                                            args=(item[bstack1l1_opy_ (u"ࠩࡤࡶ࡬࠭෴")],)))
      for t in bstack11l11llll_opy_:
        t.start()
      for t in bstack11l11llll_opy_:
        t.join()
  elif bstack1l1llll1l_opy_ == bstack1l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෵"):
    try:
      from behave.__main__ import main as bstack1ll1ll11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11lllll1_opy_(e, bstack1l1l1_opy_)
    bstack1l1ll11l1_opy_()
    bstack1ll1l1ll1_opy_ = True
    bstack1l1lllll1_opy_ = 1
    if bstack1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෶") in CONFIG:
      bstack1l1lllll1_opy_ = CONFIG[bstack1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ෷")]
    bstack1l11lll1l_opy_ = int(bstack1l1lllll1_opy_)*int(len(CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෸")]))
    config = Configuration(args)
    bstack1llll111_opy_ = config.paths
    bstack11llll1ll_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack1llll111_opy_:
        bstack11llll1ll_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l1_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨ෹"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1llll111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l111lll1_opy_)))
                    for bstack1l111lll1_opy_ in bstack1llll111_opy_]
    bstack1l11l11l_opy_ = []
    for spec in bstack1llll111_opy_:
      bstack11ll11111_opy_ = []
      bstack11ll11111_opy_ += bstack11llll1ll_opy_
      bstack11ll11111_opy_.append(spec)
      bstack1l11l11l_opy_.append(bstack11ll11111_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ෺")]):
      for bstack11ll11111_opy_ in bstack1l11l11l_opy_:
        item = {}
        item[bstack1l1_opy_ (u"ࠩࡤࡶ࡬࠭෻")] = bstack1l1_opy_ (u"ࠪࠤࠬ෼").join(bstack11ll11111_opy_)
        item[bstack1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ෽")] = index
        execution_items.append(item)
    bstack11l111_opy_ = bstack1111l11l_opy_(execution_items, bstack1l11lll1l_opy_)
    for execution_item in bstack11l111_opy_:
      bstack11l11llll_opy_ = []
      for item in execution_item:
        bstack11l11llll_opy_.append(bstack11l1l1l1_opy_(name=str(item[bstack1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ෾")]),
                                            target=bstack1l11lllll_opy_,
                                            args=(item[bstack1l1_opy_ (u"࠭ࡡࡳࡩࠪ෿")],)))
      for t in bstack11l11llll_opy_:
        t.start()
      for t in bstack11l11llll_opy_:
        t.join()
  else:
    bstack11l111l11_opy_(bstack1l11l1lll_opy_)
  if not bstack1l111l111_opy_:
    bstack1l11l1_opy_()
def bstack1l11l1_opy_():
  [bstack11l1_opy_, bstack11l1l111_opy_] = bstack1ll11llll_opy_()
  if bstack11l1_opy_ is not None and bstack111lllll_opy_() != -1:
    sessions = bstack1ll111ll1_opy_(bstack11l1_opy_)
    bstack1lll11l11_opy_(sessions, bstack11l1l111_opy_)
def bstack1llll_opy_(bstack11l1ll1ll_opy_):
    if bstack11l1ll1ll_opy_:
        return bstack11l1ll1ll_opy_.capitalize()
    else:
        return bstack11l1ll1ll_opy_
def bstack1l1l1l_opy_(bstack1ll1111ll_opy_):
    if bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ฀") in bstack1ll1111ll_opy_ and bstack1ll1111ll_opy_[bstack1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ก")] != bstack1l1_opy_ (u"ࠩࠪข"):
        return bstack1ll1111ll_opy_[bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨฃ")]
    else:
        bstack1111_opy_ = bstack1l1_opy_ (u"ࠦࠧค")
        if bstack1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬฅ") in bstack1ll1111ll_opy_ and bstack1ll1111ll_opy_[bstack1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ฆ")] != None:
            bstack1111_opy_ += bstack1ll1111ll_opy_[bstack1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧง")] + bstack1l1_opy_ (u"ࠣ࠮ࠣࠦจ")
            if bstack1ll1111ll_opy_[bstack1l1_opy_ (u"ࠩࡲࡷࠬฉ")] == bstack1l1_opy_ (u"ࠥ࡭ࡴࡹࠢช"):
                bstack1111_opy_ += bstack1l1_opy_ (u"ࠦ࡮ࡕࡓࠡࠤซ")
            bstack1111_opy_ += (bstack1ll1111ll_opy_[bstack1l1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩฌ")] or bstack1l1_opy_ (u"࠭ࠧญ"))
            return bstack1111_opy_
        else:
            bstack1111_opy_ += bstack1llll_opy_(bstack1ll1111ll_opy_[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨฎ")]) + bstack1l1_opy_ (u"ࠣࠢࠥฏ") + (bstack1ll1111ll_opy_[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫฐ")] or bstack1l1_opy_ (u"ࠪࠫฑ")) + bstack1l1_opy_ (u"ࠦ࠱ࠦࠢฒ")
            if bstack1ll1111ll_opy_[bstack1l1_opy_ (u"ࠬࡵࡳࠨณ")] == bstack1l1_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢด"):
                bstack1111_opy_ += bstack1l1_opy_ (u"ࠢࡘ࡫ࡱࠤࠧต")
            bstack1111_opy_ += bstack1ll1111ll_opy_[bstack1l1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬถ")] or bstack1l1_opy_ (u"ࠩࠪท")
            return bstack1111_opy_
def bstack1l1llllll_opy_(bstack1ll11l1l_opy_):
    if bstack1ll11l1l_opy_ == bstack1l1_opy_ (u"ࠥࡨࡴࡴࡥࠣธ"):
        return bstack1l1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧน")
    elif bstack1ll11l1l_opy_ == bstack1l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧบ"):
        return bstack1l1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩป")
    elif bstack1ll11l1l_opy_ == bstack1l1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢผ"):
        return bstack1l1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨฝ")
    elif bstack1ll11l1l_opy_ == bstack1l1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣพ"):
        return bstack1l1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬฟ")
    elif bstack1ll11l1l_opy_ == bstack1l1_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧภ"):
        return bstack1l1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪม")
    elif bstack1ll11l1l_opy_ == bstack1l1_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢย"):
        return bstack1l1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨร")
    else:
        return bstack1l1_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬฤ")+bstack1llll_opy_(bstack1ll11l1l_opy_)+bstack1l1_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨล")
def bstack1lll1l1_opy_(session):
    return bstack1l1_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪฦ").format(session[bstack1l1_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨว")],bstack1l1l1l_opy_(session), bstack1l1llllll_opy_(session[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫศ")]), bstack1l1llllll_opy_(session[bstack1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ษ")]), bstack1llll_opy_(session[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨส")] or session[bstack1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨห")] or bstack1l1_opy_ (u"ࠩࠪฬ")) + bstack1l1_opy_ (u"ࠥࠤࠧอ") + (session[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ฮ")] or bstack1l1_opy_ (u"ࠬ࠭ฯ")), session[bstack1l1_opy_ (u"࠭࡯ࡴࠩะ")] + bstack1l1_opy_ (u"ࠢࠡࠤั") + session[bstack1l1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬา")], session[bstack1l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫำ")] or bstack1l1_opy_ (u"ࠪࠫิ"), session[bstack1l1_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨี")] if session[bstack1l1_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩึ")] else bstack1l1_opy_ (u"࠭ࠧื"))
def bstack1lll11l11_opy_(sessions, bstack11l1l111_opy_):
  try:
    bstack1ll1111l1_opy_ = bstack1l1_opy_ (u"ุࠢࠣ")
    if not os.path.exists(bstack1l1l11l11_opy_):
      os.mkdir(bstack1l1l11l11_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱู࠭")), bstack1l1_opy_ (u"ࠩࡵฺࠫ")) as f:
      bstack1ll1111l1_opy_ = f.read()
    bstack1ll1111l1_opy_ = bstack1ll1111l1_opy_.replace(bstack1l1_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧ฻"), str(len(sessions)))
    bstack1ll1111l1_opy_ = bstack1ll1111l1_opy_.replace(bstack1l1_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫ฼"), bstack11l1l111_opy_)
    bstack1ll1111l1_opy_ = bstack1ll1111l1_opy_.replace(bstack1l1_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭฽"), sessions[0].get(bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪ฾")) if sessions[0] else bstack1l1_opy_ (u"ࠧࠨ฿"))
    with open(os.path.join(bstack1l1l11l11_opy_, bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬเ")), bstack1l1_opy_ (u"ࠩࡺࠫแ")) as stream:
      stream.write(bstack1ll1111l1_opy_.split(bstack1l1_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧโ"))[0])
      for session in sessions:
        stream.write(bstack1lll1l1_opy_(session))
      stream.write(bstack1ll1111l1_opy_.split(bstack1l1_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨใ"))[1])
    logger.info(bstack1l1_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨไ").format(bstack1l1l11l11_opy_));
  except Exception as e:
    logger.debug(bstack1lll1llll_opy_.format(str(e)))
def bstack1ll111ll1_opy_(bstack11l1_opy_):
  global CONFIG
  try:
    host = bstack1l1_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩๅ") if bstack1l1_opy_ (u"ࠧࡢࡲࡳࠫๆ") in CONFIG else bstack1l1_opy_ (u"ࠨࡣࡳ࡭ࠬ็")
    user = CONFIG[bstack1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨ่ࠫ")]
    key = CONFIG[bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ้࠭")]
    bstack11ll1l1_opy_ = bstack1l1_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ๊ࠪ") if bstack1l1_opy_ (u"ࠬࡧࡰࡱ๋ࠩ") in CONFIG else bstack1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ์")
    url = bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬํ").format(user, key, host, bstack11ll1l1_opy_, bstack11l1_opy_)
    headers = {
      bstack1l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ๎"): bstack1l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ๏"),
    }
    proxies = bstack1lllll_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ๐")], response.json()))
  except Exception as e:
    logger.debug(bstack11l11ll1l_opy_.format(str(e)))
def bstack1ll11llll_opy_():
  global CONFIG
  try:
    if bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๑") in CONFIG:
      host = bstack1l1_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨ๒") if bstack1l1_opy_ (u"࠭ࡡࡱࡲࠪ๓") in CONFIG else bstack1l1_opy_ (u"ࠧࡢࡲ࡬ࠫ๔")
      user = CONFIG[bstack1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ๕")]
      key = CONFIG[bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ๖")]
      bstack11ll1l1_opy_ = bstack1l1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ๗") if bstack1l1_opy_ (u"ࠫࡦࡶࡰࠨ๘") in CONFIG else bstack1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ๙")
      url = bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭๚").format(user, key, host, bstack11ll1l1_opy_)
      headers = {
        bstack1l1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭๛"): bstack1l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ๜"),
      }
      if bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ๝") in CONFIG:
        params = {bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ๞"):CONFIG[bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ๟")], bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๠"):CONFIG[bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๡")]}
      else:
        params = {bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๢"):CONFIG[bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ๣")]}
      proxies = bstack1lllll_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1llll111l_opy_ = response.json()[0][bstack1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬ๤")]
        if bstack1llll111l_opy_:
          bstack11l1l111_opy_ = bstack1llll111l_opy_[bstack1l1_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ๥")].split(bstack1l1_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪ๦"))[0] + bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭๧") + bstack1llll111l_opy_[bstack1l1_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ๨")]
          logger.info(bstack1ll111l1_opy_.format(bstack11l1l111_opy_))
          bstack11ll11lll_opy_ = CONFIG[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ๩")]
          if bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๪") in CONFIG:
            bstack11ll11lll_opy_ += bstack1l1_opy_ (u"ࠩࠣࠫ๫") + CONFIG[bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ๬")]
          if bstack11ll11lll_opy_!= bstack1llll111l_opy_[bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ๭")]:
            logger.debug(bstack1l11l1l11_opy_.format(bstack1llll111l_opy_[bstack1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ๮")], bstack11ll11lll_opy_))
          return [bstack1llll111l_opy_[bstack1l1_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ๯")], bstack11l1l111_opy_]
    else:
      logger.warn(bstack111lll1_opy_)
  except Exception as e:
    logger.debug(bstack1ll1111_opy_.format(str(e)))
  return [None, None]
def bstack1l1l11_opy_(url, bstack111llll1_opy_=False):
  global CONFIG
  global bstack11l1lll_opy_
  if not bstack11l1lll_opy_:
    hostname = bstack1llll11l1_opy_(url)
    is_private = bstack1ll1l_opy_(hostname)
    if (bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ๰") in CONFIG and not CONFIG[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ๱")]) and (is_private or bstack111llll1_opy_):
      bstack11l1lll_opy_ = hostname
def bstack1llll11l1_opy_(url):
  return urlparse(url).hostname
def bstack1ll1l_opy_(hostname):
  for bstack1lll11ll_opy_ in bstack11111lll_opy_:
    regex = re.compile(bstack1lll11ll_opy_)
    if regex.match(hostname):
      return True
  return False