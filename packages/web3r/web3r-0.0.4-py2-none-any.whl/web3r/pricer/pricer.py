# Import required modules and classes
import logging
from web3r.utils import Utils
from web3 import Web3
from web3.contract import Contract
from etherscan import Etherscan
from web3r.tokens import Tokens
from web3r.datatypes import Token
from web3r.datatypes import TheGraphUniswapV3Pool

# Import the required modules and classes
from web3r.pricer.uniswapV2 import UniswapV2
from web3r.pricer.uniswapV3 import UniswapV3

# Configure the logger with INFO level, this will capture all logs with level INFO and above
logging.basicConfig(level=logging.INFO)
# Create a logger instance for this module
logger = logging.getLogger(__name__)

class Pricer(UniswapV2, UniswapV3):
    def __init__(self, web3: Web3, etherscan: Etherscan, utils: Utils, tokens: Tokens, grph_uniV3: TheGraphUniswapV3Pool):
        # Explicitly call the constructors of both parent classes
        # This allows the Pricer to inherit functionality from both Uniswap interactors

        self.etherscan = etherscan
        self.web3 = web3
        self.utils = utils
        self.tokens = tokens
        self.grph_uniV3 = grph_uniV3
    
        UniswapV2.__init__(self, web3, etherscan, utils, grph_uniV3)
        UniswapV3.__init__(self, web3, etherscan, utils, grph_uniV3)

    def get_fallbacked_price(self, block_number: int, v2_pair: Contract, v3_pool: Contract, v2_order_correct: bool, v3_order_correct: bool, decimal_adj: int):
        """
        Attempt to fetch the price of a token from Uniswap V3 first, then Uniswap V2 as a fallback.

        Args:
            v2_pair (str): The pair address for Uniswap V2.
            v3_pool (str): The pool address for Uniswap V3.
            v2_order_correct (bool): Indicates if the token order in the Uniswap V2 pair is correct.
            v3_order_correct (bool): Indicates if the token order in the Uniswap V3 pool is correct.
            decimal_adj (int): The decimal places adjustment for the price.

        Returns:
            The price of the token, or None if the price couldn't be fetched from either Uniswap V3 or V2.
        """
        try:
            # Try getting the price from Uniswap V3 first
            if v3_pool is not None:
                return self.get_uniswap_v3_price(block_number, v3_pool, v3_order_correct, decimal_adj)
        except Exception as e:
            if(v2_pair):
                logger.error(f"Uniswap V3 Failed to get price from Uniswap V3 due to: {str(e)}. Falling back to V2")
            else:
                raise ValueError(f"Uniswap V3 Failed to get price: {str(e)}")

        try:
            # Try getting the price from Uniswap V2 as a fallback
            if v2_pair is not None:
                price = self.get_uniswap_v2_price(block_number, v2_pair, v2_order_correct, decimal_adj)
                print('Uniswap V2 Price Recieved: ', price)
                return price
        except Exception as e:
            # Log an error if Uniswap V2 also fails
            raise ValueError(f"Uniswap V2 Failed to get price: {str(e)}")

    def get_fallbacked_decimal_adj(self, tokenA: Token, tokenB: Token, v2_order_correct: bool, v3_order_correct: bool) -> int:
        """Calculates the decimal adjustment between two tokens.

        Args:
            tokenA_address (str): The address of token A.
            tokenB_address (str): The address of token B.
            v2_order_correct (bool): Indicates if the token order in the Uniswap V2 pair is correct.
            v3_order_correct (bool): Indicates if the token order in the Uniswap V3 pool is correct.

        Returns:
            The decimal adjustment between the two tokens.
        """
        try:
            # Calculate decimal adjustment for Uniswap V3
            if v3_order_correct:
                dec_adj_v3 = tokenA.decimals - tokenB.decimals
            else:
                dec_adj_v3 = tokenB.decimals - tokenA.decimals

            # Calculate decimal adjustment for Uniswap V2
            if v2_order_correct:
                dec_adj_v2 = tokenA.decimals - tokenB.decimals
            else:
                dec_adj_v2 = tokenB.decimals - tokenA.decimals

            # Depending on your criteria, return the decimal adjustment from V3 or V2
            # In this example, we prefer V3, and fallback to V2
            return dec_adj_v3 if dec_adj_v3 is not None else dec_adj_v2
        except Exception as e:
            logger.error(f"Failed to calculate decimal adjustment: {e}")
            return None

