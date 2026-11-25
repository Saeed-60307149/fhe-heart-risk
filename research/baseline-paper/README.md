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

## Their parameter sweep (Tables 8-10): our main evidence for the cost levers
Wisconsin, logistic regression, N = 8192, scale 2^26, only the number of middle primes changes (Table 9):

| Chain | Time, encrypted test set (s) | Encrypted input (bytes) | Encrypted result (bytes) |
|---|---|---|---|
| Base: 31, 26×6, 31 (8 primes) | 15.60 | 476,922 | 409,928 |
| Set 1: 7 primes | 11.84 | 409,624 | 343,372 |
| Set 2: 6 primes | 8.59 | 343,532 | 276,292 |
| Set 3: 5 primes | 5.88 | 276,395 | 209,971 |

The MLP shows the same trend (280 s down to 105 s). Accuracy stayed at the base-set values for sets 1-3 (their
text, p. 19). Table 10: scale 2^27 or 2^24 and the 22-bit chain change accuracy, and 2^24 and 2^22 collapse it
(e.g. the MLP falls to 0.68 and 0.35). They never vary N. Limits: their hardware, their model, one dataset.

## Their model comparison (Tables 2-5): our evidence for Track 2 (model-side accuracy)
Test accuracy, plaintext = CKKS in every row (no loss at their base setting). Same encrypted time ordering on both datasets.

| Model | Wisconsin accuracy (114 test) | Wisconsin encrypted time (s) | Cleveland accuracy (60 test) | Cleveland encrypted time (s) |
|---|---|---|---|---|
| LR | 0.9211 | 15.60 | 0.7883 | 4.71 |
| Linear SVM | 0.9649 | 15.66 | 0.7667 | 4.71 |
| MLP (square activation) | 0.9737 | 280.22 | 0.8167 | 65.62 |
| LR-MLP hybrid | 0.9825 | 279.81 | 0.8667 | 66.28 |
| SVM-MLP hybrid | 0.9825 | 285.51 | 0.8667 | 66.56 |

Reading: the MLP and hybrids are more accurate but about 18x (Wisconsin) and 14x (Cleveland) slower under encryption.
Cautions: single 80/20 split, test sets of 60 and 114 patients, the Cleveland table is internally inconsistent
(see Cautions above), no ablation of the hybrid initialisation. This is suggestive evidence, not proof.

