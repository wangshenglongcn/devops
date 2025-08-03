
## yaml vim配置

推荐yaml配置, 在~/.vimrc中添加以下内容:
```shell
autocmd FileType yaml setlocal ai et sw=2 ts=2 sts=2 cuc
```

- `autocmd FileType yaml`：检测到当前缓冲区的文件类型是yaml时触发后面的命令。
- `ai`：自动缩进（autoindent），新行会继承上一行的缩进。
- `et`：将制表符（Tab）转化为空格（expandtab）。
- `sw=2`：`shiftwidth=2`，表示每次缩进的宽度是 2 个空格。
- `ts=2`：`tabstop=2`，Tab 在编辑器中显示的宽度是 2 个空格。
- `sts=2`：`softtabstop=2`，按退格或 Tab 键时视为 2 个空格。
- `cuc`：显示当前光标所在列的高亮线（cursorcolumn）

## 安装


Ubuntu
```shell
apt-get install ansible
```

## 配置密钥

在管控节点中通过ssh-keygen生成密钥，需要通过ssh-copy-id将密钥拷贝到所有被管控节点。

对于自动化流程而言，这一过程手动实现会有点突兀，这时我们需要用一个自动化脚本来批量配置，详情见`config_ssh`，仅需执行一次即可。

## 配置文件

优先级从低到高如下所示, 最后的配置是所有配置按优先级合并的结果, 存在重复项保留高优先级

```shell
/etc/ansible/ansible.cfg
~/.ansible.cfg

# 若当前目录为cur, 配置文件为ansible.cfg
$cur/ansible.cfg

# 环境变量
$ANSIBLE_CONFIG
```

配置文件内容示例:
```shell
[defaults]
# 库存文件位置
inventory = ./inventory

# 默认模块路径
library = ./library

# 提高并发数（默认5）
forks = 20

# 关闭 host key 检查（初期调试时方便）
host_key_checking = False

# 默认远程用户（可用 -u 覆盖）
remote_user = root

# 私钥文件（免密登录用）
private_key_file = ~/.ssh/id_ed25519

# 输出更详细信息（v，vv，vvv）
# verbosity = 1

# 默认 become 行为
become = True
become_method = sudo
become_user = root

# 日志文件
log_path = ./ansible.log

# 显示中文时防止乱码
display_skipped_hosts = False

# 设置超时时间（默认10s）
timeout = 30


[privilege_escalation]
# 默认 sudo 配置
become = True
become_method = sudo
become_user = root

```

| **Directive  指令** | **Description  描述**                                                                                                                                                                                                                                                                                                                |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| inventory         | Specifies the path to the inventory file.  <br>指定库存文件的路径。                                                                                                                                                                                                                                                                          |
| remote_user  | Specifies the username that Ansible uses to connect to the managed hosts. If not specified, the current user's name is used. (In a container-based automation execution environment run by ansible-navigator, this is always root.)  <br>指定 Ansible 用于连接到受管主机的用户名。如果未指定，则使用当前用户名。（在由 ansible-navigator 运行的基于容器的自动化执行环境中，始终为 root。） |
| ask_pass          | Specifies whether to prompt for an SSH password. (Can be false, which is the default, if using SSH public key authentication.)  <br>指定是否提示输入 SSH 密码。（如果使用 SSH 公钥认证，可以设置为 false，这是默认值。）                                                                                                                                             |
| become    | Specifies whether to automatically switch users on the managed host (typically to root) after connecting. This can also be specified by a play.  <br>指定在连接到受管主机后是否自动切换用户（通常切换到 root）。这也可以通过 play 来指定。                                                                                                                              |
| become_method     | Specifies how to switch users (typically sudo, which is the default, but su is an option).  <br>说明如何切换用户（通常使用 sudo，这是默认设置，但 su 也是一个选项）。                                                                                                                                                                                            |
| become_user       | Specifies which user to switch to on the managed host (typically root, which is the default).  <br>指定在受管理主机上切换到的用户（通常使用 root，这是默认设置）。                                                                                                                                                                                              |
| become_ask_pass   | Specifies whether to prompt for a password for the become_method parameter. Defaults to false.  <br>指定是否为 become_method 参数提示密码。默认为 false。                                                                                                                                                                                          |
## 清单

清单放在ansible.cfg中指定的目录中

默认有一个组all, 包含所有被管控节点.
清单文件有ini/yaml区别, 下面以ini示例:
```shell
[aliyun]  # 自定义组名
1.111.111.1

[linux:children]  # 为指定组添加父类
aliyun
```

查看清单结构:
```shell
ansible-inventory --graph # 阅读性高
ansible-inventory --list # json
```

## playbook

按playbook中顺序执行, 以下是一个简单示例:

playbook.yml
```yaml
- name: play1
  hosts: all
  tasks:
    - name: Ensure directory exists
      file:
        path: /home/demo
        state: directory
        mode: '0755'

    - name: Copy local file to remote
      copy:
        src: ./demo
        dest: /home/demo/demo
```

通过命令`ansible-playbook playbook.yml`执行

### 关于playbook中的内置方法从哪查询？

比如上面的copy等，建议从[ansible官方文档](https://docs.ansible.com/ansible/latest/collections/index_module.html)中查找到具体的名字，如搜copy出现ansible.builtin.copy

然后在安装了ansible的环境中使用 `ansible-doc ansible.builtin.copy`查看具体的参数及示例

---

## 变量

命名规则：字母开头，仅包含字母、数字、下划线

当引用变量开头时，需要加双引号
```yaml
msg: asfasf{{ var }}
msg: "{{ var }}"
```

变量可以在很多地方定义，选一个适合当前情况的方式去定义，不同的定义方法请参考[官方文档](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence)

以下为常用的方式，并从低到高的顺序：


1. role default

在如`roles/xxx/defaults/main.yml`中定义

2. inventory group vars

inventory同级目录下yml，如：`inventory/group_vars/linux.yml`

3. playbook group vars

playbook同级目录下yml，如：`group_vars/linux.yml`

4. inventory host vars

inventory同级目录下yml，如：`inventory/host_vars/ip_addr.yml`

5. playbook host vars

playbook同级目录下yml，如：`host_vars/ip_addr.yml`

6. play var

在playbook中定义变量，如：
```yaml
- name: Demo
  hosts: all
  vars:
    app_env: staging
  
  tasks:
    - name: task1
      ...
```

7. play var file

在playbook中引用外部变量文件，如：
```yaml
- name: xxx
  host: xxx
  var_files:
    - vars/common.yml
    - vars/extra.yml
  
  ...
```

8. set fact

在playbook或task中用set_fact定义，如：
```yaml
- name: Demo set_fact example
  hosts: all
  gather_facts: false

  vars:
    initial_var: "hello"

  tasks:
    - name: Print initial var
      debug:
        msg: "initial_var is {{ initial_var }}"

    - name: Set a new fact
      set_fact:
        dynamic_var: "{{ initial_var }} world"

    - name: Use dynamic var
      debug:
        msg: "dynamic_var is {{ dynamic_var }}"

```

9. extra vars -e

在执行时传参，如`ansible-playbook playbook.yml -e "port=9000"`


## Roles

