# -*- coding: utf-8 -*-

import click
import sys
import os
import webbrowser
try:
    import SimpleHTTPServer
except:
    import http.server as SimpleHTTPServer
try:
    import SocketServer
except:
    import socketserver as SocketServer
import threading
import time
# from jinja2 import FileSystemLoader
# from jinja2.environment import Environment
# from bs4 import BeautifulSoup as bs
from cookiecutter.main import cookiecutter
# from wikicreator import Generator
sys.path.append(os.getcwd())
try:
    from generators import Generator
except:
    from wikicreator.default import Generator


@click.command()
@click.option('--openfile/--no_openfile',
              '-o/-n', default=False,
              help='Open in browser')
@click.option('--serve/--no_serve',
              '-s/-t', default=False,
              help='Serve up the file')
@click.option('--init/--no_init', '-i/-j',
              default=False,
              help='Initialize a wikicreator project')
def main(openfile, serve, init):
    if init:
        cookiecutter('https://github.com/' +
                     'MatanSilver/cookiecutter-wikicreator.git')
    else:
        gen = Generator()
        gen.generate()
        if serve:
            PORT = gen.find_free_port()
            url = "localhost:" + str(PORT) + "/public/"
            server_thread = threading.Thread(target=gen.server_worker,
                                             args=(PORT,))
            files_thread = threading.Thread(target=gen.files_worker)
            server_thread.daemon = True
            files_thread.daemon = True
            server_thread.start()
            files_thread.start()
            if openfile:
                webbrowser.open_new_tab(url)
            try:
                while(True):
                    time.sleep(1)
            except KeyboardInterrupt:
                print ("Exiting")
                sys.exit(1)


if __name__ == "__main__":
    main()
