import os
import subprocess


from loguru import logger

def run_ytdlp(title, liveurl, debug=False):
    """
    docker run --rm -it -v "$(pwd):/downloads:rw" jauderho/yt-dlp:latest --wait-for-video 60 --extract-audio --audio-format mp3 --audio-quality 64K --postprocessor-args "-ac 1" --output "${TITLE}_%(epoch>%Y%m%d%H%M%S)s_%(id)s" %{LIVEURL}
    """
    ytdlp_command = [        
        "docker",
        "run",
        "--rm",
        "-it",
        "-v",
        f"{os.getcwd()}:/downloads:rw",
        "jauderho/yt-dlp:latest",
        "--wait-for-video",
        "600",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "64K",
        "--postprocessor-args",
        f"ffmpeg:-ac 1",
        "--output",
        f"{title}_%(epoch>%Y%m%d%H%M%S)s_%(id)s",
        liveurl,
    ]
    
    # "--live-from-start" is experimental and might fail if stream isn't 'is_live' 
    if is_live(liveurl):
        ytdlp_command.append("--live-from-start")
        logger.info(
            "The livestream is already on the air. Trying to capture it from the start..."
        )
    
    if not debug: #be quiet if not debug
        ytdlp_command.append("--quiet")
        
    with open(f"{title}.log", "a") as log:
        subprocess.run(
        ytdlp_command,
        check=True,
        stdout=log,
        stderr=log
        )

def is_live(liveurl):
    """
    It returns True if given stream is already on the air.
    
    To try this from terminal, run the commands below:
    python -c 'import <module>; <module>.is_live("https://www.youtube.com/channel/UCpcGAVuBSJEFs48MBxhf9eg/live")'
    """
    ytdlp_command = [
        "docker",
        "run",
        "--rm",
        "-it",
        "jauderho/yt-dlp:latest",
        "--print",
        "%(live_status)s",
        liveurl,
    ]
        
    live_status = subprocess.run(
        ytdlp_command,
        capture_output=True,
        text=True,
    ).stdout.rstrip('\n') #yt-dlp returns "is_live\n"
    if live_status == 'is_live':
        return True
    else:
        return False