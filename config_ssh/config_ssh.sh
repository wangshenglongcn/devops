#!/bin/bash
# 用途：将当前机器ssh拷贝到被管控机器


set -e
WORKSPACE=$(dirname $0)

# 不存在~/.ssh则生成
if ! ls ~/.ssh/id_* 2> /dev/null | grep -v '.pub'; then
    # -f执行目录， -N指定passphrass
    ssh-keygen -f ~/.ssh/id_rsa -N ""
fi

if [ ! -f ${WORKSPACE}/hosts ]; then
    echo "不存在hosts文件"
    exit 0
fi

# 不存在sshpass则安装
if ! which sshpass; then
    apt-get install sshpass -y
fi

cat ${WORKSPACE}/hosts | grep -v '^[[:space:]\r]*$' | while IFS=, read -r ip password; do
    sshpass -p ${password} ssh-copy-id -o StrictHostKeyChecking=no root@${ip}
done