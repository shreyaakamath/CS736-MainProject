#!/bin/bash
#./getData.sh small2 52.32.40.201 "ec2-52-32-40-201.us-west-2.compute.amazonaws.com" cs736_micro_iperf.pem
name=$1
server=$2
instance=$3
perm=$4
echo $name
echo $server
echo $instance
#server=54.186.41.160
#instance="ec2-54-186-41-160.us-west-2.compute.amazonaws.com"
#erm="ubuntu-common-2.pem"
ssh -i $perm $instance  -t "sudo service apache2 start"
start=10
for i in {1..100} 
do
	ab -n 10000 -c $start http://$server/ >> ${name}_apache2_c_${start}
	start=$(($start+10))
done
ssh -i $perm $instance  -t "sudo service apache2 stop"

ssh -i $perm $instance  -t "sudo service nginx start"
start=10
for i in {1..100} 
do
	ab -n 1000 -c $i http://$server/ >> ${name}_nginx_c_${start}
	start=$(($start+10))
done
ssh -i $perm $instance  -t "sudo service nginx stop"


ssh -i $perm $instance  -t "sudo /etc/init.d/lighttpd start"
start=10
for i in {1..100} 
do
	ab -n 1000 -c $i http://$server/ >> ${name}_lighttpd_c_${start}
	start=$(($start+10))
done
ssh -i $perm $instance  -t "sudo /etc/init.d/lighttpd stop"
