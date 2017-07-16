#!/usr/bin/env python2.7
import paramiko
import os
import time
from neutronclient.v2_0 import client
from novaclient.v2.client import Client
from credentials import get_credentials
from credentials import get_nova_credentials


#To obtain floating IP of an instance
def findFloatingIP(server):
    for network in server.networks:
        if len(server.networks[network]) > 1:
           return server.networks[network][1]

#returns IP Address of a VM instance in a particular network address
def findIPAddrInNetwork(nova_client, server, netName):
        return server.networks[netName][0]

#Returns first subnet a VM instance was connected to.
def findSubnet(nova_client, server):
        for network in server.networks:
                ipaddr = server.networks[network][0]
                index = ipaddr.rfind('.')
                return unicode (ipaddr[0:index] + '.0/24')

#Configuring Host
def configureHost(nova_client, instance_name, hostNet, gateway_name):
        instance = nova_client.servers.find(name=instance_name)
        gateway = nova_client.servers.find(name=gateway_name)
        #setup ssh connection
        paramiko.util.log_to_file('ssh.log') 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print "tryng to ssh to ", instance_name
        key = paramiko.RSAKey.from_private_key_file("./id_rsa")
        ssh.connect(findFloatingIP(instance), username='ubuntu', pkey=key)
        subnetHost = findSubnet(nova_client, instance)
        gateWayIP = findIPAddrInNetwork(nova_client,gateway, hostNet)
        publicIP = findFloatingIP(instance)
        trimmed_publicIP = publicIP[0:publicIP.rfind('.')]
        trimmed_publicIP = trimmed_publicIP[0:trimmed_publicIP.rfind('.')]
        print "Trying to execute following commands on ", instance_name
        for subnet in subnets['subnets']:
            trimmed_subnet = subnet['cidr'][0:subnet['cidr'].rfind('.')]
            trimmed_subnet =  trimmed_subnet[0:trimmed_subnet.rfind('.')]
            if subnet['cidr'] != subnetHost and trimmed_subnet != trimmed_publicIP:
                        #print "other subnets are ", subnet['cidr']
                print 'route add -net ' + subnet['cidr'] + ' gw ' + gateWayIP
                stdin, stdout, stderr = ssh.exec_command('sudo route add -net ' + subnet['cidr'] + ' gw ' + gateWayIP)

                for line in stdout:
                    print line.strip('\n')
                    print "Errors: "
                for line in stderr:
                    print line.strip('\n')
        ssh.close()


credentials = get_credentials()
neutron = client.Client(**credentials)
nova_credentials = get_nova_credentials()
nova_client = Client(**nova_credentials)
neutron.format = 'json'

subnets = neutron.list_subnets()

                                                               
