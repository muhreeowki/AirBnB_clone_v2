#!/usr/bin/python3
"""Module for do_pack function"""
from datetime import datetime
from fabric.api import local
import os


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
