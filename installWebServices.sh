#!/bin/bash
sudo apt-get update
sudo apt-get --assume-yes install apache2-utils
sudo apt-get --assume-yes install nginx
sudo service nginx stop
sudo apt-get --assume-yes install apache2
sudo service apache2 stop
sudo apt-get --assume-yes install lighttpd
sudo service lighttpd stop
