# ssh_auto_connect
## 1. 启动命令
`python new_ssh_alias`
## 2. 脚本用处
通过编写`expect`脚本 和在`bashrc/zshrc`中添加 alias 命令
来实现快速的通过ssh 连接至服务器
## 3. 依赖环境
在linux/mac上 依赖expect 若没有手动安装即可
对于python 则仅仅依赖pathlib，pathlib在Python3.4就加入了标准库
```
╰─○ linux/macos
- expect 
╰─○ python
- python >= 3.4
```
## 4. 使用教程
```
(base) ╭─cgl at 11-3090 in /data/zeke/ssh_auto_connect 23-07-12 - 20:04:34
╰─○ python new_ssh_alias.py

请输入你想添加的ssh(按q 或 ctrl+c 退出)
别名：sn93
host: 192.155.1.93
user: root
password: 1234567890
port(不填即回车 默认为22):
ssh_file_home(不填即回车 空格默认为~/.ssh/home):
写入的shellrc(可选bash,zsh, 不填即回车bash与zsh全部写入):
*******************************************************
生成/home/cgl/.ssh/home/sn93文件成功!!!
修改/home/cgl/.ssh/home/sn93文件权限成功
正在写入 /home/cgl/.bashrc 文件:
可以通过使用 new_ssh 快速执行本脚本
写入 /home/cgl/.bashrc 文件成功
正在写入 /home/cgl/.zshrc 文件:
可以通过使用 new_ssh 快速执行本脚本
写入 /home/cgl/.zshrc 文件成功

sn93添加成功
请通过 source ~/.bashrc 或 source ~/.zshrc 使配置生效


请输入你想添加的ssh(按q 或 ctrl+c 退出)
别名：q
(base) ╭─cgl at 11-3090 in /data/zeke/ssh_auto_connect 23-07-12 - 20:04:48
╰─○ source ~/.zshrc
(base) ╭─cgl at 11-3090 in /data/zeke/ssh_auto_connect 23-07-12 - 20:04:54
╰─○ sn93
spawn ssh -p 22 root@192.155.1.93
root@192.155.1.93's password:
Last login: Wed Jul 12 19:59:37 2023 from 192.155.1.11
(base) [root@localhost ~]# 登出
Connection to 192.155.1.93 closed.
(base) ╭─cgl at 11-3090 in /data/zeke/ssh_auto_connect 23-07-12 - 20:05:05
╰─○
```
