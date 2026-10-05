from observation import Observation
from participant import Participant
from report import Report
from sample_data import get_sample_data
from session import Session


def new_fitness_session(profile_in, observations_in):
    """Convert raw data into participant, observations, and a session object."""
    if not Participant.is_valid_baseline(
        profile_in["baseline_heart_rate"],
        profile_in["baseline_skin_response"],
        profile_in["baseline_temperature"],
    ):
        raise ValueError("Invalid participant baseline data.")

    profile = Participant(
        profile_in["participant_id"],
        profile_in["baseline_heart_rate"],
        profile_in["baseline_skin_response"],
        profile_in["baseline_temperature"],
    )

    observations = [
        Observation(
            obs["timestamp"],
            obs["heart_rate"],
            obs["skin_response"],
            obs["temperature"],
            obs["activity_level"],
            obs["signal_quality"],
        )
        for obs in observations_in
    ]

    session = Session(profile)
    for obs in observations:
        session.add_single_observation(obs)

    return profile, session


def main():
    """Run the basic fitness session analysis workflow."""
    profile, observations = get_sample_data()
    profile, session = new_fitness_session(profile, observations)

    report = Report(session)
    report.print_report()


if __name__ == "__main__":
    main()

