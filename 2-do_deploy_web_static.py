#!/usr/bin/python3
"""
A Fabric script that generates a .tgz archive from the
contents of the web_static folder of AirBnB Clone repo, using
the function `do_pack`.
"""

from fabric.api import local, env, run, put
from datetime import datetime
import os

env.hosts = ['52.90.23.6', '52.207.96.101']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """distributes an archive to env.hosts web servers"""

    #  if empty argument passed
    if not os.path.exists(archive_path):
        return False

    basename = os.path.basename(archive_path)
    path = basename.replace('.tgz', '')
    path = '/data/web_static/releases/{}'.format(path)

    #  upload archive to server
    put(archive_path, '/tmp/')
    run('mkdir -p {}'.format(path))
    run('tar -xvzf /tmp/{} -C {}'.format(basename, path))
    run('mv {}/web_static/* {}'.format(path, path))
    run('rm -rf {}/web_static/'.format(path))
    run('rm /data/web_static/current')
    run('ln -s {} /data/web_static/current'.format(path))
    return True
