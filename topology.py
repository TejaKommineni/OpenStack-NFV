#!/usr/bin/env python2.7
import time
from credentials import get_credentials
from credentials import get_nova_credentials
from neutronclient.v2_0 import client
import novaclient.v2.client as nvclient

#create Network
def createNetwork(network_name, subnet_name, cidr):
    credentials = get_credentials()
    neutron = client.Client(**credentials)
    try:
     body_sample = {'network': {'name': network_name,
                   'admin_state_up': True}}

     netw = neutron.create_network(body=body_sample)
     net_dict = netw['network']
     network_id = net_dict['id']
     print('Network %s created' % network_id)
     body_create_subnet = {'subnets': [{'cidr': cidr,
                          'ip_version': 4,'name':subnet_name,'network_id': network_id}]}

     subnet = neutron.create_subnet(body=body_create_subnet)
     print('Created subnet %s' % subnet)
    finally:
     print("Execution completed")

#create virtual machine
def createInstance(instance_name, key_name, image_name, first_network, second_network):
    credentials = get_nova_credentials()
    nova_client = nvclient.Client(**credentials)
    try:
     image = nova_client.images.find(name=image_name)
     flavor = nova_client.flavors.find(name="m1.tiny")

     if not second_network:
      net = nova_client.networks.find(label=first_network)
      nics = [{'net-id': net.id}]
     else: 
      fnet = nova_client.networks.find(label=first_network)
      snet = nova_client.networks.find(label=second_network)
      nics = [{'net-id': fnet.id},{'net-id': snet.id}]

     instance = nova_client.servers.create(name=instance_name, image=image,
                                      flavor=flavor, key_name=key_name, nics=nics)
     print("Sleeping for 5s after create command")
     time.sleep(10)
     print("List of VMs")
     print(nova_client.servers.list())
    finally:
     print("Execution Completed")

#create router
def createRouter():
    credentials = get_nova_credentials()
    nova_client = nvclient.Client(**credentials)
    net = nova_client.networks.find(label="ext-net")
    try:
     credentials = get_credentials()
     neutron = client.Client(**credentials)
     neutron.format = 'json'
     request = {'router': {'name': 'External Router',
                          'admin_state_up': True, 'external_gateway_info':{'network_id':net.id}}}
     router = neutron.create_router(request)
     router_id = router['router']['id']
     
     router = neutron.show_router(router_id)
     print(router)

     addInterface(neutron,router_id,'FirstSubnet')
     addInterface(neutron,router_id,'SecondSubnet')
     addInterface(neutron,router_id,'ThirdSubnet')
     addInterface(neutron,router_id,'FourthSubnet')
    finally:
     print("created router")

# add interface to router
def addInterface(neutron,router_id,network_name):
    credentials = get_nova_credentials()
    nova_client = nvclient.Client(**credentials)
    subnets = neutron.list_subnets(name=network_name)
    subnet_id = subnets['subnets'][0]['id']
    print(subnet_id)    
    router_interface = {'subnet_id':subnet_id}
    neutron.add_interface_router(router_id, router_interface)

# assign floating ip to the virtual machines
def assignFloatingIP(instance_name):
    credentials = get_nova_credentials()
    nova_client = nvclient.Client(**credentials) 
    nova_client.floating_ip_pools.list()
    floating_ip = nova_client.floating_ips.create(nova_client.floating_ip_pools.list()[0].name)
    print("Floating IP is ", floating_ip)
    instance = nova_client.servers.find(name=instance_name)
    instance.add_floating_ip(floating_ip)



