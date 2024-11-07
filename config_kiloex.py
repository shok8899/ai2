import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
BASE = int(1e8)
BASE12 = int(1e12)
MARGIN_MIN = int(10)
LEVERAGE_MIN = int(2)

class KiloConfig:
    def __init__(self, chain='', chain_id=0, rpc='', wallet='', private_key='',
                 margin_contract='', market_contract='', market_trigger_contract='', 
                 order_book_contract='', vault_address='', view_address='', usdt_contract='',
                 execution_fee=0, gas=0):
        self.chain = chain
        self.chain_id = chain_id
        self.rpc = rpc
        self.wallet = wallet
        self.private_key = private_key
        self.margin_contract = margin_contract
        self.market_contract = market_contract
        self.market_trigger_contract = market_trigger_contract
        self.order_book_contract = order_book_contract
        self.vault_address = vault_address
        self.view_address = view_address
        self.usdt_contract = usdt_contract
        self.execution_fee = execution_fee
        self.gas = gas

    def __str__(self):
        return f"KiloConfig(chain={self.chain}, wallet={self.wallet}, chain_id={self.chain_id})"

# OPBNB Configuration
opbnb_config = KiloConfig(
    chain='OPBNB',
    chain_id=204,
    rpc='https://opbnb-mainnet-rpc.bnbchain.org',
    wallet=os.getenv('WALLET_ADDRESS'),
    private_key=os.getenv('PRIVATE_KEY'),
    margin_contract='0x19653dc8D30E39442B9cc96cb60d755E49A2717c',
    market_contract='0xa02d433868C7Ad58C8A2A820d6C3FF8a15536ACc',
    market_trigger_contract='0xe0eE1Cb99843c6dCdeb701707DaaDf9Ea8b752f7',
    order_book_contract='0x43E3E6FFb2E363E64cD480Cbb7cd0CF47bc6b477',
    vault_address='0xA2E2F3726DF754C1848C8fd1CbeA6aAFF84FC5B2',
    view_address='0x796f1793599D7b6acA6A87516546DdF8E5F3aA9d',
    usdt_contract='0x9e5AAC1Ba1a2e6aEd6b32689DFcF62A509Ca96f3',
    execution_fee=7000000000000,
    gas=500000
)

# Export configuration
kiloconfigs = {'OPBNB': opbnb_config}