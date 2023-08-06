
from typing import List, Dict, Any
import logging
from web3.exceptions import TransactionNotFound
from web3 import Web3
from etherscan import Etherscan
from web3r.datatypes import Token
from web3r.datatypes import Transfer 
from web3r.utils import Utils
from tqdm import tqdm
from web3.exceptions import (
    LogTopicError,
    BlockNumberOutofRange
)
from web3r.exeptions import TooManyResultsError
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STANDARD_ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                "type": "address"
            },
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            },
            {
                "name": "_spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "payable": True,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
]

class Tokens:
    """
    This class is used for interacting and producing ERC20 tokens.
    """
    def __init__(self, web3: Web3, etherscan: Etherscan, utils: Utils) -> None:
        """
        Initializes the Tokens class with instances of Web3 and Etherscan.

        Args:
            web3 (Web3): The instance of Web3.
            etherscan (Etherscan): The instance of Etherscan.
        """
        self.web3 = web3
        self.etherscan = etherscan
        self.utils = utils

    def initiate_erc20_contract(self, contract_address: str):
        """Initiates an ERC20 token contract.

        Args:
            contract_address (str): The address of the contract.

        Returns:
            An initiated ERC20 token contract.
        """
        try:
            return self.web3.eth.contract(address=contract_address, abi=STANDARD_ERC20_ABI)
        except Exception as e:
            print(f"An error occurred while initiating the ERC20 contract: {str(e)}")
            return None

    def get_decoded_transfer_logs(self, from_block: int, to_block: int, token: Token) -> List[Dict[str, Any]]:
        try:
            contract = self.initiate_erc20_contract(token.address)
            event_filter = contract.events.__dict__['Transfer'].create_filter(fromBlock=from_block, toBlock=to_block)
            events = event_filter.get_all_entries()

            if not events:
                return []

            return [{'address':  token.address, 'from': event.args['from'], 'to': event.args['to'], 'quantity': event.args['value'], 'blockNumber': event.blockNumber, 'transactionHash': event.transactionHash.hex()} for event in events]
        except Exception as e:
            error_message = str(e.args[0]['message'])
            if 'query returned more than 10000 results' in error_message.lower():
                raise TooManyResultsError(error_message)
            else:
                raise ValueError(error_message)

    def get_balance(self, contract_address: str, address: str) -> int:
        """Fetches the balance of a specific address.

        Args:
            contract_address (str): The address of the contract.
            address (str): The address whose balance is being fetched.

        Returns:
            The balance of the specified address.
        """
        try:
            contract = self.initiate_erc20_contract(contract_address)
            return contract.functions.balanceOf(address).call()
        except Exception as e:
            print(f"An error occurred while getting the balance: {str(e)}")
            return None

    def get_total_supply(self, contract_address: str) -> int:
        """Fetches the total supply for the token.

        Args:
            contract_address (str): The address of the contract.

        Returns:
            The total supply of the token.
        """
        try:
            contract = self.initiate_erc20_contract(contract_address)
            return contract.functions.totalSupply().call()
        except Exception as e:
            print(f"An error occurred while getting the total supply: {str(e)}")
            return None
        
    def get_symbol(self, contract_address: str) -> str:
        """Fetches the symbol of the token.

        Args:
            contract_address (str): The address of the contract.

        Returns:
            The symbol of the token.
        """
        try:
            contract = self.initiate_erc20_contract(contract_address)
            return contract.functions.symbol().call()
        except Exception as e:
            print(f"An error occurred while getting the symbol: {str(e)}")
            return None
        
    def get_name(self, contract_address: str) -> str:
        """Fetches the name of the token.

        Args:
            contract_address (str): The address of the contract.

        Returns:
            The name of the token.
        """
        try:
            contract = self.initiate_erc20_contract(contract_address)
            return contract.functions.name().call()
        except Exception as e:
            print(f"An error occurred while getting the symbol: {str(e)}")
            return None
        
    def get_decimals(self, contract_address: str) -> int:
        """Fetches the decimals of the token.

        Args:
            contract_address (str): The address of the contract.

        Returns:
            The decimals of the token.
        """
        try:
            contract = self.initiate_erc20_contract(contract_address)
            return contract.functions.decimals().call()
        except Exception as e:
            print(f"An error occurred while getting the decimals: {str(e)}")
            return None
        
    def get_token(self, token_address: str) -> Token:
        """
        Gets a Token object with all its properties including address, symbol, name, decimals,
        total supply, block timestamp, block number, and block hash.

        Args:
            token_address (str): The address of the token contract.

        Returns:
            A Token object.
        """
        try:
            print(f"Getting {token_address} data...")

            address = self.web3.to_checksum_address(token_address)
            creation_timestamp, creation_block_number, creation_hash = self.utils.get_contract_creation_timestamp_block_hash(address)
            symbol = self.get_symbol(address)
            name= self.get_name(address)
            decimals = self.get_decimals(address)
            total_supply = self.get_total_supply(address)
            block_timestamp= creation_timestamp
            block_number= creation_block_number
            block_hash= creation_hash

            print(f"{token_address} retrieved as {name} ({symbol}) made at {block_number}")
            # Create a new Token object for each row in the DataFrame.
            return Token(
                address= address,
                symbol = symbol,
                name= name,
                decimals = decimals,
                total_supply = total_supply,
                block_timestamp= block_timestamp,
                block_number= block_number,
                block_hash= block_hash
            )
        except Exception as e:
            logger.error(f"An error occurred while getting the token details: {str(e)}")
            return None
        

    def get_all_transfers(self, token: Token) -> List[Dict[str, any]]:
        """
        Finds all transfers for a Token within the Ethereum blockchain, and returns them as a list of dictionaries.
        Each transfer is represented by a dictionary with keys: 'address', 'from', 'to', 'quantity', 'blockNumber', and 'transactionHash'.

        Args:
            token (Token): An object representing the token. Must have 'block_number' and 'address' attributes.

        Returns:
            transfers (List[Dict[str, any]]): A list of transfers for the provided token.
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

        # Block range to search for transfers
        from_block = token.block_number  # Start from the block where the token was created
        to_block = self.web3.eth.block_number  # End at the current block

        # Finding the initial block chunk size
        block_chunk_size = initial_block_chunk_size

        # List to hold the transfer events
        transfers: List[Transfer] = []

        # Progress bar initialization
        with tqdm(total=to_block - from_block, desc='Finding transfers in blocks: ') as pbar:

            while from_block < to_block:
                try:
                    # Get events for the specified range and token
                    events = self.get_decoded_transfer_logs(from_block, min(from_block + block_chunk_size, to_block), token)
                
                    # If there are events, add them to the transfers list
                    if events:
                        transfers.extend(events)
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

            return transfers