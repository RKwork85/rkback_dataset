# 使用现有的dsmysql:1.0镜像作为基础镜像
FROM dsmysql:1.0

# 将本地的dsmysql卷内容复制到镜像的/var/lib/mysql目录
COPY data/ /var/lib/mysql

# 如果需要复制配置文件，也可以添加类似下面的指令
# COPY /path/to/local/conf.d /etc/mysql/conf.d

# 其他需要的指令，例如EXPOSE端口等
EXPOSE 3306

# 指定容器启动时执行的命令
CMD ["mysqld"]