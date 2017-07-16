#!/usr/bin/env python2.7

import time
import paramiko
from credentials import get_credentials
from credentials import get_nova_credentials
from neutronclient.v2_0 import client
import novaclient.v2.client as nvclient
from convertToRouter import connectToInstance
from convertToRouter import installQuagga
from convertToRouter import configureOspf

# The virtual machines are calling quaaga and ospf functions to get configured as routers.
ssh = connectToInstance('Router1','FirstNetwork','SecondNetwork')
installQuagga(ssh,'Router1')
configureOspf(ssh,'Router1',40)
ssh = connectToInstance('Router2','SecondNetwork','ThirdNetwork')
installQuagga(ssh,'Router2')
configureOspf(ssh,'Router2',40)
ssh = connectToInstance('Router3','ThirdNetwork','FourthNetwork')
installQuagga(ssh,'Router3')
configureOspf(ssh,'Router3',40)

