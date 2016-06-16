import sys
import webbrowser

dicts = {
    'g': 'https://www.google.com/search?q={q}',
    'bd': 'https://www.baidu.com/#ie=UTF-8&wd={q}',
    'wiki': 'https://en.wikipedia.org/wiki/{q}',
    'github': 'https://github.com/search?q={q}',
    'vimeo': 'https://vimeo.com/search?q={q}',
    'fy_en': 'http://translate.google.cn/#en/zh-CN/{q}',
    'fy_cn': 'http://translate.google.cn/#zh-CN/en/{q}',
    'sg': 'http://translate.google.cn/#zh-CN/en/{q}',
    'hb': 'http://huaban.com/search/?q={q}',
    'h_pyside': 'https://srinikom.github.io/pyside-docs/search.html?q={q}',
    'h_maya': ''
}