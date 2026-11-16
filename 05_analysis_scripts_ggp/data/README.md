# Workshop 5 data

25 real pilot participants from the lab's gestalt grouping study (GGP2026 Replication,
Repetition Discrimination Task), drawn at random from the pilot sessions, with two
participants kept on purpose because their sessions show problems worth discussing.

- **IDs are new random codes** (`101`–`998`). The key to the original IDs is held by the
  instructor, outside this repository.
- `age` and `sex` were removed. Every other column and every row is exactly what the
  experiment wrote.
- 22 participants ran 3 blocks (720 trials). 3 early pilots ran 5 blocks (1,200 trials).
- `RDTdata_999.csv` is the debug ID's file: a header and no trials. It's left in on
  purpose, because real data folders contain files like it.

Please keep these files inside the workshop: don't share or post them.

## Files

| File | Written by | Rows |
|---|---|---|
| `rawdata/RDTdata_<id>.csv` | the experiment (`RDT02_Lab.py`, PsychoPy) | one per trial |
| `rawdata/RDTdata_999.csv` | a debug run | none |

## Columns

| column | meaning |
|---|---|
| `subjectId` | participant code (re-coded for this workshop). Read it as text. |
| `block` | block number, from 1 |
| `trial` | trial number within the block, restarting at 1 (240 per block) |
| `trialID` | which of the 240 conditions (1–240) |
| `cueType` | `PROX`, `SIM`, `CR`, `EC`, `COMMONFATE`, `SYNCHRONY`, `IPG`, or `NEUTRAL` (no cue) |
| `wbn` | `WITHIN` (repeated pair inside one group), `BETWEEN` (split across two), or `NEUTRAL` |
| `targPos` | position of the repeated pair (3–6) |
| `colorCond` | `BLACK` or `WHITE` items |
| `ipgColor` | flanker gray for IPG trials (`DARKGRAY`/`LIGHTGRAY`; recorded on every trial) |
| `targType` | which shape repeated: `SQUARE` or `CIRCLE` |
| `resp` | the shape the participant chose |
| `ac` | 1 = correct, 0 = wrong |
| `rt` | reaction time in **seconds**, from a clock started just before the display |

Each block has 240 trials: 16 NEUTRAL + 7 cues × 2 (WITHIN/BETWEEN) × 16, in random order.
