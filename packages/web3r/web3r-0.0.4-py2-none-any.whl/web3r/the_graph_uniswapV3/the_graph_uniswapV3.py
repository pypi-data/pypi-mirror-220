import requests
import json
import logging
from typing import List, Dict, Any
from web3r.datatypes.the_graph_uniV3 import TheGraphUniswapV3Pool
from web3 import Web3
from web3.contract import Contract

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TheGraphUniswapV3:
    """
    Contains utility methods for interacting with TheGraph API.
    """
    def __init__(self, web3: Web3, subgraph_name: str = "uniswap/uniswap-v3") -> None:
        """
        Initializes the TheGraph class with a specific subgraph name.

        Args:
            subgraph_name (str): The name of the subgraph to interact with.
        """
        self.web3 = web3
        self.url = f"https://api.thegraph.com/subgraphs/name/{subgraph_name}"

    def _run_query(self, query: str) -> Dict[str, Any]:
        """
        Makes a request to the TheGraph API with the provided GraphQL query and returns the response.

        Args:
            query (str): The GraphQL query to run.

        Returns:
            The response data as a dictionary.
        """
        try:
            response = requests.post(self.url, json={"query": query})
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            logger.exception("Request failed: %s", e)
            raise e
        except json.JSONDecodeError as e:
            logger.exception("Failed to parse response: %s", e)
            raise e
        
    def format_pools_by_address(self, res: List[Dict[str, Any]]) -> List[TheGraphUniswapV3Pool]:
        formatted = []
        for pool in res:
            token0 = pool.pop('token0')  # Remove 'token0' and store its value
            pool['token0_address'] = token0['id']
            pool['token0_symbol'] = token0['symbol']
            pool['token0_totalSupply'] = token0['totalSupply']

            token1 = pool.pop('token1')  # Remove 'token1' and store its value
            pool['token1_address'] = token1['id']
            pool['token1_symbol'] = token1['symbol']
            pool['token1_totalSupply'] = token1['totalSupply']

            pool['address'] = self.web3.to_checksum_address(pool.pop('id'))
            pool['liquidity'] = pool['liquidity']
            pool['created_at_timestamp'] = pool.pop('createdAtTimestamp')  # Key name changed
            pool['created_at_block_number'] = pool.pop('createdAtBlockNumber')  # Key name changed
            pool['total_value_locked_token1'] = pool.pop('totalValueLockedToken1') # Key name changed
            pool['sqrt_price'] = pool.pop('sqrtPrice') # Key name changed
            pool['tick'] = pool['tick']
            pool['fee_tier'] = int(pool.pop('feeTier'))  # Key name changed

            formatted.append(TheGraphUniswapV3Pool(**pool))
        return formatted

    def get_all_pools_by_one_address(self, token_address: str) -> List[TheGraphUniswapV3Pool]:
        """
        Retrieves pools associated with a given token address.

        Args:
            token_address (str): The address of the token.

        Returns:
            A list of dictionaries containing pool data.
        """
        query = f"""
        {{
            pools(first: 1000, orderBy: createdAtTimestamp, orderDirection: desc, where: {{ token1: "{token_address}" }}) {{
                id
                liquidity
                token0 {{
                    id 
                    symbol
                    totalSupply
                }}
                token1 {{
                    id
                    symbol
                    totalSupply
                }}
                createdAtTimestamp
                createdAtBlockNumber
                totalValueLockedToken1
                sqrtPrice
                tick
                feeTier
            }}
        }}
        """
        try:
            res = self._run_query(query)['data']['pools']
            formatted = self.format_pools_by_address(res)
            return formatted
        except requests.exceptions.RequestException as e:
            logger.exception("Failed to execute request: %s", e)
            raise
        except json.JSONDecodeError as e:
            logger.exception("Failed to decode JSON: %s", e)
            raise
        except Exception as e:
            logger.exception("Failed to get pool data by token address: %s", e)
            raise


    def get_pool_info_by_pool(self, v3_pool: Contract) -> TheGraphUniswapV3Pool:
        """
        Retrieves data for a specific pool.

        Args:
            pool_address (str): The address of the pool.

        Returns:
            TheGraphUniswapV3Pool: The pool data.
        """
        query = f"""
        {{
            pools(first: 1000, orderBy: createdAtTimestamp, orderDirection: desc, where: {{id: "{v3_pool.address.lower()}"}}) {{
                id
                liquidity
                token0 {{
                    id
                    symbol
                    totalSupply
                }}
                token1 {{
                    id
                    symbol
                    totalSupply
                }}
                createdAtTimestamp
                createdAtBlockNumber
                totalValueLockedToken1
                sqrtPrice
                tick
                feeTier
            }}
        }}
        """
        try:
            res = self._run_query(query)['data']['pools']
            formatted = self.format_pools_by_address(res)
            return formatted[0]
        except requests.exceptions.RequestException as e:
            logger.exception("Failed to execute request: %s", e)
            raise
        except json.JSONDecodeError as e:
            logger.exception("Failed to decode JSON: %s", e)
            raise
        except Exception as e:
            logger.exception("Failed to get pool data: %s", e)
            raise

    def get_top_pools(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieves the top pools by liquidity.

        Args:
            limit (int): The number of pools to retrieve.

        Returns:
            A list of dictionaries containing the pool data.
        """
        query = f"""
        {{
            pools(first: {limit}, orderBy: liquidity, orderDirection: desc) {{
                id
                liquidity
                token0 {{
                    id 
                    symbol
                    totalSupply
                }}
                token1 {{
                    id
                    symbol
                    totalSupply
                }}
                createdAtTimestamp
                createdAtBlockNumber
                totalValueLockedToken1
                sqrtPrice
                tick
                feeTier
            }}
        }}
        """
        try:
            return self._run_query(query)
        except Exception as e:
            logger.exception(f"Failed to get top pools: {e}")
            raise e
        

    def get_user_transactions(self, user_address: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieves the transactions of a specific user.

        Args:
            user_address (str): The address of the user.
            limit (int): The number of transactions to retrieve.

        Returns:
            A list of dictionaries containing the transaction data.
        """
        query = f"""
        {{
            transactions(where: {{ user: "{user_address}" }}, first: {limit}, orderBy: timestamp, orderDirection: desc) {{
                id
                timestamp
                token0 {{
                    symbol
                }}
                token1 {{
                    symbol
                }}
                amount0
                amount1
                to
            }}
        }}
        """
        try:
            return self._run_query(query)
        except Exception as e:
            logger.exception(f"Failed to get user transactions: {e}")
            raise e

