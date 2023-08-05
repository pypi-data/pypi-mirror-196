#!/usr/bin/env python3
import argparse
import json
import os
import pprint
import time
import uuid

import dotenv
import requests
import web3
from eth_typing import HexStr
from web3.contract import Contract
from web3.exceptions import TransactionNotFound
from web3.middleware import geth_poa_middleware
from web3.types import RPCResponse

import secure_web3.lib.style
from secure_web3.lib import abi_lib, inputs
from secure_web3.lib.w3_validation import validate_addr, valid_token
from secure_web3.lib.wallet_manager import WalletManager


class SecureWeb3:
    def __init__(self, wallet_file: str = None, network: str = 'ethereum'):
        dotenv.load_dotenv()
        self.endpoint = None
        self.token_abi = None
        self.account = None
        self.wallet = None
        self.flashbots_endpoint = None
        self.tokens = []
        self.printer = secure_web3.lib.style.PrettyText(0)
        self.wallet_file = wallet_file
        self.network = network
        self.w3 = self.setup_w3()
        self.eth_price = 0
        self._session = requests.Session()

    def setup_w3(self) -> web3.Web3:
        self.flashbots_endpoint = os.environ.get(f'flashbots_{self.network}_endpoint')
        w3_endpoint = os.environ.get(f'{self.network}_http_endpoint')
        if self.flashbots_endpoint:
            self.printer.normal('Flashbots RPC available')
            w3_endpoint = self.flashbots_endpoint
        self.w3 = web3.Web3(web3.HTTPProvider(w3_endpoint))
        if self.w3.isConnected:
            self.printer.good(f"Connected to chain: {self.w3.eth.chain_id}")
        else:
            self.printer.error(f'Web3 could connect to remote endpoint: {w3_endpoint}')
        if self.network == 'ethereum':
            self.token_abi = secure_web3.lib.abi_lib.EIP20_ABI
        elif self.network == 'polygon':
            self.token_abi = secure_web3.lib.abi_lib.EIP20_ABI
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        elif self.network == 'bsc':
            self.token_abi = secure_web3.lib.abi_lib.BEP_ABI
            # self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            self.endpoint = 'https://bsc.api.0x.org/'
            self.printer.warning('Connected to BSC, which has not been tested very well yet.')
        elif self.network == 'aurora':
            self.token_abi = secure_web3.lib.abi_lib.EIP20_ABI

        self.printer.good(f'Web3 connected to chain: {self.w3.eth.chain_id}')
        return self.w3

    def load_wallet(self) -> bool:
        if not self.wallet_file:
            self.wallet_file = os.environ.get('default_wallet_location')
        self.wallet = WalletManager(self.wallet_file)
        # w.setup_wizard()
        denc, conf = self.wallet.decrypt_load_wallet()
        # print(conf)
        self.account = web3.Account.from_key(denc)
        tokens = conf.get('tokens')
        if tokens is None:
            self.tokens = []
        else:
            self.tokens = tokens
        if self.account:
            # overwrite in memory
            # w = uuid.uuid4().hex
            denc = uuid.uuid4().hex
            # del w
            del denc
            return True
        return False

    def configure_wallet(self) -> None:
        w = WalletManager(self.wallet_file)
        w.setup_wizard()
        w = uuid.uuid4().hex
        del w

    @property
    def web3(self) -> web3.Web3:
        return self.w3

    def query_eth_price(self) -> None:
        if self.w3.eth.chain_id == 0 or self.w3.eth.chain_id == 5:
            s, r = self._session.get(
                url=f'https://api.etherscan.io/api?module=stats&action=ethprice&apikey='
                    f'{os.environ.get("etherscan_api_key")}')
            eth_price = json.loads(json.dumps(r))
            self.eth_price = eth_price.get('result').get('ethusd')
        elif self.w3.eth.chain_id == 56:
            s, r = self._session.get(
                f'https://api.bscscan.com/api?module=stats&action=bnbprice&apikey='
                f'{os.environ.get("bscan_api_key")}')
            eth_price = json.loads(json.dumps(r))
            self.eth_price = eth_price.get('result').get('ethusd')
        elif self.w3.eth.chain_id == 137:
            r = requests.get(
                'https://api.polygonscan.com/' + 'api' +
                f'?module=stats&action=maticprice&apikey={os.environ.get("polygonscan_api_key")}')
            r = r.json()
            eth_price = json.loads(json.dumps(r))
            self.eth_price = eth_price.get('result').get('maticusd')

    def query_gas_api(self) -> (int, int):
        """curl -H 'Authorization: f5534c3e-c1e0-477d-9978-412b9a1276a6'
        'https://api.blocknative.com/gasprices/blockprices?chainid=137'"""
        if self.w3.eth.chain_id == 5:
            chainId = 1
        else:
            chainId = self.w3.eth.chain_id
        ret = self._session.get('https://api.blocknative.com/gasprices/blockprices',
                                params={'chainid': chainId},
                                headers={'Authorization': os.environ.get('blocknative_api_key')})
        if ret.status_code == 200:
            ret = ret.json()
        max_priority_fee_per_gas = ret.get('blockPrices')[0].get('estimatedPrices')[0].get(
            'maxPriorityFeePerGas')
        max_fee_per_gas = ret.get('blockPrices')[0].get('estimatedPrices')[0].get('maxFeePerGas')
        return max_priority_fee_per_gas, max_fee_per_gas

    def switch_network(self, network_name: str, poa: bool = False) -> None:
        """
        Switch network of w3 connections
        :param network_name:
        :param poa: load point of authority middleware for networks like polygon
        """
        endpoint = os.environ.get(f'infura_{network_name}_endpoint')
        if not endpoint:
            self.printer.error('Could not find network, is it configured?')
            return
        w3 = web3.Web3(web3.HTTPProvider(endpoint))
        if network_name == 'polygon':
            poa = True
        if poa:
            w3.middleware_onion.inject(geth_poa_middleware)
        if w3.isConnected():
            self.printer.good(f'Successfully switched to {network_name}')
        else:
            self.printer.error(f'Web3 could not connect to endpoint at {endpoint}')


class EtherShellWallet:
    def __init__(self, sw3: SecureWeb3):
        self.sw3 = sw3
        self._balance = 0

    def build_private_tx(self, tx: dict):
        block = self.sw3.w3.eth.get_block_number() + 1
        _tx = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_sendPrivateTransaction",
            "params": [{"tx": tx, "maxBlockNumber": block}]}
        return _tx

    def broadcast_raw_tx(self, tx: dict, private: bool = False) -> (HexStr, RPCResponse):
        """
        Send a raw transaction to the rpc for broadcast
        :param tx: Signed Transaction
        :param private: send via private transaction method
        :return: transaction hash
        """
        tx['nonce'] = self.sw3.w3.eth.get_transaction_count(sw3.account.address)
        self.sw3.printer.normal(f'Loaded TX:\n{tx}')
        sign = input('Broadcast? y/n >> ')
        if sign.lower() in ['yes', 'y']:
            signed_tx = self.sw3.account.sign_transaction(tx)
            if private:

                payload = self.build_private_tx(tx)

                headers = {
                    "accept": "application/json",
                    "content-type": "application/json"
                }

                response = requests.post(self.sw3.flashbots_endpoint, json=payload, headers=headers)
                resp = response.json()
                print(response.status_code, resp)
                return resp.get('result').get('bundleHash')
            return web3.Web3.toHex(self.sw3.w3.eth.send_raw_transaction(signed_tx.rawTransaction))

    def _token(self, token_address: str) -> Contract:
        """
        Create and return a Contract object with the ERC/BEP/20 abi
        :param token_address: contract address string
        :return: Contract object
        """
        if self.sw3.w3.eth.chain_id == 56:
            token = self.sw3.w3.eth.contract(self.sw3.w3.toChecksumAddress(token_address), abi=lib.abi_lib.BEP_ABI)
        else:
            token = self.sw3.w3.eth.contract(self.sw3.w3.toChecksumAddress(token_address), abi=lib.abi_lib.EIP20_ABI)
        return token

    def eth_balance(self, raw: bool = False) -> (int, float):
        """

        :param raw: if true return raw integer
        :return:
        """
        self._balance = sw3.w3.eth.getBalance(sw3.account.address)
        if raw:
            return self._balance
        return self._balance / (10 ** 18)

    def token_convert(self, token_address: str, qty: int) -> float:
        for token in self.sw3.tokens:
            if self.sw3.w3.toChecksumAddress(token_address) == self.sw3.w3.toChecksumAddress(token.get("address")):
                dec = token.get('decimals')
                return int(qty / (10 ** dec))

    def token_balance(self, token_address: str, raw: bool = False) -> (int, float):
        token = self._token(token_address)
        token_balance = token.functions.balanceOf(self.sw3.account.address).call()
        if raw:
            return token_balance
        for tok in self.sw3.tokens:
            if self.sw3.w3.toChecksumAddress(tok.get('address')) == self.sw3.w3.toChecksumAddress(token_address):
                dec = int(tok.get('decimals'))
                return token_balance / (10 ** dec)

    def poll_receipt(self, tx_hash: hex):
        poll = 0
        while True:
            if poll > 100:
                break
            poll += 1
            self.sw3.printer.normal(f'Polling for receipt: {poll}/100 ... ')
            try:
                receipt = self.sw3.w3.eth.get_transaction_receipt(tx_hash)
            except web3.exceptions.TransactionNotFound:
                # await asyncio.sleep(1)
                time.sleep(1)
            else:
                receipt = receipt.__dict__
                return receipt
        self.sw3.printer.error('Timed out, transaction may be underpriced!')

    def send_erc20_token(self, raw_amount: int, destination: str, token_address: str, legacy: bool = False,
                         private: bool = False) -> HexStr:
        token = self.sw3.w3.eth.contract(self.sw3.w3.toChecksumAddress(token_address), abi=lib.abi_lib.EIP20_ABI)
        mpfpg, mfpg = self.sw3.query_gas_api()
        if self.sw3.w3.eth.chain_id in [0, 1, 5, 137]:
            tx = {
                'maxPriorityFeePerGas': self.sw3.w3.toWei(mpfpg, 'gwei'),
                'maxFeePerGas': self.sw3.w3.toWei(mfpg, 'gwei'),
                "to": self.sw3.w3.toChecksumAddress(destination),
                "value": "0x0",
                "data": token.encodeABI('transfer', args=(self.sw3.w3.toChecksumAddress(destination), raw_amount)),
                "nonce": self.sw3.w3.eth.get_transaction_count(self.sw3.account.address),
                "chainId": self.sw3.w3.eth.chain_id
            }
            if legacy:
                tx.pop('maxFeePerGas')
                tx.pop('maxPriorityFeePerGas')
                tx.pop('type')
                tx.update({'gasPrice': self.sw3.w3.toWei(int(self.sw3.w3.eth.gas_price * 1.1), 'gwei')})

            gas = self.sw3.w3.eth.estimate_gas(tx)
            tx.update({'gas': gas})
            return self.broadcast_raw_tx(tx, private)

    def send_eth(self, raw_amount: int, destination: str, legacy: bool = False, private: bool = False) -> HexStr:
        mpfpg, mfpg = self.sw3.query_gas_api()

        tx = {
            'nonce': self.sw3.w3.eth.get_transaction_count(self.sw3.account.address),
            'to': self.sw3.w3.toChecksumAddress(destination),
            'value': raw_amount,
            'maxFeePerGas': self.sw3.w3.toWei(mfpg, 'gwei'),
            'maxPriorityFeePerGas': self.sw3.w3.toWei(mpfpg, 'gwei'),
            'type': 2,
            'chainId': hex(self.sw3.w3.eth.chain_id)
        }
        if legacy:
            tx.pop('maxFeePerGas')
            tx.pop('maxPriorityFeePerGas')
            tx.pop('type')
            tx.update({'gasPrice': self.sw3.w3.toWei(int(self.sw3.w3.eth.gas_price * 1.1), 'gwei')})
        gas = self.sw3.w3.eth.estimate_gas(tx)
        tx.update({'gas': gas})
        return self.broadcast_raw_tx(tx, private)

    def import_token(self, token_address: str) -> bool:
        if not validate_addr(token_address):
            return False
        if not valid_token(self._token(token_address)):
            return False
        token = self._token(token_address)
        decimals = token.functions.decimals().call()
        symbol = token.functions.symbol().call()
        balance = token.functions.balanceOf(self.sw3.account.address).call()
        token_dict = {'address': self.sw3.w3.toChecksumAddress(token_address),
                      'network': self.sw3.w3.eth.chain_id,
                      'decimals': decimals,
                      'symbol': symbol,
                      'balance': balance}
        self.sw3.tokens.append(token_dict)
        self.sw3.wallet.wallet.update_wallet('tokens', self.sw3.tokens)
        return True

    def interactive(self, action: str = 'send', _type: str = 'eth', legacy: bool = False, private: bool = False):
        # print(action, _type, legacy)
        if action == 'send':
            balance = self.eth_balance()
            self.sw3.printer.normal(f'Launching interactive wallet shell.\n')
            self.sw3.printer.good(f'Account Balance: {balance} ')
            destination = secure_web3.lib.inputs.get_dest_addr()
            if self.sw3.w3.eth.getCode(destination):
                self.sw3.printer.warning('Warning! This is a contract address!')
            if _type == 'eth':
                while True:
                    amount = input("Amount in ether >> ")
                    amount = float(amount)
                    if float(amount):
                        if amount <= balance:
                            break
                        else:
                            self.sw3.printer.error(f'Amount exceeds current wallet balance: {balance}')
                self.sw3.printer.normal(f'Transaction parameters: \nSend {amount} to {destination}')
                if secure_web3.lib.inputs.confirmation():
                    amount = amount * (10 ** 18)
                    txid = self.send_eth(int(amount), destination, legacy, private)
                    self.sw3.printer.good(f'TXID: {txid}')
                    receipt = self.poll_receipt(txid)
                    if receipt:
                        pprint.pprint(receipt)
            if _type == 'erc20':
                self.sw3.printer.normal('Select a token to send: ')
                while True:
                    for x, token in enumerate(self.sw3.tokens):
                        addr = token.get('address')
                        token_balance = self.token_convert(addr, token.get('balance'))
                        addr = addr[:4] + '..' + addr[-4:]
                        print(f'[{x}], {token.get("symbol")}@{addr}, Balance: {token_balance} (local)')
                    selection = input('Selection # >> ')
                    if int(selection) <= int(len(self.sw3.tokens) - 1):
                        token = self.sw3.tokens[int(selection)]
                        symbol = token.get('symbol')
                        token_address = token.get('address')
                        token_short_addr = token_address[:4] + '..' + token_address[-4:]
                        token_balance = self.token_balance(token_address)
                        self.sw3.printer.normal(f'Balance: {token_balance} (live)')
                        break
                while True:
                    amount = input(f"Amount in {symbol} >> ")
                    amount = float(amount)
                    if float(amount):
                        if amount <= token_balance:
                            break
                        else:
                            self.sw3.printer.error(f'Amount exceeds current wallet balance: {token_balance}')
                qty = int(amount * (10 ** int(token.get('decimals'))))
                if balance <= 0:
                    self.sw3.printer.error('Not enough ETH to pay for gas!')
                    return False
                self.sw3.printer.normal(f'Transaction parameters: \nSend {amount} of {symbol} @{token_short_addr} '
                                        f'to {destination}')
                if secure_web3.lib.inputs.confirmation():
                    txid = self.send_erc20_token(qty, destination, token.get('address'), legacy, private)
                    if txid:
                        receipt = self.poll_receipt(txid)
                        pprint.pprint(receipt)


if __name__ == '__main__':
    args = argparse.ArgumentParser('Secure Web3 Cli')
    general_opts = args.add_argument_group(description='Wallet managment options.')
    general_opts.add_argument('-i', '--init', dest='init_wallet', type=str, nargs=1,
                              default=None, help='Initialize this new wallet')
    general_opts.add_argument('-o', '--open', dest='open_wallet', type=str, default=None,
                              nargs='?', help='Unlock a wallet, use default wallet if not specified.')
    general_opts.add_argument('-l', '--lock', dest='lock_wallet', action='store_true',
                              help='Lock all open wallets.')
    general_opts.add_argument('-n', '--network', type=str, default='ethereum',
                              choices=['ethereum', 'polygon', 'bsc', 'aurora', 'goerli'])
    config_options = args.add_argument_group(description='Wallet configuration options and functions')
    config_options.add_argument('-it', '--import-token', dest='import_token', type=str,
                                default=None, help='Add this token to the specified wallet.')
    read_opts = args.add_argument_group(description='EVM State-Reading functions.')
    read_opts.add_argument('-b', '--balance', action='store_true', help='Get wallet balance info.')
    tx_options = args.add_argument_group(description='EVM State-Writing related options.')
    tx_options.add_argument('-r', '--raw', dest='broadcast_raw', type=str, help='Load a json tx from '
                                                                                'this file to sign and broadcast.')
    tx_options.add_argument('-s', '--send', choices=['eth', 'erc20'], default=None,
                            help='Open interactive shell to send ethereum.')
    tx_options.add_argument('-p', '--private', dest='use_private_tx', action='store_true',
                            help='Submit transaction private via flashbots (if available).')

    tx_options.add_argument('-L', '--legacy', action='store_true', default=False, help='Use legacy gas protocol.')

    args = args.parse_args()
    dotenv.load_dotenv()

    if args.init_wallet:
        print(f'[+] Configuring new wallet "{args.init_wallet[0]}" ... ')
        manager = WalletManager(args.init_wallet[0])
        manager.setup_wizard()
        exit(0)
    if not args.open_wallet:
        wallet_file = os.environ.get('default_wallet_location')
    else:
        wallet_file = args.open_wallet
    sw3 = SecureWeb3(wallet_file, args.network)
    sw3.printer.normal(f'Opening wallet "{wallet_file}" ... ')
    sw3.load_wallet()
    wallet = EtherShellWallet(sw3)
    if args.import_token:
        wallet.import_token(args.import_token)
    if args.balance:
        ether_balance = wallet.eth_balance()
        sw3.printer.normal(f'Ethereum Balance: {ether_balance}')
    if args.broadcast_raw:
        with open(args.broadcast_raw, 'r') as f:
            tx = json.load(fp=f)
        txid = wallet.broadcast_raw_tx(tx, private=args.private)
        sw3.printer.normal(f'TXID: {txid}')
        wallet.poll_receipt(txid)
    if args.send:
        wallet.interactive(action='send', _type=args.send, legacy=args.legacy, private=args.use_private_tx)
