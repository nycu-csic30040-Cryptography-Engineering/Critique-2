import argparse
import time
import hashlib
import math
from typing import List, Sequence, Tuple

NUM_BLOCKS = 128
BLOCK_SIZE = 1024 * 1024
HASH_SIZE = 32


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def read_binary_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def write_binary_file(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)


def split_into_blocks(data: bytes, num_blocks: int = NUM_BLOCKS, block_size: int = BLOCK_SIZE) -> List[bytes]:
    expected_size = num_blocks * block_size
    if len(data) != expected_size:
        raise ValueError(f"File size mismatch: expected {expected_size}, got {len(data)}")
    return [data[i * block_size : (i + 1) * block_size] for i in range(num_blocks)]


def join_blocks(blocks: Sequence[bytes]) -> bytes:
    return b"".join(blocks)


def build_merkle_tree_from_blocks(blocks: Sequence[bytes]) -> List[List[bytes]]:
    current_level = [sha256(block) for block in blocks]
    tree = [current_level]
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            next_level.append(sha256(current_level[i] + current_level[i + 1]))
        tree.append(next_level)
        current_level = next_level
    return tree


def build_merkle_tree_from_hashes(leaf_hashes: Sequence[bytes]) -> List[List[bytes]]:
    current_level = list(leaf_hashes)
    tree = [current_level]
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            next_level.append(sha256(current_level[i] + current_level[i + 1]))
        tree.append(next_level)
        current_level = next_level
    return tree


def merkle_root(tree: Sequence[Sequence[bytes]]) -> bytes:
    return tree[-1][0]


def tree_height(num_leaves: int) -> int:
    return int(math.log2(num_leaves))


def internal_nodes_memory_overhead(tree: Sequence[Sequence[bytes]]) -> int:
    return sum(len(level) for level in tree[1:]) * HASH_SIZE


def parse_trusted_tree_bytes(raw: bytes, num_blocks: int = NUM_BLOCKS, hash_size: int = HASH_SIZE) -> List[List[bytes]]:
    levels = []
    offset = 0
    nodes = num_blocks
    while nodes >= 1:
        level_size = nodes * hash_size
        level_raw = raw[offset : offset + level_size]
        if len(level_raw) != level_size:
            raise ValueError("trusted_merkle_tree.bin format/size is invalid")
        level = [level_raw[i * hash_size : (i + 1) * hash_size] for i in range(nodes)]
        levels.append(level)
        offset += level_size
        if nodes == 1:
            break
        nodes //= 2
    if offset != len(raw):
        raise ValueError("trusted_merkle_tree.bin has unexpected trailing bytes")
    return levels


def main() -> None:
    parser = argparse.ArgumentParser(description="Task1: Single Hash vs Merkle Tree baseline.")
    parser.add_argument("--input", default="test_128mb.bin", help="Path to 128MB dataset file")
    args = parser.parse_args()

    data = read_binary_file(args.input)
    blocks = split_into_blocks(data)

    t0 = time.perf_counter()
    single_hash = sha256(data)
    single_hash_time = time.perf_counter() - t0

    t1 = time.perf_counter()
    tree = build_merkle_tree_from_blocks(blocks)
    merkle_time = time.perf_counter() - t1

    print("Task 1 - Single Hash vs Merkle Tree")
    print(f"Single hash (SHA-256): {single_hash.hex()}")
    print(f"Single hash time (s): {single_hash_time:.6f}")
    print(f"Merkle root: {merkle_root(tree).hex()}")
    print(f"Merkle tree construction time (s): {merkle_time:.6f}")
    print(f"Internal node memory overhead (bytes): {internal_nodes_memory_overhead(tree)}")


if __name__ == "__main__":
    main()
