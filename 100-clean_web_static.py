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


def do_pack():
    """Compress the contents of web_static"""

    #  create `versions` dir if not exists
    local('mkdir -p versions')

    #  create compressed tgz file
    time_stamp = datetime.now().strftime('%Y%m%d%H%M%S')
    path = 'versions/web_static_' + time_stamp + '.tgz'
    result = local('tar -cvzf {} web_static/'.format(path))
    if result.succeeded:
        return path
    else:
        return None


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


def deploy():
    """creates and distributes an archive to web servers"""
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)


def do_clean(number=0):
    """Delete out-of-date archives.
    Args:
        number (int): The number of archives to keep.
    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
