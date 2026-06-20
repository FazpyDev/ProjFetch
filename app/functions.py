from app import settings

def validateSettingKey(keyname, defaultval):
    settingKeys = list(settings.keys())
    if keyname not in settingKeys:
        settings.update({keyname: defaultval})        