try:
    from utils.bot.gpt4real import *
    from utils.bot.set_preferences import *
    from utils.bot.AIs import *
    from utils.bot.basebots import *
    from utils.bot.install_tinyllm import *
    from utils.bot.tinyllm import *
    #from utils.bot.copilot import * # errors...
except ImportError:
    from bot.gpt4real import *
    from bot.set_preferences import *
    from bot.AIs import *
    from bot.basebots import *
    from bot.install_tinyllm import *
    from bot.tinyllm import *
    #from bot.copilot import *
