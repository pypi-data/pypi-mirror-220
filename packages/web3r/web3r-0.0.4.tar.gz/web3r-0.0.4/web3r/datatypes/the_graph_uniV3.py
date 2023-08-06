from dataclasses import dataclass
from typing import Optional

@dataclass
class TheGraphUniswapV3Pool:
    address: str
    liquidity: str
    created_at_timestamp: str
    created_at_block_number: str
    total_value_locked_token1: str
    sqrt_price: str
    tick: Optional[int]
    token0_address: str
    token0_symbol: str
    token0_totalSupply: int
    token1_address: str
    token1_symbol: str
    token1_totalSupply: int
    fee_tier: int

    def __repr__(self):
        return f'TheGraphUniswapV3Pool(id={self.address}, liquidity={self.liquidity}, created_at_timestamp={self.created_at_timestamp}, created_at_block_number={self.created_at_block_number}, total_value_locked_token1={self.total_value_locked_token1}, sqrt_price={self.sqrt_price}, tick={self.tick}, token0_address={self.token0_address}, token0_symbol={self.token0_symbol}, token0_totalSupply={self.token0_totalSupply}, token1_address={self.token1_address}, token1_symbol={self.token1_symbol}, token1_totalSupply={self.token1_totalSupply}, fee_tier={self.fee_tier})'