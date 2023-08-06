import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from web3.contract import Contract
from typing import List, Dict, Tuple
from typing import Optional
from web3r.utils import Utils
from web3 import Web3
from etherscan import Etherscan
from web3r.datatypes.token import Token
from web3r.exeptions import ZeroAddressError
from web3r.the_graph_uniswapV3 import TheGraphUniswapV3

UNISWAP_V2_FACTORY_ABI = [
    {
        "constant": True,
        "inputs": [
            {
                "name": "tokenA",
                "type": "address"
            },
            {
                "name": "tokenB",
                "type": "address"
            }
        ],
        "name": "getPair",
        "outputs": [
            {
                "name": "pair",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]
UNISWAP_V2_PAIR_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "getReserves",
        "outputs": [
            {"internalType": "uint112", "name": "_reserve0", "type": "uint112"},
            {"internalType": "uint112", "name": "_reserve1", "type": "uint112"},
            {"internalType": "uint32", "name": "_blockTimestampLast", "type": "uint32"}
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "token0",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "token1",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]
UNISWAP_V2_FACTORY_CONTRACT_ADDRESS = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f' 

class UniswapV2:
    def __init__(self, web3: Web3, etherscan: Etherscan, utils: Utils, grph_uniV3: TheGraphUniswapV3 ):
        """Initializes the UniswapV2Utilities class.

        Inherits from the ERC20 class and sets up the Uniswap V2 Factory contract.
        
        Args:
            provider_url (str): The URL of the Ethereum provider.
        """
        self.etherscan = etherscan
        self.web3 = web3
        self.utils = utils
        self.grph_uniV3 = grph_uniV3

        self.v2_factory_contract = self.web3.eth.contract(address=self.web3.to_checksum_address(UNISWAP_V2_FACTORY_CONTRACT_ADDRESS), abi=UNISWAP_V2_FACTORY_ABI) 

    def get_uniswap_v2_pair_address(self, tokenA: Token, tokenB: Token) -> Optional[str]:
        """Fetches the address of the Uniswap V2 Pair for the given tokens.

        Args:
            tokenA (str): The address of token A.
            tokenB (str): The address of token B.

        Returns:
            The address of the Uniswap V2 Pair or None if an error occurred.
        """
        try:
            v2_pair_address = self.web3.to_checksum_address(self.v2_factory_contract.functions.getPair(tokenA.address, tokenB.address).call())
            if v2_pair_address == '0x0000000000000000000000000000000000000000':
                raise ZeroAddressError(v2_pair_address)
            else:
                return v2_pair_address
        except ZeroAddressError as ze:
            logger.error(f"No Uniswap V2 Pair Address: {str(ze)}")
            return None
        except Exception as e:
            logger.error(f"Failed to get Pair address: {str(e)}")
            raise Exception

    def get_uniswap_v2_pair(self, v2_pair_address: str) -> Optional[Contract]:
        """Gets the Uniswap V2 Pair contract based on the pair address.

        Args:
            v2_pair_address (str): The address of the Uniswap V2 Pair.

        Returns:
            The Uniswap V2 Pair contract or None if an error occurred.
        """
        try:
            v2_pair = self.web3.eth.contract(address=self.web3.to_checksum_address(v2_pair_address), abi=UNISWAP_V2_PAIR_ABI) 
            return v2_pair
        except Exception as e:
            logger.error(f"Failed to get Pair: {e}")
            return None

    def v2_pair_token_order_correct(self, v2_pair: Contract, tokenA_address: str, tokenB_address: str) -> Optional[bool]:
        """Checks the token order in the Uniswap V2 Pair contract.

        Args:
            v2_pair: The Uniswap V2 Pair contract.
            tokenA_address (str): The address of token A.
            tokenB_address (str): The address of token B.

        Returns:
            True if the order is correct, False if the order is incorrect, or None if an error occurred.
        """
        try:
            token0_address = v2_pair.functions.token0().call()
            token1_address = v2_pair.functions.token1().call()
            if tokenA_address == token0_address and tokenB_address == token1_address:
                return True
            elif tokenA_address == token1_address and tokenB_address == token0_address:
                return False
        except Exception as e:
            logger.error(f"Failed to get token order: {e}")
            return None

    def get_uniswap_v2_price(self, block_number: int, v2_pair: Contract, order_correct: bool, decimal_adj: int) -> Optional[float]:
        """Fetches the price of the token pair at the given block number.

        Only calls get reserves to ensure no more than one call is made. 

        Args:
            block_number (int): The block number.
            v2_pair: The Uniswap V2 Pair contract.
            order_correct (bool): Whether the order of tokens in the pair contract is correct.
            decimal_adj (int): The number of decimals to adjust the price.

        Returns:
            The price of the token pair or None if an error occurred.
        """
        try:
            reserve0, reserve1, _ = v2_pair.functions.getReserves().call(block_identifier=int(block_number))
            if reserve1 != 0:  # Avoid ZeroDivisionError
                if order_correct:
                    return (reserve0 / reserve1) * 10**decimal_adj
                elif order_correct == False:
                    return (reserve1 / reserve0) * 10**decimal_adj
        except ZeroDivisionError as e:
            logger.error(f"Division by zero encountered while getting price: {e}")
            return None
        except Exception as e:
            raise ValueError(str(e))
        
    def get_v2_pair_info(self, tokenA: Token, tokenB: Token) -> Tuple[Optional[str], Optional[Contract], Optional[bool], Optional[int], Optional[int], Optional[str]]:
        """
        Fetches the pair details from Uniswap V2 and returns the pair address, 
        the pair contract, and the token order correctness. Also gets the contract
        creation timestamp, block number, and transaction hash.

        Args:
            tokenA_address (str): The address of token A.
            tokenB_address (str): The address of token B.

        Returns:
            Tuple of the pair address (str), the pair contract (Contract), a boolean indicating if the 
            token order is correct, the contract creation timestamp (int), block number (int), 
            and transaction hash (str).
        """        
        v2_pair_address = self.get_uniswap_v2_pair_address(tokenA, tokenB)
        if v2_pair_address:
            v2_pair = self.get_uniswap_v2_pair(v2_pair_address)  
            v2_order_correct = self.v2_pair_token_order_correct(v2_pair, tokenA.address, tokenB.address)
            return v2_pair_address, v2_pair, v2_order_correct
        else:
            return None, None, None