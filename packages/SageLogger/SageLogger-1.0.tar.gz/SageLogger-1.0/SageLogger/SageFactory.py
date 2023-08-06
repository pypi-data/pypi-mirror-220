from . import Logger

def create(name : str = "", savetofile : bool = False, logfile : str = "log"):
    return Logger.SageLogger(name, savetofile, logfile)

def create_remote(method, url, headers, body, name : str = "", savetofile : bool = False, logfile : str = "log"):
    return Logger.SageRemoteLogger(method, url, headers, body, name, savetofile, logfile)

def create_discord_webhook_remote(url, name : str = "", savetofile : bool = False, logfile : str = "log"):
    return Logger.SageDiscordWebhookLogger.create(url, name, savetofile, logfile)

def create_temporary():
    return create(name="temporary", savetofile=False)