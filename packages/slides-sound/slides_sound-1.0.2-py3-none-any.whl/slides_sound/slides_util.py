import re
import os
import subprocess

def cmpfile( file1 ):
    name1 = os.path.basename(file1)
    pat = "([A-Za-z_\-]+)([0-9]+).*"
    m1 = re.match(pat, name1)

    if not m1:
        return name1
    else:
        base1 = m1.groups()[0]
        num1 = m1.groups()[1]
        return "%20.20s%20.20s"%(base1,num1)

def run( cmd, raiseException = True, verbose = False ):
    p = subprocess.Popen(cmd,
                   shell=True,
                   bufsize=1024,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT)
    output = p.stdout.read()
    result = p.wait()
    if result and raiseException:
        raise Exception(cmd,output,result)
    if verbose:
        print("Result:",result)
        print(output)
    return result

def saferemove( fname ):
    if os.path.exists(fname):
        os.remove(fname)
