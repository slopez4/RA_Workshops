"""
Project:       RA Workshops, Workshop 6 (copied from the Dispupil
               study; study-agnostic: see STUDY_CONVENTIONS.md, section 18)
Script:        06_advanced_psychopy/counterbalancing.py
               (in a study repo it lives in experiment_files/)
Creator:       <name> (AI-assisted: Claude, see AI_Disclosure.md)
Purpose:       Reads and updates the counterbalancing sheet. The experiment
               imports it to give each new participant a condition; the crash
               report imports it to exclude a participant and reopen their
               configuration. It is the only code that writes to the sheet.
Last updated:  2026-11-15

Usage:
    from counterbalancing import assign, mark_complete      (in the experiment)
    python experiment_files/counterbalancing.py --status    counts per condition
    python experiment_files/counterbalancing.py --new A B --n 40
                                                            new sheet: 40 slots,
                                                            conditions A and B
                                                            alternating

Dependencies:  Python standard library only
Reads:         experiment_files/counterbalancing.csv
Writes:        experiment_files/counterbalancing.csv
               experiment_files/counterbalancing_backups/counterbalancing_<timestamp>.csv
"""

import argparse
import csv
import os
import re
import shutil
import sys
from datetime import datetime

# Paths are resolved from this file's own location, never the working
# directory (STUDY_CONVENTIONS.md, section 1).
HERE = os.path.dirname(os.path.abspath(__file__))
SHEET_PATH = os.path.join(HERE, "counterbalancing.csv")
BACKUP_DIR_NAME = "counterbalancing_backups"

# One row per slot. File order is the order slots are filled.
COLUMNS = [
    "Slot",              # unique slot number, never reused
    "Condition",         # the counterbalancing configuration for this slot
    "Participant",       # study code of whoever filled the slot ("" if open)
    "Status",            # open | assigned | complete | excluded
    "Assigned_At",       # when the experiment gave this slot out
    "Replaces_Slot",     # slot whose lost data this row makes up for ("" if none)
    "Exclusion_Reason",  # one of crash_report.REASONS
    "Exclusion_Notes",   # free text from the RA: what happened, no names
    "Excluded_By",       # RA initials
    "Excluded_At",       # when the crash report was filed
]

OPEN, ASSIGNED, COMPLETE, EXCLUDED = "open", "assigned", "complete", "excluded"

# Reserved participant IDs (STUDY_CONVENTIONS.md, section 2). Neither kind
# takes a counterbalancing slot.
PILOT_FIRST, PILOT_LAST = 1, 100   # piloting
DEBUG_ID = 999                     # debugging, always excluded from analysis


class SheetError(Exception):
    """A problem the RA can fix (missing sheet, sheet open in Excel, ...)."""


# --------------------------------------------------------------------------
# Participant IDs
# --------------------------------------------------------------------------

def id_number(subid):
    """Return the numeric part of a participant ID ("A101" -> 101), or None."""
    digits = re.sub(r"\D", "", str(subid))
    return int(digits) if digits else None


def id_kind(subid):
    """Classify an ID as "debug", "pilot", "real" or "unknown" (no digits)."""
    number = id_number(subid)
    if number is None:
        return "unknown"
    if number == DEBUG_ID:
        return "debug"
    if PILOT_FIRST <= number <= PILOT_LAST:
        return "pilot"
    return "real"


def same_id(a, b):
    """Compare IDs as text, ignoring case and surrounding spaces.

    IDs are never compared as numbers, so "0101" and "101" stay different
    participants and leading zeros are never silently dropped.
    """
    return str(a).strip().lower() == str(b).strip().lower()


# --------------------------------------------------------------------------
# Reading and writing the sheet
# --------------------------------------------------------------------------

def _now():
    """Timestamp used in the sheet (local time, to the second)."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load(path=None):
    """Read the sheet and return its rows as a list of dicts (all strings)."""
    path = path or SHEET_PATH
    if not os.path.exists(path):
        raise SheetError(
            "No counterbalancing sheet at:\n  %s\n"
            "The experiment never picks a condition without it." % path)
    # utf-8-sig tolerates the byte-order mark Excel adds if someone re-saved
    # the sheet by hand.
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise SheetError("The counterbalancing sheet is missing column(s): "
                             + ", ".join(missing))
        rows = [{c: (row.get(c) or "").strip() for c in COLUMNS} for row in reader]
    for row in rows:
        row["Status"] = row["Status"].lower()
        if row["Status"] not in (OPEN, ASSIGNED, COMPLETE, EXCLUDED):
            raise SheetError("Slot %s has an unknown Status: %r"
                             % (row["Slot"], row["Status"]))
    return rows


def save(rows, path=None):
    """Write the sheet back, keeping a timestamped backup of the old version.

    The new sheet is written to a temporary file first and only then swapped
    in, so a crash or a locked file can never leave a half-written sheet.
    """
    path = path or SHEET_PATH
    folder = os.path.dirname(path)
    tmp = path + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    try:
        if os.path.exists(path):
            backup_dir = os.path.join(folder, BACKUP_DIR_NAME)
            os.makedirs(backup_dir, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            shutil.copy2(path, os.path.join(
                backup_dir, "counterbalancing_%s.csv" % stamp))
        os.replace(tmp, path)
    except PermissionError:
        # On Windows this is what happens when the sheet is open in Excel.
        os.remove(tmp)
        raise SheetError("Could not write the counterbalancing sheet. "
                         "Close it in Excel and try again. Nothing was changed.")


def find_active(rows, subid):
    """Return the participant's assigned/complete row, or None."""
    for row in rows:
        if same_id(row["Participant"], subid) and row["Status"] in (ASSIGNED, COMPLETE):
            return row
    return None


# --------------------------------------------------------------------------
# What the experiment calls
# --------------------------------------------------------------------------

def assign(subid, path=None):
    """Give a participant their condition and return it.

    A new participant takes the first open row, top to bottom. A participant
    who already holds a slot (a resumed session) gets the same condition back,
    so it cannot drift between runs.
    """
    kind = id_kind(subid)
    if kind != "real":
        raise SheetError("ID %s is a %s ID and takes no counterbalancing slot."
                         % (subid, kind))
    rows = load(path)
    current = find_active(rows, subid)
    if current:
        return current["Condition"]
    if any(same_id(r["Participant"], subid) for r in rows):
        # Only excluded rows are left for this ID.
        raise SheetError("Participant %s was excluded in a crash report. "
                         "Run the session again under a new ID." % subid)
    for row in rows:
        if row["Status"] == OPEN:
            row["Participant"] = str(subid).strip()
            row["Status"] = ASSIGNED
            row["Assigned_At"] = _now()
            save(rows, path)
            return row["Condition"]
    raise SheetError("Every slot in the counterbalancing sheet is taken. "
                     "Add rows before running another participant.")


def mark_complete(subid, path=None):
    """Mark a participant's slot complete (call at the end of the last block)."""
    rows = load(path)
    row = find_active(rows, subid)
    if row is None:
        raise SheetError("Participant %s holds no slot in the sheet." % subid)
    row["Status"] = COMPLETE
    save(rows, path)


# --------------------------------------------------------------------------
# What the crash report calls
# --------------------------------------------------------------------------

def exclude(subid, reason, notes, excluded_by, path=None):
    """Exclude a participant and reopen their configuration.

    The participant's row is kept and marked excluded. A new open row with the
    same Condition is placed at the front of the open queue, so the very next
    participant makes up the lost data. Returns (excluded_row, new_row).
    """
    rows = load(path)
    row = find_active(rows, subid)
    if row is None:
        raise SheetError("Participant %s holds no slot that can be excluded."
                         % subid)
    row["Status"] = EXCLUDED
    row["Exclusion_Reason"] = reason
    row["Exclusion_Notes"] = notes
    row["Excluded_By"] = excluded_by
    row["Excluded_At"] = _now()

    new_row = {c: "" for c in COLUMNS}
    new_row["Slot"] = str(max(int(r["Slot"]) for r in rows) + 1)
    new_row["Condition"] = row["Condition"]
    new_row["Status"] = OPEN
    new_row["Replaces_Slot"] = row["Slot"]

    # Front of the open queue = just before the first open row.
    first_open = next((i for i, r in enumerate(rows) if r["Status"] == OPEN),
                      len(rows))
    rows.insert(first_open, new_row)
    save(rows, path)
    return row, new_row


def counts(rows):
    """Return {condition: {"counted": n, "excluded": n, "open": n}}.

    "Counted" means assigned or complete: data that is in, or coming in.
    """
    table = {}
    for row in rows:
        c = table.setdefault(row["Condition"],
                             {"counted": 0, "excluded": 0, "open": 0})
        if row["Status"] in (ASSIGNED, COMPLETE):
            c["counted"] += 1
        else:
            c[row["Status"]] += 1
    return table


def counts_text(rows):
    """The counts as a few lines of text, for dialogs and the terminal."""
    lines = []
    for condition, c in counts(rows).items():
        lines.append("%s: %d counted, %d excluded, %d open"
                     % (condition, c["counted"], c["excluded"], c["open"]))
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------

def new_sheet(conditions, n, path=None):
    """Create a sheet of n open slots, cycling through the conditions."""
    path = path or SHEET_PATH
    if os.path.exists(path):
        raise SheetError("A sheet already exists at %s. It is never overwritten."
                         % path)
    rows = []
    for i in range(n):
        row = {c: "" for c in COLUMNS}
        row.update(Slot=str(i + 1), Condition=conditions[i % len(conditions)],
                   Status=OPEN)
        rows.append(row)
    save(rows, path)


def main():
    parser = argparse.ArgumentParser(description="Counterbalancing sheet tools.")
    parser.add_argument("--sheet", default=None, help="path to the sheet "
                        "(default: counterbalancing.csv next to this script)")
    parser.add_argument("--status", action="store_true",
                        help="print the counts per condition")
    parser.add_argument("--new", nargs="+", metavar="CONDITION",
                        help="create a new sheet with these conditions")
    parser.add_argument("--n", type=int, default=40,
                        help="number of slots for --new (default 40)")
    args = parser.parse_args()
    try:
        if args.new:
            new_sheet(args.new, args.n, args.sheet)
            print("Created %d slots." % args.n)
        print(counts_text(load(args.sheet)))
    except SheetError as err:
        sys.exit(str(err))


if __name__ == "__main__":
    main()
