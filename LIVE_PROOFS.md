# StudioNet proofs

Current contract: [0xE77438Dcf0E931eC869ee4D5Ef6DF3F1F2bEAb97](https://explorer-studio.genlayer.com/address/0xE77438Dcf0E931eC869ee4D5Ef6DF3F1F2bEAb97). Explorer source was read back and compared with `contracts/CurriculumDriftSentinel.py`; the source text matches. Each cited transaction is FINALIZED with `MAJORITY_AGREE` and successful leader execution. Validator receipts marked `idle` are not state-changing errors.

| Step | Finalized transaction | Observed result |
| --- | --- | --- |
| Deploy | [0xbeff97…cd6c11](https://explorer-studio.genlayer.com/tx/0xbeff978e54d5355aaafa4cf849ded160963d05ef597f409e45ed213708cd6c11) | Corrected source published. |
| Register material-change policy | [0x7f10ee…93b53](https://explorer-studio.genlayer.com/tx/0x7f10ee153f0007cd57b89b2f214766e839e5bfb9112f819baf275a0086093b53) | Hash-pinned baseline and current-document URLs stored. |
| Material-change audit | [0x6d9488…7f3bc](https://explorer-studio.genlayer.com/tx/0x6d9488edfa3e4425848a3dbe76512994b6c7c3a1c19bdd890f8030be6637f3bc) | Both sources returned 200; baseline SHA-256 matched; `method=UNCHANGED`, `evidence=MATERIAL`; policy `PAUSED`, round 1. |
| Register unchanged control | [0x290c4d…06c03](https://explorer-studio.genlayer.com/tx/0x290c4d84daee926af50f222018d9ce3f9304f07edfe1ad2e21063c9393506c03) | Separate policy references equal-content baseline/current files. |
| Unchanged audit | [0xca0bdb…80c62](https://explorer-studio.genlayer.com/tx/0xca0bdb875ca1b5baab9eae623d6c741e13a4319368296cfb643a2a6f18180c62) | Both hashes equal, every label `UNCHANGED`; `CONTINUE`, policy `ACTIVE`. |
| Register bad-hash control | [0xa438f9…6d5db](https://explorer-studio.genlayer.com/tx/0xa438f99ad818dbdb2163bbc988e19f71a1c5a51ae52ef92a0465da5fe036d5db) | Baseline commitment deliberately incorrect. |
| Bad-hash audit | [0x2d40e6…8438c](https://explorer-studio.genlayer.com/tx/0x2d40e616633e9953532c3b4ae31de9cb15443bffa5c30bad279c0e80e3c8438c) | Fetched baseline hash mismatch; `INCONCLUSIVE`, policy `REVIEW_REQUIRED`, round 1. |

The earlier deployment [0x40908e…FBCf5](https://explorer-studio.genlayer.com/address/0x40908ee1F795AACb29d5026eD3c772a33cCFBCf5) is **superseded**: its inconclusive path did not close the active gate. Its transactions are not offered as proof for the corrected source. Two all-digit-hash CLI attempts on that old deployment also failed execution and are excluded.

All syllabus documents are synthetic test fixtures in `examples/`. `PAUSED` demonstrates an evidence-driven gate, not a claim that a real school changed its course.
