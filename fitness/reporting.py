import csv
from pathlib import Path

from .report import Report


def write_outputs(sessions, rejected, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = output_dir / "analysis_summary.csv"
    report_path = output_dir / "analysis_report.txt"
    rejected_path = output_dir / "rejected_records.txt"

    # Summary CSV
    with open(summary_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "session_id",
            "participant_id",
            "usable_observations",
            "classification",
            "average_heart_rate",
            "heart_rate_difference_from_baseline",
        ])

        for session_id, session in sessions.items():
            result = Report(session).generate()

            heart_summary = result["summary"]["heart_rate"]
            heart_difference = result["comparison_to_baseline"]["heart_rate"]

            writer.writerow([
                session_id,
                session.participant.participant_id,
                result["usable_observations"],
                result["classification"],
                heart_summary["average"],
                heart_difference,
            ])

    # Readable text report
    with open(report_path, "w", encoding="utf-8") as file:
        for session_id, session in sessions.items():
            result = Report(session).generate()

            file.write(f"Session: {session_id}\n")
            file.write(
                f"Participant: {session.participant.participant_id}\n"
            )
            file.write(
                f"Classification: {result['classification']}\n"
            )
            file.write(
                f"Usable observations: {result['usable_observations']}\n"
            )
            file.write(
                f"Explanation: {result['explanation']}\n"
            )
            file.write("\n")

    # Rejected records
    with open(rejected_path, "w", encoding="utf-8") as file:
        if not rejected:
            file.write("No rejected records.\n")
        else:
            for item in rejected:
                file.write(
                    f"File: {item['filename']}, "
                    f"row: {item['row_number']}, "
                    f"field: {item['field']}, "
                    f"reason: {item['reason']}\n"
                )

    return [summary_path, report_path, rejected_path]