import argparse
import subprocess
import os
from run import *

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--run", type=str, default=None, help=("""请求参数, JSON格式如下: 
    {
        \"task_id\": [task_id],
        \"widget_id\": [widget_id],
        \"pending_count\": [pending_count],
        \"fn_name\": \"test\",
        \"param\": {"
            \"text\":\"Hello World\"
        }"""))
parser.add_argument("--out", type=str, default=None, help=("output file path"))
cmd_opts = parser.parse_args()


def main(cmd_opts):
    if cmd_opts.run == None or cmd_opts.out == None:
        print("args fail!")
        return
    
    if os.path.exists(cmd_opts.run):
        with open(cmd_opts.run, 'r') as f:
            data = json.load(f)
    result = runTask(data)
    with open(cmd_opts.out, 'w') as f:
        json.dump(result, f)

if __name__ == '__main__':
    subprocess.run(f"mecord widget add {os.getcwd()}", stdout=None)
    main(cmd_opts)
