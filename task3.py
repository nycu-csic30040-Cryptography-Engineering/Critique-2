import argparse
import time

from utils.merkle_utils import (
    build_merkle_tree_from_blocks,
    merkle_root,
    read_binary_file,
    replace_node_path_update,
    split_into_blocks,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Task3: Efficient Node Replacement.")
    parser.add_argument("index", type=int, help="Block index to replace (0~127)")
    args = parser.parse_args()

    if not (0 <= args.index < 128):
        raise ValueError("Block index must be in range 0~127")

    original_blocks = split_into_blocks(read_binary_file("test_128mb.bin"))
    replacement_block = read_binary_file("test_1mb.bin")
    if len(replacement_block) != 1024 * 1024:
        raise ValueError("Replacement block must be exactly 1MB")

    base_tree = build_merkle_tree_from_blocks(original_blocks)
    original_root = merkle_root(base_tree)

    blocks_for_path = list(original_blocks)
    blocks_for_path[args.index] = replacement_block
    tree_for_path = [list(level) for level in base_tree]

    t_path_0 = time.perf_counter()
    path_root = replace_node_path_update(tree_for_path, args.index, replacement_block)
    path_elapsed = time.perf_counter() - t_path_0

    t_full_0 = time.perf_counter()
    full_root = merkle_root(build_merkle_tree_from_blocks(blocks_for_path))
    full_elapsed = time.perf_counter() - t_full_0

    speedup = full_elapsed / path_elapsed if path_elapsed > 0 else float("inf")

    print("Task 3 - Efficient Node Replacement")
    print(f"Original Merkle root: {original_root.hex()}")
    print(f"Updated root (replace_node path update): {path_root.hex()}")
    print(f"Updated root (full reconstruction): {full_root.hex()}")
    print(f"Roots identical: {path_root == full_root}")
    print(f"replace_node() time (s): {path_elapsed:.6f}")
    print(f"Full reconstruction time (s): {full_elapsed:.6f}")
    print(f"Speedup factor (full/path): {speedup:.2f}")


if __name__ == "__main__":
    main()
