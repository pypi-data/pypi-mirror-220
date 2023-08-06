from typing import Optional
from dataclasses import dataclass

@dataclass
class Token:
    address: Optional[str] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    decimals: Optional[int] = None
    total_supply: Optional[int] = None
    block_timestamp: Optional[int] = None
    block_number: Optional[int] = None
    block_hash: Optional[str] = None

    def __repr__(self):
        return f'Token(address={self.address}, symbol={self.symbol}, name={self.name}, decimals={self.decimals}, total_supply={self.total_supply}, block_timestamp={self.block_timestamp}, block_number={self.block_number}, block_hash={self.block_hash})'
