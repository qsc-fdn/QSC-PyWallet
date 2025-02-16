import os
from binascii import hexlify, a2b_base64
from collections import namedtuple
from decimal import Decimal
from random import seed
from typing import List

import grpc
import simplejson as json
from google.protobuf.json_format import MessageToJson
from pyqrllib.pyqrllib import mnemonic2bin, hstr2bin, bin2hstr

from qsc.core import config
from qsc.core.txs.SlaveTransaction import SlaveTransaction
from qsc.crypto.xmss import XMSS
from qsc.generated import qsc_pb2_grpc, qsc_pb2
from qsc.crypto.doctest_data import *

from models.model import Model

def slave_tx_generate(xmss_pk, src_xmss, xmss):
    """
    Generates Slave Transaction for the wallet
    """
    access_types = []
    fee_shor = 0 #100000
    master_addr = None

    slave_xmss = []
    slave_pks = []
    slave_xmss_seed = []

    for i in range(1):
        print("Generating Slave #" + str(i + 1))
        xmss = XMSS.from_height(config.dev.xmss_tree_height)
        slave_xmss.append(xmss)
        slave_xmss_seed.append(xmss.extended_seed)
        slave_pks.append(xmss.pk)
        access_types.append(0)
        print("Successfully Generated Slave %s/%s" % (str(i + 1), 100))

    try:
        tx = SlaveTransaction.create(slave_pks = slave_pks,
                                    access_types = access_types,
                                    fee = fee_shor,
                                    xmss_pk = src_xmss.pk,
                                    master_addr = master_addr)
        
        ots_indx = int(Model.getAddressOtsKeyIndex(src_xmss.qaddress, 'main'))
        print(f'-> OTS index: {ots_indx}')
        src_xmss.set_ots_index(ots_indx)
        tx.sign(src_xmss)
        if not tx.validate(True):
            raise Exception("Invalid Transaction")

        node_public_address = '127.0.0.1:19009' #get_node_IP() 
        print(f"Sending Tx to a QSC Node: {node_public_address} ...")
        channel = grpc.insecure_channel(node_public_address)
        stub = qsc_pb2_grpc.PublicAPIStub(channel)
        push_transaction_req = qsc_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
        push_transaction_resp = stub.PushTransaction(push_transaction_req, timeout=5)

        if push_transaction_resp.error_code != qsc_pb2.PushTransactionResp.SUBMITTED:
            raise Exception(push_transaction_resp.error_description)

        print(f'tx_hash: {bin2hstr(tx.txhash)}')

        '''
        with open('slaves.json', 'w') as f:
            json.dump([bin2hstr(src_xmss.address), slave_xmss_seed, tx.to_json()], f)
        print('Successfully created slaves.json')
        print('Move slaves.json file from current directory to the mining node inside ~/.qrl/')
        '''

    except Exception as e:
        print("Unhandled error: {}".format(str(e)))
        quit(1)