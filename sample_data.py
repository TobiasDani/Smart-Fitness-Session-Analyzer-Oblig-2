from data_generator import generate_fitness_data


def get_sample_data():
    profile, observations = generate_fitness_data(
        participant_id="P001",
        scenario="recovery",
        seed=42,
        number_of_windows=10,
    )
    return profile, observations

