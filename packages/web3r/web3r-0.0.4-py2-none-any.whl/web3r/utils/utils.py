from typing import List, Dict, Any
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from web3.exceptions import TransactionNotFound
from web3 import Web3
from etherscan import Etherscan

class Utils:
    """
    Contains utility methods.
    """

    def __init__(self, web3: Web3, etherscan: Etherscan) -> None:
        """
        Initializes the Utils class with instances of Web3 and Etherscan.

        Args:
            web3 (Web3): The instance of Web3.
            etherscan (Etherscan): The instance of Etherscan.
        """
        self.web3 = web3
        self.etherscan = etherscan

    def get_earliest_transaction_hash(self, contract_address: str) -> str:
        """
        Retrieves the transaction hash of a contract creation, if available.
        If a contract creation transaction cannot be found, returns the earliest transaction involving the contract.
        After this is used, you can use Infura to get the block data (number etc).

        Args:
            contract_address (str): The address of the contract.

        Returns:
            The transaction hash as a string.
        """
        try:
            # Retrieve the first transaction by address in ascending order
            print(contract_address)
            tx_list = self.etherscan.get_normal_txs_by_address_paginated(
                address=contract_address,
                page=1,
                offset=1,
                startblock=0,
                endblock=99999999,
                sort='asc'
            )

            # Check if the list is empty
            if len(tx_list) == 0:
                logger.info("No transaction found for this address.")
                return None

            # Retrieve the first transaction
            tx = tx_list[0]

            # Check if this is a contract creation transaction
            if tx['to'] == "":
                return tx['hash']
            else:
                return tx['hash']

        except Exception as e:
            logger.exception(f"Failed to get earliest transaction hash: {e}")
            raise e

    def get_contract_creation_timestamp_block_hash(self, contract_address: str):
        """
        Retrieves the contract creation timestamp, block number, and transaction hash.

        Args:
            contract_address (str): The address of the contract.

        Returns:
            A tuple containing the contract creation timestamp (int),
            block number (int), and transaction hash (str).
        """
        creation_hash = None
        try:
            # Get the earliest transaction hash for contract creation
            creation_hash = self.get_earliest_transaction_hash(contract_address=contract_address)
        except Exception as e:
            logger.error(f"Error while getting contract creation transaction hash: {e}")
            raise ValueError

        creation_block_number = None
        tx_receipt = None
        try:
            # Get the transaction receipt to retrieve the block number
            tx_receipt = self.web3.eth.get_transaction_receipt(creation_hash)
            creation_block_number = tx_receipt['blockNumber']
        except Exception as e:
            logger.error(f"Error while getting block number: {e}")
            raise ValueError

        creation_timestamp = None
        try:
            # Get the block timestamp using the block number
            creation_timestamp = self.web3.eth.get_block(creation_block_number)['timestamp']
        except Exception as e:
            logger.error(f"Error while getting timestamp: {e}")
            raise ValueError

        return creation_timestamp, creation_block_number, creation_hash