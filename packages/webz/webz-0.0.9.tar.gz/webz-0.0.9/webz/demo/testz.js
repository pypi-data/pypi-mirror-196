[
[1,[
    //(url前缀, key, 初始化参数)
    ("func/", test.func)
    ("rest/upload", test.file)
    ("page/", webz.static, ["page", "pages"])

    //要用项目自带的js的话最后固定要加这两行
    ("webz/js/", webz.static, ["webz/js", "webz.js"])
    ("webz/css/", webz.static, ["webz/css", "webz.css"])
]],
//优先级为0，最先判断
[0, [
    ("/", test.prev)
]],
[2, [("func/aft", test.aft)]]

]