import os
import site
import subprocess

import click
from loguru import logger
import requests

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()

def send_slack_notification(message):
    data = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=data)

def run_dropcaster(title, hostname):
    """
    docker 
    run \
    -it \
    --rm \
    --mount type=bind,source="$(pwd)",target=/public_html \
    --mount type=bind,source="$(pwd)/../../channel.yml.example",target=/public_html/channel.yml \
    --mount type=bind,source="$(pwd)/../../channel.rss.erb",target=/public_html/channel.rss.erb \
    nerab/dropcaster \
    dropcaster \
        --title "${TITLE}" \
        --description "${TITLE}" \
        --url "${PODCASTURL}" > index.rss
    """
    user_site_path = site.getusersitepackages()
    with open("index.rss", "w") as rss:
        subprocess.run(
            [
            "docker",
            "run",
            "-it",
            "--rm",
            "--mount",
            f"type=bind,source={os.getcwd()},target=/public_html",
            "--mount",
            f"type=bind,source={user_site_path}/ytpodgen/channel.yml.example,target=/public_html/channel.yml",
            "--mount",
            f"type=bind,source={user_site_path}/ytpodgen/channel.rss.erb,target=/public_html/channel.rss.erb",
            "nerab/dropcaster",
            "dropcaster",
            "--channel-template",
            "channel.rss.erb",
            "--title",
            title,
            "--description",
            title,
            "--url",
            f"https://{hostname}/{title}/",
            ],
            check = True,
            stdout = rss,
            stderr = rss
        )

def generate_rss(args):
    pass

def run_rclone(title):
    subprocess.run(
    [
        'rclone',
        'sync',
        '--progress',
        '--include',
        'index.rss',
        '--include',
        '*.mp3',
        '.',
        f'cloudflare:podcast/{title}/'
    ],
    check = True
    )

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
        "--live-from-start",
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
    if not debug: #be quiet if not debug
        ytdlp_command.insert(len(ytdlp_command)-1, "--quiet")
        
    with open(f"{title}.log", "a") as log:
        subprocess.run(
        ytdlp_command,
        check=True,
        stdout=log,
        stderr=log
        )

@click.command()
@click.option('--title', prompt='enter title', help='title for the podcast')
@click.option(
    '--hostname',
    prompt='enter hostname',
    help='hostname(custom or r2.dev) to serve files'
)
@click.option(
    '--liveurl',
    help='watch for and download the specified YouTube Live URL'
)
@click.option(
    '--upload',
    is_flag=True,
    help='if specified, upload mp3s/RSS to Cloudflare R2'
)
@click.option('--debug', is_flag=True, help='run yt-dlp in debug mode')
@click.option(
    '--version',
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True
)
def cli(title, hostname, liveurl, upload, debug):
    """
    Download YouTube livestream and generate podcast RSS to Current Dir
    """
    logger.add(
        f"{title}.log",
        level="INFO"
    )
    if SLACK_WEBHOOK_URL:
        logger.add(
            send_slack_notification,
            level="SUCCESS"
        )

    try:
        while True:
            if liveurl:
                logger.info("Running yt-dlp...")
                run_ytdlp(title, liveurl, debug)

            logger.info("Generating feeds...")
            run_dropcaster(title, hostname)

            if upload:
                logger.info("Uploading files...")
                run_rclone(title)
                logger.success(
                    f"""
                    Upload completed.
                    Podcast feed url: https://{hostname}/{title}/index.rss
                    """
                )
            
            if liveurl is None:
                break
    except subprocess.CalledProcessError as e:
        logger.error(f"ytpodgen failed with following error messages: {e}")

if __name__ == '__main__':
    cli()
