import os
from binascii import hexlify, a2b_base64
from collections import namedtuple
from decimal import Decimal
from typing import List

import grpc
import simplejson as json
from google.protobuf.json_format import MessageToJson
from pyqrllib.pyqrllib import mnemonic2bin, hstr2bin, bin2hstr


from qsc.core.txs.TransferTransaction import TransferTransaction
from qsc.generated import qsc_pb2_grpc, qsc_pb2
import walletApp

from models.utils import get_node_IP, CONNECTION_TIMEOUT


##################################################################################################################

def tx_unbase64(tx_json_str):
    tx_json = json.loads(tx_json_str)
    tx_json["publicKey"] = base64tohex(tx_json["publicKey"])
    tx_json["signature"] = base64tohex(tx_json["signature"])
    tx_json["transactionHash"] = base64tohex(tx_json["transactionHash"])
    tx_json["transfer"]["addrsTo"] = [base64tohex(v) for v in tx_json["transfer"]["addrsTo"]]
    return json.dumps(tx_json, indent=True, sort_keys=True)

def base64tohex(data):
    return hexlify(a2b_base64(data))


def tx_transfer(addrs_to, amounts, message_data, fee, xmss_pk, src_xmss, ots_key, network):
    # Create transaction
    master_addr = None 
    bytes_addrs_to = []
    addrs_to_recipients = (' '.join(i for i in bytes_addrs_to))
    if len(addrs_to) > 1:
        for i in addrs_to:
            bytes_addrs_to.append(bytes(hstr2bin(i)))
    elif len(addrs_to) == 1:
        bytes_addrs_to.append(bytes(hstr2bin(addrs_to[0])))

    shor_amounts = [int(float(str(i) + "e9")) for i in amounts]
    print(f'-> address to: {addrs_to}')
    print(f'-> amount: {shor_amounts}')
    amounts_recipients = (" ".join(i for i in list(map(str, shor_amounts))))
    #print(bytes_addrs_to)

    tx = TransferTransaction.create(addrs_to = bytes_addrs_to,
                                        amounts = shor_amounts,
                                        message_data = message_data,
                                        fee = fee,
                                        xmss_pk= xmss_pk,
                                        master_addr=master_addr)

    print(f'-> message: {message_data}')
    print(f'-> xmss_pk: {xmss_pk}')
    print(f'-> data: {tx.get_data_hash()}')

    # Sign transaction
    src_xmss.set_ots_index(ots_key)
    tx.sign(src_xmss)
    print(f'-> signature(1)={tx.signature}')

    # Print result
    txjson = tx_unbase64(tx.to_json())
    print(txjson)

    #print(f'xmss PK: {xmss_pk}')
    #print(f'tx pk: {tx.PK}')
    print(f'data hash: {bin2hstr(tx.get_data_hash())}')
    print(f'signature(2): {bin2hstr(tx.signature)}')
    print(f'PK: {bin2hstr(tx.PK)}')

    print(f'-> to validate Tx ...')
    if not tx.validate():
        print("Failed to validate the signature!")
        return None

    print("\nTransaction Blob (signed): \n")
    txblob = tx.pbdata.SerializeToString()
    txblobhex = hexlify(txblob).decode()
    print(txblobhex)

    # Push transaction
    node_public_address = get_node_IP(None) 
    print(f"Sending to a QSC Node: {node_public_address} ...")
    channel = grpc.insecure_channel(node_public_address)
    stub = qsc_pb2_grpc.PublicAPIStub(channel)
    push_transaction_req = qsc_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
    push_transaction_resp = stub.PushTransaction(push_transaction_req, timeout=CONNECTION_TIMEOUT)

    # Print result
    if push_transaction_resp.error_code != qsc_pb2.PushTransactionResp.SUBMITTED:
        print('->Tx Submission Failed, Response Code: %s, error description: %s', push_transaction_resp.error_code, push_transaction_resp.error_description)
        return None

    hxTxHash = bin2hstr(tx.txhash)
    print(f'tx_hash: {hxTxHash}')

    return hxTxHash
