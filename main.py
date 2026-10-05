import argparse

from fitness.csv_reader import load_participants, load_sessions
from fitness.reporting import write_outputs


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze fitness sessions from CSV files."
    )

    parser.add_argument(
        "--profiles",
        default="data/participants.csv",
        help="Path to participant profile CSV file",
    )

    parser.add_argument(
        "--sessions",
        default="data/fitness_sessions.csv",
        help="Path to valid fitness session CSV file",
    )

    parser.add_argument(
        "--invalid-sessions",
        default="data/fitness_sessions_invalid.csv",
        help="Path to intentionally invalid fitness session CSV file",
    )

    parser.add_argument(
        "--output",
        default="output",
        help="Directory for generated reports",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    participants, rejected_participants = load_participants(
        args.profiles
    )

    valid_sessions, rejected_valid = load_sessions(
        args.sessions,
        participants,
    )

    invalid_sessions, rejected_invalid = load_sessions(
        args.invalid_sessions,
        participants,
    )

    sessions = {
        **valid_sessions,
        **invalid_sessions,
    }

    rejected = (
        rejected_participants
        + rejected_valid
        + rejected_invalid
    )

    created_files = write_outputs(
        sessions,
        rejected,
        args.output,
    )

    accepted_session_rows = sum(
        len(session.observations)
        for session in sessions.values()
    )

    accepted_rows = len(participants) + accepted_session_rows

    print(f"Accepted rows: {accepted_rows}")
    print(f"Rejected rows: {len(rejected)}")

    print("Created files:")
    for file in created_files:
        print(file)


if __name__ == "__main__":
    main()
