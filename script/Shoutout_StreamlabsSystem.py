#---------------------------------------
#   Import Libraries
#---------------------------------------
import sys
import clr
import json
import codecs
import os
import re
import random
import datetime
import glob
import time
import threading
import shutil
import tempfile

# sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "libs/updater"))
# import ChatbotUpdater


clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------------------
#   [Required] Script Information
#---------------------------------------
ScriptName = "Shoutout Overlay"
Website = "http://darthminos.tv"
Description = "A Shoutout overlay that pulls casters avatar picture from twitch API and displays it on screen"
Creator = "DarthMinos"
Version = "1.0.0-snapshot"
Repo = "camalot/chatbot-shoutout"

ReadMeFile = "https://github.com/" + Repo + "/blob/develop/ReadMe.md"
SettingsFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.json")
UIConfigFile = os.path.join(os.path.dirname(__file__), "UI_Config.json")
ScriptSettings = None

class Settings(object):
    """ Class to hold the script settings, matching UI_Config.json. """

    def __init__(self, settingsfile=None):
        """ Load in saved settings file if available else set default values. """
        defaults = self.DefaultSettings(UIConfigFile)
        try:
            # self.Command = "!so"
            # self.Cooldown = 30
            # self.Duration = 10
            # self.LinkText = "https://twitch.tv/{username}"
            # self.ShowLink = True
            # self.UserColor = "rgba(255,0,0,1)"
            # self.LinkColor = "rgba(255,0,0,1)"
            # self.Permission = "Moderator"
            # self.InTransition = "slideInRight"
            # self.OutTransition = "slideOutLeft"
            # self.AttentionAnimation = "none"
            # self.ImageShape = "circle"
            # self.EnableShadow = True
            self.__dict__.update(defaults)

            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                fileSettings = json.load(f, encoding="utf-8")
                self.__dict__.update(fileSettings)
        except Exception as e:
            self.__dict__.update(defaults)
            Parent.Log(ScriptName, str(e))


    def DefaultSettings(self, settingsfile=None):
        defaults = dict()
        with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
            ui = json.load(f, encoding="utf-8")
        for key in ui:
            try:
                if "value" in ui[key]:
                    defaults[key] = ui[key]['value']
            except:
                if key != "output_file":
                    Parent.Log(ScriptName, "DefaultSettings(): Could not find key {0} in settings".format(key))
        return defaults

    def Reload(self, jsonData):
        """ Reload settings from the user interface by given json data. """
        Parent.Log(ScriptName, "Reload Settings")
        fileLoadedSettings = json.loads(jsonData, encoding="utf-8")
        self.__dict__.update(fileLoadedSettings)
# ---------------------------------------
#	Functions
# ---------------------------------------


def SendUsernameWebsocket(username):
    # Broadcast WebSocket Event
    payload = {
        "user": username
    }
    SendWebsocketData("EVENT_SO_COMMAND", payload)
    return
def SendSettingsUpdate():
    SendWebsocketData("EVENT_SO_SETTINGS", ScriptSettings.__dict__)
def SendWebsocketData(eventName, payload):
    Parent.Log(ScriptName, "Trigger Event: " + eventName)
    Parent.BroadcastWsEvent(eventName, json.dumps(payload))
    return
#---------------------------------------
#   [Required] Initialize Data / Load Only
#---------------------------------------


def Init():
    global ScriptSettings
    ScriptSettings = Settings(SettingsFile)
    SendSettingsUpdate()
    return

def Unload():
    # End of Unload
    return

def ScriptToggled(state):
    Parent.Log(ScriptName, "State Changed: " + str(state))
    if state:
        Init()
    else:
        Unload()
    return

# ---------------------------------------
# Chatbot Save Settings Function
# ---------------------------------------
def ReloadSettings(jsondata):
    Unload()
    Init()
    return


def Execute(data):
    if data.IsChatMessage():
        commandTrigger = data.GetParam(0).lower()
        if Parent.HasPermission(data.User, ScriptSettings.Permission, ""):
            if commandTrigger == ScriptSettings.Command and not Parent.IsOnCooldown(ScriptName, commandTrigger):
                if data.GetParamCount() > 1:
                    Parent.Log(ScriptName, "Trigger Command")
                    SendUsernameWebsocket(data.GetParam(1).strip("@"))
                    Parent.AddCooldown(ScriptName, ScriptSettings.Command, ScriptSettings.Cooldown)
    return


def Tick():
    return

# ---------------------------------------
# Script UI Button Functions
# ---------------------------------------

def OpenOverlayInBrowser():
    os.startfile(os.path.realpath(os.path.join(os.path.dirname(__file__), "overlay.html")))
    return
def SendTestEvent():
    SendUsernameWebsocket(Parent.GetChannelName())
    return
def OpenScriptUpdater():
    currentDir = os.path.realpath(os.path.dirname(__file__))
    chatbotRoot = os.path.realpath(os.path.join(currentDir, "../../../"))
    libsDir = os.path.join(currentDir, "libs/updater")
    Parent.Log(ScriptName, libsDir)
    try:
        src_files = os.listdir(libsDir)
        tempdir = tempfile.mkdtemp()
        Parent.Log(ScriptName, tempdir)
        for file_name in src_files:
            full_file_name = os.path.join(libsDir, file_name)
            if os.path.isfile(full_file_name):
                Parent.Log(ScriptName, "Copy: " + full_file_name)
                shutil.copy(full_file_name, tempdir)
        updater = os.path.join(tempdir, "ApplicationUpdater.exe")
        updaterConfigFile = os.path.join(tempdir, "update.manifest")
        repoVals = Repo.split('/')
        updaterConfig = {
            "path": os.path.realpath(os.path.join(currentDir,"../")),
            "version": Version,
            "name": ScriptName,
            "requiresRestart": True,
            "kill": [],
            "execute": {
                "before": [{
                    "command": "cmd",
                    "arguments": [ "/c", "del /q /f /s *" ],
                    "workingDirectory": "${PATH}\\${FOLDERNAME}\\Libs\\updater\\",
                    "ignoreExitCode": True,
                    "validExitCodes": [ 0 ]
                }],
                "after": []
            },
            "application": os.path.join(chatbotRoot, "Streamlabs Chatbot.exe"),
            "folderName": os.path.basename(os.path.dirname(os.path.realpath(__file__))),
            "processName": "Streamlabs Chatbot",
            "website": Website,
            "repository": {
                "owner": repoVals[0],
                "name": repoVals[1]
            }
        }
        Parent.Log(ScriptName, updater)
        configJson = json.dumps(updaterConfig)
        Parent.Log(ScriptName, configJson)
        with open(updaterConfigFile, "w+") as f:
            f.write(configJson)
        os.startfile(updater)
    except OSError as exc: # python >2.5
        raise

def OpenFollowOnTwitchLink():
    os.startfile("https://twitch.tv/DarthMinos")
    return

def OpenReadMeLink():
    os.startfile(ReadMeFile)
    return

def OpenPaypalDonateLink():
    os.startfile("https://paypal.me/camalotdesigns/10")
    return
def OpenGithubDonateLink():
    os.startfile("https://github.com/sponsors/camalot")
    return
def OpenTwitchDonateLink():
    os.startfile("http://twitch.tv/darthminos/subscribe")
    return
def OpenDiscordLink():
    os.startfile("https://discord.com/invite/vzdpjYk")
    return
