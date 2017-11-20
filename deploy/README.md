Setting up a stand-alone spark cluster on OpenStack
===================================================

This describes how to deploy OpenStack Tempest+Rallistart using two [ansible](http://www.ansible.com) 
playbooks. This has been tested on the [FIWARE Lab](https://cloud.lab.fiware.org) 
cloud.

It will install OpenStack Tempest+Ralli, and start the required service. 
Any pull requests to improve upon this to bring it closer to a production ready 
state are very much appreciated.

The OpenStack dynamic inventory code presented here is taken from the repository 
https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/openstack.py

How to start it?
-----------------
- Create virtualenv and activate it:
```
virtualenv -p python2.7 $NAME_VIRTUAL_ENV
source $NAME_VIRTUAL_ENV/bin/activate
```
- Install the pre-requisites:
```
pip install -r requirements.txt
```
- Put the correct path to your '/env/bin/python' into the localhost_inventory file.
- Download you OpenStack RC file from the OpenStack dashboard (it's available under 
"info" option on the top left of the FIWARE Lab Cloud Portal). Please, do not forget 
to fill in with your password.
```
export OS_REGION_NAME=xxxxxx
export OS_USERNAME=xxxxx
export OS_PASSWORD=xxxxxx
export OS_AUTH_URL=http://130.206.84.8:4730/v3/
export OS_TENANT_NAME=xxxxxxx
```
- You have to add the following to your .openrc file
```
export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default
export OS_IDENTITY_API_VERSION=3
```
- [OPTIONAL] I suggest to add the following line to it.
```
export PS1='(`basename \"$VIRTUAL_ENV`)[\u@FIWARE Lab \W(keystone_user)]\$ '
```
- Source your OpenStack RC file: `source <path to rc file>`. This will load information 
about you OpenStack Setup into your environment.
- Create the security group for spark. Since spark will start some services on random 
ports this will allow all tcp traffic within the security group:
```
openstack security group create <YOUR SEC. GROUP NAME> --description "internal security group for Tempest+Ralli"
openstack security group rule create <YOUR SEC. GROUP NAME> --protocol tcp --dst-port 22
openstack security group rule create <YOUR SEC. GROUP NAME> --protocol tcp --dst-port 80
```
- Create a keypair to be used in your instances:
```
openstack keypair create <NAME OF THE KEY PAIR> > <YOUR SSH KEY>
```
- Change permissions to the ssh key file:
```
chmod 400 <YOUR SSH KEY>
```
- Edit the setup variables to fit your setup. Open `vars/main.yml` and setup the 
variables as explained there.
- One all the variables are in place you should now be able to create your instances:
```
ansible-playbook -i localhost_inventory --private-key=<YOUR SSH KEY> create_tempest-ralli_cloud_playbook.yml
```
- Then install tempest+ralli on the node (I have noticed that sometimes it takes a while 
for the ssh-server on the nodes to start, therefore if you get an initial ssh-error, 
wait a few minutes and try again).
```
ansible-playbook -i openstack_inventory.py --user=ubuntu --private-key=<YOUR SSH KEY>  deploy_tempest-ralli_playbook.yml
```
- Once this has finished successfully your OpenStack Tempest+Ralli server is installed and configured 
to connect to the FIWARE Lab node. Now you're ready to enter into it and start checking the sanity
status of your node. 

```
Installation of Rally is done!

Rally is now installed in your system. Information about your Rally
installation:

  * Method: system
  * Database at: /var/lib/rally/database
  * Configuration file at: /etc/rally
  * Samples at: /usr/share/rally/samples
```
