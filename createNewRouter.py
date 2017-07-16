#!/usr/bin/env python2.7

import time
import paramiko
from credentials import get_credentials
from credentials import get_nova_credentials
from neutronclient.v2_0 import client
import novaclient.v2.client as nvclient
from topology import createInstance
from topology import assignFloatingIP
from convertToRouter import connectToInstance
from convertToRouter import installQuagga
from convertToRouter import configureOspf


#Code to create new router
createInstance('Router4','cheetos','trusty-server-multi-nic','SecondNetwork','ThirdNetwork')
credentials = get_credentials()
neutron = client.Client(**credentials)
routers= neutron.list_routers()
print((routers.get('routers')[0]).get('id'))
assignFloatingIP('Router4')
ssh = connectToInstance('Router4','SecondNetwork','ThirdNetwork')
installQuagga(ssh,'Router4')
configureOspf(ssh,'Router4',40)



