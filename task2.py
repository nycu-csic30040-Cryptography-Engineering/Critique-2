import argparse
from typing import List, Sequence, Tuple

from task1 import (
    build_merkle_tree_from_blocks,
    merkle_root,
    parse_trusted_tree_bytes,
    read_binary_file,
    split_into_blocks,
    tree_height,
)

def locate_error(
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Task2: Efficient Error Localization.")
    parser.add_argument("--corrupted", default="test_128mb_corrupted.bin", help="Corrupted 128MB file")
    parser.add_argument("--trusted-tree", default="trusted_merkle_tree.bin", help="Trusted full merkle tree .bin")
    args = parser.parse_args()

    trusted_tree = parse_trusted_tree_bytes(read_binary_file(args.trusted_tree))
    corrupted_blocks = split_into_blocks(read_binary_file(args.corrupted))
    corrupted_tree = build_merkle_tree_from_blocks(corrupted_blocks)

    block_index, comparison_count = locate_error(trusted_tree, corrupted_tree)
    expected = tree_height(len(corrupted_blocks))

    print("Task 2 - Efficient Error Localization")
    print(f"Trusted Merkle root: {merkle_root(trusted_tree).hex()}")
    print(f"Corrupted file root: {merkle_root(corrupted_tree).hex()}")
    print(f"Corrupted block index: {block_index}")
    print(f"Comparison count: {comparison_count}")
    print(f"Expected H=log2(n): {expected}")
    print(f"Comparison count equals H: {comparison_count == expected}")


if __name__ == "__main__":
    main()
