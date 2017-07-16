#!/usr/bin/env python2.7

import time
import paramiko
from credentials import get_credentials
from credentials import get_nova_credentials
from neutronclient.v2_0 import client
import novaclient.v2.client as nvclient
from convertToRouter import configureOspf



# Here we connect to the newly connected router and change its link weight
key = paramiko.RSAKey.from_private_key_file("./id_rsa")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
credentials = get_nova_credentials()
nova_client = nvclient.Client(**credentials)
instance = nova_client.servers.find(name='Router4')
server = nova_client.servers.get(instance)
if len(server.networks.get('SecondNetwork'))==1:
   public_ip=server.networks.get('ThirdNetwork')[1]
else:
   public_ip=server.networks.get('SecondNetwork')[1]
   print(public_ip)

ssh.connect(public_ip, username='ubuntu', pkey=key)
configureOspf(ssh,'Router4',20)

