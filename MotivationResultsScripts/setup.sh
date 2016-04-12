
#Command to install iperf3
sudo apt-get -y update
sudo apt-get -y install software-properties-common
sudo add-apt-repository "ppa:patrickdk/general-lucid" -y
sudo apt-get -y update
sudo apt-get -y install iperf3

echo "Ensure the server is setup and run the python script to measure bandwidth"

#Command to run iperf script 
#python iperf_infinite_loop.py server_ip &

#Command to terminate iperf script
#killall python;killall iperf3

#Command to setup server
#iperf3 -s

