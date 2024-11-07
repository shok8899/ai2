import os
from web3 import Web3
import market_trade_kiloex
import api_kiloex
from config import SYMBOL_TO_PRODUCT_ID, SLIPPAGE
import logging
from config_kiloex import kiloconfigs
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class TradeHandler:
    def __init__(self):
        self.config = kiloconfigs['OPBNB']
    
    def get_product_id(self, symbol):
        """Get product ID from symbol"""
        product_id = SYMBOL_TO_PRODUCT_ID.get(symbol.upper())
        if not product_id:
            raise ValueError(f"Unsupported symbol: {symbol}")
        return product_id
    
    def execute_trade(self, trade_data):
        """Execute market trade"""
        try:
            # Get product ID
            product_id = self.get_product_id(trade_data['symbol'])
            
            # Get current market price
            market_price = api_kiloex.index_price(product_id, 'OPBNB')
            logger.info(f"Current market price for {trade_data['symbol']}: {market_price}")
            
            # Trade parameters
            is_long = trade_data['side'].lower() == 'buy'
            leverage = float(trade_data['leverage'])
            margin = float(trade_data['margin'])
            
            # Set acceptable price with slippage
            acceptable_price = (
                market_price * (1 + SLIPPAGE) if is_long 
                else market_price * (1 - SLIPPAGE)
            )
            
            logger.info(f"Executing {'long' if is_long else 'short'} position: "
                       f"margin={margin}, leverage={leverage}, "
                       f"acceptable_price={acceptable_price}")
            
            # Execute market trade
            tx_hash = market_trade_kiloex.open_market_increase_position(
                config=self.config,
                product_id=product_id,
                margin=margin,
                leverage=leverage,
                is_long=is_long,
                acceptable_price=acceptable_price,
                referral_code=bytearray(32)
            )
            
            trade_result = {
                'tx_hash': tx_hash.hex(),
                'symbol': trade_data['symbol'],
                'side': 'LONG' if is_long else 'SHORT',
                'market_price': market_price,
                'acceptable_price': acceptable_price,
                'leverage': leverage,
                'margin': margin,
                'status': 'submitted'
            }
            
            logger.info(f"Trade submitted successfully: {trade_result}")
            return trade_result
            
        except Exception as e:
            logger.error(f"Error executing trade: {str(e)}", exc_info=True)
            raise