#!/usr/bin/env python

# Copyright (C) 2007 Giampaolo Rodola' <g.rodola@gmail.com>.
# Use of this source code is governed by MIT license that can be
# found in the LICENSE file.

"""A basic FTP server which uses a DummyAuthorizer for managing 'virtual
users', setting a limit for incoming connections and a range of passive
ports.
"""

import os
from pathlib import Path

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer



def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Getting a path to ../files directory
    realpath = os.path.realpath(__file__)
    p = Path(realpath)
    working_dir = str(p.parent.parent) + "/files"

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    # authorizer.add_user('ftp_user', 'ftp_password', os.getcwd(), perm='elradfmwMT')
    # authorizer.add_anonymous(os.getcwd())

    authorizer.add_user('ftp_user', 'ftp_password', working_dir, perm='elradfmwMT')
    authorizer.add_anonymous(working_dir)


    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib beeed ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in ceee you're behind a NAT.
    # handler.masquerade_address = '151.25.42.11'
    handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', 21)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()


if __name__ == '__main__':
    main()
