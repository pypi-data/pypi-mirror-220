# Import the required modules and classes
from web3 import Web3
from web3.providers import BaseProvider
from etherscan import Etherscan
from web3r.pricer import Pricer
from web3r.utils import Utils
from web3r.the_graph_uniswapV3 import TheGraphUniswapV3
from web3r.tokens import Tokens

class Web3R(Web3):
    """
    Main client class that wraps Web3 and Etherscan, and adds additional functionality for research.
    """
    
    def __init__(self, web3_provider: BaseProvider, etherscan_api_token: str) -> None:
        """
        Initialize an instance of Web3R.

        :param web3_provider: A provider that should be used for the connection.
        :param etherscan_api_token: The API token for Etherscan.
        """
        self.web3 = Web3(web3_provider)  # Composition: Web3R "has a" Web3
        self.etherscan = Etherscan(etherscan_api_token)  # Composition: Web3R "has a" Etherscan
        
        #Initialising the graph
        self.grph_uniV3 = TheGraphUniswapV3(self.web3)

        #Initiating a Utility Class to be used in the below children. 
        self.utils = Utils(self.web3, self.etherscan)

        self.tokens = Tokens(self.web3, self.etherscan, self.utils) 
        self.pricer = Pricer(self.web3, self.etherscan, self.utils, self.tokens, self.grph_uniV3) #Tokens passed to pricer are 'priced'



    def is_connected(self) -> bool:
        """
        Checks if the Web3 and Etherscan instances are connected and available.

        :return: True if both services are available, False otherwise.
        """
        try:
            return self.web3.isConnected() and self.etherscan.get_eth_supply() is not None
        except Exception:
            return False
        
#