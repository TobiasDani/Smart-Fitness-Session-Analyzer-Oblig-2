from participant import Participant
from observation import Observation
from session import Session


def make_session(heart_values, activity_values, signal_quality=0.9):
    participant = Participant("P001", 72, 2.1, 32.5)
    session = Session(participant)

    for i, (hr, activity) in enumerate(zip(heart_values, activity_values)):
        session.add_single_observation(
            Observation(i, hr, 2.1, 32.5, activity, signal_quality)
        )

    return session


def test_resting_session():
    session = make_session([72, 74, 73], [0.10, 0.12, 0.11])
    assert session.classify_session() == "resting"


def test_moderate_activity_session():
    session = make_session([80, 84, 86], [0.40, 0.45, 0.50])
    assert session.classify_session() == "moderate activity"


def test_high_activity_session():
    session = make_session([110, 118, 125], [0.75, 0.80, 0.85])
    assert session.classify_session() == "high activity"


def test_recovery_session():
    session = make_session([120, 110, 90, 80], [0.80, 0.70, 0.30, 0.20])
    assert session.classify_session() == "recovering"


def test_invalid_data_session():
    participant = Participant("P001", 72, 2.1, 32.5)
    session = Session(participant)

    session.add_single_observation(Observation(0, None, 2.0, 32.5, 0.3, 0.9))
    session.add_single_observation(Observation(1, 75, 2.0, 32.5, 0.3, 0.9))
    session.add_single_observation(Observation(2, 76, 2.0, 32.5, 0.3, 0.9))

    assert session.classify_session() == "insufficient data"


if __name__ == "__main__":
    test_resting_session()
    test_moderate_activity_session()
    test_high_activity_session()
    test_recovery_session()
    test_invalid_data_session()
    print("5 tests passed.")

