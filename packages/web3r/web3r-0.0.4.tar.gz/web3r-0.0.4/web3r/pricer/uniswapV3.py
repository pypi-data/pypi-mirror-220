import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from web3.contract import Contract
from typing import List, Dict, Tuple
from typing import Optional
from web3r.utils import Utils
from web3 import Web3
from etherscan import Etherscan
from web3r.datatypes import Token
from web3r.exeptions import ZeroAddressError
from typing import List, Dict, Any
from web3r.exeptions import TooManyResultsError
from tqdm import tqdm
from web3r.the_graph_uniswapV3 import TheGraphUniswapV3

UNISWAP_V3_FACTORY_ABI = [
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
        },
        {
            "name": "fee",
            "type": "uint24"
        }
    ],
    "name": "getPool",
    "outputs": [
        {
            "name": "",
            "type": "address"
        }
    ],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
}
]
UNISWAP_V3_POOL_ABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"int24","name":"tickLower","type":"int24"},{"indexed":True,"internalType":"int24","name":"tickUpper","type":"int24"},{"indexed":False,"internalType":"uint128","name":"amount","type":"uint128"},{"indexed":False,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":False,"internalType":"address","name":"recipient","type":"address"},{"indexed":True,"internalType":"int24","name":"tickLower","type":"int24"},{"indexed":True,"internalType":"int24","name":"tickUpper","type":"int24"},{"indexed":False,"internalType":"uint128","name":"amount0","type":"uint128"},{"indexed":False,"internalType":"uint128","name":"amount1","type":"uint128"}],"name":"Collect","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"sender","type":"address"},{"indexed":True,"internalType":"address","name":"recipient","type":"address"},{"indexed":False,"internalType":"uint128","name":"amount0","type":"uint128"},{"indexed":False,"internalType":"uint128","name":"amount1","type":"uint128"}],"name":"CollectProtocol","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"sender","type":"address"},{"indexed":True,"internalType":"address","name":"recipient","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"paid0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"paid1","type":"uint256"}],"name":"Flash","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint16","name":"observationCardinalityNextOld","type":"uint16"},{"indexed":False,"internalType":"uint16","name":"observationCardinalityNextNew","type":"uint16"}],"name":"IncreaseObservationCardinalityNext","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"},{"indexed":False,"internalType":"int24","name":"tick","type":"int24"}],"name":"Initialize","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"sender","type":"address"},{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"int24","name":"tickLower","type":"int24"},{"indexed":True,"internalType":"int24","name":"tickUpper","type":"int24"},{"indexed":False,"internalType":"uint128","name":"amount","type":"uint128"},{"indexed":False,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint8","name":"feeProtocol0Old","type":"uint8"},{"indexed":False,"internalType":"uint8","name":"feeProtocol1Old","type":"uint8"},{"indexed":False,"internalType":"uint8","name":"feeProtocol0New","type":"uint8"},{"indexed":False,"internalType":"uint8","name":"feeProtocol1New","type":"uint8"}],"name":"SetFeeProtocol","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"sender","type":"address"},{"indexed":True,"internalType":"address","name":"recipient","type":"address"},{"indexed":False,"internalType":"int256","name":"amount0","type":"int256"},{"indexed":False,"internalType":"int256","name":"amount1","type":"int256"},{"indexed":False,"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"},{"indexed":False,"internalType":"uint128","name":"liquidity","type":"uint128"},{"indexed":False,"internalType":"int24","name":"tick","type":"int24"}],"name":"Swap","type":"event"},{"inputs":[{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint128","name":"amount","type":"uint128"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint128","name":"amount0Requested","type":"uint128"},{"internalType":"uint128","name":"amount1Requested","type":"uint128"}],"name":"collect","outputs":[{"internalType":"uint128","name":"amount0","type":"uint128"},{"internalType":"uint128","name":"amount1","type":"uint128"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint128","name":"amount0Requested","type":"uint128"},{"internalType":"uint128","name":"amount1Requested","type":"uint128"}],"name":"collectProtocol","outputs":[{"internalType":"uint128","name":"amount0","type":"uint128"},{"internalType":"uint128","name":"amount1","type":"uint128"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"fee","outputs":[{"internalType":"uint24","name":"","type":"uint24"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeGrowthGlobal0X128","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeGrowthGlobal1X128","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"flash","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"observationCardinalityNext","type":"uint16"}],"name":"increaseObservationCardinalityNext","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"liquidity","outputs":[{"internalType":"uint128","name":"","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxLiquidityPerTick","outputs":[{"internalType":"uint128","name":"","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint128","name":"amount","type":"uint128"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mint","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"observations","outputs":[{"internalType":"uint32","name":"blockTimestamp","type":"uint32"},{"internalType":"int56","name":"tickCumulative","type":"int56"},{"internalType":"uint160","name":"secondsPerLiquidityCumulativeX128","type":"uint160"},{"internalType":"bool","name":"initialized","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32[]","name":"secondsAgos","type":"uint32[]"}],"name":"observe","outputs":[{"internalType":"int56[]","name":"tickCumulatives","type":"int56[]"},{"internalType":"uint160[]","name":"secondsPerLiquidityCumulativeX128s","type":"uint160[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"positions","outputs":[{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"feeGrowthInside0LastX128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthInside1LastX128","type":"uint256"},{"internalType":"uint128","name":"tokensOwed0","type":"uint128"},{"internalType":"uint128","name":"tokensOwed1","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"protocolFees","outputs":[{"internalType":"uint128","name":"token0","type":"uint128"},{"internalType":"uint128","name":"token1","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"feeProtocol0","type":"uint8"},{"internalType":"uint8","name":"feeProtocol1","type":"uint8"}],"name":"setFeeProtocol","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"slot0","outputs":[{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"},{"internalType":"int24","name":"tick","type":"int24"},{"internalType":"uint16","name":"observationIndex","type":"uint16"},{"internalType":"uint16","name":"observationCardinality","type":"uint16"},{"internalType":"uint16","name":"observationCardinalityNext","type":"uint16"},{"internalType":"uint8","name":"feeProtocol","type":"uint8"},{"internalType":"bool","name":"unlocked","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"}],"name":"snapshotCumulativesInside","outputs":[{"internalType":"int56","name":"tickCumulativeInside","type":"int56"},{"internalType":"uint160","name":"secondsPerLiquidityInsideX128","type":"uint160"},{"internalType":"uint32","name":"secondsInside","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"bool","name":"zeroForOne","type":"bool"},{"internalType":"int256","name":"amountSpecified","type":"int256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[{"internalType":"int256","name":"amount0","type":"int256"},{"internalType":"int256","name":"amount1","type":"int256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int16","name":"","type":"int16"}],"name":"tickBitmap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tickSpacing","outputs":[{"internalType":"int24","name":"","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int24","name":"","type":"int24"}],"name":"ticks","outputs":[{"internalType":"uint128","name":"liquidityGross","type":"uint128"},{"internalType":"int128","name":"liquidityNet","type":"int128"},{"internalType":"uint256","name":"feeGrowthOutside0X128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthOutside1X128","type":"uint256"},{"internalType":"int56","name":"tickCumulativeOutside","type":"int56"},{"internalType":"uint160","name":"secondsPerLiquidityOutsideX128","type":"uint160"},{"internalType":"uint32","name":"secondsOutside","type":"uint32"},{"internalType":"bool","name":"initialized","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]
UNISWAP_V3_FACTORY_CONTRACT_ADDRESS = '0x1F98431c8aD98523631AE4a59f267346ea31F984'

class UniswapV3:
    def __init__(self, web3: Web3, etherscan: Etherscan, utils: Utils, grph_uniV3: TheGraphUniswapV3):
        """Initializes the UniswapV3 class.

        Args:
            etherscan (Etherscan): An instance of the Etherscan class.
            web3 (Web3): An instance of the Web3 class.
        """
        self.etherscan = etherscan
        self.web3 = web3
        self.utils = utils
        self.grph_uniV3 = grph_uniV3

        self.v3_factory_contract = self.web3.eth.contract(address=self.web3.to_checksum_address(UNISWAP_V3_FACTORY_CONTRACT_ADDRESS), abi=UNISWAP_V3_FACTORY_ABI)

    def get_uniswap_v3_pool_address(self, tokenA_address: str, tokenB_address: str, fee: int) -> Optional[str]:
        """Fetches the address of the Uniswap V3 Pool for the given tokens and fee tier.

        Args:
            tokenA_address (str): The address of token A.
            tokenB_address (str): The address of token B.
            fee (int): The fee tier.

        Returns:
            The address of the Uniswap V3 Pool or None if an error occurred.
        """
        try:
            v3_pool_address = self.web3.to_checksum_address( self.v3_factory_contract.functions.getPool(tokenA_address, tokenB_address, fee).call() )
            if v3_pool_address == "0x0000000000000000000000000000000000000000":
                raise ZeroAddressError(v3_pool_address)
            else:
                return v3_pool_address
        except ZeroAddressError as ze:
            logger.error(f"No Uniswap V3 Pool Present: {str(ze)}")
            return False
        except Exception as e:
            logger.error(f"Failed to get Pool address: {str(e)}")
            raise Exception

    def get_uniswap_v3_pool(self, v3_pool_address: str) -> Optional[Contract]:
        """Gets the Uniswap V3 Pool contract based on the pool address.

        Args:
            v3_pool_address (str): The address of the Uniswap V3 Pool.

        Returns:
            The Uniswap V3 Pool contract or None if an error occurred.
        """
        try:
            v3_pool = self.web3.eth.contract(address=self.web3.to_checksum_address(v3_pool_address), abi=UNISWAP_V3_POOL_ABI)
            return v3_pool
        except Exception as e:
            logger.error(f"Failed to get Pool: {e}")
            return None

    @staticmethod
    def v3_pool_token_order_correct(v3_pool: Contract, tokenA_address: str, tokenB_address: str) -> Optional[bool]:
        """Checks the token order in the Uniswap V3 Pool contract.

        Args:
            v3_pool (Contract): The Uniswap V3 Pool contract.
            tokenA_address (str): The address of token A.
            tokenB_address (str): The address of token B.

        Returns:
            True if the order is correct, False if the order is incorrect, or None if an error occurred.
        """
        try:
            token0_address = v3_pool.functions.token0().call()
            token1_address = v3_pool.functions.token1().call()
            if tokenA_address == token0_address and tokenB_address == token1_address:
                return True
            elif tokenA_address == token1_address and tokenB_address == token0_address:
                return False
        except Exception as e:
            logger.error(f"Failed to get token order: {e}")
            return None
        
    def get_uniswap_v3_price(self, block_number: int, v3_pool: Contract, order_correct: bool, decimal_adj: int) -> Optional[float]:
        try:
            slot0 = v3_pool.functions.slot0().call(block_identifier=int(block_number))
            sqrtPriceX96 = slot0[0]
            if order_correct:
                price = (sqrtPriceX96 ** 2 * 10 ** decimal_adj) / (2 ** 192)
            else:
                price = 1 / ((sqrtPriceX96 ** 2 * 10 ** decimal_adj) / (2 ** 192))
            return price
        except Exception as e:
            raise ValueError(e)

    def get_v3_pool_info(self, tokenA: Token, tokenB: Token, fee: int) -> Tuple[Optional[str], Optional[Contract], Optional[bool], Optional[int], Optional[int], Optional[str]]:
        """
        Fetches the pool details from Uniswap V3 and returns the pool address, 
        the pool contract, and the token order correctness. Also gets the contract
        creation timestamp, block number, and transaction hash.

        Args:
            tokenA_address (str): The address of token A.
            tokenB_address (str): The address of token B.
            fee (int): The fee tier.

        Returns:
            Tuple of the pool address, the pool contract, a boolean indicating if the 
            token order is correct, the contract creation timestamp, block number, 
            and transaction hash.
        """
        v3_pool_address = self.get_uniswap_v3_pool_address(tokenA.address, tokenB.address, fee)
        if v3_pool_address:
            v3_pool = self.get_uniswap_v3_pool(v3_pool_address)
            v3_order_correct = self.v3_pool_token_order_correct(v3_pool, tokenA.address, tokenB.address)
            return v3_pool_address, v3_pool, v3_order_correct 
        else:
            return None, None, None

    def get_decoded_v3_swap_logs(self, from_block: int, to_block: int, v3_pool: Contract) -> List[Dict[str, Any]]:
        """
        Get decoded swap events from the Uniswap V3 pool between specified blocks.

        Args:
            from_block (int): The block number to start looking for swap events from.
            to_block (int): The block number to stop looking for swap events.
            v3_pool_contract (Contract): The Uniswap V3 Pool contract instance.

        Returns:
            List[Dict[str, Any]]: A list of swap events found between the specified blocks. 
            Each event is represented as a dictionary that includes:
                - 'address': The address of the Uniswap V3 Pool contract.
                - 'sender': The address of the sender of the swap transaction.
                - 'recipient': The address of the recipient of the swap transaction.
                - 'amount0': The swapped amount of the token 0.
                - 'amount1': The swapped amount of the token 1.
                - 'sqrtPriceX96': The square root of the price, scaled by 2^96.
                - 'tick': The current tick of the pool.
                - 'blockNumber': The block number where the swap event occurred.
                - 'transactionHash': The hash of the swap transaction.
        
        Raises:
            TooManyResultsError: If the query returned more than 10000 results.
            ValueError: If any other error occurred.
        """
        try:
            # Create a filter for 'Swap' events between the specified blocks
            event_filter = v3_pool.events.__dict__['Swap'].create_filter(fromBlock=from_block, toBlock=to_block)
            
            # Retrieve the events using the filter
            events = event_filter.get_all_entries()

            # If no events found, return an empty list
            if not events:
                return []

            # Decode the events and return as a list of dictionaries
            return [{'address': v3_pool.address,
                    'sender': event.args['sender'],
                    'recipient': event.args['recipient'],
                    'amount0': event.args['amount0'],
                    'amount1': event.args['amount1'],
                    'sqrtPriceX96': event.args['sqrtPriceX96'],
                    'tick': event.args['tick'],
                    'blockNumber': event.blockNumber,
                    'transactionHash': event.transactionHash.hex()} for event in events]
        except Exception as e:
            # Handle possible exceptions
            error_message = str(e.args[0]['message'])
            if 'query returned more than 10000 results' in error_message.lower():
                raise TooManyResultsError(error_message)
            else:
                raise ValueError(error_message)

            
    def get_all_v3_swaps_by_pool(self, v3_pool: Contract) -> List[Dict[str, any]]:
        """
        Finds all swaps in the Uniswap V3 pool within the Ethereum blockchain, 
        and returns them as a list of dictionaries.
        Each swap is represented by a dictionary with keys: 
        'address', 'sender', 'recipient', 'amount0', 'amount1', 
        'sqrtPriceX96', 'tick', 'blockNumber', and 'transactionHash'.

        Args:
            v3_pool_contract (Contract): The contract instance for Uniswap V3 pool.

        Returns:
            swaps (List[Dict[str, any]]): A list of swaps for the provided Uniswap V3 pool.
        """

        def _halve_block_chunk_size(block_chunk_size: int, min_block_chunk_size: int) -> int:
            """
            Halves the block chunk size, ensuring it doesn't fall below the minimum block chunk size.

            Args:
                block_chunk_size (int): The current size of the block chunk.
                min_block_chunk_size (int): The minimum allowable size of the block chunk.

            Returns:
                int: The halved block chunk size.
            """
            return max(round(block_chunk_size / 2), min_block_chunk_size)

        def _double_block_chunk_size(block_chunk_size: int) -> int:
            """
            Doubles the block chunk size.

            Args:
                block_chunk_size (int): The current size of the block chunk.

            Returns:
                int: The doubled block chunk size.
            """
            return block_chunk_size * 2

        # Initial and minimum block chunk sizes
        initial_block_chunk_size = 5000
        min_block_chunk_size = 1

        # Block range to search for swaps
        graph_data = self.grph_uniV3.get_pool_info_by_pool(v3_pool)
        from_block = int(graph_data.created_at_block_number)  # Start from the block where the Uniswap V3 pool was created
        to_block = self.web3.eth.block_number  # End at the current block

        print(graph_data.created_at_block_number, to_block)

        # Finding the initial block chunk size
        block_chunk_size = initial_block_chunk_size

        # List to hold the swap events
        swaps: List[Dict] = []

        # Progress bar initialization
        with tqdm(total=to_block - from_block, desc='Finding V3 swaps in blocks: ') as pbar:

            while from_block < to_block:
                try:
                    # Get events for the specified range and pool contract
                    events = self.get_decoded_v3_swap_logs(from_block, min(from_block + block_chunk_size, to_block), v3_pool)
                
                    # If there are events, add them to the swaps list
                    if events:
                        swaps.extend(events)
                    else:
                        block_chunk_size = _double_block_chunk_size(block_chunk_size)

                    # Update the progress bar
                    processed_blocks = min(from_block + block_chunk_size, to_block) - from_block
                    pbar.update(processed_blocks)

                    # Move to the next block chunk
                    from_block += block_chunk_size + 1

                except TooManyResultsError as e:
                    block_chunk_size = _halve_block_chunk_size(block_chunk_size, min_block_chunk_size)
                    logging.info(f'Too Many Results: Adjusting Block Chunk Size to: {block_chunk_size}')
                    continue

                except ValueError as e:
                    logging.error(f'Unexpected ValueError: {e}')
                    raise

            return swaps