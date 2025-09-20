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

with open(source_json_path) as f:
    data = json.load(f)

url = data["remote"]
name = data["name"]
target_dir = os.path.join(os.path.dirname(source_json_path), "source")

if os.path.exists(target_dir):
    shutil.rmtree(target_dir)

subprocess.check_call(["git", "clone", url, target_dir])
