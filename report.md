# Project 2 Implementation Report

## 1. Objective

This project implements a Dynamic Merkle Tree workflow for a 128MB dataset split into 128 blocks (1MB each).  
The goals are:

1. Compare single-file hashing and Merkle-tree hashing.
2. Locate one corrupted block efficiently.
3. Update one modified block efficiently.
4. Recover one corrupted block using parity and re-verify integrity.

## 2. Environment and Inputs

- Language: Python 3
- Hash function: SHA-256
- Data files:
  - `test_128mb.bin`
  - `test_128mb_corrupted.bin`
  - `test_1mb.bin`
  - `trusted_merkle_tree.bin`
  - `parity_blocks.bin`
- Merkle tree settings:
  - Number of blocks: 128
  - Block size: 1MB
  - Tree height: `log2(128) = 7`

## 3. Methods

### Task 1 - Single Hash vs. Merkle Tree

- Compute one SHA-256 hash for the whole 128MB file.
- Build the full Merkle tree from 128 leaf hashes.
- Measure:
  - Single hash time
  - Full Merkle tree construction time
  - Internal node memory overhead

### Task 2 - Efficient Error Localization

- Build Merkle tree from corrupted file.
- Load trusted full tree from `trusted_merkle_tree.bin`.
- Use top-down comparison:
  - Compare child hashes at each level.
  - Move to the mismatched child only.
- Record:
  - Corrupted block index
  - Number of comparisons

### Task 3 - Efficient Node Replacement

- Replace one block using `test_1mb.bin`.
- Compute updated root with two methods:
  1. Path update (`replace_node`) from leaf to root.
  2. Full tree reconstruction.
- Measure both runtimes and speedup.

### Task 4 - Advanced Self-Healing

- Locate corrupted block (same method as Task 2).
- Recover corrupted block with XOR parity:
  - `Recovered = Parity XOR Sibling`
- Update Merkle path and compute repaired root.
- Verify repaired root equals trusted root.

## 4. Experimental Results

The following values are collected from one full execution:

- **Task 1**
  - Single hash: `0c05acf58bb36284a9e73f0222f2fd0621954bb8eb5c16ee50a45341b5cd4594`
  - Single hash time: `0.063371 s`
  - Merkle root: `3cd74d8d7171cce47fb900a1aca739b74286b6f84e5da9490f54559dbecc8668`
  - Merkle tree time: `0.063545 s`
  - Internal node overhead: `4064 bytes`

- **Task 2**
  - Corrupted block index: `37`
  - Comparison count: `7`
  - Expected height `H`: `7`
  - Check `comparison_count == H`: `True`

- **Task 3**
  - Updated root (path update): `429aa1c65eadf7c4a2773ff5770c49de2f450db8f47ea7488778b13c781ab66b`
  - Updated root (full rebuild): `429aa1c65eadf7c4a2773ff5770c49de2f450db8f47ea7488778b13c781ab66b`
  - Roots identical: `True`
  - Path update time: `0.000427 s`
  - Full rebuild time: `0.054026 s`
  - Speedup (full/path): `126.58x`

- **Task 4**
  - Corrupted block index: `37`
  - Comparison count: `7`
  - Parity block index: `18`
  - Sibling block index: `36`
  - Repaired root: `3cd74d8d7171cce47fb900a1aca739b74286b6f84e5da9490f54559dbecc8668`
  - Repaired root equals trusted root: `True`

## 5. Required Comparison Table (n = 2^7 blocks)

| Operation | Single Hash | Merkle Tree | Improvement Factor |
|---|---:|---:|---:|
| Detecting Error | Scans 128 MB | Scans about 1 MB (target block + hash path verification) | ~128x less data |
| Localizing Error | Impossible | 7 comparisons | From impossible to O(log n) |
| Updating 1 Block | Computes 128 MB | Computes about 1 MB + 7 hash recomputations | ~128x less data |
| Proof Size (Bytes) | Not practical for block proof | `7 * 32 = 224` bytes | Compact logarithmic proof |

Note: The table reports the algorithmic behavior for dynamic update/verification.  
Measured runtime results are shown in Section 4.

## 6. Discussion

The implementation confirms the expected benefit of Merkle trees in large systems:

1. **Error localization is efficient**: only one branch is checked per level (`O(log n)`).
2. **Single-block update is efficient**: only one leaf-to-root path is recomputed.
3. **Self-healing is possible** with parity + trusted Merkle structure, even without the clean original file.

Single hash remains simple for full-file integrity checks, but it is not suitable when the system requires localization, partial update, and block-level recovery.

## 7. Conclusion

All four required tasks are implemented and verified on the 128MB dataset.  
The results show correct corruption detection, exact corrupted-block localization, efficient root update, and successful parity-based recovery with final root consistency.
