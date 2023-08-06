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
cmd_opts = parser.parse_args()

if __name__ == '__main__':
    subprocess.run(f"mecord widget add {os.getcwd()}", stdout=None)
    runTask(cmd_opts)
