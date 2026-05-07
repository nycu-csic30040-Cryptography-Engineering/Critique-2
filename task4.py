import argparse

from utils.merkle_utils import (
    BLOCK_SIZE,
    NUM_BLOCKS,
    build_merkle_tree_from_blocks,
    locate_error_path,
    merkle_root,
    parse_trusted_tree_bytes,
    read_binary_file,
    replace_node_path_update,
    split_into_blocks,
)
from utils.parity_utils import (
    parity_block_index_for_data_block,
    read_parity_blocks,
    recover_block,
    sibling_index,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Task4: Advanced Self-Healing Correction module.")
    parser.add_argument("--corrupted", default="test_128mb_corrupted.bin", help="Corrupted 128MB file")
    parser.add_argument("--trusted-tree", default="trusted_merkle_tree.bin", help="Trusted full Merkle tree")
    parser.add_argument("--parity", default="parity_blocks.bin", help="Parity blocks file")
    args = parser.parse_args()

    trusted_tree = parse_trusted_tree_bytes(read_binary_file(args.trusted_tree))
    corrupted_blocks = split_into_blocks(read_binary_file(args.corrupted))
    corrupted_tree = build_merkle_tree_from_blocks(corrupted_blocks)

    corrupted_index, comparison_count = locate_error_path(trusted_tree, corrupted_tree)
    parity_index = parity_block_index_for_data_block(corrupted_index)
    sib_index = sibling_index(corrupted_index)

    parity_blocks = read_parity_blocks(
        read_binary_file(args.parity), block_size=BLOCK_SIZE, num_parity_blocks=NUM_BLOCKS // 2
    )
    repaired_block = recover_block(parity_blocks[parity_index], corrupted_blocks[sib_index])

    repaired_tree = [list(level) for level in corrupted_tree]
    repaired_root = replace_node_path_update(repaired_tree, corrupted_index, repaired_block)

    print("Task 4 - Advanced Self-Healing")
    print(f"Trusted Merkle root: {merkle_root(trusted_tree).hex()}")
    print(f"Corrupted file root: {merkle_root(corrupted_tree).hex()}")
    print(f"Corrupted block index: {corrupted_index}")
    print(f"Comparison count: {comparison_count}")
    print(f"Parity block index used for recovery: {parity_index}")
    print(f"Sibling block index: {sib_index}")
    print(f"Repaired Merkle root: {repaired_root.hex()}")
    print(f"Repaired root equals trusted root: {repaired_root == merkle_root(trusted_tree)}")


if __name__ == "__main__":
    main()
