import os
import subprocess
from bottle import route, run, template, static_file

from web.information import getInf


@route('/hello/:name')
def index(name='World'):
    return '<strong>Hello {}!'.format(name)


@route('/<filename:path>')
def server_static(filename):
    root = os.path.join(os.path.dirname(__file__), "configui", "dist")
    return static_file(filename, root=root)


def serverRun():
    getInf()
    _build()
    run(host='localhost', port=8080)


def _build():
    subprocess.run(["npm", "run", "build"], shell=True, cwd="web/configui")
