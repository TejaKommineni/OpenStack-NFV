#!/usr/bin/env python2.7

import paramiko
import os
import time
from neutronclient.v2_0 import client
from novaclient.v2.client import Client
from credentials import get_credentials
from credentials import get_nova_credentials


# After changing the weights we delete the old router
nova_credentials = get_nova_credentials()
nova_client = Client(**nova_credentials)
instance = nova_client.servers.find(name='Router2')
nova_client.servers.delete(instance)


