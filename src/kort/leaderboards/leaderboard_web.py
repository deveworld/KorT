import gradio
import pandas

from .base_leaderboard import BaseLeaderBoard
from ..data import EVAL_DATA, Categories, LangCode
from kort import data


class LeaderboardWeb(BaseLeaderBoard):
    def __init__(self, input_dir):
        super().__init__(input_dir)

    def launch(self):
        self.interface = gradio.TabbedInterface(
            [self.leaderboard(), self.view_raw_data(), self.view_sentences()],
            ["Leaderboard", "View raw data", "View sentences"],
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
            gradio.Markdown("## Leaderboard")

            pd_data = pandas.DataFrame(self.leaderboard_data)
            gradio.Dataframe(pd_data)

        return leaderboard

    def view_raw_data(self):
        with gradio.Blocks() as raw_data:
            gradio.Markdown("# KorT Leaderboard")
            gradio.Markdown("## Raw Data")
            gradio.Markdown("### [현재 데이터](https://github.com/deveworld/KorT/blob/main/src/kort/data/generate.py#L48)")

            pd_data = pandas.DataFrame(self.raw_data)
            gradio.Dataframe(pd_data)

        return raw_data

    def view_sentences(self):
        data = []
        for lang_code, lang in EVAL_DATA.items():
            for category, examples in lang.items():
                for example in examples:
                    data.append(
                        {
                            "category": category.name,
                            "source": example.source,
                            "reference": [(k, v) for k, v in example.translation.items()][0][1],
                            "source_lang": lang_code.name,
                            "target_lang": [(k, v) for k, v in example.translation.items()][0][0].name,
                        }
                    )

        with gradio.Blocks() as sentences:
            gradio.Markdown("# KorT Leaderboard")
            gradio.Markdown("## Sentences")
            gradio.Markdown("### [문장 출처](https://github.com/deveworld/KorT/blob/main/eval_data.md)")

            pd_data = pandas.DataFrame(data)
            gradio.Dataframe(pd_data)
        
        return sentences