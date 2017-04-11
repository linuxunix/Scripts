#coding:utf-8
#!/usr/bin/env python
import sys

with open(sys.argv[1],'r') as f:
    for line in f.readlines():
        with open(sys.argv[1]+'_bak','a+') as f2:
            if '\u' in line:
                f2.write(line.decode("unicode-escape").encode("utf-8"))
            else:
                f2.write(line)