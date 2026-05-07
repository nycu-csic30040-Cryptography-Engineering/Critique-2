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


def locate_error_path(
    trusted_tree: Sequence[Sequence[bytes]], current_tree: Sequence[Sequence[bytes]]
) -> Tuple[int, int]:
    if len(trusted_tree) != len(current_tree):
        raise ValueError("Tree height mismatch")
    node_index = 0
    comparison_count = 0
    for level in range(len(trusted_tree) - 1, 0, -1):
        left = node_index * 2
        right = left + 1
        comparison_count += 1
        if trusted_tree[level - 1][left] != current_tree[level - 1][left]:
            node_index = left
        else:
            node_index = right
    return node_index, comparison_count


def replace_node_path_update(tree: List[List[bytes]], block_index: int, new_block: bytes) -> bytes:
    tree[0][block_index] = sha256(new_block)
    node = block_index
    for level in range(1, len(tree)):
        parent = node // 2
        left = parent * 2
        right = left + 1
        tree[level][parent] = sha256(tree[level - 1][left] + tree[level - 1][right])
        node = parent
    return tree[-1][0]
