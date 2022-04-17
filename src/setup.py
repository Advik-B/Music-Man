from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = dict(
    packages=["os", "yaml", "datetime", "termcolor", "colorama", "qt_material"],
    excludes=["tkinter"],
    include_files=["assets", "themes"],
    include_msvcr=True,
)

import sys

base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable(
        "__main__.py",
        base=base,
        targetName="PulsePlayer.exe",
        icon="assets/icon.ico",
    )
]

setup(
    name="Pulse Player",
    version="0.1",
    description="A one-stop app for all your music needs",
    options=dict(build_exe=buildOptions),
    executables=executables,
)
