from nonebot import require

require("nonebot_plugin_apscheduler")

from .common.utils import initFile
from .onebotv11.main import Chatbot

initFile()
