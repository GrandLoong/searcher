import config
import subprocess


def run(cmd):
    cmd_split = cmd.split(' ')
    if cmd_split:
        cmd_file = config.normpath(config.PLUGINS_DIR, 'cmd', '{0}.bat'.format(cmd_split[0]))
        command = 'start {0} {1}'.format(cmd_file, ' '.join(cmd_split[1:]))
    else:
        cmd_file = config.normpath(config.PLUGINS_DIR, 'cmd', '{0}.bat'.format(cmd))
        command = 'start {0}'.format(cmd_file)
    return subprocess.Popen(command, shell=True)


# print run('ping www.baidu.com')
