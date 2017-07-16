#! /bin/bash 


cd /
cd root
cd setup
source admin-openrc.sh

neutron router-interface-delete flat-lan-1-router flat-lan-1-subnet
neutron router-interface-delete tun0-router tun0-subnet

neutron net-delete flat-lan-1-net
neutron net-delete tun0-net

neutron router-delete flat-lan-1-router
neutron router-delete tun0-router


