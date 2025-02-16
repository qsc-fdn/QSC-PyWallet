import requests
import json
from pyqrllib.pyqrllib import XmssFast, mnemonic2bin, hstr2bin, getRandomSeed, bin2hstr

from qsc.crypto.xmss import XMSS


def getBlockExplorerURL(network):
    return 'http://127.0.0.1:3000/api'
    #return f'https://{network}explorer.theqrl.org/api'

class Model:

    def __init__(self):
        pass
        
    def getAddress(xmss_height, xmss_hash):
        seed = getRandomSeed(48, '')
        xmss = XMSS(XmssFast(seed, xmss_height, xmss_hash))
        return xmss.qaddress, xmss.mnemonic, xmss.hexseed

    def getAddressExperimental(xmss_height, xmss_hash, mouse_seed):
        xmss = XMSS(XmssFast(mouse_seed, xmss_height, xmss_hash))
        return xmss.qaddress, xmss.mnemonic, xmss.hexseed

    def recoverAddressHexseed(seed):
        bin_seed = hstr2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        return recovered_xmss.qaddress

    def recoverAddressMnemonic(seed):
        bin_seed = mnemonic2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        return recovered_xmss.qaddress

    def getHexSeedMnemonic(mnemonic):
        bin_seed = mnemonic2bin(mnemonic)
        return bin2hstr(bin_seed)
   

    def recoverMnemonicHexseed(seed):
        bin_seed = hstr2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        return recovered_xmss.mnemonic

    def recoverHexseedMnemonic(seed):
        bin_seed = mnemonic2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        return recovered_xmss.hexseed

    def getOTSNumbers(hex_seed):
        bin_seed = hstr2bin(hex_seed)
        xmss = XMSS.from_extended_seed(bin_seed)
        return xmss.number_signatures
    
    def getOTSIndex(signatures): # NOTE: if lots of Txs, could slow?
        max_ots_indx = 0
        for signature in signatures:
            if signature is not None:
                ots_indx = int.from_bytes(signature[:3], "big")
                if ots_indx > max_ots_indx:
                    max_ots_indx = ots_indx
        return max_ots_indx + 1



                
    
    def getAddressBalance(address, network):
        url = getBlockExplorerURL(network) #'http://127.0.0.1:3000/api' #f'https://{network}explorer.theqrl.org/api' 
        address = address.replace('q', 'Q', 1)
        request = requests.get(url +'/a/'+address)
        response = request.text
        getAddressResp = json.loads(response)
        jsonResponse = getAddressResp
        return jsonResponse["state"]["balance"]

    def getAddressOtsKeyIndex(address, network):
        url = getBlockExplorerURL(network) #'http://127.0.0.1:3000/api' #f'https://{network}explorer.theqrl.org/api'
        address = address.replace('q', 'Q', 1)
        request = requests.get( url +'/a/'+address)
        response = request.text
        print(f'-> address: {address}, reponse: {response}')
        getAddressResp = json.loads(response)
        jsonResponse = getAddressResp
        return jsonResponse["state"]["used_ots_key_count"]

    
    def getTransactionByHash(tx_hash, network):
        url = getBlockExplorerURL(network) #'http://127.0.0.1:3000/api' #f'https://{network}explorer.theqrl.org/api' 
        request = requests.get(url + '/tx/'+tx_hash)
        response = request.text
        getTXResp = json.loads(response)
        jsonResponse = getTXResp
        return(jsonResponse)

    


# getting timestamp from transaction hash
# print(Model.getTransactionByHash("992ac5dfdedf7259fed52ce406e961556796fc238ab79cb43331655b670b627a")["transaction"]["header"]["timestamp_seconds"])

# #getting amount from transaction hash
# print(Model.getTransactionByHash("357db33e4fc2944fe6bb3bc630a710df7e107e8394fa154196a6ce7db705e786")["transaction"]["tx"]["amount"])

# #check if it comes from own address or not (+ or -)
# print(Model.getTransactionByHash("0c95416023f147bb7447a0160285cc4ae5f1a1dc02d3b97e528f04577cacfd24")["transaction"]["explorer"]["from_hex"])
