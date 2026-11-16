"""
Project:       RA Workshops, Workshop 6 (copied from the Dispupil
               study; study-agnostic: see STUDY_CONVENTIONS.md, section 18)
Script:        06_advanced_psychopy/crash_report.py
               (in a study repo it lives in experiment_files/)
Creator:       <name> (AI-assisted: Claude, see AI_Disclosure.md)
Purpose:       Lets an RA exclude a participant whose session had a problem,
               with a reason, in under a minute. The participant's row in the
               counterbalancing sheet is marked excluded and a replacement slot
               with the same condition is opened, so the next participant makes
               up the lost data. Raw data is never touched.
Last updated:  2026-11-15

Usage:
    python experiment_files/crash_report.py            pick a participant
    python experiment_files/crash_report.py 104        participant pre-selected
    python experiment_files/crash_report.py --console  terminal prompts, no window
    python experiment_files/crash_report.py --sheet <path>   use another sheet

    From the experiment's existing-participant dialog ("Crash report"):
        import crash_report
        crash_report.run(subid)

Dependencies:  experiment_files/counterbalancing.py
               psychopy (for the dialog; without it the script falls back to
               terminal prompts)
Reads:         experiment_files/counterbalancing.csv
Writes:        experiment_files/counterbalancing.csv (through counterbalancing.py,
               which backs up the old version first)
"""

import argparse
import sys

import counterbalancing as cb

# Fixed list so exclusions can be counted by reason later. Edit per study;
# keep "Other" last (it makes the notes mandatory).
REASONS = [
    "Experiment crashed, could not resume",
    "Eye tracker failure",
    "Other equipment failure",
    "Participant withdrew or ran out of time",
    "Participant did not follow instructions",
    "Experimenter error",
    "Other",
]

NO_NAMES = "Never write names or identifying details, only what happened."


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def candidates(rows):
    """Participants who can be excluded, most recently assigned first."""
    active = [r for r in rows if r["Status"] in (cb.ASSIGNED, cb.COMPLETE)]
    active.sort(key=lambda r: r["Assigned_At"], reverse=True)
    return [r["Participant"] for r in active]


def check_answers(answers):
    """Return a message if the RA's answers are incomplete, else None."""
    if not answers["by"]:
        return "Enter your initials."
    if answers["reason"] == REASONS[-1] and not answers["notes"]:
        return 'With "Other", say what happened in the notes.'
    return None


# --------------------------------------------------------------------------
# Terminal version (also what runs when PsychoPy is not installed)
# --------------------------------------------------------------------------

def tell_console(message):
    print("\n" + message)


def ask_console(ids, subid):
    """Ask for participant, reason, notes and initials. None if cancelled."""
    print("\nCRASH REPORT  (leave Participant empty to cancel)")
    if subid is None:
        print("Participants in the sheet: " + ", ".join(ids))
        subid = input("Participant: ").strip()
        if not subid:
            return None
    else:
        print("Participant: %s" % subid)
    for number, reason in enumerate(REASONS, start=1):
        print("  %d. %s" % (number, reason))
    while True:
        choice = input("Reason (1-%d): " % len(REASONS)).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(REASONS):
            break
    print(NO_NAMES)
    answers = {"subid": subid, "reason": REASONS[int(choice) - 1],
               "notes": input("Notes: ").strip(),
               "by": input("Your initials: ").strip()}
    problem = check_answers(answers)
    while problem:
        print(problem)
        if not answers["by"]:
            answers["by"] = input("Your initials: ").strip()
        else:
            answers["notes"] = input("Notes: ").strip()
        problem = check_answers(answers)
    return answers


def confirm_console(question):
    return input("\n" + question + "\nType YES to confirm: ").strip() == "YES"


# --------------------------------------------------------------------------
# Dialog version (PsychoPy)
# NOT YET RUN: written without PsychoPy available. Run it once on the testing
# machine before relying on it, and keep the flag open in AI_Disclosure.md
# until then.
# --------------------------------------------------------------------------

def _dialog_values(data):
    """Dlg.show() returns a list in older PsychoPy and a dict in newer ones."""
    return list(data.values()) if isinstance(data, dict) else list(data)


def tell_dialog(message):
    from psychopy import gui
    dlg = gui.Dlg(title="Crash report")
    for line in message.split("\n"):
        dlg.addText(line)
    dlg.show()


def ask_dialog(ids, subid):
    """Ask for participant, reason, notes and initials. None if cancelled."""
    from psychopy import gui
    problem = None
    answers = {"subid": subid or ids[0], "reason": REASONS[0], "notes": "", "by": ""}
    while True:
        dlg = gui.Dlg(title="Crash report")
        dlg.addText("Exclude a participant from the counterbalancing.")
        if problem:
            dlg.addText(problem, color="red")
        # Earlier answers are filled back in if the dialog has to be shown again.
        dlg.addField("Participant", choices=ids, initial=answers["subid"])
        dlg.addField("Reason", choices=REASONS, initial=answers["reason"])
        dlg.addField("Notes", initial=answers["notes"])
        dlg.addText(NO_NAMES)
        dlg.addField("Your initials", initial=answers["by"])
        data = dlg.show()
        if not dlg.OK:
            return None
        values = _dialog_values(data)
        answers = {"subid": str(values[0]).strip(), "reason": values[1],
                   "notes": str(values[2]).strip(), "by": str(values[3]).strip()}
        problem = check_answers(answers)
        if not problem:
            return answers


def confirm_dialog(question):
    from psychopy import gui
    dlg = gui.Dlg(title="Crash report: confirm")
    for line in question.split("\n"):
        dlg.addText(line)
    dlg.show()
    return bool(dlg.OK)


# --------------------------------------------------------------------------
# The crash report itself
# --------------------------------------------------------------------------

def run(subid=None, use_console=False, sheet_path=None):
    """Run one crash report. Returns True if a participant was excluded.

    subid       participant to pre-select (the experiment passes the ID the RA
                just typed); None lets the RA pick from the sheet.
    use_console True for terminal prompts instead of the PsychoPy dialog.
    sheet_path  another sheet to use (testing); default is the study's own.
    """
    if not use_console:
        try:
            import psychopy.gui  # noqa: F401  (only checking it is available)
        except ImportError:
            use_console = True
    tell = tell_console if use_console else tell_dialog
    ask = ask_console if use_console else ask_dialog
    confirm = confirm_console if use_console else confirm_dialog

    try:
        rows = cb.load(sheet_path)

        # Pilot and debug IDs hold no slot, so there is nothing to exclude.
        if subid is not None and cb.id_kind(subid) in ("pilot", "debug"):
            tell("%s is a %s ID. It takes no counterbalancing slot, so there "
                 "is nothing to exclude." % (subid, cb.id_kind(subid)))
            return False

        ids = candidates(rows)
        if not ids:
            tell("No participant in the sheet can be excluded.")
            return False
        if subid is not None and cb.find_active(rows, subid) is None:
            tell("Participant %s holds no slot in the counterbalancing sheet "
                 "(never assigned, or already excluded). Nothing was changed."
                 % subid)
            return False

        answers = ask(ids, subid)
        if answers is None:
            tell("Cancelled. Nothing was changed.")
            return False
        row = cb.find_active(rows, answers["subid"])
        if row is None:
            tell("Participant %s holds no slot in the counterbalancing sheet. "
                 "Nothing was changed." % answers["subid"])
            return False

        # Two steps, like overwriting a participant: show exactly what will
        # happen, then ask again.
        question = ("Exclude participant %s?\n"
                    "Condition: %s (slot %s)\n"
                    "Reason: %s\n"
                    "A new open slot with the same condition will be next in line."
                    % (row["Participant"], row["Condition"], row["Slot"],
                       answers["reason"]))
        if not confirm(question):
            tell("Cancelled. Nothing was changed.")
            return False

        excluded, new_row = cb.exclude(answers["subid"], answers["reason"],
                                       answers["notes"], answers["by"],
                                       sheet_path)
        tell("Participant %s excluded.\n"
             "Slot %s (%s) is now next in line.\n\n%s"
             % (excluded["Participant"], new_row["Slot"], new_row["Condition"],
                cb.counts_text(cb.load(sheet_path))))
        return True

    except cb.SheetError as err:
        tell(str(err))
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Exclude a participant and reopen their counterbalancing slot.")
    parser.add_argument("subid", nargs="?", default=None,
                        help="participant ID to pre-select")
    parser.add_argument("--console", action="store_true",
                        help="terminal prompts instead of the dialog")
    parser.add_argument("--sheet", default=None,
                        help="path to another counterbalancing sheet")
    args = parser.parse_args()
    done = run(args.subid, use_console=args.console, sheet_path=args.sheet)
    sys.exit(0 if done else 1)


if __name__ == "__main__":
    main()
