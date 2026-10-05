from fitness.csv_reader import load_participants, load_sessions
from fitness.observation import Observation


def test_valid_files():
    participants, participant_errors = load_participants(
        "data/participants.csv"
    )

    sessions, session_errors = load_sessions(
        "data/fitness_sessions.csv",
        participants,
    )

    assert len(participants) == 3
    assert len(sessions) == 5
    assert len(participant_errors) == 0
    assert len(session_errors) == 0


def test_invalid_file():
    participants, _ = load_participants(
        "data/participants.csv"
    )

    sessions, rejected = load_sessions(
        "data/fitness_sessions_invalid.csv",
        participants,
    )

    assert len(sessions) == 1
    assert len(rejected) == 10


def test_missing_file():
    participants, _ = load_participants(
        "data/participants.csv"
    )

    sessions, rejected = load_sessions(
        "data/does_not_exist.csv",
        participants,
    )

    assert sessions == {}
    assert len(rejected) == 1
    assert rejected[0]["reason"] == "File not found"


def test_boundary_values():
    lowest = Observation(
        0,
        35,
        0,
        25,
        0,
        0,
    )

    highest = Observation(
        1,
        205,
        1,
        42,
        1,
        1,
    )

    invalid = Observation(
        2,
        34,
        1,
        32,
        0.5,
        0.9,
    )

    assert lowest.is_valid() is True
    assert highest.is_valid() is True
    assert invalid.is_valid() is False


if __name__ == "__main__":
    test_valid_files()
    test_invalid_file()
    test_missing_file()
    test_boundary_values()

    print("4 tests passed.")
