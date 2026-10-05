from utils import (
    calculate_average,
    calculate_drop,
    calculate_maximum,
    calculate_minimum,
)


class Session:
    """A session is built from one participant and many observation windows.

    This is a simple example of composition: the session owns the participant and
    the observation list, rather than inheriting from them.
    """

    def __init__(self, participant):
        self.participant = participant
        self.observations = []
        self.rejected_observations = 0
        self._classification = "unclassified"

    @property
    def classification(self):
        """Protected-style attribute access through a property."""
        return self._classification

    @classification.setter
    def classification(self, value):
        if not isinstance(value, str):
            raise ValueError("Classification must be a string.")
        self._classification = value

    def add_single_observation(self, observation):
        """Store valid observations and count invalid ones."""
        if observation.is_valid():
            self.observations.append(observation)
        else:
            self.rejected_observations += 1

    def calculate_summary(self):
        attributes = [
            "heart_rate",
            "skin_response",
            "temperature",
            "activity_level",
            "signal_quality",
        ]

        summary = {}

        for field in attributes:
            values = [getattr(obs, field) for obs in self.observations if getattr(obs, field) is not None]

            if not values:
                summary[field] = {"average": None, "minimum": None, "maximum": None}
                continue

            summary[field] = {
                "average": calculate_average(values),
                "minimum": calculate_minimum(values),
                "maximum": calculate_maximum(values),
            }

        return summary

    def compare_reference(self):
        summary = self.calculate_summary()

        heart_average = summary.get("heart_rate", {}).get("average")
        skin_average = summary.get("skin_response", {}).get("average")
        temp_average = summary.get("temperature", {}).get("average")

        return {
            "heart_rate": (
                heart_average - self.participant.baseline_heart_rate
                if heart_average is not None
                else None
            ),
            "skin_response": (
                skin_average - self.participant.baseline_skin_response
                if skin_average is not None
                else None
            ),
            "temperature": (
                temp_average - self.participant.baseline_temperature
                if temp_average is not None
                else None
            ),
        }

    def classify_session(self):
        """Classify the session as a simple human-readable activity state."""
        if len(self.observations) < 3:
            self.classification = "insufficient data"
            return self.classification

        summary = self.calculate_summary()

        avg_hr = summary["heart_rate"]["average"]
        avg_activity = summary["activity_level"]["average"]
        avg_signal = summary["signal_quality"]["average"]
        baseline_hr = self.participant.baseline_heart_rate

        if avg_signal is None or avg_signal < 0.6:
            self.classification = "insufficient data"
            return self.classification

        if avg_activity < 0.2 and avg_hr <= baseline_hr + 8:
            self.classification = "resting"
            return self.classification

        if self.detect_recovery():
            self.classification = "recovering"
            return self.classification

        if avg_activity >= 0.65 or avg_hr >= baseline_hr + 30:
            self.classification = "high activity"
            return self.classification

        if avg_activity >= 0.2:
            self.classification = "moderate activity"
            return self.classification

        self.classification = "resting"
        return self.classification

    def detect_recovery(self):
        """Return True when a session shows a clear drop near the end."""
        if len(self.observations) < 4:
            return False

        mid = len(self.observations) // 2
        first_half = self.observations[:mid]
        second_half = self.observations[mid:]

        heart_drop = calculate_drop(
            [obs.heart_rate for obs in first_half],
            [obs.heart_rate for obs in second_half],
        )

        activity_drop = calculate_drop(
            [obs.activity_level for obs in first_half],
            [obs.activity_level for obs in second_half],
        )

        return heart_drop > 8 and activity_drop > 0.10

    