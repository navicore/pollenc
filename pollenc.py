#!/usr/bin/env python

# Copyright 2012 Amaret Inc. All rights reserved.

import sys
import argparse
import json
import zipfile
import os
import base64
import random
import datetime
import socket


class Pollenc:

    def __init__ (self, args):
        self.args = args
        self.workname = 'pollenc' + str(os.getpid()) + '_' + str(random.randint(1, 10000))
        self.workzip = '/tmp/' + self.workname + '_src.zip'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 2323))

    #
    # begin comm
    #
    def write(self, msg):
        self.sock.send(msg)
    
    def read(self):
        r = self.sock.recv(32768)
        return r
    #
    # end comm
    #

    # presumes path is the parent dir to the 'code' dir
    def zipdir(self, path, zip):
        for root, dirs, files in os.walk(path):
            for file in files:
                if not file.endswith('.zip'):
                    zip.write(os.path.join(root, file))


    def makezip(self, filename):
        ptmp = '.'
        #todo: calc ptmp123 dir and copy src dir to tmp/ptmp123/code
        zip = zipfile.ZipFile(filename, 'w')
        self.zipdir(ptmp, zip)
        zip.close()

    def sendzip(self):
        file = open(self.workzip, "rb")
        data = ''
        while True:
            chunk = file.read(1024)
            if not chunk: 
                break  # EOF
            data += chunk
        file.close()
        b64data = base64.b64encode(data)

        jsonstr = '{\"environment\": \"%s\", \"tid\": \"%s\", \"aid\": \"%s\", \"reply\": \"%s\", \"type\": \"request\", \"service\": \"compile\", \"user\": {\"token\": \"%s\", \"id\": \"%s\", \"name\": \"%s\"}, \"project\": {\"id\": \"%s\", \"name\": \"%s\"}, \"content\" :  {\"source\":  \"%s\", \"filename\": \"%s\", \"partnum\": \"%s\" } }' % (args.environment, 0, 42, "dummy_replyTo", args.token, 12345678, None, 'myproj123', 'myproj', b64data, args.filename, args.mcu)
        
        self.write(jsonstr)

    def run(self):

        #starttime = datetime.datetime.now()

        self.makezip(self.workzip)

        self.sendzip()

        while True:
            r = self.read()
            workobj   = json.loads(r)
            if workobj['type'] != 'response':
                print ('%s' % (workobj['content']['content']))
                continue
            if workobj['content']['error'] != 'None':
                print ('error! %s' % (workobj['content']['error']))
            break

        os.remove(self.workzip)

        content   = workobj['content']
        src       = content['content']

        #stoptime = datetime.datetime.now()
        #dur = stoptime - starttime

        return src


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--cflags', dest='cflags', action='store', help='append cflags')
    parser.add_argument('--set-cflags', dest='setcflags', action='store', help='cflags')
    parser.add_argument('-m', '--mcu',  dest='mcu', action='store', help='mcu', required=True)
    parser.add_argument('-e', '--environment',  dest='environment', action='store', help='environment', required=True)
    parser.add_argument('-t', '--token',   dest='token', action='store', help='user credential', required=True)
    parser.add_argument('-i', '--include',   dest='include', action='append', help='code dirs')
    parser.add_argument('filename', nargs='?')
        
    args = parser.parse_args()

    if args.filename == None:
        raise Exception('no filename specified')

    if args.include != None:
        for i in args.include:
          #print ("include %s" % (i))
          pass

    r = Pollenc(args).run() 
    print(r)
