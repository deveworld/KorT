import gradio
import pandas

from .base_leaderboard import BaseLeaderBoard


class LeaderboardWeb(BaseLeaderBoard):
    def __init__(self, input_dir):
        super().__init__(input_dir)

    def launch(self):
        self.interface = gradio.TabbedInterface(
            [self.leaderboard()],
            ["Leaderboard"],
            title="KorT Leaderboard",
        )
        self.interface.queue(
            status_update_rate=10,
            default_concurrency_limit=10,
            api_open=False,
        )
        self.interface.launch(
            max_threads=16,
        )

    def leaderboard(self):
        with gradio.Blocks() as leaderboard:
            gradio.Markdown("# KorT Leaderboard")
            gradio.Markdown("## Models")

            pd_data = pandas.DataFrame(self.leaderboard_data)
            gradio.Dataframe(pd_data)

        return leaderboard
