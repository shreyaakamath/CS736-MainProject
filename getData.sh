#!/bin/bash
sudo service nginx start
for j in 1 2 3
do
				for i in 10 20 30 40 50 60 70 80 90 100
				do
								ab -n 100 -c $i http://localhost/ >> nginx_c_${j}_${i}
				done
done
sudo service nginx stop

sudo service apache2 start
for j in 1 2 3
do
				for i in 10 20 30 40 50 60 70 80 90 100
				do
								ab -n 100 -c $i http://localhost/ >> apache2_c_${j}_${i}
				done
done
sudo service apache2 stop

sudo /etc/init.d/lighttpd start
for j in 1 2 3
do
				for i in 10 20 30 40 50 60 70 80 90 100
				do
								ab -n 100 -c $i http://localhost/ >> lighttpd_c_${j}_${i}
				done
done
sudo /etc/init.d/lighttpd stop

