# Ethics and Data Note
Owner: Sarim, Hassan Zahid · updated 11 Nov 2026 from Progress Report 2 (section A.5, data statement)

## Datasets
| | UCI Heart Disease – Cleveland | Edinburgh Myocardial Infarction |
|---|---|---|
| Reference | Detrano et al. (1989), *Am. J. Cardiology* 64(5) | Kennedy et al. (1996), *Eur. Heart J.* 17(8) |
| Where we get it | https://archive.ics.uci.edu/dataset/45/heart+disease (`processed.cleveland.data`) | Public copy distributed with Kim et al. (2018): github.com/kimandrik/IDASH2017 (`edin.txt`) |
| Licence | UCI: CC BY 4.0 | Repository licence CC BY-NC 3.0 (CryptoLab) – non-commercial academic use only; cite Kennedy et al. and Kim et al. |
| Size | 303 rows → 297 after dropping missing values; 13 features + label | 1,253 rows; 9 binary features + label |
| Personal data? | No – de-identified, public | No – de-identified, public; columns anonymised (x1–x9) |
| In git? | No (downloaded by script to `code/data/raw/`, git-ignored) | No (same) |

Results for the two datasets are reported separately, never pooled (different variables).

## IRB
- **Needed? No.** Both datasets are public and fully de-identified; no data are collected from
  people and there are no human participants. The demo uses only test-set rows. (PR2, data statement.)
- Supervisor meeting of 1 Oct discussed this; record the supervisor's exact words in
  `meetings/MEETING_NOTES.md` if they differ.

## SLR records
Titles and abstracts exported from IEEE Xplore and Scopus through UDST Library access are for
review use only. **Note (11 Nov):** PR2 calls the repository private, but on 11 Nov GitHub served it
to anonymous visitors, i.e. it is **public**. Either make it private (Settings → General → Danger
Zone → Change visibility) or remove the database exports and report PDFs before they stay public.
