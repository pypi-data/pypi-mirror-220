# coding: UTF-8
import sys
bstack1l_opy_ = sys.version_info [0] == 2
bstack1l1l_opy_ = 2048
bstack1_opy_ = 7
def bstackl_opy_ (bstack11l_opy_):
    global bstack11_opy_
    stringNr = ord (bstack11l_opy_ [-1])
    bstack1ll_opy_ = bstack11l_opy_ [:-1]
    bstack111_opy_ = stringNr % len (bstack1ll_opy_)
    bstack1l1_opy_ = bstack1ll_opy_ [:bstack111_opy_] + bstack1ll_opy_ [bstack111_opy_:]
    if bstack1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l_opy_ - (bstack1ll1_opy_ + stringNr) % bstack1_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1l1l_opy_ - (bstack1ll1_opy_ + stringNr) % bstack1_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1_opy_)])
    return eval (bstack1lll_opy_)
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
bstack11ll1l111_opy_ = {
	bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstackl_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstackl_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstackl_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstackl_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstackl_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstackl_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstackl_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstackl_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstackl_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstackl_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstackl_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstackl_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstackl_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstackl_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstackl_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstackl_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstackl_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstackl_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstackl_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstackl_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstackl_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstackl_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstackl_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstackl_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack1111l_opy_ = [
  bstackl_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstackl_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstackl_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstackl_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack1l1ll11_opy_ = {
  bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstackl_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstackl_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack11l11l1l_opy_ = {
  bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstackl_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack1l11l1l_opy_ = {
  bstackl_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstackl_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstackl_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstackl_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstackl_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstackl_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstackl_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack1lll11l1_opy_ = [
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstackl_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstackl_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstackl_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstackl_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstackl_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstackl_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstackl_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack11l11l1_opy_ = [
  bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstackl_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack11lllll11_opy_ = [
  bstackl_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstackl_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstackl_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstackl_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstackl_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstackl_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstackl_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstackl_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstackl_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstackl_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstackl_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstackl_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstackl_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstackl_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstackl_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstackl_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstackl_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstackl_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstackl_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstackl_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstackl_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstackl_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstackl_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstackl_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstackl_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstackl_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstackl_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstackl_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstackl_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstackl_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstackl_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstackl_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstackl_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstackl_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstackl_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstackl_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstackl_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstackl_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstackl_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstackl_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstackl_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstackl_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstackl_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstackl_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstackl_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstackl_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstackl_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstackl_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstackl_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstackl_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstackl_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstackl_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstackl_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstackl_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstackl_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstackl_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstackl_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstackl_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstackl_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstackl_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstackl_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstackl_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstackl_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstackl_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstackl_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstackl_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstackl_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstackl_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstackl_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstackl_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1l111ll11_opy_ = {
  bstackl_opy_ (u"࠭ࡶࠨच"): bstackl_opy_ (u"ࠧࡷࠩछ"),
  bstackl_opy_ (u"ࠨࡨࠪज"): bstackl_opy_ (u"ࠩࡩࠫझ"),
  bstackl_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstackl_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstackl_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstackl_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstackl_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstackl_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstackl_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstackl_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstackl_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstackl_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstackl_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstackl_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstackl_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstackl_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstackl_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstackl_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstackl_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstackl_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstackl_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstackl_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstackl_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstackl_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack11llll_opy_ = bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1111l1l1_opy_ = bstackl_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack1l1l11l1l_opy_ = bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack1111llll_opy_ = {
  bstackl_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstackl_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstackl_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstackl_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstackl_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack1l1111l1l_opy_ = bstack1111llll_opy_[bstackl_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack11l111_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack11ll111l1_opy_ = bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1l1l1lll1_opy_ = bstackl_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1l1ll1ll_opy_ = bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack1l11ll1l1_opy_ = [bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstackl_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack1l11ll1_opy_ = [bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstackl_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack1ll111111_opy_ = [
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstackl_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstackl_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstackl_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstackl_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstackl_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstackl_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstackl_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstackl_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstackl_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstackl_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstackl_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstackl_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstackl_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstackl_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstackl_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstackl_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstackl_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstackl_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstackl_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstackl_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstackl_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstackl_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstackl_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstackl_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstackl_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstackl_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstackl_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstackl_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstackl_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstackl_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstackl_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstackl_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstackl_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstackl_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstackl_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstackl_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstackl_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstackl_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstackl_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstackl_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstackl_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstackl_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstackl_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstackl_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstackl_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstackl_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstackl_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstackl_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstackl_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstackl_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstackl_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstackl_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstackl_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstackl_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstackl_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstackl_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstackl_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstackl_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstackl_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstackl_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstackl_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstackl_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstackl_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstackl_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstackl_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstackl_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstackl_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstackl_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstackl_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstackl_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstackl_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstackl_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstackl_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstackl_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstackl_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstackl_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstackl_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstackl_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstackl_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstackl_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstackl_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstackl_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstackl_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstackl_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstackl_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstackl_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstackl_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstackl_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstackl_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstackl_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstackl_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstackl_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstackl_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstackl_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstackl_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstackl_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstackl_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstackl_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstackl_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstackl_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstackl_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstackl_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstackl_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstackl_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstackl_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstackl_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstackl_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstackl_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstackl_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstackl_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstackl_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstackl_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack1l11l1ll_opy_ = bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack11ll1111_opy_ = [bstackl_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstackl_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstackl_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack1l11ll11_opy_ = [bstackl_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstackl_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstackl_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstackl_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack1l11l11l1_opy_ = {
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstackl_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstackl_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstackl_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstackl_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstackl_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack1111l11_opy_ = [
  bstackl_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstackl_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstackl_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstackl_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstackl_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack1lll11ll_opy_ = bstack11l11l1_opy_ + bstack11lllll11_opy_ + bstack1ll111111_opy_
bstack1l1ll1l1_opy_ = [
  bstackl_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstackl_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstackl_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstackl_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstackl_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstackl_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstackl_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstackl_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack11l11lll_opy_ = bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack1llll11l_opy_ = bstackl_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack111l1ll_opy_ = [ bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack1lllll11l_opy_ = [ bstackl_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack1l1l11l11_opy_ = [ bstackl_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack1ll1ll_opy_ = bstackl_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack11111l1_opy_ = bstackl_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack1l111l1ll_opy_ = bstackl_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack111lll11_opy_ = bstackl_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack1ll1l1_opy_ = [
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
bstack1l1l111_opy_ = bstackl_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧਧ")
def bstack1111l111_opy_():
  global CONFIG
  headers = {
        bstackl_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩਨ"): bstackl_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ਩"),
      }
  proxy = bstack111111_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨਪ")) or CONFIG.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪਫ")):
    proxies = {
      bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ਬ"): proxy
    }
  try:
    response = requests.get(bstack1l1l11l1l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11ll11ll1_opy_ = response.json()[bstackl_opy_ (u"ࠨࡪࡸࡦࡸ࠭ਭ")]
      logger.debug(bstack11lll1lll_opy_.format(response.json()))
      return bstack11ll11ll1_opy_
    else:
      logger.debug(bstack1l1l11ll1_opy_.format(bstackl_opy_ (u"ࠤࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡏ࡙ࡏࡏࠢࡳࡥࡷࡹࡥࠡࡧࡵࡶࡴࡸࠠࠣਮ")))
  except Exception as e:
    logger.debug(bstack1l1l11ll1_opy_.format(e))
def bstack1l1lllll_opy_(hub_url):
  global CONFIG
  url = bstackl_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧਯ")+  hub_url + bstackl_opy_ (u"ࠦ࠴ࡩࡨࡦࡥ࡮ࠦਰ")
  headers = {
        bstackl_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ਱"): bstackl_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩਲ"),
      }
  proxy = bstack111111_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪਲ਼")) or CONFIG.get(bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ਴")):
    proxies = {
      bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨਵ"): proxy
    }
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll1l1l1l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l1l1ll11_opy_.format(hub_url, e))
def bstack1l1lll11l_opy_():
  try:
    global bstack1l111111_opy_
    bstack11ll11ll1_opy_ = bstack1111l111_opy_()
    with Pool() as pool:
      results = pool.map(bstack1l1lllll_opy_, bstack11ll11ll1_opy_)
    bstack11lll1l1_opy_ = {}
    for item in results:
      hub_url = item[bstackl_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫਸ਼")]
      latency = item[bstackl_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬ਷")]
      bstack11lll1l1_opy_[hub_url] = latency
    bstack11111ll_opy_ = min(bstack11lll1l1_opy_, key= lambda x: bstack11lll1l1_opy_[x])
    bstack1l111111_opy_ = bstack11111ll_opy_
    logger.debug(bstack1l11111ll_opy_.format(bstack11111ll_opy_))
  except Exception as e:
    logger.debug(bstack111l11_opy_.format(e))
bstack11ll1llll_opy_ = bstackl_opy_ (u"࡙ࠬࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠻ࠢࡾࢁࠬਸ")
bstack11l1ll11l_opy_ = bstackl_opy_ (u"࠭ࡃࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡶࡩࡹࡻࡰࠢࠩਹ")
bstack1l11lll1_opy_ = bstackl_opy_ (u"ࠧࡑࡣࡵࡷࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠩ਺")
bstack1l11l_opy_ = bstackl_opy_ (u"ࠨࡕࡤࡲ࡮ࡺࡩࡻࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂ࠭਻")
bstack1lll1lll1_opy_ = bstackl_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡪࡸࡦࠥࡻࡲ࡭࠼ࠣࡿࢂ਼࠭")
bstack1ll1l1l_opy_ = bstackl_opy_ (u"ࠪࡗࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࡼࡿࠪ਽")
bstack1l1l11l_opy_ = bstackl_opy_ (u"ࠫࡗ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡩ࡯ࡶࡨࡶࡷࡻࡰࡵ࠮ࠣࡩࡽ࡯ࡴࡪࡰࡪࠫਾ")
bstack1ll1l111l_opy_ = bstackl_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪਿ")
bstack1l1111l1_opy_ = bstackl_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡢࡰࡧࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫੀ")
bstack1ll1l11ll_opy_ = bstackl_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡴࡲࡦࡴࡺࠬࠡࡲࡤࡦࡴࡺࠠࡢࡰࡧࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡲࡩࡣࡴࡤࡶࡾࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡶࡲࠤࡷࡻ࡮ࠡࡴࡲࡦࡴࡺࠠࡵࡧࡶࡸࡸࠦࡩ࡯ࠢࡳࡥࡷࡧ࡬࡭ࡧ࡯࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠳ࡰࡢࡤࡲࡸࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࡡࠩੁ")
bstack1lll1_opy_ = bstackl_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡥࡩ࡭ࡧࡶࡦࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡤࡨ࡬ࡦࡼࡥࡡࠩੂ")
bstack1l1111111_opy_ = bstackl_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡥࡵࡶࡩࡶ࡯࠰ࡧࡱ࡯ࡥ࡯ࡶࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡄࡴࡵ࡯ࡵ࡮࠯ࡓࡽࡹ࡮࡯࡯࠯ࡆࡰ࡮࡫࡮ࡵࡢࠪ੃")
bstack111111ll_opy_ = bstackl_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡤࠬ੄")
bstack11lll1_opy_ = bstackl_opy_ (u"ࠫࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡧ࡫ࡱࡨࠥ࡫ࡩࡵࡪࡨࡶ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡰࡴࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡷࡥࡱࡲࠠࡵࡪࡨࠤࡷ࡫࡬ࡦࡸࡤࡲࡹࠦࡰࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡷࡶ࡭ࡳ࡭ࠠࡱ࡫ࡳࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠫ੅")
bstack1lll1l11l_opy_ = bstackl_opy_ (u"ࠬࡎࡡ࡯ࡦ࡯࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥ࡯ࡳࡸ࡫ࠧ੆")
bstack1l11l111l_opy_ = bstackl_opy_ (u"࠭ࡁ࡭࡮ࠣࡨࡴࡴࡥࠢࠩੇ")
bstack11ll1l1_opy_ = bstackl_opy_ (u"ࠧࡄࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࠦࡡࡵࠢࡤࡲࡾࠦࡰࡢࡴࡨࡲࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡲࡪࠥࠨࡻࡾࠤ࠱ࠤࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡣ࡭ࡷࡧࡩࠥࡧࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮࠲ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠠࡧ࡫࡯ࡩࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡴࡦࡵࡷࡷ࠳࠭ੈ")
bstack1l11l1lll_opy_ = bstackl_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡴࡨࡨࡪࡴࡴࡪࡣ࡯ࡷࠥࡴ࡯ࡵࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡧࡤࡥࠢࡷ࡬ࡪࡳࠠࡪࡰࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠤࡦࡹࠠࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥࠤࡦࡴࡤࠡࠤࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠧࠦ࡯ࡳࠢࡶࡩࡹࠦࡴࡩࡧࡰࠤࡦࡹࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳ࠻ࠢࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦࠥࡧ࡮ࡥࠢࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞ࠨࠧ੉")
bstack1l111l1_opy_ = bstackl_opy_ (u"ࠩࡐࡥࡱ࡬࡯ࡳ࡯ࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠦࢀࢃࠢࠨ੊")
bstack1l1111_opy_ = bstackl_opy_ (u"ࠪࡉࡳࡩ࡯ࡶࡰࡷࡩࡷ࡫ࡤࠡࡧࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣ࠱ࠥࢁࡽࠨੋ")
bstack1lll11_opy_ = bstackl_opy_ (u"ࠫࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠫੌ")
bstack11ll1l11_opy_ = bstackl_opy_ (u"࡙ࠬࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰ੍ࠬ")
bstack1lll1l111_opy_ = bstackl_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠤ࡮ࡹࠠ࡯ࡱࡺࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠦ࠭੎")
bstack11lll1l1l_opy_ = bstackl_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲ࠺ࠡࡽࢀࠫ੏")
bstack1l11111_opy_ = bstackl_opy_ (u"ࠨࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡥ࡭ࡳࡧࡲࡺࠢࡺ࡭ࡹ࡮ࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࡾࢁࠬ੐")
bstack1lll111l1_opy_ = bstackl_opy_ (u"ࠩࡘࡴࡩࡧࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠪੑ")
bstack1ll11111_opy_ = bstackl_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠩ੒")
bstack1lll11ll1_opy_ = bstackl_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࠥࡧ࡮ࠡࡣࡳࡴࡷࡵࡰࡳ࡫ࡤࡸࡪࠦࡆࡘࠢࠫࡶࡴࡨ࡯ࡵ࠱ࡳࡥࡧࡵࡴࠪࠢ࡬ࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠯ࠤࡸࡱࡩࡱࠢࡷ࡬ࡪࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡮ࡩࡾࠦࡩ࡯ࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡪࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡳࡪ࡯ࡳࡰࡪࠦࡰࡺࡶ࡫ࡳࡳࠦࡳࡤࡴ࡬ࡴࡹࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡢࡰࡼࠤࡋ࡝࠮ࠨ੓")
bstack11ll111_opy_ = bstackl_opy_ (u"࡙ࠬࡥࡵࡶ࡬ࡲ࡬ࠦࡨࡵࡶࡳࡔࡷࡵࡸࡺ࠱࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾࠦࡩࡴࠢࡱࡳࡹࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡲࡲࠥࡩࡵࡳࡴࡨࡲࡹࡲࡹࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡵࡦࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࠬࢀࢃࠩ࠭ࠢࡳࡰࡪࡧࡳࡦࠢࡸࡴ࡬ࡸࡡࡥࡧࠣࡸࡴࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭࠿࠿࠷࠲࠵࠴࠰ࠡࡱࡵࠤࡷ࡫ࡦࡦࡴࠣࡸࡴࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡥࡱࡦࡷ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠱ࡵࡹࡳ࠳ࡴࡦࡵࡷࡷ࠲ࡨࡥࡩ࡫ࡱࡨ࠲ࡶࡲࡰࡺࡼࠧࡵࡿࡴࡩࡱࡱࠤ࡫ࡵࡲࠡࡣࠣࡻࡴࡸ࡫ࡢࡴࡲࡹࡳࡪ࠮ࠨ੔")
bstack111l1lll_opy_ = bstackl_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡼࡱࡱࠦࡦࡪ࡮ࡨ࠲࠳࠭੕")
bstack1lll1lll_opy_ = bstackl_opy_ (u"ࠧࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡧࡦࡰࡨࡶࡦࡺࡥࡥࠢࡷ࡬ࡪࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨࠥࠬ੖")
bstack11l1l1ll_opy_ = bstackl_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡴࡩࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫࠮ࠡࡽࢀࠫ੗")
bstack1l111llll_opy_ = bstackl_opy_ (u"ࠩࡈࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡺࠠ࡭ࡧࡤࡷࡹࠦ࠱ࠡ࡫ࡱࡴࡺࡺࠬࠡࡴࡨࡧࡪ࡯ࡶࡦࡦࠣ࠴ࠬ੘")
bstack1lllll_opy_ = bstackl_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡧࡹࡷ࡯࡮ࡨࠢࡄࡴࡵࠦࡵࡱ࡮ࡲࡥࡩ࠴ࠠࡼࡿࠪਖ਼")
bstack11lll11l1_opy_ = bstackl_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲ࡯ࡳࡦࡪࠠࡂࡲࡳ࠲ࠥࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࢀࢃ࠮ࠨਗ਼")
bstack1ll1ll11_opy_ = bstackl_opy_ (u"ࠬࡑࡥࡺࡵࠣࡧࡦࡴ࡮ࡰࡶࠣࡧࡴ࠳ࡥࡹ࡫ࡶࡸࠥࡧࡳࠡࡣࡳࡴࠥࡼࡡ࡭ࡷࡨࡷ࠱ࠦࡵࡴࡧࠣࡥࡳࡿࠠࡰࡰࡨࠤࡵࡸ࡯ࡱࡧࡵࡸࡾࠦࡦࡳࡱࡰࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠮ࠣࡳࡳࡲࡹࠡࠤࡳࡥࡹ࡮ࠢࠡࡣࡱࡨࠥࠨࡣࡶࡵࡷࡳࡲࡥࡩࡥࠤࠣࡧࡦࡴࠠࡤࡱ࠰ࡩࡽ࡯ࡳࡵࠢࡷࡳ࡬࡫ࡴࡩࡧࡵ࠲ࠬਜ਼")
bstack111l1l_opy_ = bstackl_opy_ (u"࡛࠭ࡊࡰࡹࡥࡱ࡯ࡤࠡࡣࡳࡴࠥࡶࡲࡰࡲࡨࡶࡹࡿ࡝ࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠡࡣࡵࡩࠥࢁࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡵࡧࡴࡩ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿ࡿ࠱ࠤࡋࡵࡲࠡ࡯ࡲࡶࡪࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡱ࡮ࡨࡥࡸ࡫ࠠࡷ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡥࡱࡦࡷ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡰࡪࡷࡰ࠳ࡸ࡫ࡴ࠮ࡷࡳ࠱ࡹ࡫ࡳࡵࡵ࠲ࡷࡵ࡫ࡣࡪࡨࡼ࠱ࡦࡶࡰࠨੜ")
bstack1l1ll1l_opy_ = bstackl_opy_ (u"ࠧ࡜ࡋࡱࡺࡦࡲࡩࡥࠢࡤࡴࡵࠦࡰࡳࡱࡳࡩࡷࡺࡹ࡞ࠢࡖࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡼࡡ࡭ࡷࡨࡷࠥࡵࡦࠡࡣࡳࡴࠥࡧࡲࡦࠢࡲࡪࠥࢁࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡵࡧࡴࡩ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿ࡿ࠱ࠤࡋࡵࡲࠡ࡯ࡲࡶࡪࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡱ࡮ࡨࡥࡸ࡫ࠠࡷ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡥࡱࡦࡷ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡰࡪࡷࡰ࠳ࡸ࡫ࡴ࠮ࡷࡳ࠱ࡹ࡫ࡳࡵࡵ࠲ࡷࡵ࡫ࡣࡪࡨࡼ࠱ࡦࡶࡰࠨ੝")
bstack1l1l11ll_opy_ = bstackl_opy_ (u"ࠨࡗࡶ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡤࡴࡵࠦࡩࡥࠢࡾࢁࠥ࡬࡯ࡳࠢ࡫ࡥࡸ࡮ࠠ࠻ࠢࡾࢁ࠳࠭ਫ਼")
bstack11l11ll1_opy_ = bstackl_opy_ (u"ࠩࡄࡴࡵࠦࡕࡱ࡮ࡲࡥࡩ࡫ࡤࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠡࡋࡇࠤ࠿ࠦࡻࡾࠩ੟")
bstack11l1111l_opy_ = bstackl_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢࡄࡴࡵࠦ࠺ࠡࡽࢀ࠲ࠬ੠")
bstack1l1llll_opy_ = bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡱࡵࠤࡻࡧ࡮ࡪ࡮࡯ࡥࠥࡶࡹࡵࡪࡲࡲࠥࡺࡥࡴࡶࡶ࠰ࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡵࡧࡲࡢ࡮࡯ࡩࡱࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡁࠥ࠷ࠧ੡")
bstack11ll11111_opy_ = bstackl_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࠾ࠥࢁࡽࠨ੢")
bstack1l1llll11_opy_ = bstackl_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡦࡰࡴࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳ࠼ࠣࡿࢂ࠭੣")
bstack1lll1ll1_opy_ = bstackl_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣ࡫ࡪࡺࠠࡳࡧࡤࡷࡴࡴࠠࡧࡱࡵࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫࡫ࡡࡵࡷࡵࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪ࠴ࠠࡼࡿࠪ੤")
bstack1lll1l11_opy_ = bstackl_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡢࡲ࡬ࠤࡨࡧ࡬࡭࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭੥")
bstack1ll111l_opy_ = bstackl_opy_ (u"ࠩࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡨࡰࡹࠣࡦࡺ࡯࡬ࡥࠢࡘࡖࡑ࠲ࠠࡢࡵࠣࡦࡺ࡯࡬ࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾࠦࡩࡴࠢࡱࡳࡹࠦࡵࡴࡧࡧ࠲ࠬ੦")
bstack1l1l111l_opy_ = bstackl_opy_ (u"ࠪࡗࡪࡸࡶࡦࡴࠣࡷ࡮ࡪࡥࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠬࢀࢃࠩࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡤࡱࡪࠦࡡࡴࠢࡦࡰ࡮࡫࡮ࡵࠢࡶ࡭ࡩ࡫ࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠫࡿࢂ࠯ࠧ੧")
bstack11ll1_opy_ = bstackl_opy_ (u"࡛ࠫ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡨࡦࡹࡨࡣࡱࡤࡶࡩࡀࠠࡼࡿࠪ੨")
bstack1l111_opy_ = bstackl_opy_ (u"࡛ࠬ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡣࡦࡧࡪࡹࡳࠡࡣࠣࡴࡷ࡯ࡶࡢࡶࡨࠤࡩࡵ࡭ࡢ࡫ࡱ࠾ࠥࢁࡽࠡ࠰ࠣࡗࡪࡺࠠࡵࡪࡨࠤ࡫ࡵ࡬࡭ࡱࡺ࡭ࡳ࡭ࠠࡤࡱࡱࡪ࡮࡭ࠠࡪࡰࠣࡽࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠼ࠣࡠࡳ࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯ࠣࡠࡳࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮࠽ࠤࡹࡸࡵࡦࠢ࡟ࡲ࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮ࠩ੩")
bstack1ll1llll1_opy_ = bstackl_opy_ (u"࠭ࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࡢࡩࡷࡸ࡯ࡳࠢ࠽ࠤࢀࢃࠧ੪")
bstack1l1ll1l1l_opy_ = bstackl_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡳࡪ࡟ࡢ࡯ࡳࡰ࡮ࡺࡵࡥࡧࡢࡩࡻ࡫࡮ࡵࠢࡩࡳࡷࠦࡓࡅࡍࡖࡩࡹࡻࡰࠡࡽࢀࠦ੫")
bstack11l1l1ll1_opy_ = bstackl_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠࡣࡰࡴࡱ࡯ࡴࡶࡦࡨࡣࡪࡼࡥ࡯ࡶࠣࡪࡴࡸࠠࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠣࡿࢂࠨ੬")
bstack111lll1_opy_ = bstackl_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠥࢁࡽࠣ੭")
bstack111l1l11_opy_ = bstackl_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬ࡩࡳࡧࡢࡶࡪࡷࡵࡦࡵࡷࠤࢀࢃࠢ੮")
bstack1l111l111_opy_ = bstackl_opy_ (u"ࠦࡕࡕࡓࡕࠢࡈࡺࡪࡴࡴࠡࡽࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦ࠺ࠡࡽࢀࠦ੯")
bstack1111ll_opy_ = bstackl_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡵࡸ࡯ࡹࡻࠣࡷࡪࡺࡴࡪࡰࡪࡷ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩੰ")
bstack11lll1lll_opy_ = bstackl_opy_ (u"࠭ࡒࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦ࠯࡯ࡧࡻࡸࡤ࡮ࡵࡣࡵࠣࡿࢂ࠭ੱ")
bstack1l1l11ll1_opy_ = bstackl_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣ࠳ࡳ࡫ࡸࡵࡡ࡫ࡹࡧࡹ࠺ࠡࡽࢀࠫੲ")
bstack1l11111ll_opy_ = bstackl_opy_ (u"ࠨࡐࡨࡥࡷ࡫ࡳࡵࠢ࡫ࡹࡧࠦࡡ࡭࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡷ࠿ࠦࡻࡾࠩੳ")
bstack111l11_opy_ = bstackl_opy_ (u"ࠩࡈࡖࡗࡕࡒࠡࡋࡑࠤࡆࡒࡌࡐࡅࡄࡘࡊࠦࡈࡖࡄࠣࡿࢂ࠭ੴ")
bstack1ll1l1l1l_opy_ = bstackl_opy_ (u"ࠪࡐࡦࡺࡥ࡯ࡥࡼࠤࡴ࡬ࠠࡩࡷࡥ࠾ࠥࢁࡽࠡ࡫ࡶ࠾ࠥࢁࡽࠨੵ")
bstack1l1l1ll11_opy_ = bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠ࡭ࡣࡷࡩࡳࡩࡹࠡࡨࡲࡶࠥࢁࡽࠡࡪࡸࡦ࠿ࠦࡻࡾࠩ੶")
bstack111111l_opy_ = bstackl_opy_ (u"ࠬࡎࡵࡣࠢࡸࡶࡱࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡰࡲࡷ࡭ࡲࡧ࡬ࠡࡪࡸࡦ࠿ࠦࡻࡾࠩ੷")
bstack1ll11l111_opy_ = bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡲࡴࡹ࡯࡭ࡢ࡮ࠣ࡬ࡺࡨࠠࡶࡴ࡯࠾ࠥࢁࡽࠨ੸")
bstack1l111l1l_opy_ = bstackl_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡮࡬ࡷࡹࡹ࠺ࠡࡽࢀࠫ੹")
bstack11l1ll1_opy_ = bstackl_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹ࠺ࠡࡽࢀࠫ੺")
bstack11l11ll1l_opy_ = bstackl_opy_ (u"ࠩࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠢࠣ࡭࡫࠮ࡰࡢࡩࡨࠤࡂࡃ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠢࡾࡠࡳࠦࠠࠡࡶࡵࡽࢀࡢ࡮ࠡࡥࡲࡲࡸࡺࠠࡧࡵࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮࡜ࠨࡨࡶࡠࠬ࠯࠻࡝ࡰࠣࠤࠥࠦࠠࡧࡵ࠱ࡥࡵࡶࡥ࡯ࡦࡉ࡭ࡱ࡫ࡓࡺࡰࡦࠬࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩ࠮ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡵࡥࡩ࡯ࡦࡨࡼ࠮ࠦࠫࠡࠤ࠽ࠦࠥ࠱ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭࠮ࡡࡸࡣ࡬ࡸࠥࡴࡥࡸࡒࡤ࡫ࡪ࠸࠮ࡦࡸࡤࡰࡺࡧࡴࡦࠪࠥࠬ࠮ࠦ࠽࠿ࠢࡾࢁࠧ࠲ࠠ࡝ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠨࡽ࡝ࠩࠬ࠭࠮ࡡࠢࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠥࡡ࠮ࠦࠫࠡࠤ࠯ࡠࡡࡴࠢࠪ࡞ࡱࠤࠥࠦࠠࡾࡥࡤࡸࡨ࡮ࠨࡦࡺࠬࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡿ࡟ࡲࠥࠦ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠩ੻")
bstack1ll1ll1_opy_ = bstackl_opy_ (u"ࠪࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡢ࡮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮ࡴ࡮࡬ࡧࡪ࠮࠰࠭ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷࠮ࡢ࡮ࡤࡱࡱࡷࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮ࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ࠯࠻࡝ࡰ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰࡯ࡥࡺࡴࡣࡩࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶ࠭ࠥࡃ࠾ࠡࡽ࡟ࡲࡱ࡫ࡴࠡࡥࡤࡴࡸࡁ࡜࡯ࡶࡵࡽࠥࢁ࡜࡯ࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࢃ࡜࡯ࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶࠫࡿࡡࡴࠠࠡࠢࠣࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺ࠺ࠡࡢࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠨࢀ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬࢁࡥ࠲࡜࡯ࠢࠣࠤࠥ࠴࠮࠯࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩ੼")
from ._version import __version__
bstack1l1l11111_opy_ = None
CONFIG = {}
bstack1l11ll111_opy_ = {}
bstack1ll11ll_opy_ = {}
bstack1l11ll_opy_ = None
bstack11l11l111_opy_ = None
bstack1l11111l1_opy_ = None
bstack1ll1lll1_opy_ = -1
bstack11111l11_opy_ = bstack1l1111l1l_opy_
bstack1l11ll11l_opy_ = 1
bstack1l11l1l1_opy_ = False
bstack11ll1lll1_opy_ = False
bstack1llllllll_opy_ = bstackl_opy_ (u"ࠫࠬ੽")
bstack1l1ll11l1_opy_ = bstackl_opy_ (u"ࠬ࠭੾")
bstack11111l_opy_ = False
bstack1ll11l11l_opy_ = True
bstack1l1lll_opy_ = bstackl_opy_ (u"࠭ࠧ੿")
bstack1lll1llll_opy_ = []
bstack1l111111_opy_ = bstackl_opy_ (u"ࠧࠨ઀")
bstack1ll111l1l_opy_ = False
bstack11l1l_opy_ = None
bstack11llll1_opy_ = -1
bstack1lllll1l1_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠨࢀࠪઁ")), bstackl_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩં"), bstackl_opy_ (u"ࠪ࠲ࡷࡵࡢࡰࡶ࠰ࡶࡪࡶ࡯ࡳࡶ࠰࡬ࡪࡲࡰࡦࡴ࠱࡮ࡸࡵ࡮ࠨઃ"))
bstack1l1l1l11l_opy_ = []
bstack11lll_opy_ = False
bstack11l11l11l_opy_ = None
bstack1lllllll_opy_ = None
bstack1lll1ll_opy_ = None
bstack1llll_opy_ = None
bstack11l11l11_opy_ = None
bstack1l11111l_opy_ = None
bstack1111l11l_opy_ = None
bstack1ll1l11l1_opy_ = None
bstack1llll1lll_opy_ = None
bstack11llll1l_opy_ = None
bstack11l11111_opy_ = None
bstack1lll1l1l_opy_ = None
bstack11llll1ll_opy_ = None
bstack1ll111ll1_opy_ = None
bstack1lll11l11_opy_ = None
bstack1l111l_opy_ = bstackl_opy_ (u"ࠦࠧ઄")
class bstack1ll1lll_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack1ll1lll_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11111l11_opy_,
                    format=bstackl_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪઅ"),
                    datefmt=bstackl_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨઆ"))
def bstack11lll1l11_opy_():
  global CONFIG
  global bstack11111l11_opy_
  if bstackl_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩઇ") in CONFIG:
    bstack11111l11_opy_ = bstack1111llll_opy_[CONFIG[bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪઈ")]]
    logging.getLogger().setLevel(bstack11111l11_opy_)
def bstack111111l1_opy_():
  global CONFIG
  global bstack11lll_opy_
  bstack111l1ll1_opy_ = bstack1ll1111ll_opy_(CONFIG)
  if(bstackl_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫઉ") in bstack111l1ll1_opy_ and str(bstack111l1ll1_opy_[bstackl_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઊ")]).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩઋ")):
    bstack11lll_opy_ = True
def bstack1lll111l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll11lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11l1l1l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstackl_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤઌ") == args[i].lower() or bstackl_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢઍ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1lll_opy_
      bstack1l1lll_opy_ += bstackl_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ઎") + path
      return path
  return None
def bstack1l1l1111_opy_():
  bstack1ll11l_opy_ = bstack1l11l1l1l_opy_()
  if bstack1ll11l_opy_ and os.path.exists(os.path.abspath(bstack1ll11l_opy_)):
    fileName = bstack1ll11l_opy_
  if bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬએ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭ઐ")])) and not bstackl_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬઑ") in locals():
    fileName = os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ઒")]
  if bstackl_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧઓ") in locals():
    bstack1ll11llll_opy_ = os.path.abspath(fileName)
  else:
    bstack1ll11llll_opy_ = bstackl_opy_ (u"࠭ࠧઔ")
  bstack11l1llll_opy_ = os.getcwd()
  bstack1llllll1l_opy_ = bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪક")
  bstack111l11l_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬખ")
  while (not os.path.exists(bstack1ll11llll_opy_)) and bstack11l1llll_opy_ != bstackl_opy_ (u"ࠤࠥગ"):
    bstack1ll11llll_opy_ = os.path.join(bstack11l1llll_opy_, bstack1llllll1l_opy_)
    if not os.path.exists(bstack1ll11llll_opy_):
      bstack1ll11llll_opy_ = os.path.join(bstack11l1llll_opy_, bstack111l11l_opy_)
    if bstack11l1llll_opy_ != os.path.dirname(bstack11l1llll_opy_):
      bstack11l1llll_opy_ = os.path.dirname(bstack11l1llll_opy_)
    else:
      bstack11l1llll_opy_ = bstackl_opy_ (u"ࠥࠦઘ")
  if not os.path.exists(bstack1ll11llll_opy_):
    bstack1l1l1ll_opy_(
      bstack11ll1l1_opy_.format(os.getcwd()))
  with open(bstack1ll11llll_opy_, bstackl_opy_ (u"ࠫࡷ࠭ઙ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1l1l1ll_opy_(bstack1l111l1_opy_.format(str(exc)))
def bstack1111ll1l_opy_(config):
  bstack1lllll11_opy_ = bstack11llllll_opy_(config)
  for option in list(bstack1lllll11_opy_):
    if option.lower() in bstack1l111ll11_opy_ and option != bstack1l111ll11_opy_[option.lower()]:
      bstack1lllll11_opy_[bstack1l111ll11_opy_[option.lower()]] = bstack1lllll11_opy_[option]
      del bstack1lllll11_opy_[option]
  return config
def bstack11lll11_opy_():
  global bstack1ll11ll_opy_
  for key, bstack111l1l1_opy_ in bstack1l1ll11_opy_.items():
    if isinstance(bstack111l1l1_opy_, list):
      for var in bstack111l1l1_opy_:
        if var in os.environ:
          bstack1ll11ll_opy_[key] = os.environ[var]
          break
    elif bstack111l1l1_opy_ in os.environ:
      bstack1ll11ll_opy_[key] = os.environ[bstack111l1l1_opy_]
  if bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧચ") in os.environ:
    bstack1ll11ll_opy_[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪછ")] = {}
    bstack1ll11ll_opy_[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫજ")][bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪઝ")] = os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫઞ")]
def bstack111llll1_opy_():
  global bstack1l11ll111_opy_
  global bstack1l1lll_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstackl_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ટ").lower() == val.lower():
      bstack1l11ll111_opy_[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨઠ")] = {}
      bstack1l11ll111_opy_[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩડ")][bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨઢ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1lll11l1l_opy_ in bstack11l11l1l_opy_.items():
    if isinstance(bstack1lll11l1l_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lll11l1l_opy_:
          if idx<len(sys.argv) and bstackl_opy_ (u"ࠧ࠮࠯ࠪણ") + var.lower() == val.lower() and not key in bstack1l11ll111_opy_:
            bstack1l11ll111_opy_[key] = sys.argv[idx+1]
            bstack1l1lll_opy_ += bstackl_opy_ (u"ࠨࠢ࠰࠱ࠬત") + var + bstackl_opy_ (u"ࠩࠣࠫથ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstackl_opy_ (u"ࠪ࠱࠲࠭દ") + bstack1lll11l1l_opy_.lower() == val.lower() and not key in bstack1l11ll111_opy_:
          bstack1l11ll111_opy_[key] = sys.argv[idx+1]
          bstack1l1lll_opy_ += bstackl_opy_ (u"ࠫࠥ࠳࠭ࠨધ") + bstack1lll11l1l_opy_ + bstackl_opy_ (u"ࠬࠦࠧન") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack11lllll1l_opy_(config):
  bstack11l1l1l11_opy_ = config.keys()
  for bstack1l1ll11ll_opy_, bstack1ll1l1111_opy_ in bstack11ll1l111_opy_.items():
    if bstack1ll1l1111_opy_ in bstack11l1l1l11_opy_:
      config[bstack1l1ll11ll_opy_] = config[bstack1ll1l1111_opy_]
      del config[bstack1ll1l1111_opy_]
  for bstack1l1ll11ll_opy_, bstack1ll1l1111_opy_ in bstack1l11l1l_opy_.items():
    if isinstance(bstack1ll1l1111_opy_, list):
      for bstack111lllll_opy_ in bstack1ll1l1111_opy_:
        if bstack111lllll_opy_ in bstack11l1l1l11_opy_:
          config[bstack1l1ll11ll_opy_] = config[bstack111lllll_opy_]
          del config[bstack111lllll_opy_]
          break
    elif bstack1ll1l1111_opy_ in bstack11l1l1l11_opy_:
        config[bstack1l1ll11ll_opy_] = config[bstack1ll1l1111_opy_]
        del config[bstack1ll1l1111_opy_]
  for bstack111lllll_opy_ in list(config):
    for bstack1l11l1l11_opy_ in bstack1lll11ll_opy_:
      if bstack111lllll_opy_.lower() == bstack1l11l1l11_opy_.lower() and bstack111lllll_opy_ != bstack1l11l1l11_opy_:
        config[bstack1l11l1l11_opy_] = config[bstack111lllll_opy_]
        del config[bstack111lllll_opy_]
  bstack111ll1l1_opy_ = []
  if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ઩") in config:
    bstack111ll1l1_opy_ = config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪપ")]
  for platform in bstack111ll1l1_opy_:
    for bstack111lllll_opy_ in list(platform):
      for bstack1l11l1l11_opy_ in bstack1lll11ll_opy_:
        if bstack111lllll_opy_.lower() == bstack1l11l1l11_opy_.lower() and bstack111lllll_opy_ != bstack1l11l1l11_opy_:
          platform[bstack1l11l1l11_opy_] = platform[bstack111lllll_opy_]
          del platform[bstack111lllll_opy_]
  for bstack1l1ll11ll_opy_, bstack1ll1l1111_opy_ in bstack1l11l1l_opy_.items():
    for platform in bstack111ll1l1_opy_:
      if isinstance(bstack1ll1l1111_opy_, list):
        for bstack111lllll_opy_ in bstack1ll1l1111_opy_:
          if bstack111lllll_opy_ in platform:
            platform[bstack1l1ll11ll_opy_] = platform[bstack111lllll_opy_]
            del platform[bstack111lllll_opy_]
            break
      elif bstack1ll1l1111_opy_ in platform:
        platform[bstack1l1ll11ll_opy_] = platform[bstack1ll1l1111_opy_]
        del platform[bstack1ll1l1111_opy_]
  for bstack111ll11_opy_ in bstack1l11l11l1_opy_:
    if bstack111ll11_opy_ in config:
      if not bstack1l11l11l1_opy_[bstack111ll11_opy_] in config:
        config[bstack1l11l11l1_opy_[bstack111ll11_opy_]] = {}
      config[bstack1l11l11l1_opy_[bstack111ll11_opy_]].update(config[bstack111ll11_opy_])
      del config[bstack111ll11_opy_]
  for platform in bstack111ll1l1_opy_:
    for bstack111ll11_opy_ in bstack1l11l11l1_opy_:
      if bstack111ll11_opy_ in list(platform):
        if not bstack1l11l11l1_opy_[bstack111ll11_opy_] in platform:
          platform[bstack1l11l11l1_opy_[bstack111ll11_opy_]] = {}
        platform[bstack1l11l11l1_opy_[bstack111ll11_opy_]].update(platform[bstack111ll11_opy_])
        del platform[bstack111ll11_opy_]
  config = bstack1111ll1l_opy_(config)
  return config
def bstack1l11lllll_opy_(config):
  global bstack1l1ll11l1_opy_
  if bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬફ") in config and str(config[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭બ")]).lower() != bstackl_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩભ"):
    if not bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨમ") in config:
      config[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩય")] = {}
    if not bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨર") in config[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")]:
      bstack11ll11l_opy_ = datetime.datetime.now()
      bstack1llll1l11_opy_ = bstack11ll11l_opy_.strftime(bstackl_opy_ (u"ࠨࠧࡧࡣࠪࡨ࡟ࠦࡊࠨࡑࠬલ"))
      hostname = socket.gethostname()
      bstack1llll11_opy_ = bstackl_opy_ (u"ࠩࠪળ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstackl_opy_ (u"ࠪࡿࢂࡥࡻࡾࡡࡾࢁࠬ઴").format(bstack1llll1l11_opy_, hostname, bstack1llll11_opy_)
      config[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨવ")][bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧશ")] = identifier
    bstack1l1ll11l1_opy_ = config[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪષ")][bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩસ")]
  return config
def bstack1l111lll1_opy_():
  if (
    isinstance(os.getenv(bstackl_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑ࠭હ")), str) and len(os.getenv(bstackl_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠧ઺"))) > 0
  ) or (
    isinstance(os.getenv(bstackl_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠩ઻")), str) and len(os.getenv(bstackl_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇ઼ࠪ"))) > 0
  ):
    return os.getenv(bstackl_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫઽ"), 0)
  if str(os.getenv(bstackl_opy_ (u"࠭ࡃࡊࠩા"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬિ") and str(os.getenv(bstackl_opy_ (u"ࠨࡅࡌࡖࡈࡒࡅࡄࡋࠪી"))).lower() == bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧુ"):
    return os.getenv(bstackl_opy_ (u"ࠪࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒ࠭ૂ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠫࡈࡏࠧૃ"))).lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪૄ") and str(os.getenv(bstackl_opy_ (u"࠭ࡔࡓࡃ࡙ࡍࡘ࠭ૅ"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬ૆"):
    return os.getenv(bstackl_opy_ (u"ࠨࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧે"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠩࡆࡍࠬૈ"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨૉ") and str(os.getenv(bstackl_opy_ (u"ࠫࡈࡏ࡟ࡏࡃࡐࡉࠬ૊"))).lower() == bstackl_opy_ (u"ࠬࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠧો"):
    return 0 # bstack111l1_opy_ bstack1l11l11ll_opy_ not set build number env
  if os.getenv(bstackl_opy_ (u"࠭ࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠩૌ")) and os.getenv(bstackl_opy_ (u"ࠧࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖ્ࠪ")):
    return os.getenv(bstackl_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠪ૎"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠩࡆࡍࠬ૏"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨૐ") and str(os.getenv(bstackl_opy_ (u"ࠫࡉࡘࡏࡏࡇࠪ૑"))).lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪ૒"):
    return os.getenv(bstackl_opy_ (u"࠭ࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫ૓"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠧࡄࡋࠪ૔"))).lower() == bstackl_opy_ (u"ࠨࡶࡵࡹࡪ࠭૕") and str(os.getenv(bstackl_opy_ (u"ࠩࡖࡉࡒࡇࡐࡉࡑࡕࡉࠬ૖"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨ૗"):
    return os.getenv(bstackl_opy_ (u"ࠫࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠧ૘"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠬࡉࡉࠨ૙"))).lower() == bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫ૚") and str(os.getenv(bstackl_opy_ (u"ࠧࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠪ૛"))).lower() == bstackl_opy_ (u"ࠨࡶࡵࡹࡪ࠭૜"):
    return os.getenv(bstackl_opy_ (u"ࠩࡆࡍࡤࡐࡏࡃࡡࡌࡈࠬ૝"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠪࡇࡎ࠭૞"))).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩ૟") and str(os.getenv(bstackl_opy_ (u"ࠬࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠨૠ"))).lower() == bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫૡ"):
    return os.getenv(bstackl_opy_ (u"ࠧࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩૢ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠨࡖࡉࡣࡇ࡛ࡉࡍࡆࠪૣ"))).lower() == bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૤"):
    return os.getenv(bstackl_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪ૥"), 0)
  return -1
def bstack1l1l1l1l1_opy_(bstack11lll111l_opy_):
  global CONFIG
  if not bstackl_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭૦") in CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૧")]:
    return
  CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૨")] = CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")].replace(
    bstackl_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ૪"),
    str(bstack11lll111l_opy_)
  )
def bstack1lll1l_opy_():
  global CONFIG
  if not bstackl_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨ૫") in CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૬")]:
    return
  bstack11ll11l_opy_ = datetime.datetime.now()
  bstack1llll1l11_opy_ = bstack11ll11l_opy_.strftime(bstackl_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ૭"))
  CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮")] = CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯")].replace(
    bstackl_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭૰"),
    bstack1llll1l11_opy_
  )
def bstack1ll1l1ll_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૱") in CONFIG and not bool(CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૲")]):
    del CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૳")]
    return
  if not bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴") in CONFIG:
    CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૵")] = bstackl_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩ૶")
  if bstackl_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭૷") in CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૸")]:
    bstack1lll1l_opy_()
    os.environ[bstackl_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ૹ")] = CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬૺ")]
  if not bstackl_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ૻ") in CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧૼ")]:
    return
  bstack11lll111l_opy_ = bstackl_opy_ (u"࠭ࠧ૽")
  bstack1l11l1ll1_opy_ = bstack1l111lll1_opy_()
  if bstack1l11l1ll1_opy_ != -1:
    bstack11lll111l_opy_ = bstackl_opy_ (u"ࠧࡄࡋࠣࠫ૾") + str(bstack1l11l1ll1_opy_)
  if bstack11lll111l_opy_ == bstackl_opy_ (u"ࠨࠩ૿"):
    bstack11l1l1lll_opy_ = bstack1l11ll1l_opy_(CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ଀")])
    if bstack11l1l1lll_opy_ != -1:
      bstack11lll111l_opy_ = str(bstack11l1l1lll_opy_)
  if bstack11lll111l_opy_:
    bstack1l1l1l1l1_opy_(bstack11lll111l_opy_)
    os.environ[bstackl_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧଁ")] = CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ଂ")]
def bstack11l11llll_opy_(bstack1ll11l1l_opy_, bstack11l1ll_opy_, path):
  bstack1llll1ll1_opy_ = {
    bstackl_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩଃ"): bstack11l1ll_opy_
  }
  if os.path.exists(path):
    bstack1ll1111l1_opy_ = json.load(open(path, bstackl_opy_ (u"࠭ࡲࡣࠩ଄")))
  else:
    bstack1ll1111l1_opy_ = {}
  bstack1ll1111l1_opy_[bstack1ll11l1l_opy_] = bstack1llll1ll1_opy_
  with open(path, bstackl_opy_ (u"ࠢࡸ࠭ࠥଅ")) as outfile:
    json.dump(bstack1ll1111l1_opy_, outfile)
def bstack1l11ll1l_opy_(bstack1ll11l1l_opy_):
  bstack1ll11l1l_opy_ = str(bstack1ll11l1l_opy_)
  bstack1l1l1lll_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠨࢀࠪଆ")), bstackl_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩଇ"))
  try:
    if not os.path.exists(bstack1l1l1lll_opy_):
      os.makedirs(bstack1l1l1lll_opy_)
    file_path = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠪࢂࠬଈ")), bstackl_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଉ"), bstackl_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧଊ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstackl_opy_ (u"࠭ࡷࠨଋ")):
        pass
      with open(file_path, bstackl_opy_ (u"ࠢࡸ࠭ࠥଌ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstackl_opy_ (u"ࠨࡴࠪ଍")) as bstack1l1l1l1l_opy_:
      bstack11lll1111_opy_ = json.load(bstack1l1l1l1l_opy_)
    if bstack1ll11l1l_opy_ in bstack11lll1111_opy_:
      bstack1l11l11l_opy_ = bstack11lll1111_opy_[bstack1ll11l1l_opy_][bstackl_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭଎")]
      bstack11l1lllll_opy_ = int(bstack1l11l11l_opy_) + 1
      bstack11l11llll_opy_(bstack1ll11l1l_opy_, bstack11l1lllll_opy_, file_path)
      return bstack11l1lllll_opy_
    else:
      bstack11l11llll_opy_(bstack1ll11l1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11ll11111_opy_.format(str(e)))
    return -1
def bstack1l11ll1ll_opy_(config):
  if not config[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬଏ")] or not config[bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧଐ")]:
    return True
  else:
    return False
def bstack11l11l1ll_opy_(config):
  if bstackl_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ଑") in config:
    del(config[bstackl_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ଒")])
    return False
  if bstack1ll11lll_opy_() < version.parse(bstackl_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭ଓ")):
    return False
  if bstack1ll11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧଔ")):
    return True
  if bstackl_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩକ") in config and config[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪଖ")] == False:
    return False
  else:
    return True
def bstack11ll1lll_opy_(config, index = 0):
  global bstack11111l_opy_
  bstack111l111l_opy_ = {}
  caps = bstack11l11l1_opy_ + bstack1lll11l1_opy_
  if bstack11111l_opy_:
    caps += bstack1ll111111_opy_
  for key in config:
    if key in caps + [bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଗ")]:
      continue
    bstack111l111l_opy_[key] = config[key]
  if bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଘ") in config:
    for bstack1lll1111_opy_ in config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଙ")][index]:
      if bstack1lll1111_opy_ in caps + [bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଚ"), bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଛ")]:
        continue
      bstack111l111l_opy_[bstack1lll1111_opy_] = config[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଜ")][index][bstack1lll1111_opy_]
  bstack111l111l_opy_[bstackl_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬଝ")] = socket.gethostname()
  if bstackl_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬଞ") in bstack111l111l_opy_:
    del(bstack111l111l_opy_[bstackl_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ଟ")])
  return bstack111l111l_opy_
def bstack1l1l111l1_opy_(config):
  global bstack11111l_opy_
  bstack1ll1lll1l_opy_ = {}
  caps = bstack1lll11l1_opy_
  if bstack11111l_opy_:
    caps+= bstack1ll111111_opy_
  for key in caps:
    if key in config:
      bstack1ll1lll1l_opy_[key] = config[key]
  return bstack1ll1lll1l_opy_
def bstack1l11lll11_opy_(bstack111l111l_opy_, bstack1ll1lll1l_opy_):
  bstack1l1l1llll_opy_ = {}
  for key in bstack111l111l_opy_.keys():
    if key in bstack11ll1l111_opy_:
      bstack1l1l1llll_opy_[bstack11ll1l111_opy_[key]] = bstack111l111l_opy_[key]
    else:
      bstack1l1l1llll_opy_[key] = bstack111l111l_opy_[key]
  for key in bstack1ll1lll1l_opy_:
    if key in bstack11ll1l111_opy_:
      bstack1l1l1llll_opy_[bstack11ll1l111_opy_[key]] = bstack1ll1lll1l_opy_[key]
    else:
      bstack1l1l1llll_opy_[key] = bstack1ll1lll1l_opy_[key]
  return bstack1l1l1llll_opy_
def bstack1l1111ll_opy_(config, index = 0):
  global bstack11111l_opy_
  caps = {}
  bstack1ll1lll1l_opy_ = bstack1l1l111l1_opy_(config)
  bstack111ll1l_opy_ = bstack1lll11l1_opy_
  bstack111ll1l_opy_ += bstack1111l11_opy_
  if bstack11111l_opy_:
    bstack111ll1l_opy_ += bstack1ll111111_opy_
  if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ") in config:
    if bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଡ") in config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଢ")][index]:
      caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧଣ")] = config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ତ")][index][bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଥ")]
    if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଦ") in config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][index]:
      caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨନ")] = str(config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index][bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪପ")])
    bstack1l1lll11_opy_ = {}
    for bstack11lll1ll1_opy_ in bstack111ll1l_opy_:
      if bstack11lll1ll1_opy_ in config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଫ")][index]:
        if bstack11lll1ll1_opy_ == bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ବ"):
          bstack1l1lll11_opy_[bstack11lll1ll1_opy_] = str(config[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଭ")][index][bstack11lll1ll1_opy_] * 1.0)
        else:
          bstack1l1lll11_opy_[bstack11lll1ll1_opy_] = config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩମ")][index][bstack11lll1ll1_opy_]
        del(config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଯ")][index][bstack11lll1ll1_opy_])
    bstack1ll1lll1l_opy_ = update(bstack1ll1lll1l_opy_, bstack1l1lll11_opy_)
  bstack111l111l_opy_ = bstack11ll1lll_opy_(config, index)
  for bstack111lllll_opy_ in bstack1lll11l1_opy_ + [bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ର"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ଱")]:
    if bstack111lllll_opy_ in bstack111l111l_opy_:
      bstack1ll1lll1l_opy_[bstack111lllll_opy_] = bstack111l111l_opy_[bstack111lllll_opy_]
      del(bstack111l111l_opy_[bstack111lllll_opy_])
  if bstack11l11l1ll_opy_(config):
    bstack111l111l_opy_[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪଲ")] = True
    caps.update(bstack1ll1lll1l_opy_)
    caps[bstackl_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬଳ")] = bstack111l111l_opy_
  else:
    bstack111l111l_opy_[bstackl_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ଴")] = False
    caps.update(bstack1l11lll11_opy_(bstack111l111l_opy_, bstack1ll1lll1l_opy_))
    if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଵ") in caps:
      caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨଶ")] = caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଷ")]
      del(caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧସ")])
    if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫହ") in caps:
      caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭଺")] = caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭଻")]
      del(caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ଼ࠧ")])
  return caps
def bstack11ll11l1_opy_():
  global bstack1l111111_opy_
  if bstack1ll11lll_opy_() <= version.parse(bstackl_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧଽ")):
    if bstack1l111111_opy_ != bstackl_opy_ (u"ࠨࠩା"):
      return bstackl_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥି") + bstack1l111111_opy_ + bstackl_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢୀ")
    return bstack1111l1l1_opy_
  if  bstack1l111111_opy_ != bstackl_opy_ (u"ࠫࠬୁ"):
    return bstackl_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢୂ") + bstack1l111111_opy_ + bstackl_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢୃ")
  return bstack11llll_opy_
def bstack1l1111l_opy_(options):
  return hasattr(options, bstackl_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨୄ"))
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
def bstack111llll_opy_(options, bstack11l1l1l_opy_):
  for bstack11llll11_opy_ in bstack11l1l1l_opy_:
    if bstack11llll11_opy_ in [bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୅"), bstackl_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭୆")]:
      next
    if bstack11llll11_opy_ in options._experimental_options:
      options._experimental_options[bstack11llll11_opy_]= update(options._experimental_options[bstack11llll11_opy_], bstack11l1l1l_opy_[bstack11llll11_opy_])
    else:
      options.add_experimental_option(bstack11llll11_opy_, bstack11l1l1l_opy_[bstack11llll11_opy_])
  if bstackl_opy_ (u"ࠪࡥࡷ࡭ࡳࠨେ") in bstack11l1l1l_opy_:
    for arg in bstack11l1l1l_opy_[bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩୈ")]:
      options.add_argument(arg)
    del(bstack11l1l1l_opy_[bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪ୉")])
  if bstackl_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ୊") in bstack11l1l1l_opy_:
    for ext in bstack11l1l1l_opy_[bstackl_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫୋ")]:
      options.add_extension(ext)
    del(bstack11l1l1l_opy_[bstackl_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬୌ")])
def bstack11l11ll_opy_(options, bstack111ll_opy_):
  if bstackl_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ୍") in bstack111ll_opy_:
    for bstack1l1ll111l_opy_ in bstack111ll_opy_[bstackl_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ୎")]:
      if bstack1l1ll111l_opy_ in options._preferences:
        options._preferences[bstack1l1ll111l_opy_] = update(options._preferences[bstack1l1ll111l_opy_], bstack111ll_opy_[bstackl_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ୏")][bstack1l1ll111l_opy_])
      else:
        options.set_preference(bstack1l1ll111l_opy_, bstack111ll_opy_[bstackl_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୐")][bstack1l1ll111l_opy_])
  if bstackl_opy_ (u"࠭ࡡࡳࡩࡶࠫ୑") in bstack111ll_opy_:
    for arg in bstack111ll_opy_[bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬ୒")]:
      options.add_argument(arg)
def bstack11ll1l1ll_opy_(options, bstack1111111l_opy_):
  if bstackl_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩ୓") in bstack1111111l_opy_:
    options.use_webview(bool(bstack1111111l_opy_[bstackl_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ୔")]))
  bstack111llll_opy_(options, bstack1111111l_opy_)
def bstack1llll111_opy_(options, bstack1ll1l_opy_):
  for bstack11llll11l_opy_ in bstack1ll1l_opy_:
    if bstack11llll11l_opy_ in [bstackl_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ୕"), bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩୖ")]:
      next
    options.set_capability(bstack11llll11l_opy_, bstack1ll1l_opy_[bstack11llll11l_opy_])
  if bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪୗ") in bstack1ll1l_opy_:
    for arg in bstack1ll1l_opy_[bstackl_opy_ (u"࠭ࡡࡳࡩࡶࠫ୘")]:
      options.add_argument(arg)
  if bstackl_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ୙") in bstack1ll1l_opy_:
    options.use_technology_preview(bool(bstack1ll1l_opy_[bstackl_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬ୚")]))
def bstack1ll1111l_opy_(options, bstack11ll11lll_opy_):
  for bstack1lllll111_opy_ in bstack11ll11lll_opy_:
    if bstack1lllll111_opy_ in [bstackl_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭୛"), bstackl_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଡ଼")]:
      next
    options._options[bstack1lllll111_opy_] = bstack11ll11lll_opy_[bstack1lllll111_opy_]
  if bstackl_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨଢ଼") in bstack11ll11lll_opy_:
    for bstack11ll11l11_opy_ in bstack11ll11lll_opy_[bstackl_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୞")]:
      options.add_additional_option(
          bstack11ll11l11_opy_, bstack11ll11lll_opy_[bstackl_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪୟ")][bstack11ll11l11_opy_])
  if bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬୠ") in bstack11ll11lll_opy_:
    for arg in bstack11ll11lll_opy_[bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ୡ")]:
      options.add_argument(arg)
def bstack11l1lll11_opy_(options, caps):
  if not hasattr(options, bstackl_opy_ (u"ࠩࡎࡉ࡞࠭ୢ")):
    return
  if options.KEY == bstackl_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨୣ") and options.KEY in caps:
    bstack111llll_opy_(options, caps[bstackl_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୤")])
  elif options.KEY == bstackl_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ୥") and options.KEY in caps:
    bstack11l11ll_opy_(options, caps[bstackl_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ୦")])
  elif options.KEY == bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ୧") and options.KEY in caps:
    bstack1llll111_opy_(options, caps[bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ୨")])
  elif options.KEY == bstackl_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୩") and options.KEY in caps:
    bstack11ll1l1ll_opy_(options, caps[bstackl_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ୪")])
  elif options.KEY == bstackl_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୫") and options.KEY in caps:
    bstack1ll1111l_opy_(options, caps[bstackl_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ୬")])
def bstack11l1ll1l1_opy_(caps):
  global bstack11111l_opy_
  if bstack11111l_opy_:
    if bstack1lll111l_opy_() < version.parse(bstackl_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬ୭")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ୮")
    if bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୯") in caps:
      browser = caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ୰")]
    elif bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫୱ") in caps:
      browser = caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ୲")]
    browser = str(browser).lower()
    if browser == bstackl_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬ୳") or browser == bstackl_opy_ (u"࠭ࡩࡱࡣࡧࠫ୴"):
      browser = bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧ୵")
    if browser == bstackl_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩ୶"):
      browser = bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ୷")
    if browser not in [bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ୸"), bstackl_opy_ (u"ࠫࡪࡪࡧࡦࠩ୹"), bstackl_opy_ (u"ࠬ࡯ࡥࠨ୺"), bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭୻"), bstackl_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨ୼")]:
      return None
    try:
      package = bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ୽").format(browser)
      name = bstackl_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪ୾")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1111l_opy_(options):
        return None
      for bstack111lllll_opy_ in caps.keys():
        options.set_capability(bstack111lllll_opy_, caps[bstack111lllll_opy_])
      bstack11l1lll11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l111l1_opy_(options, bstack11lllll_opy_):
  if not bstack1l1111l_opy_(options):
    return
  for bstack111lllll_opy_ in bstack11lllll_opy_.keys():
    if bstack111lllll_opy_ in bstack1111l11_opy_:
      next
    if bstack111lllll_opy_ in options._caps and type(options._caps[bstack111lllll_opy_]) in [dict, list]:
      options._caps[bstack111lllll_opy_] = update(options._caps[bstack111lllll_opy_], bstack11lllll_opy_[bstack111lllll_opy_])
    else:
      options.set_capability(bstack111lllll_opy_, bstack11lllll_opy_[bstack111lllll_opy_])
  bstack11l1lll11_opy_(options, bstack11lllll_opy_)
  if bstackl_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩ୿") in options._caps:
    if options._caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ஀")] and options._caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ஁")].lower() != bstackl_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧஂ"):
      del options._caps[bstackl_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ஃ")]
def bstack1l11llll1_opy_(proxy_config):
  if bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ஄") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫஅ")] = proxy_config[bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧஆ")]
    del(proxy_config[bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨஇ")])
  if bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨஈ") in proxy_config and proxy_config[bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩஉ")].lower() != bstackl_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧஊ"):
    proxy_config[bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ஋")] = bstackl_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩ஌")
  if bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨ஍") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧஎ")] = bstackl_opy_ (u"ࠬࡶࡡࡤࠩஏ")
  return proxy_config
def bstack1l1llll1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬஐ") in config:
    return proxy
  config[bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭஑")] = bstack1l11llll1_opy_(config[bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧஒ")])
  if proxy == None:
    proxy = Proxy(config[bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨஓ")])
  return proxy
def bstack111ll11l_opy_(self):
  global CONFIG
  global bstack1llll1lll_opy_
  if bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ஔ") in CONFIG:
    return CONFIG[bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧக")]
  elif bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஖") in CONFIG:
    return CONFIG[bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ஗")]
  else:
    return bstack1llll1lll_opy_(self)
def bstack11l111l_opy_():
  global CONFIG
  return bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ஘") in CONFIG or bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬங") in CONFIG
def bstack111111_opy_(config):
  if not bstack11l111l_opy_():
    return
  if config.get(bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬச")):
    return config.get(bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭஛"))
  if config.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨஜ")):
    return config.get(bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஝"))
def bstack11l11l1l1_opy_():
  return bstack11l111l_opy_() and bstack1ll11lll_opy_() >= version.parse(bstack111lll11_opy_)
def bstack11llllll_opy_(config):
  if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪஞ") in config:
    return config[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫட")]
  if bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ஠") in config:
    return config[bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ஡")]
  return {}
def bstack1ll1111ll_opy_(config):
  if bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ஢") in config:
    return config[bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩண")]
  return {}
def bstack11l1111_opy_(caps):
  global bstack1l1ll11l1_opy_
  if bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭த") in caps:
    caps[bstackl_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ஥")][bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭஦")] = True
    if bstack1l1ll11l1_opy_:
      caps[bstackl_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ஧")][bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫந")] = bstack1l1ll11l1_opy_
  else:
    caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨன")] = True
    if bstack1l1ll11l1_opy_:
      caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬப")] = bstack1l1ll11l1_opy_
def bstack1l111l1l1_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ஫") in CONFIG and CONFIG[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ஬")]:
    bstack1lllll11_opy_ = bstack11llllll_opy_(CONFIG)
    bstack1ll1l1ll1_opy_(CONFIG[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ஭")], bstack1lllll11_opy_)
def bstack1ll1l1ll1_opy_(key, bstack1lllll11_opy_):
  global bstack1l1l11111_opy_
  logger.info(bstack1lll11_opy_)
  try:
    bstack1l1l11111_opy_ = Local()
    bstack11ll1l1l_opy_ = {bstackl_opy_ (u"ࠨ࡭ࡨࡽࠬம"): key}
    bstack11ll1l1l_opy_.update(bstack1lllll11_opy_)
    logger.debug(bstack1l11111_opy_.format(str(bstack11ll1l1l_opy_)))
    bstack1l1l11111_opy_.start(**bstack11ll1l1l_opy_)
    if bstack1l1l11111_opy_.isRunning():
      logger.info(bstack1lll1l111_opy_)
  except Exception as e:
    bstack1l1l1ll_opy_(bstack11lll1l1l_opy_.format(str(e)))
def bstack1ll111l11_opy_():
  global bstack1l1l11111_opy_
  if bstack1l1l11111_opy_.isRunning():
    logger.info(bstack11ll1l11_opy_)
    bstack1l1l11111_opy_.stop()
  bstack1l1l11111_opy_ = None
def bstack1l111111l_opy_(bstack11111111_opy_=[]):
  global CONFIG
  bstack11l1ll11_opy_ = []
  bstack11l11lll1_opy_ = [bstackl_opy_ (u"ࠩࡲࡷࠬய"), bstackl_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ர"), bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨற"), bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧல"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫள"), bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨழ")]
  try:
    for err in bstack11111111_opy_:
      bstack11111lll_opy_ = {}
      for k in bstack11l11lll1_opy_:
        val = CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫவ")][int(err[bstackl_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨஶ")])].get(k)
        if val:
          bstack11111lll_opy_[k] = val
      bstack11111lll_opy_[bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩஷ")] = {
        err[bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩஸ")]: err[bstackl_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫஹ")]
      }
      bstack11l1ll11_opy_.append(bstack11111lll_opy_)
  except Exception as e:
    logger.debug(bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨ஺") +str(e))
  finally:
    return bstack11l1ll11_opy_
def bstack1llll1l1l_opy_():
  global bstack1l111l_opy_
  global bstack1lll1llll_opy_
  global bstack1l1l1l11l_opy_
  if bstack1l111l_opy_:
    logger.warning(bstack1l111_opy_.format(str(bstack1l111l_opy_)))
  logger.info(bstack1lll1l11l_opy_)
  global bstack1l1l11111_opy_
  if bstack1l1l11111_opy_:
    bstack1ll111l11_opy_()
  try:
    for driver in bstack1lll1llll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l11l111l_opy_)
  bstack1lll11111_opy_()
  if len(bstack1l1l1l11l_opy_) > 0:
    message = bstack1l111111l_opy_(bstack1l1l1l11l_opy_)
    bstack1lll11111_opy_(message)
  else:
    bstack1lll11111_opy_()
def bstack1l1ll_opy_(self, *args):
  logger.error(bstack1l1l11l_opy_)
  bstack1llll1l1l_opy_()
  sys.exit(1)
def bstack1l1l1ll_opy_(err):
  logger.critical(bstack1l1111_opy_.format(str(err)))
  bstack1lll11111_opy_(bstack1l1111_opy_.format(str(err)))
  atexit.unregister(bstack1llll1l1l_opy_)
  sys.exit(1)
def bstack11ll1111l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1lll11111_opy_(message)
  atexit.unregister(bstack1llll1l1l_opy_)
  sys.exit(1)
def bstack1l111ll1_opy_():
  global CONFIG
  global bstack1l11ll111_opy_
  global bstack1ll11ll_opy_
  global bstack1ll11l11l_opy_
  CONFIG = bstack1l1l1111_opy_()
  bstack11lll11_opy_()
  bstack111llll1_opy_()
  CONFIG = bstack11lllll1l_opy_(CONFIG)
  update(CONFIG, bstack1ll11ll_opy_)
  update(CONFIG, bstack1l11ll111_opy_)
  CONFIG = bstack1l11lllll_opy_(CONFIG)
  if bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ஻") in CONFIG and str(CONFIG[bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ஼")]).lower() == bstackl_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ஽"):
    bstack1ll11l11l_opy_ = False
  if (bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ா") in CONFIG and bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧி") in bstack1l11ll111_opy_) or (bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨீ") in CONFIG and bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩு") not in bstack1ll11ll_opy_):
    if os.getenv(bstackl_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫூ")):
      CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௃")] = os.getenv(bstackl_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭௄"))
    else:
      bstack1ll1l1ll_opy_()
  elif (bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௅") not in CONFIG and bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ெ") in CONFIG) or (bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨே") in bstack1ll11ll_opy_ and bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩை") not in bstack1l11ll111_opy_):
    del(CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௉")])
  if bstack1l11ll1ll_opy_(CONFIG):
    bstack1l1l1ll_opy_(bstack1l11l1lll_opy_)
  bstack11l1l1l1l_opy_()
  bstack1lll1111l_opy_()
  if bstack11111l_opy_:
    CONFIG[bstackl_opy_ (u"ࠨࡣࡳࡴࠬொ")] = bstack1l1lll1_opy_(CONFIG)
    logger.info(bstack11l1111l_opy_.format(CONFIG[bstackl_opy_ (u"ࠩࡤࡴࡵ࠭ோ")]))
def bstack1lll1111l_opy_():
  global CONFIG
  global bstack11111l_opy_
  if bstackl_opy_ (u"ࠪࡥࡵࡶࠧௌ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11ll1111l_opy_(e, bstack1l1111111_opy_)
    bstack11111l_opy_ = True
def bstack1l1lll1_opy_(config):
  bstack1111ll11_opy_ = bstackl_opy_ (u"்ࠫࠬ")
  app = config[bstackl_opy_ (u"ࠬࡧࡰࡱࠩ௎")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11ll1111_opy_:
      if os.path.exists(app):
        bstack1111ll11_opy_ = bstack111lll_opy_(config, app)
      elif bstack11ll11ll_opy_(app):
        bstack1111ll11_opy_ = app
      else:
        bstack1l1l1ll_opy_(bstack11lll11l1_opy_.format(app))
    else:
      if bstack11ll11ll_opy_(app):
        bstack1111ll11_opy_ = app
      elif os.path.exists(app):
        bstack1111ll11_opy_ = bstack111lll_opy_(app)
      else:
        bstack1l1l1ll_opy_(bstack1l1ll1l_opy_)
  else:
    if len(app) > 2:
      bstack1l1l1ll_opy_(bstack1ll1ll11_opy_)
    elif len(app) == 2:
      if bstackl_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ௏") in app and bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪௐ") in app:
        if os.path.exists(app[bstackl_opy_ (u"ࠨࡲࡤࡸ࡭࠭௑")]):
          bstack1111ll11_opy_ = bstack111lll_opy_(config, app[bstackl_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ௒")], app[bstackl_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭௓")])
        else:
          bstack1l1l1ll_opy_(bstack11lll11l1_opy_.format(app))
      else:
        bstack1l1l1ll_opy_(bstack1ll1ll11_opy_)
    else:
      for key in app:
        if key in bstack1l11ll11_opy_:
          if key == bstackl_opy_ (u"ࠫࡵࡧࡴࡩࠩ௔"):
            if os.path.exists(app[key]):
              bstack1111ll11_opy_ = bstack111lll_opy_(config, app[key])
            else:
              bstack1l1l1ll_opy_(bstack11lll11l1_opy_.format(app))
          else:
            bstack1111ll11_opy_ = app[key]
        else:
          bstack1l1l1ll_opy_(bstack111l1l_opy_)
  return bstack1111ll11_opy_
def bstack11ll11ll_opy_(bstack1111ll11_opy_):
  import re
  bstack1l1ll1_opy_ = re.compile(bstackl_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ௕"))
  bstack1ll1l111_opy_ = re.compile(bstackl_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮࠴ࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ௖"))
  if bstackl_opy_ (u"ࠧࡣࡵ࠽࠳࠴࠭ௗ") in bstack1111ll11_opy_ or re.fullmatch(bstack1l1ll1_opy_, bstack1111ll11_opy_) or re.fullmatch(bstack1ll1l111_opy_, bstack1111ll11_opy_):
    return True
  else:
    return False
def bstack111lll_opy_(config, path, bstack1l1ll1l11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstackl_opy_ (u"ࠨࡴࡥࠫ௘")).read()).hexdigest()
  bstack1ll1l11l_opy_ = bstack1ll1ll11l_opy_(md5_hash)
  bstack1111ll11_opy_ = None
  if bstack1ll1l11l_opy_:
    logger.info(bstack1l1l11ll_opy_.format(bstack1ll1l11l_opy_, md5_hash))
    return bstack1ll1l11l_opy_
  bstack1ll11l1_opy_ = MultipartEncoder(
    fields={
        bstackl_opy_ (u"ࠩࡩ࡭ࡱ࡫ࠧ௙"): (os.path.basename(path), open(os.path.abspath(path), bstackl_opy_ (u"ࠪࡶࡧ࠭௚")), bstackl_opy_ (u"ࠫࡹ࡫ࡸࡵ࠱ࡳࡰࡦ࡯࡮ࠨ௛")),
        bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ௜"): bstack1l1ll1l11_opy_
    }
  )
  response = requests.post(bstack1l11l1ll_opy_, data=bstack1ll11l1_opy_,
                         headers={bstackl_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ௝"): bstack1ll11l1_opy_.content_type}, auth=(config[bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ௞")], config[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ௟")]))
  try:
    res = json.loads(response.text)
    bstack1111ll11_opy_ = res[bstackl_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪ௠")]
    logger.info(bstack11l11ll1_opy_.format(bstack1111ll11_opy_))
    bstack1l1llll1l_opy_(md5_hash, bstack1111ll11_opy_)
  except ValueError as err:
    bstack1l1l1ll_opy_(bstack1lllll_opy_.format(str(err)))
  return bstack1111ll11_opy_
def bstack11l1l1l1l_opy_():
  global CONFIG
  global bstack1l11ll11l_opy_
  bstack11lll11ll_opy_ = 0
  bstack11ll1l11l_opy_ = 1
  if bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ௡") in CONFIG:
    bstack11ll1l11l_opy_ = CONFIG[bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ௢")]
  if bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௣") in CONFIG:
    bstack11lll11ll_opy_ = len(CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௤")])
  bstack1l11ll11l_opy_ = int(bstack11ll1l11l_opy_) * int(bstack11lll11ll_opy_)
def bstack1ll1ll11l_opy_(md5_hash):
  bstack1ll1111_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩ௥")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ௦"), bstackl_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ௧"))
  if os.path.exists(bstack1ll1111_opy_):
    bstack1ll11ll1l_opy_ = json.load(open(bstack1ll1111_opy_,bstackl_opy_ (u"ࠪࡶࡧ࠭௨")))
    if md5_hash in bstack1ll11ll1l_opy_:
      bstack1l1111l11_opy_ = bstack1ll11ll1l_opy_[md5_hash]
      bstack1l1111ll1_opy_ = datetime.datetime.now()
      bstack1llll1ll_opy_ = datetime.datetime.strptime(bstack1l1111l11_opy_[bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ௩")], bstackl_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ௪"))
      if (bstack1l1111ll1_opy_ - bstack1llll1ll_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1111l11_opy_[bstackl_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ௫")]):
        return None
      return bstack1l1111l11_opy_[bstackl_opy_ (u"ࠧࡪࡦࠪ௬")]
  else:
    return None
def bstack1l1llll1l_opy_(md5_hash, bstack1111ll11_opy_):
  bstack1l1l1lll_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠨࢀࠪ௭")), bstackl_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ௮"))
  if not os.path.exists(bstack1l1l1lll_opy_):
    os.makedirs(bstack1l1l1lll_opy_)
  bstack1ll1111_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠪࢂࠬ௯")), bstackl_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ௰"), bstackl_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭௱"))
  bstack1llllll1_opy_ = {
    bstackl_opy_ (u"࠭ࡩࡥࠩ௲"): bstack1111ll11_opy_,
    bstackl_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ௳"): datetime.datetime.strftime(datetime.datetime.now(), bstackl_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ௴")),
    bstackl_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ௵"): str(__version__)
  }
  if os.path.exists(bstack1ll1111_opy_):
    bstack1ll11ll1l_opy_ = json.load(open(bstack1ll1111_opy_,bstackl_opy_ (u"ࠪࡶࡧ࠭௶")))
  else:
    bstack1ll11ll1l_opy_ = {}
  bstack1ll11ll1l_opy_[md5_hash] = bstack1llllll1_opy_
  with open(bstack1ll1111_opy_, bstackl_opy_ (u"ࠦࡼ࠱ࠢ௷")) as outfile:
    json.dump(bstack1ll11ll1l_opy_, outfile)
def bstack1llll11l1_opy_(self):
  return
def bstack1llll1_opy_(self):
  return
def bstack1l11l1111_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack11l1l111l_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l11ll_opy_
  global bstack1ll1lll1_opy_
  global bstack1l11111l1_opy_
  global bstack1l11l1l1_opy_
  global bstack11ll1lll1_opy_
  global bstack1llllllll_opy_
  global bstack11l11l11l_opy_
  global bstack1lll1llll_opy_
  global bstack11llll1_opy_
  CONFIG[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ௸")] = str(bstack1llllllll_opy_) + str(__version__)
  command_executor = bstack11ll11l1_opy_()
  logger.debug(bstack1lll1lll1_opy_.format(command_executor))
  proxy = bstack1l1llll1_opy_(CONFIG, proxy)
  bstack1l1l1_opy_ = 0 if bstack1ll1lll1_opy_ < 0 else bstack1ll1lll1_opy_
  if bstack1l11l1l1_opy_ is True:
    bstack1l1l1_opy_ = int(multiprocessing.current_process().name)
  if bstack11ll1lll1_opy_ is True:
    bstack1l1l1_opy_ = int(threading.current_thread().name)
  bstack11lllll_opy_ = bstack1l1111ll_opy_(CONFIG, bstack1l1l1_opy_)
  logger.debug(bstack1l11lll1_opy_.format(str(bstack11lllll_opy_)))
  if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ௹") in CONFIG and CONFIG[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ௺")]:
    bstack11l1111_opy_(bstack11lllll_opy_)
  if desired_capabilities:
    bstack11ll11l1l_opy_ = bstack11lllll1l_opy_(desired_capabilities)
    bstack11ll11l1l_opy_[bstackl_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ௻")] = bstack11l11l1ll_opy_(CONFIG)
    bstack11lll11l_opy_ = bstack1l1111ll_opy_(bstack11ll11l1l_opy_)
    if bstack11lll11l_opy_:
      bstack11lllll_opy_ = update(bstack11lll11l_opy_, bstack11lllll_opy_)
    desired_capabilities = None
  if options:
    bstack11l111l1_opy_(options, bstack11lllll_opy_)
  if not options:
    options = bstack11l1ll1l1_opy_(bstack11lllll_opy_)
  if proxy and bstack1ll11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ௼")):
    options.proxy(proxy)
  if options and bstack1ll11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ௽")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1ll11lll_opy_() < version.parse(bstackl_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ௾")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11lllll_opy_)
  logger.info(bstack11l1ll11l_opy_)
  if bstack1ll11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ௿")):
    bstack11l11l11l_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll11lll_opy_() >= version.parse(bstackl_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬఀ")):
    bstack11l11l11l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧఁ")):
    bstack11l11l11l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11l11l11l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack1l11llll_opy_ = bstackl_opy_ (u"ࠨࠩం")
    if bstack1ll11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪః")):
      bstack1l11llll_opy_ = self.caps.get(bstackl_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥఄ"))
    else:
      bstack1l11llll_opy_ = self.capabilities.get(bstackl_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦఅ"))
    if bstack1l11llll_opy_:
      if bstack1ll11lll_opy_() <= version.parse(bstackl_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬఆ")):
        self.command_executor._url = bstackl_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢఇ") + bstack1l111111_opy_ + bstackl_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦఈ")
      else:
        self.command_executor._url = bstackl_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥఉ") + bstack1l11llll_opy_ + bstackl_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥఊ")
      logger.debug(bstack111111l_opy_.format(bstack1l11llll_opy_))
    else:
      logger.debug(bstack1ll11l111_opy_.format(bstackl_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦఋ")))
  except Exception as e:
    logger.debug(bstack1ll11l111_opy_.format(e))
  if bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪఌ") in bstack1llllllll_opy_:
    bstack1l1ll1ll1_opy_(bstack1ll1lll1_opy_, bstack11llll1_opy_)
  bstack1l11ll_opy_ = self.session_id
  bstack1lll1llll_opy_.append(self)
  if bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ఍") in CONFIG and bstackl_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫఎ") in CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఏ")][bstack1l1l1_opy_]:
    bstack1l11111l1_opy_ = CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫఐ")][bstack1l1l1_opy_][bstackl_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ఑")]
  logger.debug(bstack1ll1l1l_opy_.format(bstack1l11ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1ll1lll11_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll111l1l_opy_
      if(bstackl_opy_ (u"ࠥ࡭ࡳࡪࡥࡹ࠰࡭ࡷࠧఒ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠫࢃ࠭ఓ")), bstackl_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬఔ"), bstackl_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨక")), bstackl_opy_ (u"ࠧࡸࠩఖ")) as fp:
          fp.write(bstackl_opy_ (u"ࠣࠤగ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦఘ")))):
          with open(args[1], bstackl_opy_ (u"ࠪࡶࠬఙ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstackl_opy_ (u"ࠫࡦࡹࡹ࡯ࡥࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡥ࡮ࡦࡹࡓࡥ࡬࡫ࠨࡤࡱࡱࡸࡪࡾࡴ࠭ࠢࡳࡥ࡬࡫ࠠ࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠪచ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11l11ll1l_opy_)
            lines.insert(1, bstack1ll1ll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢఛ")), bstackl_opy_ (u"࠭ࡷࠨజ")) as bstack1l11l1_opy_:
              bstack1l11l1_opy_.writelines(lines)
        CONFIG[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩఝ")] = str(bstack1llllllll_opy_) + str(__version__)
        bstack1l1l1_opy_ = 0 if bstack1ll1lll1_opy_ < 0 else bstack1ll1lll1_opy_
        if bstack1l11l1l1_opy_ is True:
          bstack1l1l1_opy_ = int(threading.current_thread().getName())
        CONFIG[bstackl_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣఞ")] = False
        CONFIG[bstackl_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣట")] = True
        bstack11lllll_opy_ = bstack1l1111ll_opy_(CONFIG, bstack1l1l1_opy_)
        logger.debug(bstack1l11lll1_opy_.format(str(bstack11lllll_opy_)))
        if CONFIG[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧఠ")]:
          bstack11l1111_opy_(bstack11lllll_opy_)
        if bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧడ") in CONFIG and bstackl_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪఢ") in CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩణ")][bstack1l1l1_opy_]:
          bstack1l11111l1_opy_ = CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪత")][bstack1l1l1_opy_][bstackl_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭థ")]
        args.append(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠩࢁࠫద")), bstackl_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪధ"), bstackl_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭న")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11lllll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ఩"))
      bstack1ll111l1l_opy_ = True
      return bstack1lll1l1l_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack1lll1l1ll_opy_(self,
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
    global bstack1l11ll_opy_
    global bstack1ll1lll1_opy_
    global bstack1l11111l1_opy_
    global bstack1l11l1l1_opy_
    global bstack1llllllll_opy_
    global bstack11l11l11l_opy_
    CONFIG[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨప")] = str(bstack1llllllll_opy_) + str(__version__)
    bstack1l1l1_opy_ = 0 if bstack1ll1lll1_opy_ < 0 else bstack1ll1lll1_opy_
    if bstack1l11l1l1_opy_ is True:
      bstack1l1l1_opy_ = int(threading.current_thread().getName())
    CONFIG[bstackl_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨఫ")] = True
    bstack11lllll_opy_ = bstack1l1111ll_opy_(CONFIG, bstack1l1l1_opy_)
    logger.debug(bstack1l11lll1_opy_.format(str(bstack11lllll_opy_)))
    if CONFIG[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬబ")]:
      bstack11l1111_opy_(bstack11lllll_opy_)
    if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬభ") in CONFIG and bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨమ") in CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧయ")][bstack1l1l1_opy_]:
      bstack1l11111l1_opy_ = CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨర")][bstack1l1l1_opy_][bstackl_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫఱ")]
    import urllib
    import json
    bstack1l1l11_opy_ = bstackl_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩల") + urllib.parse.quote(json.dumps(bstack11lllll_opy_))
    browser = self.connect(bstack1l1l11_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1lll111_opy_():
    global bstack1ll111l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1lll1l1ll_opy_
        bstack1ll111l1l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1lll11_opy_
      bstack1ll111l1l_opy_ = True
    except Exception as e:
      pass
def bstack1ll1l11_opy_(context, bstack11l1l111_opy_):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤళ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ఴ")+ json.dumps(bstack11l1l111_opy_) + bstackl_opy_ (u"ࠥࢁࢂࠨవ"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤశ"), e)
def bstack1lll111ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨష"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫస") + json.dumps(message) + bstackl_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪహ") + json.dumps(level) + bstackl_opy_ (u"ࠨࡿࢀࠫ఺"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧ఻"), e)
def bstack11l1ll1l_opy_(context, status, message = bstackl_opy_ (u"఼ࠥࠦ")):
  try:
    if(status == bstackl_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦఽ")):
      context.page.evaluate(bstackl_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨా"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡸࡥࡢࡵࡲࡲࠧࡀࠧి") + json.dumps(bstackl_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡࠤీ") + str(message)) + bstackl_opy_ (u"ࠨ࠮ࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠬు") + json.dumps(status) + bstackl_opy_ (u"ࠤࢀࢁࠧూ"))
    else:
      context.page.evaluate(bstackl_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦృ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠬౄ") + json.dumps(status) + bstackl_opy_ (u"ࠧࢃࡽࠣ౅"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥె"), e)
def bstack1llllll11_opy_(self, url):
  global bstack11l11111_opy_
  try:
    bstack11ll1ll_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll1llll1_opy_.format(str(err)))
  try:
    bstack11l11111_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll1l1l11_opy_ = str(e)
      if any(err_msg in bstack1ll1l1l11_opy_ for err_msg in bstack1ll1l1_opy_):
        bstack11ll1ll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll1llll1_opy_.format(str(err)))
    raise e
def bstack11111ll1_opy_(self):
  global bstack11l1l_opy_
  bstack11l1l_opy_ = self
  return
def bstack11ll1ll11_opy_(self, test):
  global CONFIG
  global bstack11l1l_opy_
  global bstack1l11ll_opy_
  global bstack11l11l111_opy_
  global bstack1l11111l1_opy_
  global bstack1lllllll_opy_
  global bstack1lll1ll_opy_
  global bstack1lll1llll_opy_
  try:
    if not bstack1l11ll_opy_:
      with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩే")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨై"), bstackl_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ౉"))) as f:
        bstack1l1llllll_opy_ = json.loads(bstackl_opy_ (u"ࠥࡿࠧొ") + f.read().strip() + bstackl_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ో") + bstackl_opy_ (u"ࠧࢃࠢౌ"))
        bstack1l11ll_opy_ = bstack1l1llllll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1lll1llll_opy_:
    for driver in bstack1lll1llll_opy_:
      if bstack1l11ll_opy_ == driver.session_id:
        if test:
          bstack1l1l1111l_opy_ = str(test.data)
        if not bstack11lll_opy_ and bstack1l1l1111l_opy_:
          bstack1ll11ll1_opy_ = {
            bstackl_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ్࠭"): bstackl_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ౎"),
            bstackl_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ౏"): {
              bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౐"): bstack1l1l1111l_opy_
            }
          }
          bstack1l1lll1ll_opy_ = bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ౑").format(json.dumps(bstack1ll11ll1_opy_))
          driver.execute_script(bstack1l1lll1ll_opy_)
        if bstack11l11l111_opy_:
          bstack1l1l1ll1_opy_ = {
            bstackl_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫ౒"): bstackl_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ౓"),
            bstackl_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ౔"): {
              bstackl_opy_ (u"ࠧࡥࡣࡷࡥౕࠬ"): bstack1l1l1111l_opy_ + bstackl_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥౖࠣࠪ"),
              bstackl_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ౗"): bstackl_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨౘ")
            }
          }
          bstack1ll11ll1_opy_ = {
            bstackl_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫౙ"): bstackl_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨౚ"),
            bstackl_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ౛"): {
              bstackl_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ౜"): bstackl_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨౝ")
            }
          }
          if bstack11l11l111_opy_.status == bstackl_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ౞"):
            bstack1ll1ll1l1_opy_ = bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ౟").format(json.dumps(bstack1l1l1ll1_opy_))
            driver.execute_script(bstack1ll1ll1l1_opy_)
            bstack1l1lll1ll_opy_ = bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩౠ").format(json.dumps(bstack1ll11ll1_opy_))
            driver.execute_script(bstack1l1lll1ll_opy_)
          elif bstack11l11l111_opy_.status == bstackl_opy_ (u"ࠬࡌࡁࡊࡎࠪౡ"):
            reason = bstackl_opy_ (u"ࠨࠢౢ")
            bstack11l111lll_opy_ = bstack1l1l1111l_opy_ + bstackl_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨౣ")
            if bstack11l11l111_opy_.message:
              reason = str(bstack11l11l111_opy_.message)
              bstack11l111lll_opy_ = bstack11l111lll_opy_ + bstackl_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ౤") + reason
            bstack1l1l1ll1_opy_[bstackl_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ౥")] = {
              bstackl_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ౦"): bstackl_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ౧"),
              bstackl_opy_ (u"ࠬࡪࡡࡵࡣࠪ౨"): bstack11l111lll_opy_
            }
            bstack1ll11ll1_opy_[bstackl_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ౩")] = {
              bstackl_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ౪"): bstackl_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ౫"),
              bstackl_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ౬"): reason
            }
            bstack1ll1ll1l1_opy_ = bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ౭").format(json.dumps(bstack1l1l1ll1_opy_))
            driver.execute_script(bstack1ll1ll1l1_opy_)
            bstack1l1lll1ll_opy_ = bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ౮").format(json.dumps(bstack1ll11ll1_opy_))
            driver.execute_script(bstack1l1lll1ll_opy_)
  elif bstack1l11ll_opy_:
    try:
      data = {}
      bstack1l1l1111l_opy_ = None
      if test:
        bstack1l1l1111l_opy_ = str(test.data)
      if not bstack11lll_opy_ and bstack1l1l1111l_opy_:
        data[bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౯")] = bstack1l1l1111l_opy_
      if bstack11l11l111_opy_:
        if bstack11l11l111_opy_.status == bstackl_opy_ (u"࠭ࡐࡂࡕࡖࠫ౰"):
          data[bstackl_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ౱")] = bstackl_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౲")
        elif bstack11l11l111_opy_.status == bstackl_opy_ (u"ࠩࡉࡅࡎࡒࠧ౳"):
          data[bstackl_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ౴")] = bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ౵")
          if bstack11l11l111_opy_.message:
            data[bstackl_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ౶")] = str(bstack11l11l111_opy_.message)
      user = CONFIG[bstackl_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ౷")]
      key = CONFIG[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ౸")]
      url = bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳ࠭౹").format(user, key, bstack1l11ll_opy_)
      headers = {
        bstackl_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ౺"): bstackl_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭౻"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll11111_opy_.format(str(e)))
  if bstack11l1l_opy_:
    bstack1lll1ll_opy_(bstack11l1l_opy_)
  bstack1lllllll_opy_(self, test)
def bstack11llll1l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll_opy_
  bstack1llll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l11l111_opy_
  bstack11l11l111_opy_ = self._test
def bstack1l1111lll_opy_():
  global bstack1lllll1l1_opy_
  try:
    if os.path.exists(bstack1lllll1l1_opy_):
      os.remove(bstack1lllll1l1_opy_)
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ౼") + str(e))
def bstack11l1lll_opy_():
  global bstack1lllll1l1_opy_
  bstack1ll1111l1_opy_ = {}
  try:
    if not os.path.isfile(bstack1lllll1l1_opy_):
      with open(bstack1lllll1l1_opy_, bstackl_opy_ (u"ࠬࡽࠧ౽")):
        pass
      with open(bstack1lllll1l1_opy_, bstackl_opy_ (u"ࠨࡷࠬࠤ౾")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1lllll1l1_opy_):
      bstack1ll1111l1_opy_ = json.load(open(bstack1lllll1l1_opy_, bstackl_opy_ (u"ࠧࡳࡤࠪ౿")))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪಀ") + str(e))
  finally:
    return bstack1ll1111l1_opy_
def bstack1l1ll1ll1_opy_(platform_index, item_index):
  global bstack1lllll1l1_opy_
  try:
    bstack1ll1111l1_opy_ = bstack11l1lll_opy_()
    bstack1ll1111l1_opy_[item_index] = platform_index
    with open(bstack1lllll1l1_opy_, bstackl_opy_ (u"ࠤࡺ࠯ࠧಁ")) as outfile:
      json.dump(bstack1ll1111l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨಂ") + str(e))
def bstack1lll1l1l1_opy_(bstack111ll1_opy_):
  global CONFIG
  bstack111ll111_opy_ = bstackl_opy_ (u"ࠫࠬಃ")
  if not bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ಄") in CONFIG:
    logger.info(bstackl_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪಅ"))
  try:
    platform = CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಆ")][bstack111ll1_opy_]
    if bstackl_opy_ (u"ࠨࡱࡶࠫಇ") in platform:
      bstack111ll111_opy_ += str(platform[bstackl_opy_ (u"ࠩࡲࡷࠬಈ")]) + bstackl_opy_ (u"ࠪ࠰ࠥ࠭ಉ")
    if bstackl_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧಊ") in platform:
      bstack111ll111_opy_ += str(platform[bstackl_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨಋ")]) + bstackl_opy_ (u"࠭ࠬࠡࠩಌ")
    if bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ಍") in platform:
      bstack111ll111_opy_ += str(platform[bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬಎ")]) + bstackl_opy_ (u"ࠩ࠯ࠤࠬಏ")
    if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬಐ") in platform:
      bstack111ll111_opy_ += str(platform[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭಑")]) + bstackl_opy_ (u"ࠬ࠲ࠠࠨಒ")
    if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫಓ") in platform:
      bstack111ll111_opy_ += str(platform[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬಔ")]) + bstackl_opy_ (u"ࠨ࠮ࠣࠫಕ")
    if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪಖ") in platform:
      bstack111ll111_opy_ += str(platform[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫಗ")]) + bstackl_opy_ (u"ࠫ࠱ࠦࠧಘ")
  except Exception as e:
    logger.debug(bstackl_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬಙ") + str(e))
  finally:
    if bstack111ll111_opy_[len(bstack111ll111_opy_) - 2:] == bstackl_opy_ (u"࠭ࠬࠡࠩಚ"):
      bstack111ll111_opy_ = bstack111ll111_opy_[:-2]
    return bstack111ll111_opy_
def bstack1ll111_opy_(path, bstack111ll111_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1ll111ll_opy_ = ET.parse(path)
    bstack1l111ll1l_opy_ = bstack1ll111ll_opy_.getroot()
    bstack1l1l11l1_opy_ = None
    for suite in bstack1l111ll1l_opy_.iter(bstackl_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ಛ")):
      if bstackl_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨಜ") in suite.attrib:
        suite.attrib[bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧಝ")] += bstackl_opy_ (u"ࠪࠤࠬಞ") + bstack111ll111_opy_
        bstack1l1l11l1_opy_ = suite
    bstack1111ll1_opy_ = None
    for robot in bstack1l111ll1l_opy_.iter(bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪಟ")):
      bstack1111ll1_opy_ = robot
    bstack1111111_opy_ = len(bstack1111ll1_opy_.findall(bstackl_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫಠ")))
    if bstack1111111_opy_ == 1:
      bstack1111ll1_opy_.remove(bstack1111ll1_opy_.findall(bstackl_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬಡ"))[0])
      bstack11l1ll1ll_opy_ = ET.Element(bstackl_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ಢ"), attrib={bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಣ"):bstackl_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩತ"), bstackl_opy_ (u"ࠪ࡭ࡩ࠭ಥ"):bstackl_opy_ (u"ࠫࡸ࠶ࠧದ")})
      bstack1111ll1_opy_.insert(1, bstack11l1ll1ll_opy_)
      bstack11l1lll1l_opy_ = None
      for suite in bstack1111ll1_opy_.iter(bstackl_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫಧ")):
        bstack11l1lll1l_opy_ = suite
      bstack11l1lll1l_opy_.append(bstack1l1l11l1_opy_)
      bstack1ll1llll_opy_ = None
      for status in bstack1l1l11l1_opy_.iter(bstackl_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ನ")):
        bstack1ll1llll_opy_ = status
      bstack11l1lll1l_opy_.append(bstack1ll1llll_opy_)
    bstack1ll111ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬ಩") + str(e))
def bstack111ll1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1lll11l11_opy_
  global CONFIG
  if bstackl_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧಪ") in options:
    del options[bstackl_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨಫ")]
  bstack1llll1ll1_opy_ = bstack11l1lll_opy_()
  for bstack11l111ll_opy_ in bstack1llll1ll1_opy_.keys():
    path = os.path.join(os.getcwd(), bstackl_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪಬ"), str(bstack11l111ll_opy_), bstackl_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨಭ"))
    bstack1ll111_opy_(path, bstack1lll1l1l1_opy_(bstack1llll1ll1_opy_[bstack11l111ll_opy_]))
  bstack1l1111lll_opy_()
  return bstack1lll11l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1111l1l_opy_(self, ff_profile_dir):
  global bstack11l11l11_opy_
  if not ff_profile_dir:
    return None
  return bstack11l11l11_opy_(self, ff_profile_dir)
def bstack1l1l1l11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1ll11l1_opy_
  bstack1111l1_opy_ = []
  if bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨಮ") in CONFIG:
    bstack1111l1_opy_ = CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಯ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstackl_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣರ")],
      pabot_args[bstackl_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤಱ")],
      argfile,
      pabot_args.get(bstackl_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢಲ")),
      pabot_args[bstackl_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨಳ")],
      platform[0],
      bstack1l1ll11l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstackl_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ಴")] or [(bstackl_opy_ (u"ࠧࠨವ"), None)]
    for platform in enumerate(bstack1111l1_opy_)
  ]
def bstack1ll1lllll_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack11ll1l_opy_=bstackl_opy_ (u"࠭ࠧಶ")):
  global bstack1111l11l_opy_
  self.platform_index = platform_index
  self.bstack11l11ll11_opy_ = bstack11ll1l_opy_
  bstack1111l11l_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1111lll1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1l11l1_opy_
  global bstack1l1lll_opy_
  if not bstackl_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩಷ") in item.options:
    item.options[bstackl_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಸ")] = []
  for v in item.options[bstackl_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫಹ")]:
    if bstackl_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩ಺") in v:
      item.options[bstackl_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭಻")].remove(v)
    if bstackl_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ಼ࠬ") in v:
      item.options[bstackl_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨಽ")].remove(v)
  item.options[bstackl_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩಾ")].insert(0, bstackl_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪಿ").format(item.platform_index))
  item.options[bstackl_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫೀ")].insert(0, bstackl_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪು").format(item.bstack11l11ll11_opy_))
  if bstack1l1lll_opy_:
    item.options[bstackl_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ೂ")].insert(0, bstackl_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨೃ").format(bstack1l1lll_opy_))
  return bstack1ll1l11l1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l1lll1l_opy_(command, item_index):
  global bstack1l1lll_opy_
  if bstack1l1lll_opy_:
    command[0] = command[0].replace(bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬೄ"), bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫ೅") + str(item_index) + bstack1l1lll_opy_, 1)
  else:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧೆ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭ೇ") + str(item_index), 1)
def bstack111l11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l11111l_opy_
  bstack1l1lll1l_opy_(command, item_index)
  return bstack1l11111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll11lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l11111l_opy_
  bstack1l1lll1l_opy_(command, item_index)
  return bstack1l11111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l11111l_opy_
  bstack1l1lll1l_opy_(command, item_index)
  return bstack1l11111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack111l11ll_opy_(self, runner, quiet=False, capture=True):
  global bstack11ll1ll1_opy_
  bstack11lll1ll_opy_ = bstack11ll1ll1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstackl_opy_ (u"ࠪࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡥࡡࡳࡴࠪೈ")):
      runner.exception_arr = []
    if not hasattr(runner, bstackl_opy_ (u"ࠫࡪࡾࡣࡠࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࡣࡦࡸࡲࠨ೉")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11lll1ll_opy_
def bstack1llll111l_opy_(self, name, context, *args):
  global bstack111l111_opy_
  if name in [bstackl_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ೊ"), bstackl_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨೋ")]:
    bstack111l111_opy_(self, name, context, *args)
  if name == bstackl_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨೌ"):
    try:
      if(not bstack11lll_opy_):
        bstack11l1l111_opy_ = str(self.feature.name)
        bstack1ll1l11_opy_(context, bstack11l1l111_opy_)
        context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾್ࠥ࠭") + json.dumps(bstack11l1l111_opy_) + bstackl_opy_ (u"ࠩࢀࢁࠬ೎"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ೏").format(str(e)))
  if name == bstackl_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭೐"):
    try:
      if not hasattr(self, bstackl_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ೑")):
        self.driver_before_scenario = True
      if(not bstack11lll_opy_):
        bstack11ll1ll1l_opy_ = args[0].name
        bstack11l1l1111_opy_ = bstack11l1l111_opy_ = str(self.feature.name)
        bstack11l1l111_opy_ = bstack11l1l1111_opy_ + bstackl_opy_ (u"࠭ࠠ࠮ࠢࠪ೒") + bstack11ll1ll1l_opy_
        if self.driver_before_scenario:
          bstack1ll1l11_opy_(context, bstack11l1l111_opy_)
          context.browser.execute_script(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ೓") + json.dumps(bstack11l1l111_opy_) + bstackl_opy_ (u"ࠨࡿࢀࠫ೔"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪೕ").format(str(e)))
  if name == bstackl_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫೖ"):
    try:
      bstack1llll1l1_opy_ = args[0].status.name
      if str(bstack1llll1l1_opy_).lower() == bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ೗"):
        bstack11ll111l_opy_ = bstackl_opy_ (u"ࠬ࠭೘")
        bstack1l1lllll1_opy_ = bstackl_opy_ (u"࠭ࠧ೙")
        bstack1111_opy_ = bstackl_opy_ (u"ࠧࠨ೚")
        try:
          import traceback
          bstack11ll111l_opy_ = self.exception.__class__.__name__
          bstack1ll11l1ll_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1l1lllll1_opy_ = bstackl_opy_ (u"ࠨࠢࠪ೛").join(bstack1ll11l1ll_opy_)
          bstack1111_opy_ = bstack1ll11l1ll_opy_[-1]
        except Exception as e:
          logger.debug(bstack1lll1ll1_opy_.format(str(e)))
        bstack11ll111l_opy_ += bstack1111_opy_
        bstack1lll111ll_opy_(context, json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ೜") + str(bstack1l1lllll1_opy_)), bstackl_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤೝ"))
        if self.driver_before_scenario:
          bstack11l1ll1l_opy_(context, bstackl_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦೞ"), bstack11ll111l_opy_)
        context.browser.execute_script(bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ೟") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧೠ") + str(bstack1l1lllll1_opy_)) + bstackl_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧೡ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨೢ") + json.dumps(bstackl_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨೣ") + str(bstack11ll111l_opy_)) + bstackl_opy_ (u"ࠪࢁࢂ࠭೤"))
      else:
        bstack1lll111ll_opy_(context, bstackl_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧ೥"), bstackl_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ೦"))
        if self.driver_before_scenario:
          bstack11l1ll1l_opy_(context, bstackl_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ೧"))
        context.browser.execute_script(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ೨") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ೩")) + bstackl_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ೪"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦࡵࡧࡳࡴࡧࡧࠦࢂࢃࠧ೫"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭೬").format(str(e)))
  if name == bstackl_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ೭"):
    try:
      if context.failed is True:
        bstack1l1ll11l_opy_ = []
        bstack1l11l111_opy_ = []
        bstack11lll1l_opy_ = []
        bstack11ll1l1l1_opy_ = bstackl_opy_ (u"࠭ࠧ೮")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l1ll11l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll11l1ll_opy_ = traceback.format_tb(exc_tb)
            bstack11llll111_opy_ = bstackl_opy_ (u"ࠧࠡࠩ೯").join(bstack1ll11l1ll_opy_)
            bstack1l11l111_opy_.append(bstack11llll111_opy_)
            bstack11lll1l_opy_.append(bstack1ll11l1ll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1lll1ll1_opy_.format(str(e)))
        bstack11ll111l_opy_ = bstackl_opy_ (u"ࠨࠩ೰")
        for i in range(len(bstack1l1ll11l_opy_)):
          bstack11ll111l_opy_ += bstack1l1ll11l_opy_[i] + bstack11lll1l_opy_[i] + bstackl_opy_ (u"ࠩ࡟ࡲࠬೱ")
        bstack11ll1l1l1_opy_ = bstackl_opy_ (u"ࠪࠤࠬೲ").join(bstack1l11l111_opy_)
        if not self.driver_before_scenario:
          bstack1lll111ll_opy_(context, bstack11ll1l1l1_opy_, bstackl_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥೳ"))
          bstack11l1ll1l_opy_(context, bstackl_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ೴"), bstack11ll111l_opy_)
          context.browser.execute_script(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ೵") + json.dumps(bstack11ll1l1l1_opy_) + bstackl_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧ೶"))
          context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨ೷") + json.dumps(bstackl_opy_ (u"ࠤࡖࡳࡲ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰࡵࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡡࡴࠢ೸") + str(bstack11ll111l_opy_)) + bstackl_opy_ (u"ࠪࢁࢂ࠭೹"))
      else:
        if not self.driver_before_scenario:
          bstack1lll111ll_opy_(context, bstackl_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢ೺") + str(self.feature.name) + bstackl_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ೻"), bstackl_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ೼"))
          bstack11l1ll1l_opy_(context, bstackl_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ೽"))
          context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭೾") + json.dumps(bstackl_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧ೿") + str(self.feature.name) + bstackl_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧഀ")) + bstackl_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪഁ"))
          context.browser.execute_script(bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡰࡢࡵࡶࡩࡩࠨࡽࡾࠩം"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨഃ").format(str(e)))
  if name in [bstackl_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧഄ"), bstackl_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩഅ")]:
    bstack111l111_opy_(self, name, context, *args)
    if (name == bstackl_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪആ") and self.driver_before_scenario) or (name == bstackl_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪഇ") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack1lllllll1_opy_(config, startdir):
  return bstackl_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࠰ࡾࠤഈ").format(bstackl_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦഉ"))
class Notset:
  def __repr__(self):
    return bstackl_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣഊ")
notset = Notset()
def bstack1ll11l1l1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11llll1ll_opy_
  if str(name).lower() == bstackl_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧഋ"):
    return bstackl_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢഌ")
  else:
    return bstack11llll1ll_opy_(self, name, default, skip)
def bstack1llll1l_opy_(item, when):
  global bstack1ll111ll1_opy_
  try:
    bstack1ll111ll1_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11_opy_():
  return
def bstack1llllll_opy_(bstack1lllll1_opy_):
  global bstack1llllllll_opy_
  global bstack1ll111l1l_opy_
  bstack1llllllll_opy_ = bstack1lllll1_opy_
  logger.info(bstack11ll1llll_opy_.format(bstack1llllllll_opy_.split(bstackl_opy_ (u"ࠩ࠰ࠫ഍"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack1llll11l1_opy_
    Service.stop = bstack1llll1_opy_
    webdriver.Remote.__init__ = bstack11l1l111l_opy_
    webdriver.Remote.get = bstack1llllll11_opy_
    WebDriver.close = bstack1l11l1111_opy_
    bstack1ll111l1l_opy_ = True
  except Exception as e:
    pass
  bstack1l1lll111_opy_()
  if not bstack1ll111l1l_opy_:
    bstack11ll1111l_opy_(bstackl_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧഎ"), bstack11lll1_opy_)
  if bstack11l11l1l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack111ll11l_opy_
    except Exception as e:
      logger.error(bstack1111ll_opy_.format(str(e)))
  if (bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪഏ") in str(bstack1lllll1_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1111l1l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11111ll1_opy_
      except Exception as e:
        logger.warn(bstack1ll1l11ll_opy_ + str(e))
    except Exception as e:
      bstack11ll1111l_opy_(e, bstack1ll1l11ll_opy_)
    Output.end_test = bstack11ll1ll11_opy_
    TestStatus.__init__ = bstack11llll1l1_opy_
    QueueItem.__init__ = bstack1ll1lllll_opy_
    pabot._create_items = bstack1l1l1l11_opy_
    try:
      from pabot import __version__ as bstack1l111lll_opy_
      if version.parse(bstack1l111lll_opy_) >= version.parse(bstackl_opy_ (u"ࠬ࠸࠮࠲࠷࠱࠴ࠬഐ")):
        pabot._run = bstack11ll11_opy_
      elif version.parse(bstack1l111lll_opy_) >= version.parse(bstackl_opy_ (u"࠭࠲࠯࠳࠶࠲࠵࠭഑")):
        pabot._run = bstack1ll11lll1_opy_
      else:
        pabot._run = bstack111l11l1_opy_
    except Exception as e:
      pabot._run = bstack111l11l1_opy_
    pabot._create_command_for_execution = bstack1111lll1_opy_
    pabot._report_results = bstack111ll1ll_opy_
  if bstackl_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧഒ") in str(bstack1lllll1_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11ll1111l_opy_(e, bstack1lll1_opy_)
    Runner.run_hook = bstack1llll111l_opy_
    Step.run = bstack111l11ll_opy_
  if bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨഓ") in str(bstack1lllll1_opy_).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      from _pytest import runner
      pytest_selenium.pytest_report_header = bstack1lllllll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l11_opy_
      Config.getoption = bstack1ll11l1l1_opy_
      runner._update_current_test_var = bstack1llll1l_opy_
    except Exception as e:
      pass
def bstack1ll1ll1l_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩഔ") in CONFIG and int(CONFIG[bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪക")]) > 1:
    logger.warn(bstack1l1llll_opy_)
def bstack11lllll1_opy_(arg):
  arg.append(bstackl_opy_ (u"ࠦ࠲࠳ࡣࡢࡲࡷࡹࡷ࡫࠽ࡴࡻࡶࠦഖ"))
  arg.append(bstackl_opy_ (u"ࠧ࠳ࡗࠣഗ"))
  arg.append(bstackl_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡍࡰࡦࡸࡰࡪࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪ࡯ࡳࡳࡷࡺࡥࡥ࠼ࡳࡽࡹ࡫ࡳࡵ࠰ࡓࡽࡹ࡫ࡳࡵ࡙ࡤࡶࡳ࡯࡮ࡨࠤഘ"))
  global CONFIG
  bstack1llllll_opy_(bstack1l1ll1ll_opy_)
  os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨങ")] = CONFIG[bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪച")]
  os.environ[bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬഛ")] = CONFIG[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ജ")]
  from _pytest.config import main as bstack1l1l1l_opy_
  bstack1l1l1l_opy_(arg)
def bstack1ll111lll_opy_(arg):
  bstack1llllll_opy_(bstack1l1l1lll1_opy_)
  from behave.__main__ import main as bstack111l1111_opy_
  bstack111l1111_opy_(arg)
def bstack111lll1l_opy_():
  logger.info(bstack111l1lll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪഝ"), help=bstackl_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭ഞ"))
  parser.add_argument(bstackl_opy_ (u"࠭࠭ࡶࠩട"), bstackl_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫഠ"), help=bstackl_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧഡ"))
  parser.add_argument(bstackl_opy_ (u"ࠩ࠰࡯ࠬഢ"), bstackl_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩണ"), help=bstackl_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬത"))
  parser.add_argument(bstackl_opy_ (u"ࠬ࠳ࡦࠨഥ"), bstackl_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫദ"), help=bstackl_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ധ"))
  bstack11l1lll1_opy_ = parser.parse_args()
  try:
    bstack11l1l11ll_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬന")
    if bstack11l1lll1_opy_.framework and bstack11l1lll1_opy_.framework not in (bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩഩ"), bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫപ")):
      bstack11l1l11ll_opy_ = bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪഫ")
    bstack1111l1ll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1l11ll_opy_)
    bstack1lll1ll1l_opy_ = open(bstack1111l1ll_opy_, bstackl_opy_ (u"ࠬࡸࠧബ"))
    bstack111l_opy_ = bstack1lll1ll1l_opy_.read()
    bstack1lll1ll1l_opy_.close()
    if bstack11l1lll1_opy_.username:
      bstack111l_opy_ = bstack111l_opy_.replace(bstackl_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ഭ"), bstack11l1lll1_opy_.username)
    if bstack11l1lll1_opy_.key:
      bstack111l_opy_ = bstack111l_opy_.replace(bstackl_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩമ"), bstack11l1lll1_opy_.key)
    if bstack11l1lll1_opy_.framework:
      bstack111l_opy_ = bstack111l_opy_.replace(bstackl_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩയ"), bstack11l1lll1_opy_.framework)
    file_name = bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬര")
    file_path = os.path.abspath(file_name)
    bstack1111lll_opy_ = open(file_path, bstackl_opy_ (u"ࠪࡻࠬറ"))
    bstack1111lll_opy_.write(bstack111l_opy_)
    bstack1111lll_opy_.close()
    logger.info(bstack1lll1lll_opy_)
    try:
      os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ല")] = bstack11l1lll1_opy_.framework if bstack11l1lll1_opy_.framework != None else bstackl_opy_ (u"ࠧࠨള")
      config = yaml.safe_load(bstack111l_opy_)
      config[bstackl_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ഴ")] = bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭വ")
      bstack1l111ll_opy_(bstack1ll1ll_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1ll1l1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11l1l1ll_opy_.format(str(e)))
def bstack1l111ll_opy_(bstack1ll11111l_opy_, config, bstack11l1l1_opy_ = {}):
  global bstack1ll11l11l_opy_
  if not config:
    return
  bstack1ll1l1l1_opy_ = bstack1l1l11l11_opy_ if not bstack1ll11l11l_opy_ else ( bstack1lllll11l_opy_ if bstackl_opy_ (u"ࠨࡣࡳࡴࠬശ") in config else bstack111l1ll_opy_ )
  data = {
    bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫഷ"): config[bstackl_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬസ")],
    bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧഹ"): config[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨഺ")],
    bstackl_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ഻ࠪ"): bstack1ll11111l_opy_,
    bstackl_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵ഼ࠪ"): {
      bstackl_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ഽ"): str(config[bstackl_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩാ")]) if bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪി") in config else bstackl_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧീ"),
      bstackl_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧു"): bstack1lll11l_opy_(os.getenv(bstackl_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣൂ"), bstackl_opy_ (u"ࠢࠣൃ"))),
      bstackl_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪൄ"): bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ൅"),
      bstackl_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫെ"): bstack1ll1l1l1_opy_,
      bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧേ"): config[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨൈ")]if config[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ൉")] else bstackl_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣൊ"),
      bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪോ"): str(config[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫൌ")]) if bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ്ࠬ") in config else bstackl_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧൎ"),
      bstackl_opy_ (u"ࠬࡵࡳࠨ൏"): sys.platform,
      bstackl_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨ൐"): socket.gethostname()
    }
  }
  update(data[bstackl_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ൑")], bstack11l1l1_opy_)
  try:
    response = bstack1l1lll1l1_opy_(bstackl_opy_ (u"ࠨࡒࡒࡗ࡙࠭൒"), bstack1llll11l_opy_, data, config)
    if response:
      logger.debug(bstack1l111l111_opy_.format(bstack1ll11111l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111l1l11_opy_.format(str(e)))
def bstack1l1lll1l1_opy_(type, url, data, config):
  bstack11ll_opy_ = bstack11l11lll_opy_.format(url)
  proxy = bstack111111_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ൓")) or config.get(bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧൔ")):
    proxies = {
      bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪൕ"): proxy
    }
  if type == bstackl_opy_ (u"ࠬࡖࡏࡔࡖࠪൖ"):
    response = requests.post(bstack11ll_opy_, json=data,
                    headers={bstackl_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬൗ"): bstackl_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ൘")}, auth=(config[bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ൙")], config[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ൚")]), proxies=proxies)
  return response
def bstack1lll11l_opy_(framework):
  return bstackl_opy_ (u"ࠥࡿࢂ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ൛").format(str(framework), __version__) if framework else bstackl_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ൜").format(__version__)
def bstack11l1l11_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1l111ll1_opy_()
    logger.debug(bstack1l11l_opy_.format(str(CONFIG)))
    bstack11lll1l11_opy_()
    bstack111111l1_opy_()
  except Exception as e:
    logger.error(bstackl_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠤ൝") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1lllll1l_opy_
  atexit.register(bstack1llll1l1l_opy_)
  signal.signal(signal.SIGINT, bstack1l1ll_opy_)
  signal.signal(signal.SIGTERM, bstack1l1ll_opy_)
def bstack1lllll1l_opy_(exctype, value, traceback):
  global bstack1lll1llll_opy_
  try:
    for driver in bstack1lll1llll_opy_:
      driver.execute_script(
        bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡧࡣ࡬ࡰࡪࡪࠢ࠭ࠢࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠥ࠭൞") + json.dumps(bstackl_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥൟ") + str(value)) + bstackl_opy_ (u"ࠨࡿࢀࠫൠ"))
  except Exception:
    pass
  bstack1lll11111_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1lll11111_opy_(message = bstackl_opy_ (u"ࠩࠪൡ")):
  global CONFIG
  try:
    if message:
      bstack11l1l1_opy_ = {
        bstackl_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩൢ"): str(message)
      }
      bstack1l111ll_opy_(bstack1l111l1ll_opy_, CONFIG, bstack11l1l1_opy_)
    else:
      bstack1l111ll_opy_(bstack1l111l1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack111lll1_opy_.format(str(e)))
def bstack1lll1l1_opy_(bstack1ll1l1lll_opy_, size):
  bstack1lll1ll11_opy_ = []
  while len(bstack1ll1l1lll_opy_) > size:
    bstack1l1l1l1ll_opy_ = bstack1ll1l1lll_opy_[:size]
    bstack1lll1ll11_opy_.append(bstack1l1l1l1ll_opy_)
    bstack1ll1l1lll_opy_   = bstack1ll1l1lll_opy_[size:]
  bstack1lll1ll11_opy_.append(bstack1ll1l1lll_opy_)
  return bstack1lll1ll11_opy_
def run_on_browserstack(bstack1l11lll_opy_=None, bstack11111_opy_=None):
  global CONFIG
  global bstack1l111111_opy_
  bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠫࠬൣ")
  if bstack1l11lll_opy_:
    CONFIG = bstack1l11lll_opy_[bstackl_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ൤")]
    bstack1l111111_opy_ = bstack1l11lll_opy_[bstackl_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ൥")]
    bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൦")
  if len(sys.argv) <= 1:
    logger.critical(bstack1l111llll_opy_)
    return
  if sys.argv[1] == bstackl_opy_ (u"ࠨ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫ൧")  or sys.argv[1] == bstackl_opy_ (u"ࠩ࠰ࡺࠬ൨"):
    logger.info(bstackl_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠦࡶࡼࡿࠪ൩").format(__version__))
    return
  if sys.argv[1] == bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ൪"):
    bstack111lll1l_opy_()
    return
  args = sys.argv
  bstack11l1l11_opy_()
  global bstack1l11ll11l_opy_
  global bstack1l11l1l1_opy_
  global bstack11ll1lll1_opy_
  global bstack1ll1lll1_opy_
  global bstack1l1ll11l1_opy_
  global bstack1l1lll_opy_
  global bstack1l1l1l11l_opy_
  if not bstack11l1l1l1_opy_:
    if args[1] == bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൫") or args[1] == bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ൬"):
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൭")
      args = args[2:]
    elif args[1] == bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൮"):
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൯")
      args = args[2:]
    elif args[1] == bstackl_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ൰"):
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ൱")
      args = args[2:]
    elif args[1] == bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭൲"):
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ൳")
      args = args[2:]
    elif args[1] == bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ൴"):
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ൵")
      args = args[2:]
    elif args[1] == bstackl_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ൶"):
      bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ൷")
      args = args[2:]
    else:
      if not bstackl_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ൸") in CONFIG or str(CONFIG[bstackl_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ൹")]).lower() in [bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ൺ"), bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨൻ")]:
        bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨർ")
        args = args[1:]
      elif str(CONFIG[bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬൽ")]).lower() == bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩൾ"):
        bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪൿ")
        args = args[1:]
      elif str(CONFIG[bstackl_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ඀")]).lower() == bstackl_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬඁ"):
        bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ං")
        args = args[1:]
      elif str(CONFIG[bstackl_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫඃ")]).lower() == bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ඄"):
        bstack11l1l1l1_opy_ = bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඅ")
        args = args[1:]
      elif str(CONFIG[bstackl_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧආ")]).lower() == bstackl_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬඇ"):
        bstack11l1l1l1_opy_ = bstackl_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඈ")
        args = args[1:]
      else:
        os.environ[bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩඉ")] = bstack11l1l1l1_opy_
        bstack1l1l1ll_opy_(bstack1lll11ll1_opy_)
  global bstack1lll1l1l_opy_
  if bstack1l11lll_opy_:
    try:
      os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪඊ")] = bstack11l1l1l1_opy_
      bstack1l111ll_opy_(bstack11111l1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack111lll1_opy_.format(str(e)))
  global bstack11l11l11l_opy_
  global bstack1lllllll_opy_
  global bstack1lll1ll_opy_
  global bstack1llll_opy_
  global bstack11l11l11_opy_
  global bstack1l11111l_opy_
  global bstack1111l11l_opy_
  global bstack1ll1l11l1_opy_
  global bstack11llll1l_opy_
  global bstack111l111_opy_
  global bstack11ll1ll1_opy_
  global bstack11l11111_opy_
  global bstack1llll1lll_opy_
  global bstack11llll1ll_opy_
  global bstack1ll111ll1_opy_
  global bstack1lll11l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l11l11l_opy_ = webdriver.Remote.__init__
    bstack11llll1l_opy_ = WebDriver.close
    bstack11l11111_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lll1l1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack11l111l_opy_():
    if bstack1ll11lll_opy_() < version.parse(bstack111lll11_opy_):
      logger.error(bstack11ll111_opy_.format(bstack1ll11lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1llll1lll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1111ll_opy_.format(str(e)))
  if bstack11l1l1l1_opy_ != bstackl_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩඋ") or (bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪඌ") and not bstack1l11lll_opy_):
    bstack1l1lll11l_opy_()
  if (bstack11l1l1l1_opy_ in [bstackl_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪඍ"), bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫඎ"), bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧඏ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1111l1l_opy_
        bstack1lll1ll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll1l11ll_opy_ + str(e))
    except Exception as e:
      bstack11ll1111l_opy_(e, bstack1ll1l11ll_opy_)
    if bstack11l1l1l1_opy_ != bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨඐ"):
      bstack1l1111lll_opy_()
    bstack1lllllll_opy_ = Output.end_test
    bstack1llll_opy_ = TestStatus.__init__
    bstack1l11111l_opy_ = pabot._run
    bstack1111l11l_opy_ = QueueItem.__init__
    bstack1ll1l11l1_opy_ = pabot._create_command_for_execution
    bstack1lll11l11_opy_ = pabot._report_results
  if bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨඑ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11ll1111l_opy_(e, bstack1lll1_opy_)
    bstack111l111_opy_ = Runner.run_hook
    bstack11ll1ll1_opy_ = Step.run
  if bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩඒ"):
    try:
      from _pytest.config import Config
      bstack11llll1ll_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll111ll1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l1111l1_opy_)
  if bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪඓ"):
    bstack1l11l1l1_opy_ = True
    if bstack1l11lll_opy_:
      bstack1l1ll11l1_opy_ = CONFIG.get(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨඔ"), {}).get(bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧඕ"))
      bstack1llllll_opy_(bstack11l111_opy_)
      sys.path.append(os.path.dirname(os.path.abspath(bstack1l11lll_opy_[bstackl_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඖ")])))
      mod_globals = globals()
      mod_globals[bstackl_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩ඗")] = bstackl_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪ඘")
      mod_globals[bstackl_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ඙")] = os.path.abspath(bstack1l11lll_opy_[bstackl_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ක")])
      global bstack1lll1llll_opy_
      try:
        exec(open(bstack1l11lll_opy_[bstackl_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඛ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstackl_opy_ (u"ࠬࡉࡡࡶࡩ࡫ࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠬග").format(str(e)))
          for driver in bstack1lll1llll_opy_:
            bstack11111_opy_.append({
              bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫඝ"): bstack1l11lll_opy_[bstackl_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඞ")],
              bstackl_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧඟ"): str(e),
              bstackl_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨච"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࠱ࠦࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠢࠪඡ") + json.dumps(bstackl_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢජ") + str(e)) + bstackl_opy_ (u"ࠬࢃࡽࠨඣ"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1lll1llll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      bstack1l111l1l1_opy_()
      bstack1ll1ll1l_opy_()
      if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩඤ") in CONFIG:
        bstack1ll11l11_opy_ = {
          bstackl_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඥ"): args[0],
          bstackl_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨඦ"): CONFIG,
          bstackl_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪට"): bstack1l111111_opy_
        }
        bstack11l11l_opy_ = []
        manager = multiprocessing.Manager()
        bstack11l1ll111_opy_ = manager.list()
        for index, platform in enumerate(CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ඨ")]):
          bstack1ll11l11_opy_[bstackl_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪඩ")] = index
          bstack11l11l_opy_.append(multiprocessing.Process(name=str(index),
                                        target=run_on_browserstack, args=(bstack1ll11l11_opy_, bstack11l1ll111_opy_)))
        for t in bstack11l11l_opy_:
          t.start()
        for t in bstack11l11l_opy_:
          t.join()
        bstack1l1l1l11l_opy_ = list(bstack11l1ll111_opy_)
      else:
        bstack1llllll_opy_(bstack11l111_opy_)
        sys.path.append(os.path.dirname(os.path.abspath(args[0])))
        mod_globals = globals()
        mod_globals[bstackl_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧඪ")] = bstackl_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨණ")
        mod_globals[bstackl_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩඬ")] = os.path.abspath(args[0])
        exec(open(args[0]).read(), mod_globals)
  elif bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧත") or bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨථ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack11ll1111l_opy_(e, bstack1ll1l11ll_opy_)
    bstack1l111l1l1_opy_()
    bstack1llllll_opy_(bstack11ll111l1_opy_)
    if bstackl_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨද") in args:
      i = args.index(bstackl_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩධ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l11ll11l_opy_))
    args.insert(0, str(bstackl_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪන")))
    pabot.main(args)
  elif bstack11l1l1l1_opy_ == bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ඲"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11ll1111l_opy_(e, bstack1ll1l11ll_opy_)
    for a in args:
      if bstackl_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ඳ") in a:
        bstack1ll1lll1_opy_ = int(a.split(bstackl_opy_ (u"ࠨ࠼ࠪප"))[1])
      if bstackl_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ඵ") in a:
        bstack1l1ll11l1_opy_ = str(a.split(bstackl_opy_ (u"ࠪ࠾ࠬබ"))[1])
      if bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫභ") in a:
        bstack1l1lll_opy_ = str(a.split(bstackl_opy_ (u"ࠬࡀࠧම"))[1])
    bstack11l1_opy_ = None
    if bstackl_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬඹ") in args:
      i = args.index(bstackl_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ය"))
      args.pop(i)
      bstack11l1_opy_ = args.pop(i)
    if bstack11l1_opy_ is not None:
      global bstack11llll1_opy_
      bstack11llll1_opy_ = bstack11l1_opy_
    bstack1llllll_opy_(bstack11ll111l1_opy_)
    run_cli(args)
  elif bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨර"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack1llll11ll_opy_ = importlib.find_loader(bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ඼"))
    except Exception as e:
      logger.warn(e, bstack1l1111l1_opy_)
    bstack1l111l1l1_opy_()
    try:
      if bstackl_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬල") in args:
        i = args.index(bstackl_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭඾"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨ඿") in args:
        i = args.index(bstackl_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩව"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠧ࠮ࡲࠪශ") in args:
        i = args.index(bstackl_opy_ (u"ࠨ࠯ࡳࠫෂ"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪස") in args:
        i = args.index(bstackl_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫහ"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠫ࠲ࡴࠧළ") in args:
        i = args.index(bstackl_opy_ (u"ࠬ࠳࡮ࠨෆ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack11111l1l_opy_ = config.args
    bstack1l111l11_opy_ = config.invocation_params.args
    bstack1l111l11_opy_ = list(bstack1l111l11_opy_)
    bstack111l1l1l_opy_ = []
    for arg in bstack1l111l11_opy_:
      for spec in bstack11111l1l_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack111l1l1l_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧ෇"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11111l1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11llllll1_opy_)))
                    for bstack11llllll1_opy_ in bstack11111l1l_opy_]
    if (bstack11lll_opy_):
      bstack111l1l1l_opy_.append(bstackl_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ෈"))
      bstack111l1l1l_opy_.append(bstackl_opy_ (u"ࠨࡖࡵࡹࡪ࠭෉"))
    bstack111l1l1l_opy_.append(bstackl_opy_ (u"ࠩ࠰ࡴ්ࠬ"))
    bstack111l1l1l_opy_.append(bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨ෋"))
    bstack111l1l1l_opy_.append(bstackl_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭෌"))
    bstack111l1l1l_opy_.append(bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ෍"))
    bstack11l1llll1_opy_ = []
    for spec in bstack11111l1l_opy_:
      bstack1ll1ll1ll_opy_ = []
      bstack1ll1ll1ll_opy_.append(spec)
      bstack1ll1ll1ll_opy_ += bstack111l1l1l_opy_
      bstack11l1llll1_opy_.append(bstack1ll1ll1ll_opy_)
    bstack11ll1lll1_opy_ = True
    bstack1l11lll1l_opy_ = 1
    if bstackl_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭෎") in CONFIG:
      bstack1l11lll1l_opy_ = CONFIG[bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧා")]
    bstack1ll111l1_opy_ = int(bstack1l11lll1l_opy_)*int(len(CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫැ")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬෑ")]):
      for bstack1ll1ll1ll_opy_ in bstack11l1llll1_opy_:
        item = {}
        item[bstackl_opy_ (u"ࠪࡥࡷ࡭ࠧි")] = bstack1ll1ll1ll_opy_
        item[bstackl_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪී")] = index
        execution_items.append(item)
    bstack1ll11_opy_ = bstack1lll1l1_opy_(execution_items, bstack1ll111l1_opy_)
    for execution_item in bstack1ll11_opy_:
      bstack11l11l_opy_ = []
      for item in execution_item:
        bstack11l11l_opy_.append(bstack1ll1lll_opy_(name=str(item[bstackl_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫු")]),
                                            target=bstack11lllll1_opy_,
                                            args=(item[bstackl_opy_ (u"࠭ࡡࡳࡩࠪ෕")],)))
      for t in bstack11l11l_opy_:
        t.start()
      for t in bstack11l11l_opy_:
        t.join()
  elif bstack11l1l1l1_opy_ == bstackl_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧූ"):
    try:
      from behave.__main__ import main as bstack111l1111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11ll1111l_opy_(e, bstack1lll1_opy_)
    bstack1l111l1l1_opy_()
    bstack11ll1lll1_opy_ = True
    bstack1l11lll1l_opy_ = 1
    if bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ෗") in CONFIG:
      bstack1l11lll1l_opy_ = CONFIG[bstackl_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩෘ")]
    bstack1ll111l1_opy_ = int(bstack1l11lll1l_opy_)*int(len(CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ෙ")]))
    config = Configuration(args)
    bstack11111l1l_opy_ = config.paths
    bstack1lllll1ll_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack11111l1l_opy_:
        bstack1lllll1ll_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"ࠫࡼ࡯࡮ࡥࡱࡺࡷࠬේ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11111l1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11llllll1_opy_)))
                    for bstack11llllll1_opy_ in bstack11111l1l_opy_]
    bstack11l1llll1_opy_ = []
    for spec in bstack11111l1l_opy_:
      bstack1ll1ll1ll_opy_ = []
      bstack1ll1ll1ll_opy_ += bstack1lllll1ll_opy_
      bstack1ll1ll1ll_opy_.append(spec)
      bstack11l1llll1_opy_.append(bstack1ll1ll1ll_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨෛ")]):
      for bstack1ll1ll1ll_opy_ in bstack11l1llll1_opy_:
        item = {}
        item[bstackl_opy_ (u"࠭ࡡࡳࡩࠪො")] = bstackl_opy_ (u"ࠧࠡࠩෝ").join(bstack1ll1ll1ll_opy_)
        item[bstackl_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧෞ")] = index
        execution_items.append(item)
    bstack1ll11_opy_ = bstack1lll1l1_opy_(execution_items, bstack1ll111l1_opy_)
    for execution_item in bstack1ll11_opy_:
      bstack11l11l_opy_ = []
      for item in execution_item:
        bstack11l11l_opy_.append(bstack1ll1lll_opy_(name=str(item[bstackl_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨෟ")]),
                                            target=bstack1ll111lll_opy_,
                                            args=(item[bstackl_opy_ (u"ࠪࡥࡷ࡭ࠧ෠")],)))
      for t in bstack11l11l_opy_:
        t.start()
      for t in bstack11l11l_opy_:
        t.join()
  else:
    bstack1l1l1ll_opy_(bstack1lll11ll1_opy_)
  if not bstack1l11lll_opy_:
    bstack11lllllll_opy_()
def bstack11lllllll_opy_():
  [bstack1l1ll1111_opy_, bstack1l1l11lll_opy_] = bstack1l1ll111_opy_()
  if bstack1l1ll1111_opy_ is not None and bstack1l111lll1_opy_() != -1:
    sessions = bstack1l1l1ll1l_opy_(bstack1l1ll1111_opy_)
    bstack1l11l11_opy_(sessions, bstack1l1l11lll_opy_)
def bstack1lll111_opy_(bstack1l111l11l_opy_):
    if bstack1l111l11l_opy_:
        return bstack1l111l11l_opy_.capitalize()
    else:
        return bstack1l111l11l_opy_
def bstack1l1ll1lll_opy_(bstack1lll11lll_opy_):
    if bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ෡") in bstack1lll11lll_opy_ and bstack1lll11lll_opy_[bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ෢")] != bstackl_opy_ (u"࠭ࠧ෣"):
        return bstack1lll11lll_opy_[bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ෤")]
    else:
        bstack1l1l1111l_opy_ = bstackl_opy_ (u"ࠣࠤ෥")
        if bstackl_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ෦") in bstack1lll11lll_opy_ and bstack1lll11lll_opy_[bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ෧")] != None:
            bstack1l1l1111l_opy_ += bstack1lll11lll_opy_[bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ෨")] + bstackl_opy_ (u"ࠧ࠲ࠠࠣ෩")
            if bstack1lll11lll_opy_[bstackl_opy_ (u"࠭࡯ࡴࠩ෪")] == bstackl_opy_ (u"ࠢࡪࡱࡶࠦ෫"):
                bstack1l1l1111l_opy_ += bstackl_opy_ (u"ࠣ࡫ࡒࡗࠥࠨ෬")
            bstack1l1l1111l_opy_ += (bstack1lll11lll_opy_[bstackl_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭෭")] or bstackl_opy_ (u"ࠪࠫ෮"))
            return bstack1l1l1111l_opy_
        else:
            bstack1l1l1111l_opy_ += bstack1lll111_opy_(bstack1lll11lll_opy_[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ෯")]) + bstackl_opy_ (u"ࠧࠦࠢ෰") + (bstack1lll11lll_opy_[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ෱")] or bstackl_opy_ (u"ࠧࠨෲ")) + bstackl_opy_ (u"ࠣ࠮ࠣࠦෳ")
            if bstack1lll11lll_opy_[bstackl_opy_ (u"ࠩࡲࡷࠬ෴")] == bstackl_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦ෵"):
                bstack1l1l1111l_opy_ += bstackl_opy_ (u"ࠦ࡜࡯࡮ࠡࠤ෶")
            bstack1l1l1111l_opy_ += bstack1lll11lll_opy_[bstackl_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ෷")] or bstackl_opy_ (u"࠭ࠧ෸")
            return bstack1l1l1111l_opy_
def bstack1ll11ll11_opy_(bstack1l1l111ll_opy_):
    if bstack1l1l111ll_opy_ == bstackl_opy_ (u"ࠢࡥࡱࡱࡩࠧ෹"):
        return bstackl_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ෺")
    elif bstack1l1l111ll_opy_ == bstackl_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ෻"):
        return bstackl_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭෼")
    elif bstack1l1l111ll_opy_ == bstackl_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ෽"):
        return bstackl_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ෾")
    elif bstack1l1l111ll_opy_ == bstackl_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ෿"):
        return bstackl_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ฀")
    elif bstack1l1l111ll_opy_ == bstackl_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤก"):
        return bstackl_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧข")
    elif bstack1l1l111ll_opy_ == bstackl_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦฃ"):
        return bstackl_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬค")
    else:
        return bstackl_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩฅ")+bstack1lll111_opy_(bstack1l1l111ll_opy_)+bstackl_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬฆ")
def bstack11l11_opy_(session):
    return bstackl_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧง").format(session[bstackl_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬจ")],bstack1l1ll1lll_opy_(session), bstack1ll11ll11_opy_(session[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨฉ")]), bstack1ll11ll11_opy_(session[bstackl_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪช")]), bstack1lll111_opy_(session[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬซ")] or session[bstackl_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬฌ")] or bstackl_opy_ (u"࠭ࠧญ")) + bstackl_opy_ (u"ࠢࠡࠤฎ") + (session[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪฏ")] or bstackl_opy_ (u"ࠩࠪฐ")), session[bstackl_opy_ (u"ࠪࡳࡸ࠭ฑ")] + bstackl_opy_ (u"ࠦࠥࠨฒ") + session[bstackl_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩณ")], session[bstackl_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨด")] or bstackl_opy_ (u"ࠧࠨต"), session[bstackl_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬถ")] if session[bstackl_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ท")] else bstackl_opy_ (u"ࠪࠫธ"))
def bstack1l11l11_opy_(sessions, bstack1l1l11lll_opy_):
  try:
    bstack1l1l1l111_opy_ = bstackl_opy_ (u"ࠦࠧน")
    if not os.path.exists(bstack1l1l111_opy_):
      os.mkdir(bstack1l1l111_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstackl_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪบ")), bstackl_opy_ (u"࠭ࡲࠨป")) as f:
      bstack1l1l1l111_opy_ = f.read()
    bstack1l1l1l111_opy_ = bstack1l1l1l111_opy_.replace(bstackl_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫผ"), str(len(sessions)))
    bstack1l1l1l111_opy_ = bstack1l1l1l111_opy_.replace(bstackl_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨฝ"), bstack1l1l11lll_opy_)
    bstack1l1l1l111_opy_ = bstack1l1l1l111_opy_.replace(bstackl_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪพ"), sessions[0].get(bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧฟ")) if sessions[0] else bstackl_opy_ (u"ࠫࠬภ"))
    with open(os.path.join(bstack1l1l111_opy_, bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩม")), bstackl_opy_ (u"࠭ࡷࠨย")) as stream:
      stream.write(bstack1l1l1l111_opy_.split(bstackl_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫร"))[0])
      for session in sessions:
        stream.write(bstack11l11_opy_(session))
      stream.write(bstack1l1l1l111_opy_.split(bstackl_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬฤ"))[1])
    logger.info(bstackl_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬล").format(bstack1l1l111_opy_));
  except Exception as e:
    logger.debug(bstack11l1ll1_opy_.format(str(e)))
def bstack1l1l1ll1l_opy_(bstack1l1ll1111_opy_):
  global CONFIG
  try:
    host = bstackl_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ฦ") if bstackl_opy_ (u"ࠫࡦࡶࡰࠨว") in CONFIG else bstackl_opy_ (u"ࠬࡧࡰࡪࠩศ")
    user = CONFIG[bstackl_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨษ")]
    key = CONFIG[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪส")]
    bstack1l1l1l1_opy_ = bstackl_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧห") if bstackl_opy_ (u"ࠩࡤࡴࡵ࠭ฬ") in CONFIG else bstackl_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬอ")
    url = bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠲࡯ࡹ࡯࡯ࠩฮ").format(user, key, host, bstack1l1l1l1_opy_, bstack1l1ll1111_opy_)
    headers = {
      bstackl_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫฯ"): bstackl_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩะ"),
    }
    proxy = bstack111111_opy_(CONFIG)
    proxies = {}
    if CONFIG.get(bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪั")) or CONFIG.get(bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬา")):
      proxies = {
        bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨำ"): proxy
      }
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstackl_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨิ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l111l1l_opy_.format(str(e)))
def bstack1l1ll111_opy_():
  global CONFIG
  try:
    if bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧี") in CONFIG:
      host = bstackl_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨึ") if bstackl_opy_ (u"࠭ࡡࡱࡲࠪื") in CONFIG else bstackl_opy_ (u"ࠧࡢࡲ࡬ุࠫ")
      user = CONFIG[bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧูࠪ")]
      key = CONFIG[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽฺࠬ")]
      bstack1l1l1l1_opy_ = bstackl_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ฻") if bstackl_opy_ (u"ࠫࡦࡶࡰࠨ฼") in CONFIG else bstackl_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ฽")
      url = bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭฾").format(user, key, host, bstack1l1l1l1_opy_)
      headers = {
        bstackl_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭฿"): bstackl_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫเ"),
      }
      if bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫแ") in CONFIG:
        params = {bstackl_opy_ (u"ࠪࡲࡦࡳࡥࠨโ"):CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧใ")], bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨไ"):CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨๅ")]}
      else:
        params = {bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬๆ"):CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ็")]}
      proxy = bstack111111_opy_(CONFIG)
      proxies = {}
      if CONFIG.get(bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽ่ࠬ")) or CONFIG.get(bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿ้ࠧ")):
        proxies = {
          bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ๊ࠪ"): proxy
        }
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1llll1111_opy_ = response.json()[0][bstackl_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ๋")]
        if bstack1llll1111_opy_:
          bstack1l1l11lll_opy_ = bstack1llll1111_opy_[bstackl_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ์")].split(bstackl_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭ํ"))[0] + bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩ๎") + bstack1llll1111_opy_[bstackl_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ๏")]
          logger.info(bstack11ll1_opy_.format(bstack1l1l11lll_opy_))
          bstack11lll111_opy_ = CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭๐")]
          if bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๑") in CONFIG:
            bstack11lll111_opy_ += bstackl_opy_ (u"ࠬࠦࠧ๒") + CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๓")]
          if bstack11lll111_opy_!= bstack1llll1111_opy_[bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๔")]:
            logger.debug(bstack1l1l111l_opy_.format(bstack1llll1111_opy_[bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭๕")], bstack11lll111_opy_))
          return [bstack1llll1111_opy_[bstackl_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ๖")], bstack1l1l11lll_opy_]
    else:
      logger.warn(bstack1ll111l_opy_)
  except Exception as e:
    logger.debug(bstack1lll1l11_opy_.format(str(e)))
  return [None, None]
def bstack11ll1ll_opy_(url, bstack11ll111ll_opy_=False):
  global CONFIG
  global bstack1l111l_opy_
  if not bstack1l111l_opy_:
    hostname = bstack1ll1ll111_opy_(url)
    is_private = bstack11l1l11l_opy_(hostname)
    if (bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ๗") in CONFIG and not CONFIG[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ๘")]) and (is_private or bstack11ll111ll_opy_):
      bstack1l111l_opy_ = hostname
def bstack1ll1ll111_opy_(url):
  return urlparse(url).hostname
def bstack11l1l11l_opy_(hostname):
  for bstack11l1l11l1_opy_ in bstack1l1ll1l1_opy_:
    regex = re.compile(bstack11l1l11l1_opy_)
    if regex.match(hostname):
      return True
  return False