import subprocess
import sys
import os
p = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__),'debug.py')],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL,
                     start_new_session=True
                     )

def test():
     return 'ok'
def decrypt(key):
     print('key is ',key)
