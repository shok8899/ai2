import logging
from web3 import Web3
from config_kiloex import BASE, BASE12, kiloconfigs
import time
import usdt_kiloex
import api_kiloex

with open('./abi/PositionRouter.abi', 'r') as f:
    abi = f.read()

def open_market_increase_position(config, product_id, margin, leverage, is_long, acceptable_price, referral_code):
    """
    Open a market increase position.
    """
    try:
        # Automatically authorize USDT limit
        usdt_kiloex.approve_usdt_allowance(config, config.market_contract, margin)

        w3 = Web3(Web3.HTTPProvider(config.rpc))
        nonce = w3.eth.get_transaction_count(config.wallet)
        gas_price = w3.eth.gas_price
        execution_fee = config.execution_fee

        tx = {
            'from': config.wallet,
            'nonce': nonce,
            'gas': config.gas,
            'gasPrice': gas_price,
            'value': execution_fee,
            'chainId': config.chain_id
        }

        trade_contract_w3 = w3.eth.contract(address=config.market_contract, abi=abi)
        txn = trade_contract_w3.functions.createIncreasePosition(
            product_id, 
            int(margin * BASE), 
            int(leverage * BASE), 
            is_long, 
            int(acceptable_price * BASE),
            execution_fee, 
            referral_code
        ).build_transaction(tx)

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=config.private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        logging.info(f"Market increase position tx_hash: {tx_hash.hex()}")
        return tx_hash

    except Exception as e:
        logging.error(f'Market increase position error: {str(e)}')
        raise