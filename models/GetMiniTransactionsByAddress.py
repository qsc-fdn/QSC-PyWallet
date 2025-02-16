# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import heapq
from os import stat
from grpc import ServicerContext, StatusCode
from pyqrllib.pyqrllib import str2bin, hstr2bin, bin2hstr


from qsc.generated import qsc_pb2_grpc, qsc_pb2
import grpc
import base64
import walletApp

from models.utils import get_node_IP, get_qaddress, CONNECTION_TIMEOUT


##########################################################################



##########################################################################

class TableOutput:
    pass

    def getMiniTransactionsByAddressHashes(qrl_address, network):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = get_node_IP(network) #network + '-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qsc_pb2_grpc.PublicAPIStub(channel)

        request = qsc_pb2.GetMiniTransactionsByAddressReq(address=binary_qrl_address,
                                                              item_per_page=100000,
                                                              page_number=1)
        response = stub.GetMiniTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        transaction_hashes = []
        for i in range(len(response.mini_transactions)):
            transaction_hashes.append(response.mini_transactions[i].transaction_hash)
        return transaction_hashes

    def getMiniTransactionsByAddressAmount(qrl_address, network):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = get_node_IP(network) #network + '-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qsc_pb2_grpc.PublicAPIStub(channel)

        request = qsc_pb2.GetMiniTransactionsByAddressReq(address=binary_qrl_address,
                                                              item_per_page=100000,
                                                              page_number=1)
        response = stub.GetMiniTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        amount = []
        for i in range(len(response.mini_transactions)):
            amount.append(response.mini_transactions[i].amount)
        return amount
            

    def GetTransactionsByAddressAddrFrom(qrl_address, network):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = get_node_IP(network) #network + '-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qsc_pb2_grpc.PublicAPIStub(channel)

        request = qsc_pb2.GetTransactionsByAddressReq(address=binary_qrl_address,
                                                    item_per_page=1000000,
                                                    page_number=1)
        response = stub.GetTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        addr_from = []
        for i in range(len(response.transactions_detail)):
            addr_from.append("Q" + bin2hstr(response.transactions_detail[i].addr_from))
        return addr_from

    def getBalance(qrl_address, network):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = get_node_IP(network) #network + '-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qsc_pb2_grpc.PublicAPIStub(channel)

        request = qsc_pb2.GetBalanceReq(address=binary_qrl_address)
        response = stub.GetBalance(request, timeout=CONNECTION_TIMEOUT)
        return response.balance

    def getOTSIndex(qrl_address, network): # not working?
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = get_node_IP(network) #network + '-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qsc_pb2_grpc.PublicAPIStub(channel)

        request = qsc_pb2.GetOTSReq(address=binary_qrl_address, unused_ots_index_from=0, page_from=0, page_count=2**20)
        response = stub.GetOTS(request)
        #print(f'->OTS index response: {response.ots_bitfield_by_page}, {response.unused_ots_index_found}, {response.next_unused_ots_index}')
        return response.next_unused_ots_index

    def getTx(tx_hash, network):
        node_public_address = get_node_IP(network) #network + '-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qsc_pb2_grpc.PublicAPIStub(channel)

        txhash = bytes(hstr2bin(tx_hash))
        response = stub.GetTransaction(qsc_pb2.GetTransactionReq(tx_hash=txhash))
        block_header_hash = None
        if response.block_header_hash:
            block_header_hash = bin2hstr(response.block_header_hash)
        return response.tx, response.confirmations, response.block_number, block_header_hash


    def GetTransactionsByAddressAmounts(qrl_address, network):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = get_node_IP(network) #network + '-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qsc_pb2_grpc.PublicAPIStub(channel)

        request = qsc_pb2.GetTransactionsByAddressReq(address=binary_qrl_address,
                                                    item_per_page=1000000,
                                                    page_number=1)
        response = stub.GetTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        print(f'-> response: {response}')

        amount = []
        addrs_to = []
        test = []
        amount_length_data = []
        length_list = []
        mined_data = []
        for i in range(len(response.transactions_detail)):
            amount_length_data.append(response.transactions_detail[i].tx.transfer.amounts)
            for addrs in response.transactions_detail[i].tx.transfer.addrs_to:
                addrs_to.append("Q"+ bin2hstr(addrs))
            if response.transactions_detail[i].tx.transfer.amounts:
                for address, amounts in zip(response.transactions_detail[i].tx.transfer.addrs_to, response.transactions_detail[i].tx.transfer.amounts):
                    if qrl_address != "q" + bin2hstr(bytes(address)):
                        test.append("-" + str(amounts / 1000000000))
                    elif qrl_address == "q" + bin2hstr(bytes(address)):
                        test.append("+" + str(amounts / 1000000000))
            elif response.transactions_detail[i].tx.coinbase:#  for mining
                mined_data.append(response.transactions_detail[i].tx.coinbase.amount) 
                address, amounts = response.transactions_detail[i].tx.coinbase.addr_to, response.transactions_detail[i].tx.coinbase.amount
                print(f'-> mining address: {bin2hstr(bytes(address))}, amount: {amounts}')
                print(f'-> address: {qrl_address}')
                if qrl_address != "q" + bin2hstr(bytes(address)):
                    test.append("-" + str(amounts / 1000000000))
                elif qrl_address == "q" + bin2hstr(bytes(address)):
                    test.append("+" + str(amounts / 1000000000))
                
            elif response.transactions_detail[i].tx.transfer_token.amounts:
                amount.append(str(response.transactions_detail[i].tx.transfer_token.amounts[0] / 10000000000) + " " + "Tokens")
            elif response.transactions_detail[i].tx.message.message_hash:
                amount.append("message")
            else:
                for addressAmount in response.transactions_detail[i].tx.token.initial_balances:
                    amount.append("+" + str(addressAmount.amount / 10000000000) + " " + response.transactions_detail[i].tx.token.symbol.decode("utf-8"))

        print(f'-> test: {test}')
        out = test
        '''
        for brackets in amount_length_data:
            length_list.append(len(brackets))
        start=0
        for step in length_list:
            end = start+step
            l = list(map(float, test[start:end]))
            if len(set(i < 0 for i in l)) > 1:
                l = [i for i in l if i>0]
            s = sum(l)
            out.append('%s%.2f' % ('+' if s >=0 else '' , s))
            start = end
        x = 0
        print(f'-> out: {out}')
        for index, item in enumerate(out):
            if item == "+0.00":
                try:
                    out[index] = amount[x]
                except:
                    out[index] = amount[x - 1]
                x += 1
        '''
        return out



    def GetTxHistoryByAddress(qrl_address, network):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = get_node_IP(network) #network + '-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qsc_pb2_grpc.PublicAPIStub(channel)
        request = qsc_pb2.GetTransactionsByAddressReq(address=binary_qrl_address, item_per_page=1000000, page_number=1)
        response = stub.GetTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        print(f'-> Tx response: {response}')

        tx_histories = []
        for i in range(len(response.transactions_detail)):
            tx_data = response.transactions_detail[i]
            addr_from = get_qaddress(tx_data.addr_from)
            timestamp = tx_data.timestamp
            if tx_data.tx:
                #print(f'-> tx: {tx_data.tx.transfer}, {tx_data.tx.coinbase}')
                if tx_data.tx.transfer:
                    transfer = tx_data.tx.transfer
                    amounts, fees, signatures = [], [], []
                    for address_to, amount in zip(transfer.addrs_to, transfer.amounts):
                        #print(f'-> address_to={address_to}, amount={amount}')
                        if addr_from == qrl_address and qrl_address != get_qaddress(address_to):
                            str_amount = "-" + str(amount / 1000000000)
                            fees.append(tx_data.tx.fee / 1000000000)
                            signatures.append(tx_data.tx.signature)
                            amounts.append(str_amount)
                        elif addr_from != qrl_address and qrl_address == get_qaddress(address_to):
                            str_amount = "+" + str(amount / 1000000000)
                            amounts.append(str_amount)
                            fees.append(0)
                            signatures.append(None)
                    for amount, fee, signature in zip(amounts, fees, signatures):
                        tx_histories.append([addr_from, timestamp, amount, fee, signature])
                if tx_data.tx.coinbase:
                    addr_to = get_qaddress(tx_data.tx.coinbase.addr_to)
                    #print(f'-> addr_to={addr_to}, wallet address: {qrl_address}')
                    if addr_to == qrl_address:
                        str_amount = "+" + str(tx_data.tx.coinbase.amount / 1000000000)
                        tx_histories.append([addr_from, timestamp, str_amount, 0, None])
                        

        return tx_histories

# print(TableOutput.GetTransactionsByAddressAmounts("Q010400b49d2ebb003d69db2a66cc179a87592649d9b83cfb32a1200f72dbc62b4aa4903b4dd322"))
# print(TableOutput.GetTransactionsByAddressAmounts("Q010400b49d2ebb003d69db2a66cc179a87592649d9b83cfb32a1200f72dbc62b4aa4903b4dd322"))

# Q0105006e70719c46cc85a69d6b7d0a1e642968d5c996fd9fa4b6641337f13ba2213749fd19dd11