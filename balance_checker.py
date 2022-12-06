from web3 import Web3
import json
import configparser
from termcolor import colored, cprint

config = configparser.ConfigParser()
config.read('balance_checker.ini')
rpc_nodes = {
    'Ethereum ' : 'https://rpc.ankr.com/eth',
    'Arbitrum ' : 'https://rpc.ankr.com/arbitrum',
    'Optimism ' : 'https://1rpc.io/op',
    'BSC      ' : 'https://rpc-bsc.bnb48.club',
    'Polygon  ' : 'https://polygon-rpc.com',
    'Avalanche' : 'https://avalanche-evm.publicnode.com'
}
eth_list = ['Ethereum ', 'Arbitrum ', 'Optimism ', 'Avalanche']
bsc = ['BSC      ']
polygon = ['Polygon  ']
config['token']['token_abi_USDC_Avalanche']
stables = {
    'USDT Ethereum' : [config['token']['token_address_USDT_Ethereum'] ,  config['token']['token_abi_USDT_Ethereum']],
    'USDC Ethereum' : [config['token']['token_address_USDC_Ethereum'] ,  config['token']['token_abi_USDC_Ethereum']],

    'USDT Arbitrum' : [config['token']['token_address_USDT_Arbitrum'] ,  config['token']['token_abi_USDT_Arbitrum']],
    'USDC Arbitrum' : [config['token']['token_address_USDC_Arbitrum'] ,  config['token']['token_abi_USDC_Arbitrum']],

    'USDT Optimism' : [config['token']['token_address_USDT_Optimism'] ,  config['token']['token_abi_USDT_Optimis']],
    'USDC Optimism' : [config['token']['token_address_USDC_Optimism'] ,  config['token']['token_abi_USDC_Optimis']],

    'USDT BSC' : [config['token']['token_address_USDT_BSC'] ,  config['token']['token_abi_USDT_BSC']],
    'USDC BSC' : [config['token']['token_address_USDC_BSC'] ,  config['token']['token_abi_USDC_BSC']],
    'BUSD BSC' : [config['token']['token_address_BUSD_BSC'] ,  config['token']['token_abi_BUSD_BSC']],

    'USDT Polygon' : [config['token']['token_address_USDT_Polygon'] ,  config['token']['token_abi_USDT_Polygon']],
    'USDC Polygon' : [config['token']['token_address_USDC_Polygon'] ,  config['token']['token_abi_USDC_Polygon']],

    'USDT Avalanche' : [config['token']['token_address_USDT_Avalanche'] ,  config['token']['token_abi_USDT_Avalanche']],
    'USDC Avalanche' : [config['token']['token_address_USDC_Avalanche'] ,  config['token']['token_abi_USDC_Avalanche']],
}

usdt = 0
usdc = 0
busd = 0
eth = 0
bnb = 0
matic = 0
accounts = eval(config.get("accounts", "addresses"), {}, {})

if __name__ == "__main__":
    for each_acc in accounts:
        cprint("Account: " + each_acc, 'magenta', attrs=["bold"])
        for key, value in rpc_nodes.items():
            web3 = Web3(Web3.HTTPProvider(value))
            balance_wei_arbitrum = web3.eth.getBalance(each_acc)
            
            balance_arbitrum = web3.fromWei(balance_wei_arbitrum, 'ether')
            print(f"\t{key} balance is: " + str(balance_arbitrum))

            if (key in eth_list):
                eth += balance_arbitrum
            elif (key in bsc):
                bnb += balance_arbitrum
            else:
                matic += balance_arbitrum

            usdt_stable = stables.get('USDT ' + key.strip())
            token = web3.eth.contract(address = usdt_stable[0], abi = json.loads(usdt_stable[1]))
            token_balance_wei = token.functions.balanceOf(each_acc).call()
            if key.strip() == "BSC":
                token_balance = web3.fromWei(token_balance_wei, 'ether')
                token_busd = web3.eth.contract(address = config['token']['token_address_BUSD_BSC'], abi = json.loads(config['token']['token_abi_BUSD_BSC']))
                token_balance_wei_busd = token_busd.functions.balanceOf(each_acc).call()
                busd_count = web3.fromWei(token_balance_wei_busd, 'ether')
                busd += busd_count
                print("\t\tBUSD balance is: " + str(busd_count))
                
            else:
                token_balance = web3.fromWei(token_balance_wei, 'mwei')
            print("\t\tUSDT balance is: " + str(token_balance))
            usdt += token_balance

            usdc_stable = stables.get('USDC ' + key.strip())
            token = web3.eth.contract(address = usdc_stable[0], abi = json.loads(usdc_stable[1]))
            token_balance_wei = token.functions.balanceOf(each_acc).call()
            if key.strip() == "BSC":
                token_balance = web3.fromWei(token_balance_wei, 'ether')
            else:
                token_balance = web3.fromWei(token_balance_wei, 'mwei') 
            print("\t\tUSDC balance is: " + str(token_balance))
            usdc += token_balance
cprint("           Total balance:                             ", 'grey', 'on_green', attrs=["bold"])
cprint("Total ETH: " + f"{eth:,}", 'grey', attrs=["bold"])
cprint("Total BNB: " + f"{bnb:,}", 'yellow', attrs=["bold"])
cprint("Total Matic: " + f"{matic:,}", 'magenta', attrs=["bold"])
cprint("Total USDT: " + f"{usdt:,}", 'green', attrs=["bold"])
cprint("Total USDC: " + f"{usdc:,}", 'green', attrs=["bold"])
cprint("Total BUSD: " + f"{busd:,}", 'yellow', attrs=["bold"])





