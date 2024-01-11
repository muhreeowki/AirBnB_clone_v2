#!/usr/bin/python3
"""Module for do_pack function"""
from datetime import datetime
from fabric.api import local, put, run, env, sudo
import os

env.hosts = ["100.25.33.139", "54.146.73.237"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """
    Script that generates a .tgz archive
    from the contents of the web_static folder
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        if not os.path.isdir("versions"):
            local("mkdir versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static".format(now))
        return "versions/web_static_{}.tgz".format(now)
    except Exception:
        return None


def do_deploy(archive_path):
    try:
        if os.path.exists(archive_path):
            name = archive_path.split("/")[1]
            name = name.split(".")[0]
            put(local_path=archive_path, remote_path="/tmp/")
            sudo(f"mkdir -p /data/web_static/releases/{name}/")
            sudo(
                "tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}".format(
                    name, name
                )
            )
            sudo(f"rm /tmp/{name}.tgz")
            sudo(
                "cp -R /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(
                    name, name
                )
            )
            sudo(f"rm -rf /data/web_static/releases/{name}/web_static")
            sudo("rm /data/web_static/current")
            sudo(
                "ln -s /data/web_static/releases/{} /data/web_static/current".format(
                    name
                )
            )
        return False
    except Exception:
        return False
