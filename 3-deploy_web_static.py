#!/usr/bin/python3
"""Module for do_pack function"""
from datetime import datetime
from fabric.api import local, put, run, env
import os

env.hosts = ["54.174.43.223", "18.235.255.170"]


def do_pack():
    """
    Script that generates a .tgz archive
    from the contents of the web_static folder
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(now)
    if os.path.isdir("versions") is False:
        if local("mkdir versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(filename)).failed is True:
        return None
    return filename


def do_deploy(archive_path):
    """
    Script that distributes an archive to my web servers
    """
    if os.path.exists(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1].split(".")[0]
        release_path = "/data/web_static/releases/{}".format(filename)
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(release_path))
        run("tar -xzf /tmp/{}.tgz -C {}/".format(filename, release_path))
        run("rm /tmp/{}.tgz".format(filename))
        run("mv {0}/web_static/* {0}".format(release_path))
        run("rm -rf {}/web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(release_path))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Script that creates and distributes an archive to your web servers
    """
    try:
        path = do_pack()
        return do_deploy(path)
    except Exception:
        return False
