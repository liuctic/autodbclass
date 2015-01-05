#/usr/bin/env python
# -*- coding: utf-8 -*-

import autodbclass
import sys

def printHelp(selfname):
    print "Usage:", selfname, "input_db_schema_file"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        printHelp(sys.argv[0])
        exit(0)
    try:
        dbfile = open(sys.argv[1], "r")
        tbname = ''
        primk = ''
        mustk = []
        ordk = []
        primIsAuto = False
        for zline in dbfile:
            line = zline.strip()
            if len(line)<2:
                continue
            if line[0]=='%':
                continue
            elif line[0]=='#':
                if tbname == '':
                    tbname = line[1:]
                else:
                    # a new block is discovered
                    # generate the previous block
                    autodbclass.GenPHP(tbname, primk, primIsAuto, mustk, ordk)
                    # clear all
                    tbname = ''
                    primk = ''
                    primIsAuto = False
                    mustk = []
                    ordk = []
                    # set new
                    tbname = line[1:]
            elif line[0]=='*':
                if line[1]=='@':
                    primIsAuto = True
                    primk = line[2:]
                else:
                    primIsAuto = False
                    primk = line[1:]
            elif line[0]=='+':
                mustk.append(line[1:])
            else:
                ordk.append(line)
        dbfile.close()
        if tbname!='':
            # last one
            autodbclass.GenPHP(tbname, primk, primIsAuto, mustk, ordk)
    except Exception, e:
        print e
