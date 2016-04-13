#!/bin/bash
server=54.191.81.2
instance=ubuntu@ec2-54-218-59-225.us-west-2.compute.amazonaws.com
perm="ubuntu-common-2.pem"
ssh -i $perm $instance  -t "sudo service apache2 start"
for j in 1 2 3
do
				for i in 10 20 30 40 50 60 70 80 90 100
				do
								ab -n 100 -c $i http://$server/ >> tiny3_apache2_c_${j}_${i}
				done
done
ssh -i $perm $instance  -t "sudo service apache2 stop"

ssh -i $perm $instance  -t "sudo service nginx start"
for j in 1 2 3
do
				for i in 10 20 30 40 50 60 70 80 90 100
				do
								ab -n 100 -c $i http://$server/ >> tiny3_nginx_c_${j}_${i}
				done
done
ssh -i $perm $instance  -t "sudo service nginx stop"


ssh -i $perm $instance  -t "sudo /etc/init.d/lighttpd start"
for j in 1 2 3
do
				for i in 10 20 30 40 50 60 70 80 90 100
				do
								ab -n 100 -c $i http://$server/ >> tiny3_lighttpd_c_${j}_${i}
				done
done
ssh -i $perm $instance  -t "sudo /etc/init.d/lighttpd stop"
