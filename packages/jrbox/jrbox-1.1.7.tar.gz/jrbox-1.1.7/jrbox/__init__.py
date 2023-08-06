# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
''''''
import hashlib
import time
import os
import traceback
import re
import random
import base64
import html
from colorama import Fore
from tqdm import tqdm as td
from lxml import etree
import requests
import pypandoc



def test():
    print('hello world!')
    print(Fore.YELLOW + '人生苦短，我用Python！')
    print(Fore.LIGHTWHITE_EX + '人生苦短，我用Python！')
    print(Fore.LIGHTRED_EX + '人生苦短，我用Python！')
    print(Fore.LIGHTMAGENTA_EX + '人生苦短，我用Python！')
    print(Fore.LIGHTGREEN_EX + '人生苦短，我用Python！')
    print(Fore.LIGHTCYAN_EX + '人生苦短，我用Python！')
    print(Fore.LIGHTBLUE_EX + '人生苦短，我用Python！')
    print(Fore.CYAN + '人生苦短，我用Python！')
    print(Fore.LIGHTYELLOW_EX + '人生苦短，我用Python！')
    print(Fore.RED + '人生苦短，我用Python！')
    print(Fore.BLUE + '人生苦短，我用Python！')
    print(Fore.GREEN + '人生苦短，我用Python！')
    print(Fore.MAGENTA + '人生苦短，我用Python！')
    print(Fore.RESET + '人生苦短，我用Python！')
    return 'successful!'


def md5value(data, model=False):
    input_name = hashlib.md5()
    input_name.update(data.encode("utf-8"))
    if model == 'B32':
        return (input_name.hexdigest()).upper()
    elif model == 'B16':
        return (input_name.hexdigest())[8:-8].upper()
    elif model == 'S32':
        return (input_name.hexdigest()).lower()
    elif model == 'S16':
        return (input_name.hexdigest())[8:-8].lower()
    else:
        print('No Model Is ', model)
        return


def to_stamp(format_time):
    """
    2016-05-05 20:28:54 ----> 10位时间戳
    :param format_time:
    :return:
    """
    time_tuple = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
    timestamp = str(int(time.mktime(time_tuple)))
    return timestamp


def to_date(start):
    """
    start = ['567100800', '1632844924200'] --->支持10位，13位时间戳转标准时间
    :param start:
    :return:
    """
    starttime = []
    if type(start) == list:
        for timestamp in start:
            timestamp = list(timestamp)
            timestamp = int(''.join(timestamp[0: 10:]))
            time_local = time.localtime(timestamp)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            starttime.append(dt)
        return starttime
    if type(start) == str:
        timestamp = list(start)
        timestamp = int(''.join(timestamp[0: 10:]))
        time_local = time.localtime(timestamp)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt



html_clean = lambda text: re.sub(r'<[^>]+>', '', text)
# """
# 传入文本  -->  输出清除HTML标签后的文本
# :param text: Type == str
# :return: new text
# """

filename_clean = lambda filename: re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", filename)
# """
# 传入文本 --> 输出清除文件名非法字符后的文本
# :param filename: Type == str
# :return: new name
# """





def ip_to_address(ip):
    """

    :param ip: Type == str
    :return: Type == str
    """
    params = (
        ('query', ip),
        ('co', ''),
        ('resource_id', '5809'),
        ('t', '1661598345836'),
        ('ie', 'utf8'),
        ('oe', 'gbk'),
        ('cb', ['op_aladdin_callback', 'jQuery110206508062660667266_1661598209405']),
        ('format', 'json'),
        ('tn', 'baidu'),
        ('_', '1661598209414'),
    )
    response = requests.get('https://sp1.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php', params=params).text
    location = re.findall('"location":"(.*?)"', response, re.S)[0]
    address = location.encode('utf-8').decode('unicode-escape')
    return address



text_to_base64 = lambda text: base64.b64encode(text.encode('utf-8')).decode("utf-8")
"""
:param text: Type == str
:return: Type == str
"""

base64_to_text = lambda text: base64.b64decode(text.encode("utf-8")).decode("utf-8")
"""
:param text: Type == str
:return: Type == str
"""


def mkdirs(os_mkdir_path, is_getcwd=False):
    """
    If yes, print the path.
    If no, create a subfolder in the current directory.
    :param dir_name: Type == str
    :return: None
    """
    if is_getcwd == True:
        os_mkdir_path = os.getcwd() + '\\' + os_mkdir_path

    if not os.path.exists(os_mkdir_path):
        os.makedirs(os_mkdir_path)

    return

tqdm = td

video_pojie = lambda url: 'http://okjx.cc/?url=' + url
"""
支持众多主流视频站点:API拼接网页链接，访问即可
:param url: Type == str
:return: Type == str
"""

html_node_text = lambda HTML, XPATH: html.unescape(
    html_clean(str(etree.tostring(etree.HTML(HTML).xpath(XPATH)[0])))).lstrip("b'").rstrip("'")
"""
单节点方法，xpath列表请调用html_nodes_text方法
HTML: Web site source code
XPATH: Node XPATH Syntax
retur: Node, the front page display text data
"""


def html_nodes_text(XPATH_list):
    """
    该方法不完全等同于etree的//text()方法，实际应用场景请自行对比使用
    :param XPATH_list: Type == list 传入Xpath匹配到的节点群
    :return: Type == list 返回清洗后HTML标签后的文本
    """
    text_list = []
    for Xpath in XPATH_list:
        result = html.unescape(html_clean(str(etree.tostring(Xpath)))).lstrip("b'").rstrip("'")
        text_list.append(result)
    return text_list


def console(self='', *args, sep=' ', end='\n', file=None, color=None, model=True, colorful=False):
    """

    :param self:
    :param args:
    :param sep: Type == str
    :param end: Type == str
    :param file:
    :param color: Type == str
    :param model: Type == bool
    :param colorful: Type == bool
    :return: print
    """
    dic = {
        '黄色': 'Fore.YELLOW', '+黄色': 'Fore.LIGHTYELLOW_EX',
        '红色': 'Fore.RED', '+红色': 'Fore.LIGHTRED_EX',
        '青色': 'Fore.CYAN', '+青色': 'Fore.LIGHTCYAN_EX',
        '绿色': 'Fore.GREEN', '+绿色': 'Fore.LIGHTGREEN_EX',
        '蓝色': 'Fore.BLUE', '+蓝色': 'Fore.LIGHTBLUE_EX',
        # '黑色': 'Fore.BLACK', '+黑色': 'Fore.LIGHTBLACK_EX',
        '品红色': 'Fore.MAGENTA', '+品红色': 'Fore.LIGHTMAGENTA_EX',
        '!': 'Fore.RESET'
    }
    if colorful == True:
        li = list(str(self))
        for nnn in li:
            print(eval(dic[random.sample(dic.keys(), 1)[0]]) + nnn, end='')
        print('', end='  ')
        for iii in args:
            iii = list(str(iii))

            for ppp in iii:
                # breakpoint()
                print(eval(dic[random.sample(dic.keys(), 1)[0]]) + ppp, end='', )
            print('', end='  ')
        print('\n', end='')

    else:
        if color != None:
            if model != False:
                color = eval(dic[color])
            else:
                color = eval(color)
        else:
            color = Fore.LIGHTYELLOW_EX

        print(color + str(self), *args, sep=sep, end=end, file=file)


def mini_dom(node_list, title='The DOM tree reconstruction', sep='<p>\n**********\n</p>'):
    """
    :param node_list: Type == list
    :param title: Type == str
    :param sep: Type == str
    :return: New Dom Tree   Type == str
    """
    all_html_nodes = []
    for node in node_list:
        node_to_html = str(etree.tostring(node)).lstrip("b'").rstrip("'").replace(r'\n', '\n')
        all_html_nodes.append(node_to_html)
    node_to_html = sep.join(all_html_nodes)
    dom = html.unescape(f"""
            <!--JR-->
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{title}</title>
            </head>
            <body>
                {node_to_html}
            </body>
            </html>
            """).replace('\t', '').replace('\\t', '')
    return dom


re = re

etree = etree

def Incomplete_clearance(text, split_string):
    """
    All specified strings are cleared and then aggregated to remove n-1 units of a certain string.
    :param text: Type == str
    :param split_string: Type == str
    :return: new_text: Type == str
    """
    text = text.split(split_string)
    while True:
        try:
            text.remove('')
        except:
            break
    new_text = split_string.join(text)
    return new_text


occurrences = lambda text, string :len(re.findall(string, text, re.S))
# """
# Counts how often a string appears in the text.
# :param text: Type == str
# :param string: Type == str
# :return: num Type == int
# """

def cooKIE(cookie):
    cookie_dic = {}
    cookie = cookie.replace('\n', '').replace(' ', '')
    for i in cookie.split('; '):
        cookie_dic[i.split('=')[0]] = i.split('=')[1]
    return cookie_dic

"""unicode编解码"""
unicode_decode = lambda text:text.encode().decode("unicode_escape")
unicode_encode = lambda text:text.encode("unicode_escape").decode()


def html_to_word(html, output_file_path, mode):
    """
    HTML  转  WORD
    mode == True  --> html为源码状态  传入html文本
    mode == False --> html为文件状态  传入html路径
    """
    if mode == True:
        pypandoc.convert_text(html, 'docx', 'html', outputfile=output_file_path)  # 将 html 代码转化成docx
    elif mode == False:
        pypandoc.convert_file(html, 'docx', outputfile=output_file_path)  # 将网页直接转换成docx
    return


def listdir_by_time(path):
    """
    遍历文件夹内文件 时间排序
    :param path:
    :return:
    """
    files = os.listdir(path)
    creatTime = {time.ctime(os.path.getmtime(os.path.join(path, i))): i for i in files}
    creatTimeList = sorted(creatTime.items(), key=lambda x: x[0])
    return creatTimeList
