import yaml


def load_settings(setting_file):
    try:
        with open(setting_file, "r") as f:
            setting = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        settings = {
            "theme": "dark cyan",
        }
        with open(setting_file, "w") as f:
            setting = yaml.dump(settings, f)
        return settings

    return {
        "theme": setting.get("theme")
        if setting.get("themes") is not None
        else "dark cyan",
    }


def save_settings(setting_file, settings):
    with open(setting_file, "w") as f:
        setting = yaml.dump(settings, f)
