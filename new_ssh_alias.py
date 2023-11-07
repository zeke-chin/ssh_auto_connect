import time
from pathlib import Path


class SSHBuilder:
    def __init__(self, host, user, password, alias_name, port, file_home, use_proxy, proxy):
        self.host = host
        self.user = user
        self.password = password
        self.alias_name = alias_name
        self.port = port
        self.file_home = Path.home() / ".ssh/home" if file_home == "" else Path(file_home)
        self.ssh_file_path = self.file_home / self.alias_name
        self.use_proxy = use_proxy
        self.proxy = proxy

    # def build(self):
    #     self.write_ssh_file()
    #
    #     print("正在修改shellrc文件")
    # self.write_shellrc()

    def write_ssh_file(self):
        template = f'''
#!/usr/bin/expect
set PORT {self.port}
set HOST {self.host}
set USER {self.user}
set PASSWORD {self.password}

# Check if the USE_PROXY environment variable is set. If not, default to "yes" (use proxy).
if {{![info exists ::env(USE_PROXY)]}} {{
    set ::env(USE_PROXY) "{"yes" if self.use_proxy else "no"}"
}}
set use_proxy $::env(USE_PROXY)
# Proxy settings
set PROXY_COMMAND "nc -X 5 -x {self.proxy} %h %p"

if {{$use_proxy == "yes"}} {{
    spawn ssh -p $PORT -o "ProxyCommand $PROXY_COMMAND" $USER@$HOST
}} else {{
    spawn ssh -p $PORT $USER@$HOST
}}

expect {{
    -re "Are you sure you want to continue connecting.*" {{
        send "yes\\r"
        exp_continue
    }}
    "*password:*" {{
        send "$PASSWORD\\r"
    }}
}}

interact
        '''
        self.ssh_file_path.parent.mkdir(parents=True, exist_ok=True)

        # 创建文件
        if self.ssh_file_path.is_file():
            print(f"*******************************************************\n{self.ssh_file_path}文件已存在，正在备份...")
            back_name = f"{self.ssh_file_path.name}.{int(time.time())}.bak"
            self.ssh_file_path.rename(self.ssh_file_path.parent / back_name)
            print(f"=> {self.ssh_file_path.parent / back_name }")

        self.ssh_file_path.touch()
        self.ssh_file_path.write_text(template)
        print(f"*******************************************************\n生成{self.ssh_file_path}文件成功!!!")
        self.ssh_file_path.chmod(0o777)
        print(f"修改{self.ssh_file_path}文件权限成功")

    def write_shellrc(self, shellrc_choice):
        # sourcery skip: merge-list-appends-into-extend, switch
        # 写入~/.bashrc 和 ~/.zshrc
        header = "# >>> alias ssh config start >>>\n"
        footer = "# <<< alias ssh config end <<<\n"
        alias_line = f'''alias {self.alias_name}="expect {self.ssh_file_path}"\n'''

        shellrc_files = []
        if shellrc_choice == "bash":
            shellrc_files.append(self.file_home.parent.parent / ".bashrc")
        elif shellrc_choice == "zsh":
            shellrc_files.append(self.file_home.parent.parent / ".zshrc")
        else:
            shellrc_files.append(self.file_home.parent.parent / ".bashrc")
            shellrc_files.append(self.file_home.parent.parent / ".zshrc")

        for shellrc in shellrc_files:
            print(f"正在写入 {shellrc} 文件:")
            if not shellrc.exists(): shellrc.touch()
            with shellrc.open("a+") as f:
                self._extracted_from_write_shellrc_12(f, header, footer, alias_line)

    @staticmethod
    def _extracted_from_write_shellrc_12(f, header, footer, alias_line):
        # 将指针移到文件开头
        f.seek(0)
        content = f.read()
        alias_self = f'''alias new_ssh="python {Path(__file__).resolve()}"\n'''

        if alias_line in content:
            print("已存在该alias")
            return
        elif header in content and footer in content:
            # 如果存在，找到尾部位置
            footer_pos = content.find(footer)
            # 添加新的 alias 到尾部
            content = content[:footer_pos] + alias_line + content[footer_pos:]
        else:
            # 如果不存在，添加头部，尾部和新的 alias
            content = content + header + alias_self + alias_line + footer
            print("可以通过使用 new_ssh 快速执行本脚本")

        # 清空文件内容
        f.seek(0)
        f.truncate()

        # 重新写入修改后的内容
        f.write(content)
        print(f"写入 {f.name} 文件成功")


if __name__ == '__main__':
    while True:
        print("\n请输入你想添加的ssh(按q 或 ctrl+c 退出)")
        alias_name = input("别名：")
        if alias_name.lower() == 'q':
            break

        host = input("host: ")
        user = input("user: ")
        password = input("password: ")
        port_str = input("port(不填即回车 默认为22): ")
        port = int(port_str) if port_str.isdigit() else 22  # 默认端口为22
        ssh_file_home = input("ssh_file_home(不填即回车 空格默认为~/.ssh/home): ")
        ssh_file_home = ssh_file_home or ""
        ssh_use_proxy = input(
            "ssh_use_proxy(不填/回车/空格 默认为false, 使用填true. 或后期配置环境变量 USE_PROXY= true): ")
        ssh_proxy = ""
        if ssh_use_proxy.lower() == "true":
            ssh_use_proxy = True
            ssh_proxy = input("ssh_proxy(不填即回车 空格默认为127.0.0..gitignore:7890): ")
        ssh_proxy = ssh_proxy or "127.0.0..gitignore:7890"

        shellrc_choice = input("写入的shellrc(可选bash,zsh, 不填即回车bash与zsh全部写入): ").lower()

        ssh = SSHBuilder(
            host=host,
            user=user,
            password=password,
            alias_name=alias_name,
            port=port,
            file_home=ssh_file_home,
            use_proxy=ssh_use_proxy,
            proxy=ssh_proxy
        )
        ssh.write_ssh_file()
        ssh.write_shellrc(shellrc_choice)

        print(f"\n{alias_name}添加成功\n请通过 source ~/.bashrc 或 source ~/.zshrc 使配置生效\n")
