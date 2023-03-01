1. redis enable remote login
https://blog.csdn.net/qq_45760401/article/details/125134757

2. apt 和 apt-get 的区别

3. ubuntu 查看二进制包的释放位置: dpkg -L <package_name>

4. libfuse:
    sudo apt-add-repository universe
    sudo apt install libfuse2

5. 自签证书：
    https://blog.csdn.net/yulei2008_/article/details/125738803
    https://learn.microsoft.com/zh-cn/dotnet/core/additional-tools/self-signed-certificates-guide?source=recommendations#with-openssl

6. root无法登陆：
    https://blog.csdn.net/qq_39289387/article/details/123274346

7. 命令提示符问题
    ubuntu 命令提示符和 centos命令提示符不一致
    [${debian_chroot:+($debian_chroot)}\u@\h:\w]\$
    [\u@\h \W]\$

8. install python3.6
    https://www.rosehosting.com/blog/how-to-install-python-3-6-4-on-centos-7/

    sudo yum install -y https://repo.ius.io/ius-release-el7.rpm
    sudo yum update
    sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
    python3.6 -V

9. install redis
    https://zhuanlan.zhihu.com/p/34527270

10. install httpd:
    https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-centos-7
    https://blog.csdn.net/u013032788/article/details/105361380

    https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-centos-7
        curl -sSLO https://dev.mysql.com/get/mysql80-community-release-el7-7.noarch.rpm
        sudo rpm -ivh mysql80-community-release-el7-7.noarch.rpm

        sudo grep 'temporary password' /var/log/mysqld.log

11. sudoers
    https://blog.csdn.net/LelemamaAnne/article/details/113624097

12 disable selinux:
    /etc/sysconf/selinux

13 disable firewall
    systemctl stop firewall.service

14. 升级git
    https://blog.csdn.net/SaberJYang/article/details/125501124
