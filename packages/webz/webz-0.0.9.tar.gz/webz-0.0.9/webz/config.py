#coding=utf-8
from . import __path__
from . import base
from buildz import confz
import re
import os
import sys
import web
import threading
g_js_path = os.path.join(__path__[0], "js")
g_css_path = os.path.join(__path__[0], "css")

"""
[
(url, id),
(url, id, 0),
(url, id, 1),
(url, id, 0, []),
(url, id, 1, []),
(url, id, 0, [], {}),
(url, id, 1, [], {}),

]
"""
def imports_obj(path):
    spt = path.split(".")
    mds = ".".join(spt[:-1])
    md = __import__(mds)
    for k in spt[1:]:
        md = getattr(md, k)
    return md()

pass

class Static(base.Base):
    @staticmethod
    def update_time(sec):
        Static._Cache.update_time(sec)
    _Cache = base.CacheFile()
    def init(self, prefix, root):
        self.prefix = prefix
        if root == "webz.js":
            root = g_js_path
        if root == "webz.css":
            root = g_css_path
        self.root = root
    def deal(self):
        url = self.input.url
        url = url[len(self.prefix):]
        if len(url)>0 and url[0] == "/":
            url = url[1:]
        fp = os.path.join(self.root, url)
        return Static._Cache.deal(fp, self.input, self.output)

pass
class Config:
    def add_file(self, filepath):
        self.filepaths.append(filepath)
        self.reset()
    def reset(self):
        filepaths = self.filepaths
        if type(filepaths) == str:
            filepaths = [filepaths]
        self.filepaths = filepaths
        rst = []
        self.urls = []
        for fp in self.filepaths:
            rst += confz.loadfile(fp)
        for val in rst:
            if len(val)<2:
                print("Error Config:", val)
                continue
            if len(val) == 2:
                val.append("0")
            if len(val) == 3:
                val.append([])
            if len(val) == 4:
                val.append({})
            url, path, single, args, maps = val
            if single == "1":
                path = imports_obj(path)
            self.urls.append([url, path, single, args, maps])
    def __init__(self, filepaths, root = None):
        super(Config, self).__init__()
        self.filepaths = filepaths
        if root is not None:
            sys.path.append(root)
        self.reset()
    def GET(self, url):
        return ConfigWeb(self).GET(url)
    def POST(self, url):
        return ConfigWeb(self).POST(url)

pass
class ConfigWeb(base.Base):
    def add_file(self, filepath):
        self.filepaths.append(filepath)
        self.reset()
    def reset(self):
        filepaths = self.filepaths
        if type(filepaths) == str:
            filepaths = [filepaths]
        self.filepaths = filepaths
        rst = []
        self.urls = []
        for fp in self.filepaths:
            rst += confz.loadfile(fp)
        for val in rst:
            if len(val)<2:
                print("Error Config:", val)
                continue
            if len(val) == 2:
                val.append("0")
            if len(val) == 3:
                val.append([])
            if len(val) == 4:
                val.append({})
            url, path, single, args, maps = val
            if single == "1":
                path = imports_obj(path)
            self.urls.append([url, path, single, args, maps])
    def __init__(self, config):
        super(ConfigWeb, self).__init__()
        self.config = config
    def deal(self):
        url = self.input.url
        type = self.input.type
        for pt, obj, single, args, maps in self.config.urls:
            if len(pt)==0 or pt[0]!="^":
                pt = "^"+pt
            if len(re.findall(pt, url))== 0:
                continue
            if single == "0":
                obj = imports_obj(obj)
            obj._set(self)
            try:
                obj.init(*args, **maps)
                if type == base.GET:
                    obj.get()
                elif type == base.POST:
                    obj.post()
                else:
                    pass
            except Exception as exp:
                print("Exp:", exp)
                self.output.set_str(str(exp))
                self.output.finish(True)
            if self.output.finish():
                break
        if self.output() is None:
            raise web.HTTPError("404")
pass