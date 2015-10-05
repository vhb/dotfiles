#!/usr/bin/env python3
# Copyright 2013-2014 Emmanuel Vadot <elbarto@bocal.org>
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import socket
import select
import hashlib
import time
import urllib.parse
import getpass
import sys
import getopt
import os
import configparser
from uuid import getnode as get_mac
import string
import random


class NetsoulConnectionError(BaseException):
    '''Disconnected'''


class Netsoul:

    def __init__(self, login, password=None,
                 host='ns-server.epitech.net', port=4242, verbose=False):
        self._host = host
        self._port = int(port)
        self._login = login
        self._password = password
        self._verbose = verbose
        self._isconnected = False
        self._isauth = False
        self._buffer = None
        self._salut = None
        self._sock = None
        self._writefd = []

    def isauth_get(self):
        return self._isauth

    isauth = property(isauth_get)

    def connect(self):
        try:
            if self._verbose:
                print ('Connecting to ' + self._host + ' on port ' +
                       str(self._port))
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._host, self._port))
            self._isconnected = True
            self.time_to_sleep = 1
            return True
        except Exception:
            if self._verbose:
                print ("Couldn't connect to " + self._host + ' on port ' +
                       str(self._port))
            raise NetsoulConnectionError

    def _ns_auth_ag(self):
        self._buffer = b'auth_ag ext_user none none\n'
        self._expectedresp = '002'
        self._next = self._ns_ext_user_log
        self._writefd.append(self._sock)

    def _ns_ext_user_log(self):
        data = self._salut.split(' ')
        challenge = hashlib.md5()
        challenge.update(bytes(data[2] + '-' + data[3] + '/' + data[4] +
                               self._password, 'utf8'))
        self._buffer = bytes('ext_user_log ' + self._login + ' ' +
                             challenge.hexdigest() + ' ' + data[4] + ' ' +
                             urllib.parse.quote('NSLOG 0.1') + '\n', 'utf8')
        self._writefd.append(self._sock)
        self._next = self._ns_state

    def _ns_state(self):
        self._isauth = True
        self._buffer = bytes('state actif:' + str(int(time.time())) +
                             '\n', 'utf8')
        self._writefd.append(self._sock)
        self._next = None

    def loop(self):
        while 1:
            readfd, writefd, exceptfd = select.select([self._sock],
                                                      self._writefd, [])

            for i in readfd:
                if i == self._sock:
                    try:
                        rdata = self._sock.recv(4096).decode('utf8') \
                            .strip('\n')
                    except:
                        raise NetsoulConnectionError

                    if rdata == '':
                        raise NetsoulConnectionError

                    if self._verbose:
                        print ("Received : '" + rdata + "'")
                    data = rdata.split(' ')
                    if data[0] == 'salut':
                        self._salut = rdata
                        self._ns_auth_ag()
                    elif data[0] == 'rep':
                        if data[1] != self._expectedresp:
                            print ('Last command failed')
                        else:
                            if self._next:
                                self._next()
                    elif data[0] == 'ping':
                        self._buffer = bytes('ping ' + data[1], 'utf8')
                        self._writefd.append(self._sock)

            for i in writefd:
                if i == self._sock:
                    if self._verbose:
                        print ("Sent : '" + str(self._buffer) + "'")
                    self._sock.send(self._buffer)
                    self._writefd.remove(self._sock)


def daemonize():
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("os.fork() failed: %s\n" + e.strerror)
        sys.exit(1)

    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("os.fork() failed: %s\n" + e.strerror)
        sys.exit(1)


def usage():
    print ('Usage: ' + sys.argv[0] + ' [-u login] [-h] [-v] [-d]')
    sys.exit(0)


class ConfigHandler:
    class NetsoulPasswordEncryption:

        _CHARS = string.ascii_uppercase + string.digits
        _SECRET_SIZE = 32
        _BLOCK_SIZE = 32
        _PADDING = '8'

        def __init__(self, AES, base64):
            self._AES = AES
            self._base64 = base64
            seed = get_mac()
            random.seed(seed)
            secret = ''.join(random.choice(self._CHARS) for x in
                             range(self._SECRET_SIZE))
            self._c = self._AES.new(secret)

        def _pad(self, s):
            return s + (self._BLOCK_SIZE - len(s) % self._BLOCK_SIZE) \
                * self._PADDING

        def encrypt(self, s):
            tmp = self._c.encrypt(self._pad(s))
            return self._base64.b64encode(tmp).decode('ascii')

        def decrypt(self, s):
            val = self._c.decrypt(self._base64.b64decode(s)).decode("utf-8")
            val = val.rstrip(self._PADDING)
            if len(val) != 8:
                raise Exception("Canno't decrypt password, please rewrite it")
            return val

    class NoEncryption:
        def encrypt(self, s):
            return s

        def decrypt(self, s):
            raise Exception("Canno't decrypt the password, please rewrite it")

    _CONFIG_SECTION = 'config'

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def get_config(self, name):
        try:
            return self.config.get(self._CONFIG_SECTION, name)
        except configparser.NoOptionError:
            return None

    def check_password(self):
        p = self.get_config('password')
        if p is None:
            return None
        try:
            from Crypto.Cipher import AES
            import base64

            cipher = self.NetsoulPasswordEncryption(AES, base64)
        except ImportError:
            print('Warning: pycrypt not available, no encryption will be used for password')
            cipher = self.NoEncryption()
        if len(p) == 8:
            # Need to be encrypted
            encrypted = cipher.encrypt(p)
            self.config.set(self._CONFIG_SECTION, 'password', encrypted)
            with open(self.config_file_path, 'w') as f:
                self.config.write(f)
            return p
        else:
            # Need be decrypted
            decrypted = cipher.decrypt(p)
            return decrypted

    def load_config_file(self):
        with open(self.config_file_path, 'r') as f:
            self.config = configparser.ConfigParser()
            self.config.readfp(f)
            password = self.check_password()
            value = {
                'login': self.get_config('login'),
                'password': password,
                'host': self.get_config('host'),
                'port': self.get_config('port'),
            }
            return value


def merge_dict(x, y):
    z = x.copy()
    z.update(y)
    return z

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dhvu:f:',
                                   ['demonize', 'help', 'verbose', 'user=',
                                    'config-file='])
    except getopt.GetoptError as e:
        print (e)
        usage()

    options = {'verbose': False, 'login': getpass.getuser()}
    daemon = True

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-v', '--verbose'):
            options['verbose'] = True
        elif o in ('-u', '--user'):
            options['login'] = a
        elif o in ('-d', '--demonize'):
            daemon = False
        elif o in ('-f', '--config-file'):
            c = ConfigHandler(a)
            options = merge_dict(options, c.load_config_file())
        else:
            usage()

    if options.get('login', None) is None:
        options['login'] = getpass.getuser()
    if options.get('password', None) is None:
        options['password'] = getpass.getpass()

    if daemon:
        daemonize()

    time_to_sleep = 1
    while 1:
        ns = Netsoul(**options)
        try:
            ns.connect()
            ns.loop()
        except NetsoulConnectionError:
            if options['verbose']:
                print ('Disconnected, retrying in {:d} seconds'.format(time_to_sleep))
            time.sleep(time_to_sleep)
            time_to_sleep = time_to_sleep * 2
