#coding=utf-8
import sys
import os

# 下面三行代码可以删除
from . import __path__
webpath = os.path.dirname(os.path.dirname(os.path.dirname(__path__[0])))
sys.path.append(webpath)
# 上面三行代码可以删除


import webz
class Test(webz.Base):
    def deal(self):
        self.output.set("url", self.input.url)
        self.output.set("action", self.input.type)
        self.output.update(self.input.get())

pass

class Prev(webz.Base):
    def deal(self):
        self.output.set("prev", "testPrev")
        print("Test Prev")

pass
class Aft(webz.Base):
    def deal(self):
        self.output.set("aft", "testAft")
        print("Test Aft")

pass

class TestFile(webz.Base):
    def deal(self):
        self.input.default(file={})
        data = self.input.get()
        file = data['file']
        dt = file.file.read()
        print("dt:", type(dt), len(dt))
        self.output.set_bytes(dt)

pass

def show():
    print("try such url: http://127.0.0.1:8080/func/abc?d=e&f=g")
    print("try such url: http://127.0.0.1:8080/func/aft?d=e&f=g")
    print("try such url: http://127.0.0.1:8080/page/test1.html")
    print("try such url: http://127.0.0.1:8080/page/test.html")

from webz import configz

def runz(fps):
    show()
    configz.run(fps)

pass

from webz import config
def run(fp):
    show()
    webz.init(config.Config(fp))
    webz.run(8080, "127.0.0.1")

pass
