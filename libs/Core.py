import os
import sys
import re
import webbrowser
import subprocess

import cmd
import config
import WebSearchers as web_api
from completer import CustomQCompleter


class Searchers:
    def __init__(self):
        self.completer = CustomQCompleter()

    def linkify(self, text):
        urlfinder = re.compile(r'http([^\.\s]+\.[^\.\s]*)+[^\.\s]{2,}|www(.+)|(\w+)^.[a-zA-Z]')
        m = urlfinder.match(text)
        if m:
            print m.group()
            url = m.group()
            webbrowser.open_new_tab(url.encode('gb2312'))

    def run(self,data):
        math_ = re.match('(?P<key>\w+|>) (?P<cmd>.+)', data)
        if math_:
            math_key = math_.groupdict()['key']
            cmd_string = math_.groupdict()['cmd']
            if math_key == '>':
                command = '{0}'.format(cmd_string)
                cmd.run(command)
            elif math_key == 'help':
                webbrowser.open_new_tab(config.get_regylar('help')[cmd_string])
            else:
                m = re.match(config.get_regylar('web'), data)
                if m:
                    try:
                        url = m.groupdict()['url']
                        # url = unicode(url, 'utf8')
                        key_ = m.groupdict()['key']
                        web = web_api.dicts[key_]
                        assert isinstance(web.format, object)
                        webbrowser.open_new_tab(web.format(q=url.encode('gb2312')))
                    except KeyError:
                        print 'not settings {0}'.format(data)
        elif os.path.isdir(data):
            try:
                command = 'cmd /c start "" "{0}"'.format(data)
            except:
                command = 'cmd /c start {0}'.format(data)

            subprocess.Popen(command, shell=True)

        elif os.path.isfile(data):
            os.startfile(data)

        self.linkify(data)
