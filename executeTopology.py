#!/usr/bin/env python2.7
import time
from credentials import get_credentials
from credentials import get_nova_credentials
from neutronclient.v2_0 import client
import novaclient.v2.client as nvclient
from topology import createInstance
from topology import createNetwork
from topology import createRouter
from topology import assignFloatingIP



#To develop initial topology
credentials = get_nova_credentials()
nova_client = nvclient.Client(**credentials)
f=open('id_rsa.pub','r')
publickey = f.readline()[:-1]
keypair = nova_client.keypairs.create('cheetos',publickey)
f.close()
createNetwork('FirstNetwork','FirstSubnet','192.168.0.0/24')
createNetwork('SecondNetwork','SecondSubnet','192.167.0.0/24')
createNetwork('ThirdNetwork','ThirdSubnet','192.166.0.0/24')
createNetwork('FourthNetwork','FourthSubnet','192.165.0.0/24')
createInstance('HostA',keypair.name,'trusty-server','FirstNetwork','')
createInstance('Router1',keypair.name,'trusty-server-multi-nic','FirstNetwork','SecondNetwork')
createInstance('Router2',keypair.name,'trusty-server-multi-nic','SecondNetwork','ThirdNetwork')
createInstance('Router3',keypair.name,'trusty-server-multi-nic','ThirdNetwork','FourthNetwork')
createInstance('HostB',keypair.name,'trusty-server','FourthNetwork','')

createRouter()

assignFloatingIP('HostA')
assignFloatingIP('Router1')
assignFloatingIP('Router2')
assignFloatingIP('Router3')
assignFloatingIP('HostB')

