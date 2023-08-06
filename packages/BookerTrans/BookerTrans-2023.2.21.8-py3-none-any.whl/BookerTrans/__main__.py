# coding: utf-8
import re
import time
from os import path
from pyquery import PyQuery as pq
import os
from argparse import ArgumentParser
import threading
import traceback
import copy
from functools import reduce
from concurrent.futures import ThreadPoolExecutor
from . import __version__
from .apis import apis
from .config import config
from .util import *

RE_CODE = r'<(pre|code|tt|var|kbd)[^>]*?>[\s\S]*?</\1>'
RE_TAG = r'<[^>]*?>'
RE_ENTITY = r'&(\w+|#x?\d+);'

trlocal = threading.local()
pool = None

def tags_preprocess(html):

    '''
    # 去头去尾
    html = html.replace("<?xml version='1.0' encoding='utf-8'?>", '')
    html = re.sub(r'<html[^>]*?>.*?<body[^>]*?>', '', html, flags=re.RegexFlag.DOTALL)
    html = re.sub(r'</body>.*?</html>', '', html, flags=re.RegexFlag.DOTALL)
    '''
    
    tags = []
    
    def replace_func(m):
        s = m.group()
        tags.append(s)
        idx = len(tags) - 1
        tk = f'\x20【T{idx}】\x20'
        return tk
        
    # 移除 <pre|code>
    html = re.sub(RE_CODE, replace_func, html)
    # 移除其它标签
    html = re.sub(RE_TAG, replace_func, html)
    # 移除实体
    html = re.sub(RE_ENTITY, replace_func, html)
    
    # 去掉 Unix 和 Windows 换行
    # html = html.replace('\n', ' ')
    # html = html.replace('\r', '')
    return html, tags

def tags_recover(html, tags):

    # 还原标签
    for i, t in enumerate(tags):
        html = html.replace(f'【T{i}】', t)
        
    return html

def trans_real(api, src):

    dst = None
    for i in range(config['retry']):
        try:
            print(src)
            dst = api.translate(
                src, 
                src=config['src'], 
                dst=config['dst'],
            )
            print(dst)
            time.sleep(config['wait_sec'])
            if dst: break
        except Exception as ex:
            traceback.print_exc()
            time.sleep(config['wait_sec'])
    
    if not dst: return None
    
    # 修复占位符
    dst = re.sub(r'【\s*T\s*(\d+)\s*】', r'【T\1】', dst, flags=re.I)
    dst = re.sub(r'\[\s*T\s*(\d+)\s*\]', r'【T\1】', dst, flags=re.I)
    return dst

@safe()
def trans_one(args, htmls, i):
    html = htmls[i]
    if html is None or html.strip() == '':
        return
    if not re.search(r'[A-Za-z]', html) or \
        re.search(r'[\u4e00-\u9fff]', html):
        return
    # 初始化 API
    if not hasattr(trlocal, 'api'):
        trlocal.api = load_api(args)
    api = trlocal.api
    # 标签预处理
    html, tokens = tags_preprocess(html)
    # 按句子翻译
    html = trans_real(api, html)
    if not html: 
        return
    # 标签还原
    html = tags_recover(html, tokens)
    htmls[i] = html

def preprocess(html):
    html = re.sub(r'<\?xml[^>]*\?>', '', html)
    html = re.sub(r'xmlns=".+?"', '', html)
    html = html.replace('&#160;', ' ') \
               .replace('&nbsp;', ' ')
    return html

def ext_to_trans(elems):
    htmls = []
    subs = []
    for elem in elems:
        elem = pq(elem)
        if elem.children('p'): 
            htmls.append(None)
            subs.append(None)
            continue
        # 如果有子列表，就取下来
        sub_list = None
        if elem.children('ul'): sub_list = elem.children('ul')
        if elem.children('ol'): sub_list = elem.children('ol')
        if sub_list: sub_list.remove()
        htmls.append(
            (elem.html() or '')
                .replace('\r', '')
                .replace('\n', ' ')
        )
        subs.append(sub_list)
    return htmls, subs

def group_to_trans(htmls, limit):
    res = []
    for h in htmls:
        if not len(res) or \
            sum(len(s) for s in res[-1]) + len(h) > limit:
            res.append([h])
        else:
            res[-1].append(h)
    return ['\n'.join(g) for g in res]
    
def split_transed(htmls):
    res = [h.split('\n') for h in htmls]
    return list(reduce(lambda x, y: x + y, res, []))
    
@safe()
def process_file(args):
    fname = args.fname
    if not is_html(fname):
        print(f'{fname} 不是 HTML 文件！')
        return
    print(fname)
    html = open(fname, encoding='utf-8').read()
    # 预处理
    html = preprocess(html)
    root = pq(html)
    # 标签到待翻译文本
    elems = root('p, h1, h2, h3, h4, h5, h6, blockquote, td, th, li')
    elems = pq([e for e in elems if not pq(e).children('p')])
    htmls, subs = ext_to_trans(elems)
    htmls = group_to_trans(htmls, args.limit)
    # 多线程翻译
    hdls = []
    for i, to_trans in enumerate(htmls):
        if not to_trans: continue
        h = pool.submit(trans_one, args, htmls, i)
        hdls.append(h)
    for h in hdls: h.result()
    # 回写翻译结果
    htmls = split_transed(htmls)
    for i, (h, s) in enumerate(zip(htmls, subs)):
        if not h: continue
        elems.eq(i).html(h)
        if s: elems.eq(i).append(s)
    html = str(root)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)

def process_dir(args):
    dir = args.fname
    files = [
        path.join(base, f) 
        for base, _, fnames in os.walk(dir) 
        for f in fnames 
        if is_html(f)
    ]
    for f in files:
        # args = copy.deepcopy(args)
        args.fname = f
        process_file(args)
        # h = pool.submit(process_file, args)
        # hdls.append(h)
    # for h in hdls: h.result()

def load_api(args):
    api = apis[args.site]()
    api.host = args.host
    api.proxy = args.proxy
    api.timeout = args.timeout
    return api

def main():
    global pool
    
    parser = ArgumentParser(prog="BookerTrans", description="HTML Translator with Google Api for iBooker/ApacheCN")
    parser.add_argument('site', help='translate api', choices=apis.keys())
    parser.add_argument('fname', help="html file name or dir name")
    parser.add_argument('-v', '--version', action="version", version=__version__)
    parser.add_argument('-H', '--host', default='translate.google.cn', help="host for google translator")
    parser.add_argument('-P', '--proxy', help=f'proxy with format \d+\.\d+\.\d+\.\d+:\d+ or empty')
    parser.add_argument('-T', '--timeout', type=float, help=f'timeout in second')
    parser.add_argument('-t', '--threads', type=int, default=8, help=f'num of threads')
    parser.add_argument('-w', '--wait-sec', type=float, default=1.5, help='delay in second between two times of translation')
    parser.add_argument('-r', '--retry', type=int, default=10, help='count of retrying')
    parser.add_argument('-s', '--src', default='auto', help='src language')
    parser.add_argument('-d', '--dst', default='zh-CN', help='dest language')
    parser.add_argument('-D', '--debug', action='store_true', help='debug mode')
    parser.add_argument('-l', "--limit", type=int, default=5000, help='word count limit')
    args = parser.parse_args()
    
    if args.proxy:
        p = args.proxy
        args.proxy = {'http': p, 'https': p}
    
    config['wait_sec'] = args.wait_sec
    config['retry'] = args.retry
    config['src'] = args.src
    config['dst'] = args.dst
    config['debug'] = args.debug
    pool = ThreadPoolExecutor(args.threads)
    
    if path.isdir(args.fname):
        process_dir(args)
    else:
        process_file(args)
        
if __name__ == '__main__': main()
