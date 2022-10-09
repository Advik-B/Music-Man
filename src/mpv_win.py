from requests import get
from rich.console import Console
from rich.progress import track
from zipfile import ZipFile
from pathstuff import add_path
import sys
import shutil
import os
import subprocess
n64bit = sys.maxsize > 2**32

manifest_link = "https://raw.githubusercontent.com/ScoopInstaller/Extras/master/bucket/mpv.json"

ytdlp = "https://github.com/yt-dlp/yt-dlp/releases/latest/2022.10.04/yt-dlp.exe"

def download_mpv(console: Console):
    manifest = get(manifest_link).json()
    version = manifest["version"]
    console.log(f"Downloading mpv version {version}")
    url = (
        manifest["architecture"]["64bit"]["url"]
        if n64bit
        else manifest["architecture"]["32bit"]["url"]
    )
    console.log(f"Download link: {url}")
    r = get(url, stream=True)
    chunk_size = 1024
    total_size = int(r.headers.get("content-length", 0)) / chunk_size
    with open("mpv.zip", "wb") as f:
        for data in track(
            r.iter_content(chunk_size=chunk_size),
            total=total_size,
            description="Downloading MPV",):
            f.write(data)
    console.log("Downloading yt-dlp")
    r = get(ytdlp, stream=True)
    total_size = int(r.headers.get("content-length", 0)) / chunk_size
    with open("yt-dlp.exe", "wb") as f:
        for data in track(
            r.iter_content(chunk_size=chunk_size),
            total=total_size,
            description="Downloading YT-DLP",):
            f.write(data)
    console.log("Extracting mpv")

    if os.path.exists("mpv"):
        shutil.rmtree("mpv", ignore_errors=True)
        try:
            os.mkdir("mpv")
        except FileExistsError:
            pass

    else:
        os.mkdir("mpv")

    add_path("7z")
    # Unzip mpv using 7z
    subprocess.run(
        [
            "7z",
            "x",
            "mpv.zip",
            "-o./mpv",
            "-y",
        ],
        capture_output=True,
        text=True,
    )

    console.log("Copying yt-dlp")
    shutil.copy("yt-dlp.exe", "mpv/yt-dlp.exe")

    console.log("Removing temporary files")
    os.remove("mpv.zip")
    os.remove("yt-dlp.exe")
    console.log("Done!")
    console.log("You can now run mpv by typing mpv/mpv.exe in the terminal")




if __name__ == "__main__":
    console = Console()
    download_mpv(console)