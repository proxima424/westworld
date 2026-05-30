#!/usr/bin/env python3
import subprocess, sys, json

r = subprocess.run(['python3', 'feed/_rollup.py'], capture_output=True, text=True)
sys.stderr.write(r.stderr)
if r.returncode != 0:
    print('ROLLUP_FAILED', r.returncode)
    sys.exit(1)

data = json.loads(r.stdout)
r2 = subprocess.run(['python3', 'feed/_extract.py'], input=r.stdout, capture_output=True, text=True)
sys.stdout.write(r2.stdout)
sys.stderr.write(r2.stderr)
sys.exit(r2.returncode)
