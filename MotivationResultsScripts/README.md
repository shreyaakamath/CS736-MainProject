# MotivationalResultsScripts
Folder consists of scripts to get motivational results

## Requirements
Python 2.7

## Important Scripts
* <b>setup.sh</b>: Script that install all the iperf3 dependencies on Ubuntu 14.04 
* <b>iperf_infinite_runner.py</b>: Script that run iperf3 in an infinite loop
* <b>nqueen_infinite_loop.py</b>: Script that run nqueens in an infinite loop 
* <b>n-queen.o</b>: Binary file of the nqueens program to be run 

## Usage
* <b>Command to run the n-queens benchmark: </b>python nqueen_infinite_loop.py <i>binary_file</i> <i>board_size</i> &
* <b>Command to run the iperf3 benchmark: </b>python iperf_infinite_loop.py <i>server_ip</i> &  

## Note
* <b> To stop either of the benchmarks: </b> killall python; killall iperf3
* <b> Before launching the iperf3 benchmark, ensure that the server is running iperf3: </b> iperf3 -s

## Steps to run on AWS instance
* <b> Create and Launch instance: </b> Follow steps outlined in url http://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/EC2_GetStarted.html#ec2-launch-instance_linux
* <b> Store the key pair in a location </b>
* <b> Move scripts to instance: </b> scp -i /path/cs736_micro_nqueens_1.pem nqueen_infinite_loop.py n-queen.o ubuntu@<publicDNS name>:/home/ubuntu/scripts/
