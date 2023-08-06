from dataclasses import dataclass

@dataclass
class Transfer:
    address: str
    from_address: str
    to: str
    quantity: int
    block_number: int
    transaction_hash: str

    def __repr__(self):
        return f'Transfer(address={self.address}, from_address={self.from_address}, to={self.to}, quantity={self.quantity}, block_number={self.block_number}, transaction_hash={self.transaction_hash})'
