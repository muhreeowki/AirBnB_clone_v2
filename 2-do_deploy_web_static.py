#!/usr/bin/python3
"""Module for do_pack function"""
from datetime import datetime
from fabric.api import local, put, run, env
import os

env.hosts = ["54.174.43.223", "18.235.255.170"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """
    Script that generates a .tgz archive
    from the contents of the web_static folder
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.isdir("versions"):
        local("mkdir versions")
    local("tar -cvzf versions/web_static_{}.tgz web_static".format(now))
    return "versions/web_static_{}.tgz".format(now)


def do_deploy(archive_path):
    """
    Script that distributes an archive to my web servers
    """
    if os.path.exists(archive_path) is False:
        return False
    try:
        name = archive_path.split("/")[-1].split(".")[0]
        newest_release = f"/data/web_static/releases/{name}"
        put(local_path=archive_path, remote_path="/tmp/")
        run(f"sudo mkdir -p {newest_release}/")
        run(f"sudo tar -xzf /tmp/{name}.tgz -C {newest_release}/")
        run(f"sudo rm /tmp/{name}.tgz")
        run(f"sudo cp -R {newest_release}/web_static/* {newest_release}/")
        run(f"sudo rm -rf {newest_release}/web_static")
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {newest_release}/ /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
