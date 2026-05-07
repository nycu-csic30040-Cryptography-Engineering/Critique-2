import argparse
import time

from utils.merkle_utils import (
    build_merkle_tree_from_blocks,
    internal_nodes_memory_overhead,
    merkle_root,
    read_binary_file,
    sha256,
    split_into_blocks,
)


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
