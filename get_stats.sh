#! /bin/sh
python3 ./eth_eventscanner.py https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161
python3 bsc_eventscanner.py https://bsc-dataseed.binance.org/
python3 eventanalyzer.py 

