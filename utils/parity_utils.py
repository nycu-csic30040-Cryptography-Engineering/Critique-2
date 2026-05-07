from typing import Sequence


def xor_blocks(block_a: bytes, block_b: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(block_a, block_b))


def recover_block(parity_block: bytes, sibling_block: bytes) -> bytes:
    return xor_blocks(parity_block, sibling_block)


def parity_block_index_for_data_block(block_index: int) -> int:
    return block_index // 2


def sibling_index(block_index: int) -> int:
    if block_index % 2 == 0:
        return block_index + 1
    return block_index - 1


def read_parity_blocks(raw: bytes, block_size: int, num_parity_blocks: int) -> Sequence[bytes]:
    expected = block_size * num_parity_blocks
    if len(raw) != expected:
        raise ValueError(f"parity_blocks.bin size mismatch: expected {expected}, got {len(raw)}")
    return [raw[i * block_size : (i + 1) * block_size] for i in range(num_parity_blocks)]
