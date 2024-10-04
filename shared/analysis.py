from engine import ProgressState


class AnalysisEngine(ProgressState):
    """
    Used to get insight about user performance from historical performance.

    @extends ProgressState

    @returns probably fuck all
    """

    def __init__(self) -> None:
        # inherit from parent
        super().__init__()

    def get_success_rates(self):
        historical_frame = self.progress_frame

        word_success_rate_frame = historical_frame.groupby('target_word')['result'].mean() * 100

        return word_success_rate_frame


if __name__ == "__main__":
    engine = AnalysisEngine()

    engine.get_success_rates()

    print("do more stuff")
