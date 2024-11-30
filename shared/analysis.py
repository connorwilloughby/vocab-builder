from engine import ProgressState
import pandas as pd

class AnalysisEngine(ProgressState):
    """
    Used to get insight about user performance from historical performance.

    @ extends ProgressState
    """

    def __init__(self) -> None:

        # get historical user answers
        self.user_answers_df = pd.read_csv("data/progress/answers.csv")

        # inherit from parent
        super().__init__()

    def get_success_rates(self):
        word_success_rate_frame = self.user_answers_df.groupby('target_word')['result'].mean()

        word_success_rate_frame.sort_values(axis=0, inplace=True, ascending=[True])

        return word_success_rate_frame


if __name__ == "__main__":
    engine = AnalysisEngine()

    engine.get_success_rates()

    print("do more stuff")
