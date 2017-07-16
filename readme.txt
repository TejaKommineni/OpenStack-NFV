// Name : Teja Kommineni
// uid : u1072593
// cade id : tkommineni

Steps to execute :

1) Change the url and version in admin-openrc.sh file from version 3 to version 2.0
   The changed values look like this 
   OS_AUTH_URL = http://ctl:35357/v2.0
   OS_IDENTITY_API_VERSION =2.0
2) Source the admin-openrc.sh file using command source /root/setup/admin-openrc.sh
3) Execute File step1.sh
4) Execute step2.sh ; Sometimes it is throwing an error that the floating point ips cannot be alloacted from ext net pool. For, this issue we have to login to horizon and associate floating ips.
4) Execute File step3.sh 
5) Execute File step4.sh 
6) Execute File step5.sh ; one problem common with step3.sh,step4.sh and step5.sh is the public ip's are not working properly. At, times we are not able to login into the vms.The only round about for this is to disassociate ips and then connect them to another interface. I have shown the steps in the readme.png
7) Execute File step6.sh
8) Execute File step7.sh
