# coding:utf-8
from enum import Enum
from sys import platform, getwindowsversion
from helper.getvalue import configpath, autopath, autoncmaapi, autoqqmaapi, GetDefaultThemeColor
from helper.SettingHelper import get_all_api
from PyQt5.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,ColorConfigItem, EnumSerializer,
                            OptionsValidator,  FolderValidator, ConfigSerializer, FolderListValidator, Theme)

class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO

from enum import Enum

class AudioQuality(Enum):
    STANDARD = "standard"
    HIGHER = "higher"
    EXHIGH = "exhigh"
    LOSSLESS = "lossless"
    HIRES = "hires"
    JYEFFECT = "jyeffect"
    SKY = "sky"
    JYMASTER = "jymaster"


class AudioQualitySerializer:
    """ Audio Quality serializer """

    @staticmethod
    def serialize(audio_quality: AudioQuality) -> str:
        """
        Serialize the audio quality enum into its English string representation.
        """
        return audio_quality.value

    @staticmethod
    def deserialize(value: str) -> AudioQuality:
        """
        Deserialize an English string into the appropriate AudioQuality enum.
        """
        try:
            return AudioQuality(value.lower())
        except ValueError:
            return AudioQuality.STANDARD




class Config(QConfig):
    # Download
    downloadFolder = ConfigItem(
        "Download", "Folder", autopath, FolderValidator())
    ncma_api = ConfigItem(
        "Download", "ncma_api", autoncmaapi, None)
    qqma_api = ConfigItem(
        "Download", "qqma_api", autoqqmaapi, None)
    level = OptionsConfigItem(
        "Download", "level", AudioQuality.STANDARD, validator=OptionsValidator(AudioQuality), serializer=AudioQualitySerializer())

    # Application
    beta = ConfigItem(
        "Application", "beta", False, BoolValidator())
    update_card = ConfigItem(
        "Application", "update_card", False, BoolValidator(), restart=True)
        
    #pluginsFolders
    PluginFolders = ConfigItem(
        "Plugins", "Folders", [], FolderListValidator(), restart=True)
    
    # Search
    twitcard = ConfigItem(
        "Search", "twitcard", False, BoolValidator(), restart=True)
    hotcard = ConfigItem(
        "Search", "hotcard", False, BoolValidator(), restart=True)
    cookie = ConfigItem(
        "Search", "cookie", ""
    )
    
    # Personalize
    language = OptionsConfigItem(
        "Personalize", "Language", Language.CHINESE_SIMPLIFIED, OptionsValidator(Language), LanguageSerializer(), restart=True)
    micaEnabled = ConfigItem("Personalize", "MicaEnabled", platform == 'win32' and getwindowsversion().build >= 22000, BoolValidator())
    themeMode = OptionsConfigItem(
        "Personalize", "ThemeMode", Theme.LIGHT, OptionsValidator(Theme), EnumSerializer(Theme))
    themeColor = ColorConfigItem("Personalize", "ThemeColor", GetDefaultThemeColor())
    
    #BetaOnly
    toast = ConfigItem(
        "BetaOnly", "toast", False, BoolValidator())
    PluginEnable = ConfigItem(
        "BetaOnly", "EnablePlugins", False, BoolValidator(), restart=True)
    debug_card = ConfigItem(
        "BetaOnly", "debug_card", False, BoolValidator(), restart=True)

cfg = Config()
qconfig.load(configpath, cfg)

class Plufig(Config):
    apicard = OptionsConfigItem(
        "Search", "apicard", "NCMA", OptionsValidator(get_all_api(folders_arg=cfg.PluginFolders.value)))

pfg = Plufig()
qconfig.load(configpath, pfg)