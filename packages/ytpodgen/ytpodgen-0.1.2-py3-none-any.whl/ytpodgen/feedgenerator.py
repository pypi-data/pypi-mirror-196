import os
import site
import subprocess

def run_dropcaster(title, hostname):
    """generate podcast RSS feed w/ dropcaster.
    
    ref: https://github.com/nerab/dropcaster

    Args:
        title (str): title of podcast
        hostname (str): hostname to actually serve files from
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

def generate_rss():
    print(__name__)