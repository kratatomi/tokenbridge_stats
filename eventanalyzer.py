import json
import pprint #For printing results in a more readable way
 
#Tokens on the ETH/SBCH bridge, listing names and decimals 
ETH_bridge_tokens =  {"0x46520D0244bdEa36899a5b96bDFe10880575a91E": ["WBTC",  18],  
"0x68E91EF42816efaDD23Ac94011b7bD00C25082aA": ["WETH",  18], 
"0x1a5b299991664a89a212bE0D54bBc79C4E565C58": ["AAVE",  18], 
"0x3743eC0673453E5009310C727Ba4eaF7b3a1cc04": ["WBCH",  18], 
"0x028E845DCBae941E4b595E17c23e511E399A986A": ["LINK",  18], 
"0xa951e029317ef95F455316c1687b5022Bad77E98": ["UNI",  18],
"0xAa2a50312F280baBC3D2B3c8e0e21D776dEa6DbD": ["SUSHI",  18], 
"0xf79C9E2621e8712E00004e7821ff03b8727c85bA": ["USDT",  18], 
"0xa7190fE70411B595cc82BE3748e437Cc2e63Cf3B": ["DAI",  18], 
"0x30da472c030Fa63c806954639C20ADc743E3273f": ["USDC",  18],  
"0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599": ["WBTC",  8], 
"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": ["ETH",  18], 
"0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9": ["AAVE",  18], 
"0x5a5893F8B5Dd6057e8ef659fD40e204993812f17": ["WBCH",  18], 
"0x514910771AF9Ca656af840dff83E8264EcF986CA": ["LINK",  18], 
"0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984": ["UNI",  18], 
"0x6B3595068778DD592e39A122f4f5a5cF09C90fE2": ["SUSHI",  18], 
"0xdAC17F958D2ee523a2206206994597C13D831ec7": ["USDT",  6], 
"0x6B175474E89094C44Da98b954EedeAC495271d0F": ["DAI",  18], 
"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": ["USDC",  6], 
"foreign_chain": "Ethereum"}

BSC_bridge_tokens = {
"0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c": ["WBNB",  18], 
"0xC7cb02462E4F65C7f570C2E13b0B1FB8a2EFAA9c": ["WBCH",  18], 
"0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82": ["CAKE",  18], 
"0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56": ["BUSD",  18], 
"0x5831C7823AbaF0A325627da7638ACcBe959e249B": ["WBNB",  18], 
"0x3743eC0673453E5009310C727Ba4eaF7b3a1cc04": ["WBCH",  18], 
"0x530676d60c1a865BF5793cc58fC97688847C61FD": ["CAKE",  18], 
"0x64ca4917Fb219EaCf15560Aa8F82B3Bc78ABdd50": ["BUSD",  18], 
"foreign_chain": "BSC"}



def statistics(data,  token_list):
    #"Cross" are swaps to SBCH, "AcceptedCrossTransfer" from SBCH
    results = {"Cross": {},  "AcceptedCrossTransfer": {}}
    for block_number in data["blocks"]:
        for txhash in data["blocks"][block_number]:
            for tx in data["blocks"][block_number][txhash]: 
                if tx == "Cross":
                    token_address = data["blocks"][block_number][txhash][tx]["tokenAddress"]
                    if token_list[token_address][0] in results["Cross"]:
                        results["Cross"][token_list[token_address][0]]["Amount"] += data["blocks"][block_number][txhash][tx]["amount"] * 10**-token_list[token_address][1]
                        results["Cross"][token_list[token_address][0]]["No. of txs"] += 1
                    else:
                        results["Cross"][token_list[token_address][0]] = {"Amount": [], "No. of txs": []}
                        results["Cross"][token_list[token_address][0]]["Amount"] = data["blocks"][block_number][txhash][tx]["amount"] * 10**-token_list[token_address][1]
                        results["Cross"][token_list[token_address][0]]["No. of txs"] = 1
                if tx == "AcceptedCrossTransfer":
                    token_address = data["blocks"][block_number][txhash][tx]["originalTokenAddress"]
                    #Always 18 decimals for SmartBCH tokens
                    if token_list[token_address][0] in results["AcceptedCrossTransfer"]:
                        results["AcceptedCrossTransfer"][token_list[token_address][0]]["Amount"] += data["blocks"][block_number][txhash][tx]["amount"] * 10**-18
                        results["AcceptedCrossTransfer"][token_list[token_address][0]]["No. of txs"] += 1
                    else:
                        results["AcceptedCrossTransfer"][token_list[token_address][0]] = {"Amount": [], "No. of txs": []}
                        results["AcceptedCrossTransfer"][token_list[token_address][0]]["Amount"] = data["blocks"][block_number][txhash][tx]["amount"] * 10**-18
                        results["AcceptedCrossTransfer"][token_list[token_address][0]]["No. of txs"] = 1
    print("These are the tokens moved from {} to SmartBCH:\n".format(token_list["foreign_chain"]))
    pprint.pprint(results["Cross"])
    print("\n")
    print("These are the tokens moved from SmartBCH to {}:\n".format(token_list["foreign_chain"]))
    pprint.pprint(results["AcceptedCrossTransfer"])
    print("\n")

try :
    file = open("ETH_tokenbridge_events.json", )
    ETH_data = json.load(file)
    statistics(ETH_data,  ETH_bridge_tokens)
except FileNotFoundError:
    print("File with ETH bridge events doesn't exist")
                    
try :
    file = open("BSC_tokenbridge_events.json", )
    BSC_data = json.load(file)
    statistics(BSC_data,  BSC_bridge_tokens)
except FileNotFoundError:
    print("File with BSC bridge events doesn't exist")


