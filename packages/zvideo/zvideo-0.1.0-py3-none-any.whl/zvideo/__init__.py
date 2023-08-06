import os 
from subprocess import Popen


def exec(func):
    """系统调用装饰器"""
    def wrapper(*args, **kwargs):
        cmd = func(*args, **kwargs)
        print('Executing: %s' % cmd)
        cmd = cmd.split(' ')
        p = Popen(cmd)
        p.communicate()
    return wrapper


@exec
def convert(src, format):
    """ 格式转化
    convert('demo.mp4', 'mp3')
    """
    dst = src.split('/')[-1].split('.')[0]
    return 'ffmpeg -i %s %s.%s' % (src, dst, format) 
    

@exec
def add_soft_sub(src, sub, dst):
    """添加内嵌字幕
    add_soft_sub('1.mp4','1.srt','2.mp4')
    add_soft_sub('2.mkv','1.srt','3.mkv')
    """
    if('mkv' in src):
        return 'ffmpeg -i %s -i %s -c copy %s' % (src, sub, dst)
    else:
        return 'ffmpeg -i %s -i %s -c copy -c:s mov_text %s' % (src, sub, dst)


@exec
def add_hard_sub(src, sub, dst):
    """添加硬字幕"""
    return 'ffmpeg -i %s -vf subtitles=%s -y %s' % (src, sub, dst)

    