import subprocess
import os
import sys
import json
import argparse
import shutil


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source_json", required=True)
args = parser.parse_args()
source_json_path = os.path.abspath(args.source_json)
source_dir = os.path.dirname(source_json_path)

# 下载source json
with open(source_json_path) as f:
    data = json.load(f)

# 解析source json数据
url = data["remote"]
name = data["name"]
commit = data["commit"]
patches = data["patches"]
target_dir = os.path.join(os.path.dirname(source_json_path), "source")
patch_dir = os.path.join(os.path.dirname(source_json_path), "patches")

# 目录存在则先清空
if os.path.exists(target_dir):
    shutil.rmtree(target_dir)

subprocess.check_call(["git", "clone", url, target_dir])
subprocess.check_call(["git", "checkout", commit], cwd=target_dir)

for patch in patches:
    patch_path = os.path.join(patch_dir, patch)
    subprocess.check_call(["git", "apply", patch_path], cwd=target_dir)
