#!/usr/bin/env python2.7
import paramiko
import os
import time
from neutronclient.v2_0 import client
from novaclient.v2.client import Client
from credentials import get_credentials
from credentials import get_nova_credentials
from configureHost import configureHost


nova_credentials = get_nova_credentials()
nova_client = Client(**nova_credentials)
configureHost(nova_client,'HostA','FirstNetwork','Router1')
configureHost(nova_client,'HostB', 'FourthNetwork', 'Router3')

