# PubMed search notes – Sarim

Where: PubMed → **Advanced search**. Copy the string exactly from [search-strings.md](../../../research/slr/search-strings.md).

PubMed replaced ACM Digital Library on 10 Oct 2026 (see [SLR_Protocol_v4_changes.md](../../../research/slr/SLR_Protocol_v4_changes.md)).

## Exact string used

```
("homomorphic encryption"[tiab] OR "fully homomorphic"[tiab] OR FHE[tiab] OR CKKS[tiab] OR BFV[tiab] OR BGV[tiab] OR TenSEAL[tiab] OR "Microsoft SEAL"[tiab]) AND ("machine learning"[tiab] OR "logistic regression"[tiab] OR "neural network"[tiab] OR "deep learning"[tiab] OR classif*[tiab] OR predict*[tiab] OR inference[tiab]) AND (health*[tiab] OR medical[tiab] OR biomedical[tiab] OR clinical[tiab] OR patient*[tiab] OR disease*[tiab] OR diagnos*[tiab] OR genom*[tiab] OR cancer[tiab] OR diabet*[tiab] OR "heart disease"[tiab] OR cardiovascular[tiab]) AND 2016:2026[dp] AND english[la]
```

## Run record

| Item | Value |
|---|---|
| Date run (test) | 10 Oct 2026 |
| Result count (test) | 176 – a [tw] variant, tested and not used |
| Date run (logged) | 10 Oct 2026 |
| Filters applied | In the string: 2016:2026[dp], english[la] |
| Result count (logged) | 172 |
| Confirmed by partner (same-day re-run) + their count | Hassan (172) |
| Export file / format | [`PubMed_2026-10-10.nbib`](../../../research/slr/exports/PubMed_2026-10-10.nbib) (NBIB, 172 records) |

## Changes made (with reason)

| Date | Change | Reason | Agreed with |
|---|---|---|---|
| 10 Oct 2026 | ACM Digital Library replaced by PubMed | UDST has no ACM subscription; filters and export were locked | Team |
| 10 Oct 2026 | Used `[tiab]` (title/abstract), not `[tw]` | The [tw] variant (176 results) was tested and not used | Team |

If the string changes, paste the new exact string in the Search Log tab of the live PRISMA sheet too.
