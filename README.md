# tokenbridge_stats
A simple tool for getting the usage stats of tokenbridge.cash based on Web3py.

Requirements:\
-Python 3\
-Web3py: pip3 install web3\
-TQDM: pip3 install tqdm

How to run it:\
$ chmod +x get_stats.sh\
$ ./get_stats.sh

The data is stored on a JSON file, one for every bridge (ETH bridge and BSC bridge). Eventanalyzer.py script prints a table with the assets moved each way.
