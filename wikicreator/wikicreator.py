# -*- coding: utf-8 -*-
import yaml
import markdown
import os
# import shutil
try:
    import SimpleHTTPServer
except:
    import http.server as SimpleHTTPServer
try:
    import SocketServer
except:
    import socketserver as SocketServer
import time
import socket
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from bs4 import BeautifulSoup as bs
import frontmatter


class Generator():

    def find_free_port(self):
        s = socket.socket()
        s.bind(('', 0))
        return s.getsockname()[1]

    def check_config(self, categories, active_exists):
        for category in categories:
            if (not active_exists) and ('active' in category and category['active']):
                active_exists = True
            elif not ('file' in category and category['file']) and not ('categories' in category and category['categories']):
                print("Please use either a file or categories in config")
                return 1
            elif 'categories' in category and category['categories']:
                return self.check_config(category['categories'], active_exists)
        if active_exists:
            return 0
        else:
            print ("Please mark one category as active")
            return 1

    def generate(self):
        def create_tabpane(categories):
            tab_content = ""
            for category in categories:
                if category.get('file'):
                    try:
                        with open(category['file']) as f:
                            tab_body = markdown.markdown(f.read())
                            tab_content += '<div role="tabpanel" class="tab-pane' + (' active ' if 'active' in category and category['active'] else '') + '" id="' + category['file'].replace('/', '_').replace('.md', '') + '">' + tab_body + '</div>\n'
                    except:
                        print ("file " + category['file'] + " not found")
                if category.get('categories'):
                    tab_content += create_tabpane(category['categories'])
            return tab_content

        def create_sidebar(categories):
            sidebar_content = ""
            for category in categories:
                if category.get('categories') and category.get('file'):
                    sidebar_content += '\n<li><a role="button" data-toggle="collapse" href="#' + category['heading'].replace(' ', '_') + '_collapse" header-link="#' + category['file'].replace('/', '_').replace('.md', '') + '" aria-expanded="false" aria-controls="' + category['heading'].replace(' ', '_') + '_collapse"><i class="fa fa-chevron-right nav-chevron"></i>'
                    sidebar_content += category['heading']
                    sidebar_content += '</a></li>\n'
                    sidebar_content += '<div class="collapse well" id="' + category['heading'].replace(' ', '_') + '_collapse">\n<ul class="nav nav-sidebar indented">\n'
                    sidebar_content += create_sidebar(category['categories']) + '</ul>\n</div>'
                elif category.get('file'):
                    sidebar_content += '<li role="navlinkelement"' + (' class="active" ' if 'active' in category and category['active'] else '') + '><a class="navlink" data-target="#'
                    sidebar_content += category['file'].replace('/', '_').replace('.md', '') + '">'
                    sidebar_content += category['heading'] + '</a></li>\n'
                elif category.get('categories'):
                    sidebar_content += '\n<li><a role="button" data-toggle="collapse" href="#' + category['heading'].replace(' ', '_') + '_collapse" aria-expanded="false" aria-controls="' + category['heading'].replace(' ', '_') + '_collapse"><i class="fa fa-chevron-right nav-chevron"></i>'
                    sidebar_content += category['heading']
                    sidebar_content += '</a></li>\n'
                    sidebar_content += '<div class="collapse well" id="' + category['heading'].replace(' ', '_') + '_collapse">\n<ul class="nav nav-sidebar indented">\n'
                    sidebar_content += create_sidebar(category['categories']) + '</ul>\n</div>'
            return sidebar_content

        cwd = os.getcwd()
        filepath = os.path.join(cwd, 'config.yaml')
        config = open(filepath)
        dataMap = yaml.safe_load(config)
        config.close()
        if self.check_config(dataMap, False) == 0:
            env = Environment()
            env.loader = FileSystemLoader('.')
            wikitemplate = env.get_template('templates/wikitemplate.html')
            tab_content = create_tabpane(dataMap)
            sidebar_content = create_sidebar(dataMap)
            htmlcontent = wikitemplate.render(sidebar_content=sidebar_content,
                                              tab_content=tab_content)
            soup = bs(htmlcontent, 'html.parser')  # make BeautifulSoup
            prettyHTML = soup.prettify()   # prettify the html
            output = open('public/index.html', 'w')
            output.write(prettyHTML)
            output.close()
            # print ("files generated")
        else:
            print("config check failed")
            return 1

    def server_worker(self, PORT):
        """thread worker function"""
        #os.chdir("public")
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer(("", PORT), Handler)
        print ("serving at localhost:" + str(PORT) + "/public/index.html")
        httpd.serve_forever()
        pass

    def files_worker(self):
        while(True):
            self.generate()
            time.sleep(1)
        pass
