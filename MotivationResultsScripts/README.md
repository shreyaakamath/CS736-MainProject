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
<b>Command to run the n-queens benchmark: </b>python nqueen_infinite_loop.py <i>binary_file</i> <i>board_size</i> &
<b>Command to run the iperf3 benchmark: </b>python iperf_infinite_loop.py <i>server_ip</i> &  

## Note
<b> To stop either of the benchmarks: </b> killall python; killalliperf3
<b> Before launching the iperf3 benchmark, ensure that the server is running iperf3: </b> iperf3 -s