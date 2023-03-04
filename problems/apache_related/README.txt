windows上 apache python mod_wsgi  MSC VR版本的关系
    https://zhuanlan.zhihu.com/p/206743112


apache download homepage:
    https://www.apachelounge.com/download/


AH00558: httpd.exe: Could not reliably determine the server's fully qualified domain name,
using fe80::fbb3:d008:cf77:493a. Set the 'ServerName' directive globally to suppress this message
    解决： http://www.manongjc.com/detail/12-scvhgqjjouiejre.html


pip install mod_wsgi:
    https://www.qiniu.com/qfans/qnso-42323817
    https://www.likecs.com/ask-385572.html
    https://www.lfd.uci.edu/~gohlke/pythonlibs/#mod_wsgi

-----------------------------------------------------------------------------------------
在windows上配置apache和  django mod_wsgi
安装apache：https://www.apachelounge.com/download/

推荐使用python3.7
    python3.11 上出现 not module error: _socket, 怀疑是python311 VS版本高于apache的编译版本

pip install mod_wsgi: (多种方式 可以下载对应的wheel包，也可以安装 vs后 让python编译安装)
    然后: mod_wsgi-express module-config 出现如下信息：
        LoadFile "c:/program files/python37/python37.dll"
        LoadModule wsgi_module "c:/program files/python37/lib/site-packages/mod_wsgi/server/mod_wsgi.cp37-win_amd64.pyd"
        WSGIPythonHome "c:/program files/python37"
    添加到 httpd.conf


虚拟环境的问题：在 wsgi file 中 激活python虚拟环境
    import os
    activate_this = r'D:\env\django_site\Scripts\activate_this.py'
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))
    from django.core.wsgi import get_wsgi_application
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_site.settings')
    application = get_wsgi_application()

Questions:
    WSGIApplicationGroup %{GLOBAL}
    mod_access_compat.so

--------------------------------------------------------------------------------------------
https://blog.csdn.net/weixin_43848146/article/details/108570234
https://blog.csdn.net/qq_64865183/article/details/128148057