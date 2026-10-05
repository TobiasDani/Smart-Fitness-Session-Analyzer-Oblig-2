class Participant:
    """Represents one participant and their personal reference values."""

    def __init__(
        self,
        participant_id,
        baseline_heart_rate,
        baseline_skin_response,
        baseline_temperature,
    ):
        self.participant_id = participant_id
        self.baseline_heart_rate = baseline_heart_rate
        self.baseline_skin_response = baseline_skin_response
        self.baseline_temperature = baseline_temperature

    @staticmethod
    def is_valid_baseline(heart_rate, skin_response, temperature):
        """Simple validation helper for a participant baseline profile."""
        if not isinstance(heart_rate, (int, float)) or not 35 <= heart_rate <= 205:
            return False

        if not isinstance(skin_response, (int, float)) or skin_response < 0:
            return False

        if not isinstance(temperature, (int, float)) or not 25 <= temperature <= 42:
            return False

        return True

