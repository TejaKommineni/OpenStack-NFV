#!/usr/bin/env python2.7

import time
import paramiko
from credentials import get_credentials
from credentials import get_nova_credentials
from neutronclient.v2_0 import client
import novaclient.v2.client as nvclient

# To connect to the virtual machines
def connectToInstance( instance_name, network_name, network2_name):
    credentials = get_credentials()
    neutron = client.Client(**credentials)
    credentials = get_nova_credentials()
    nova_client = nvclient.Client(**credentials)
    instance = nova_client.servers.find(name=instance_name)
    server = nova_client.servers.get(instance)
    if len(server.networks.get(network_name))==1:
      public_ip=server.networks.get(network2_name)[1] 
    else:
      public_ip=server.networks.get(network_name)[1]
    print(public_ip)
    #Providing private key to keystone to authenticate.
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file("./id_rsa")
    ssh.connect(public_ip, username='ubuntu', pkey=key)
    return ssh

#This function carries code for installing quagga on vms whicha re converted to routers
def installQuagga(ssh,instance_name):
    stdin, stdout, stderr = ssh.exec_command('sudo apt-get update')
    for line in stdout:
      	 print line.strip('\n')
    for line in stderr:
         print("Exceptions: ")
         print line.strip('\n')
    stdin, stdout, stderr = ssh.exec_command('sudo apt-get install -y quagga')
    for line in stdout:
         print line.strip('\n')
    for line in stderr:
         print("Exceptions: ")
         print line.strip('\n')
    stdin, stdout, stderr = ssh.exec_command('sudo apt-get install -y traceroute')
    for line in stdout:
        print line.strip('\n')
    for line in stderr:
        print("Exceptions: ")
        print line.strip('\n')
        #enable ip forwarding
    stdin, stdout, stderr = ssh.exec_command('echo 1 | sudo tee --append /proc/sys/net/ipv4/ip_forward')
    for line in stdout:
        print line.strip('\n')
    for line in stderr:
        print "Exceptions: "
        print line.strip('\n')
  
   # Initially I have used paramiko and tried to execute commands sequentially. But, I have seen inconsistency in data we are sending and that is being written. Hence executed everything in a single command.
   # stdin, stdout, stderr = ssh.exec_command('sudo rm /etc/quagga/daemons;')
   # stdin, stdout, stderr = ssh.exec_command('echo zebra=yes | sudo tee --append  /etc/quagga/daemons')
   # stdin, stdout, stderr = ssh.exec_command('echo bgpd=no | sudo tee --append  /etc/quagga/daemons')
   # stdin, stdout, stderr = ssh.exec_command('echo ospfd=yes | sudo tee --append  /etc/quagga/daemons')
   # stdin, stdout, stderr = ssh.exec_command('echo ospf6d=no | sudo tee --append  /etc/quagga/daemons')
   # stdin, stdout, stderr = ssh.exec_command('echo ripd=no | sudo tee --append  /etc/quagga/daemons')
   # stdin, stdout, stderr = ssh.exec_command('echo ripngd=no | sudo tee --append  /etc/quagga/daemons')

   #enable daemons
    stdin, stdout, stderr = ssh.exec_command('sudo rm /etc/quagga/daemons; echo zebra=yes | sudo tee --append /etc/quagga/daemons; echo bgpd=no | sudo tee --append /etc/quagga/daemons; echo ospfd=yes | sudo tee --append  /etc/quagga/daemons; echo ospf6d=no | sudo tee --append  /etc/quagga/daemons; echo ripd=no | sudo tee --append  /etc/quagga/daemons; echo ripngd=no | sudo tee --append  /etc/quagga/daemons')
    for line in stdout:
        print line.strip('\n')
    for line in stderr:
        print "Exceptions: "
        print line.strip('\n')
      


# After installing Quagga we call this function to give ospfd and zebra daemons the configuration information.  
def configureOspf(ssh, instance_name, cost):
    stdin, stdout, stderr = ssh.exec_command('sudo rm /etc/quagga/ospfd.conf')
    #configuring ospf
    #stdin, stdout, stderr = ssh.exec_command('echo '+ line + ' | sudo tee -a /etc/quagga/ospfd.conf')
    #stdin, stdout, stderr = ssh.exec_command('echo password zebra | sudo tee -a /etc/quagga/ospfd.conf')
    #stdin, stdout, stderr = ssh.exec_command('echo log file /var/log/quagga/quagga.log | sudo tee -a /etc/quagga/ospfd.conf')
    #stdin, stdout, stderr = ssh.exec_command('echo log stdout | sudo tee -a /etc/quagga/ospfd.conf')
    #stdin, stdout, stderr = ssh.exec_command('echo interface eth0 | sudo tee -a /etc/quagga/ospfd.conf')
    #stdin, stdout, stderr = ssh.exec_command('echo ' + costLine + ' | sudo tee -a /etc/quagga/ospfd.conf')
    #stdin, stdout, stderr = ssh.exec_command('echo interface eth1 | sudo tee -a /etc/quagga/ospfd.conf')
    #stdin, stdout, stderr = ssh.exec_command('echo ' + costLine + ' | sudo tee -a /etc/quagga/ospfd.conf')
    #stdin, stdout, stderr = ssh.exec_command('echo interface lo | sudo tee -a /etc/quagga/ospfd.conf')
    #stdin, stdout, stderr = ssh.exec_command('echo router ospf | sudo tee -a /etc/quagga/ospfd.conf')

    stdin, stdout, stderr = ssh.exec_command(unicode('echo hostname '+ instance_name + ' | sudo tee --append /etc/quagga/ospfd.conf; echo password zebra | sudo tee --append /etc/quagga/ospfd.conf; echo log file /var/log/quagga/quagga.log | sudo tee --append /etc/quagga/ospfd.conf; echo log stdout | sudo tee --append /etc/quagga/ospfd.conf; echo interface eth0 | sudo tee --append /etc/quagga/ospfd.conf; echo ip ospf cost ' + str(cost) + ' | sudo tee --append /etc/quagga/ospfd.conf; echo interface eth1 | sudo tee --append /etc/quagga/ospfd.conf;  echo ip ospf cost ' + str(cost) + ' | sudo tee --append /etc/quagga/ospfd.conf; echo interface lo | sudo tee --append /etc/quagga/ospfd.conf; echo router ospf | sudo tee --append /etc/quagga/ospfd.conf'))
    for line in stdout:
        print line.strip('\n')
    for line in stderr:
        print("Exceptions: ")
        print line.strip('\n')

    subnets = []
    credentials = get_nova_credentials()
    nova_client = nvclient.Client(**credentials)
    instance = nova_client.servers.find(name=instance_name)
    for network in instance.networks:
        ipaddress = instance.networks[network][0]
        index = ipaddress.rfind('.')
        subnets.append(unicode(ipaddress[0:index] + '.0/24'))
   
    #ospfd.conf
    for subnet in subnets:     
     stdin, stdout, stderr = ssh.exec_command('echo network ' + subnet + ' area 0.0.0.0  | sudo tee --append /etc/quagga/ospfd.conf')
     for line in stdout:
      print line.strip('\n')
     for line in stderr:
      print("Exceptions: ")
      print line.strip('\n')
     stdin, stdout, stderr = ssh.exec_command('echo line vty | sudo tee --append /etc/quagga/ospfd.conf')
       
    #zeba.conf
    stdin, stdout, stderr = ssh.exec_command('sudo rm /etc/quagga/zebra.conf')
    stdin, stdout, stderr = ssh.exec_command('echo hostname '+ instance_name + ' | sudo tee --append /etc/quagga/zebra.conf; echo password zebra | sudo tee --append /etc/quagga/zebra.conf; echo enable password zebra | sudo tee --append /etc/quagga/zebra.conf')
    for line in stdout:
     print line.strip('\n')
    for line in stderr:
     print line.strip('\n')

    #services start 
    stdin, stdout, stderr = ssh.exec_command('sudo chown quagga.quaggavty /etc/quagga/*.conf; sudo chmod 640 /etc/quagga/*.conf; sudo /etc/init.d/quagga stop; sudo /etc/init.d/quagga start')
    for line in stdout:
     print line.strip('\n')
    for line in stderr:
     print line.strip('\n')






