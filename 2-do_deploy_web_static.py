#!/usr/bin/python3
'''script that generates a .tgz archive from the contents of
the web_static, using the function do_pack and that distributes
the archive to your web servers using do_deploy
'''

from fabric.api import local, run, put, get, env
from datetime import datetime
import os

env.hosts = ['52.90.23.6', '52.207.96.101']


def do_deploy(archive_path):
    '''distributes an archive to your web servers
    '''
    if not os.path.exists(archive_path):  # check if path exists
        return False
    try:
        archive_name = archive_path.split('/')[-1]
        destination = "/data/web_static/releases/{}".format(archive_name[:-4])
        put(archive_path, '/tmp/')

        run('sudo mkdir -p {}'.format(destination))
        run('sudo tar -xzf /tmp/{} -C {}'.format(archive_name, destination))
        run('sudo rm /tmp/{}'.format(archive_name))
        run('sudo mv {}/web_static/* {}'.format(destination, destination))
        run('sudo rm -rf {}/web_static'.format(destination))
        run("if [ -L /data/web_static/current ];\
                then rm /data/web_static/current; fi")
        run('sudo ln -s {} /data/web_static/current'.format(destination))
        print("\nNew Version Deployed !!!")
        return True
    except BaseException:
        return False
