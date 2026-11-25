# Baseline paper: Haq, Chen and Chen (2025)

*Privacy-Preserving Classification of Medical Tabular Data with Homomorphic Encryption.* Algorithms 18(12), 731.
https://doi.org/10.3390/a18120731 · Open access, CC BY 4.0 · PDF: [`Haq_2025_Algorithms_18_731.pdf`](Haq_2025_Algorithms_18_731.pdf)
Sent to the group by Naif. This is the work we take as our reference point (see [`planning/project-direction.md`](../../planning/project-direction.md)).

## What they did
CKKS (TenSEAL 0.3.16, i.e. the same version we pin) inference for LR, linear SVM, a one-hidden-layer MLP
(square activation) and two hybrids (MLP initialised from LR / SVM weights) on Wisconsin breast cancer
(569 rows, 114 test) and Cleveland heart disease (297 rows, 60 test). The sigmoid is **not** computed under
encryption: the server returns the weighted sum and the client decides after decryption.

## Numbers we can compare against (same machine needed, see direction §3)
| Item | Haq et al. | Ours (PR2 / 11 Nov run) |
|---|---|---|
| CKKS setting | N = 8192, chain 31,26×6,31, scale 2^26, one setting for all models | N = 16384, chain 60,40,40,40,40,60, scale 2^40 |
| Sigmoid | After decryption | Encrypted least-squares cubic (also supported: logit only) |
| Encrypted request | ≈ 477 KB per sample (all models) | ≈ 1.0 MB per feature, 13 per patient |
| Encrypted response | 410 KB (LR/SVM), 276 KB (MLP) | not yet measured separately |
| LR inference, whole test set | 15.6 s (114 samples) / 4.7 s (60 samples) | ≈ 88–213 ms per patient |
| Hardware | Google Colab, A100 GPU (SEAL does not use it) | Windows 11, Intel CPU |
| Accuracy loss from encryption | None at their base setting; collapses at scale 2^24 / 2^22 (Table 10) | None in the pilot (0.853 = 0.853) |

## What we take from it
- Their parameter sweep (Tables 8–10) is direct evidence that **scale and chain length matter** and that
  too-small values destroy accuracy. We must sweep, not guess.
- They only report one setting per model and call parameter choice "intuitive and iterative"; they list
  automated parameter selection as future work. Our levers L1–L3 address exactly that.
- Their keys stay at the hospital; ours are made in the browser and uploaded, so key size is a bigger
  issue for us.

## Cautions
1. **Cleveland Table 3 is internally inconsistent.** LR recall 0.6786 and precision 0.8261 imply TP = 19,
   FN = 9, FP = 4 on a 60-patient test set, which gives specificity 0.875 and accuracy 0.783 – the paper
   prints 0.7768 and 0.7883. Their "AUC" values in Fig. 4 also equal the printed specificities, and the ROC
   curves have a single bend, i.e. they were drawn from hard 0/1 predictions. Treat their Cleveland
   figures as indicative only. (Our own re-derivation from the paper's tables; worth one more check by a second person.)
2. Test sets are tiny (60 and 114); one patient moves accuracy by 1.7 and 0.9 points.
3. Their results for the hybrid models show no gain from encryption and no ablation of the initialisation;
   the "hybrid beats MLP" claim rests on one split.
4. Compression is not mentioned. Their ciphertext sizes (≈ 477 KB for N = 8192 and 7 data primes, where raw would be about 0.9 MB) suggest TenSEAL's default zstd is already on.
5. Time is not split into encrypt / compute / decrypt, so we cannot compare per phase.
