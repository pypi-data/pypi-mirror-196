#!/usr/bin/env python3
import subprocess

args = ['/bin/bash', '-c', 'bash && echo $HOSTNAME && bash']
subprocess.run(
        args, input=None, stdout=None, stderr=None,
)
