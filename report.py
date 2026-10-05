class Report:
    """Creates a readable summary of the final session analysis."""

    def __init__(self, session):
        self.session = session

    def generate(self):
        """Return a clean dictionary with the final results for the session."""
        valid = len(self.session.observations)
        rejected = self.session.rejected_observations
        total = valid + rejected

        classification = self.session.classify_session()
        summary = self.session.calculate_summary()
        comparison = self.session.compare_reference()

        if classification == "recovering":
            explanation = (
                "The session shows a clear drop in heart rate and activity toward the end, "
                "which is consistent with recovery."
            )
        elif classification == "high activity":
            explanation = (
                "The activity level or heart rate was high enough to classify the session "
                "as high activity."
            )
        elif classification == "moderate activity":
            explanation = (
                "The activity level was above the resting range without reaching the high "
                "activity threshold."
            )
        elif classification == "resting":
            explanation = (
                "The activity level and heart rate stayed low and close to the baseline, "
                "so the session was classified as resting."
            )
        elif classification == "insufficient data":
            explanation = (
                "There was not enough valid data, or the signal quality was too poor, "
                "so a reliable classification could not be made."
            )
        else:
            explanation = "No clear classification could be determined."

        return {
            "total_observations": total,
            "usable_observations": valid,
            "rejected_observations": rejected,
            "classification": classification,
            "summary": summary,
            "comparison_to_baseline": comparison,
            "explanation": explanation,
        }

    def print_report(self):
        result = self.generate()

        print("\nFitness Session Report")
        print("-" * 30)
        print(f"Total observations: {result['total_observations']}")
        print(f"Usable observations: {result['usable_observations']}")
        print(f"Rejected observations: {result['rejected_observations']}")
        print(f"Classification: {result['classification']}")

        heart = result["summary"].get("heart_rate", {})
        if heart.get("average") is not None:
            print("\nHeart rate")
            print(f"Average: {heart['average']:.1f}")
            print(f"Minimum: {heart['minimum']}")
            print(f"Maximum: {heart['maximum']}")
            diff = result["comparison_to_baseline"].get("heart_rate")
            print(f"Difference from baseline: {diff:+.1f}")

        print(f"\nExplanation: {result['explanation']}")

        return result

    