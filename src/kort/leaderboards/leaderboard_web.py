from typing import Optional

import gradio as gr
import pandas as pd

from ..data import EVAL_DATA, Categories
from .base_leaderboard import BaseLeaderBoard


class LeaderboardWeb(BaseLeaderBoard):
    def __init__(self, input_dir):
        super().__init__(input_dir)
        print(f"Loaded {len(self.leaderboard_data)} models for the leaderboard.")
        for i, data in enumerate(self.leaderboard_data):
            data["Rank"] = i + 1
            for category in Categories.__members__.values():
                if category.name not in data.keys():
                    continue
                data[category.value] = data[category.name]
        self.category_cols = ["Overall Score"] + [
            cat.value for cat in Categories.__members__.values()
        ]
        self.cols = ["Rank", "Model Name"] + self.category_cols

    def update_leaderboard_data(
        self, search_term: Optional[str] = None, sort_by: Optional[str] = None
    ):
        """
        Update the leaderboard data based on the search term and category.
        """
        updated_data = self.leaderboard_data.copy()

        if search_term and "Model Name" in updated_data[0]:
            updated_data = [
                item
                for item in updated_data
                if search_term.lower() in str(item["Model Name"]).lower()
            ]

        if sort_by and sort_by in updated_data[0]:
            updated_data.sort(key=lambda x: x[sort_by], reverse=True)

        return updated_data

    def leaderboard(self):
        """Creates the Gradio leaderboard tab content."""
        with gr.Blocks(fill_width=True, fill_height=True) as leaderboard_tab:
            gr.Markdown("# KorT Leaderboard")

            with gr.Row():
                search_textbox = gr.Textbox(
                    show_label=False, placeholder="🔍 Model Name"
                )
                sort_dropdown = gr.Dropdown(
                    show_label=False,
                    choices=self.category_cols,
                    value="Overall Score",
                    interactive=True,
                )

            if not self.leaderboard_data:
                gr.Markdown(
                    "No leaderboard data available. Please check the input directory and data files."
                )
                return leaderboard_tab

            data = pd.DataFrame(self.leaderboard_data, columns=pd.Index(self.cols))

            leaderboard_display = gr.DataFrame(
                data,
                headers=self.cols,
                interactive=False,
                max_height=100000,
                elem_id="leaderboard-table",
            )

            def update_display(search_term, sort_by):
                updated_data = self.update_leaderboard_data(search_term, sort_by)
                pd_updated_data = pd.DataFrame(
                    updated_data, columns=pd.Index(self.cols)
                )
                return gr.DataFrame(
                    pd_updated_data,
                    headers=self.cols,
                    interactive=False,
                    max_height=100000,
                )

            search_textbox.change(
                fn=update_display,
                inputs=[search_textbox, sort_dropdown],
                outputs=[leaderboard_display],
            )
            sort_dropdown.change(
                fn=update_display,
                inputs=[search_textbox, sort_dropdown],
                outputs=[leaderboard_display],
            )

        return leaderboard_tab

    def view_raw_data(self):
        """Creates the Gradio raw data view tab content."""
        with gr.Blocks(fill_width=True, fill_height=True) as raw_data_tab:
            gr.Markdown("# Raw Evaluation Data")
            gr.Markdown(
                "Flattened view of the evaluation results used to generate the leaderboard."
            )

            if not self.raw_data:
                gr.Markdown("No raw data available.")
                return raw_data_tab

            try:
                df = pd.DataFrame(self.raw_data)
                gr.DataFrame(df, interactive=False, max_height=100000)
            except Exception as e:
                gr.Markdown(f"Error displaying raw data: {e}")

        return raw_data_tab

    def view_sentences(self):
        """Creates the Gradio sentences view tab content."""
        with gr.Blocks(fill_width=True, fill_height=True) as sentences_tab:
            gr.Markdown("# Evaluation Sentences")
            gr.Markdown("Sentences used for the KorT evaluation.")
            gr.Markdown(
                "### [Sentence Sources](https://github.com/deveworld/KorT/blob/main/eval_data.md)"
            )
            gr.Markdown(
                "### [Latest Dataset Generation](https://github.com/deveworld/KorT/blob/main/src/kort/data/generate.py#L48)"
            )

            data = []
            if not EVAL_DATA:
                gr.Markdown("EVAL_DATA is empty or not loaded.")
                return sentences_tab

            for lang_code, lang_data in EVAL_DATA.items():
                for category, examples in lang_data.items():
                    for example in examples:
                        translation_items = list(example.translation.items())
                        if translation_items:
                            target_lang_code, reference_text = translation_items[0]
                            data.append(
                                {
                                    "Category": category.value,
                                    "Source Language": lang_code.to_english(),
                                    "Source Sentence": example.source,
                                    "Target Language": target_lang_code.to_english(),
                                    "Reference Translation": reference_text,
                                }
                            )
                        else:
                            data.append(
                                {
                                    "Category": category.value,
                                    "Source Language": lang_code.to_english(),
                                    "Source Sentence": example.source,
                                    "Target Language": "N/A",
                                    "Reference Translation": "N/A",
                                }
                            )

            if not data:
                gr.Markdown("No sentence data could be processed from EVAL_DATA.")
            else:
                df = pd.DataFrame(data)
                gr.DataFrame(df, interactive=False, max_height=100000)

        return sentences_tab

    def launch(self):
        """Launches the Gradio web interface."""
        head_content = """
<!-- HTML Meta Tags -->
<title>KorT 리더보드</title>
<meta name="description" content="한국어 번역 능력 벤치마크 KorT 리더보드 웹페이지">
<!-- Facebook Meta Tags -->
<meta property="og:url" content="https://kort.worldsw.dev">
<meta property="og:type" content="website">
<meta property="og:title" content="KorT 리더보드">
<meta property="og:description" content="한국어 번역 능력 벤치마크 KorT 리더보드 웹페이지">
<!-- Twitter Meta Tags -->
<meta name="twitter:title" content="KorT 리더보드">
<meta name="twitter:description" content="한국어 번역 능력 벤치마크 KorT 리더보드 웹페이지">
<meta property="twitter:domain" content="kort.worldsw.dev">
<meta property="twitter:url" content="https://kort.worldsw.dev">
        """
        with gr.Blocks(
            title="KorT 리더보드", fill_height=True, fill_width=True, head=head_content
        ) as app:
            with gr.Row(equal_height=False):
                # Give title more space
                with gr.Column(scale=7):
                    gr.Markdown(
                        """
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <span style="font-size: 1.8em; font-weight: bold; color: orange; margin-right: 10px;">KorT</span>
                            <span style="font-size: 1.5em; font-weight: bold;">리더보드</span>
                        </div>
                        """,
                    )
                with gr.Column(scale=1, min_width=150):
                    button = gr.Button("모델 평가 요청", elem_id="button")
                    button.click(
                        fn=lambda: None,
                        js="function openGithub() { window.open('https://github.com/deveworld/KorT#about'); }",
                    )

            # KorT Description
            gr.Markdown(
                """
                <div style="font-size: 1.2em; margin-bottom: 10px;">
                    KorT: LLM이 평가하는 한국어-다국어 번역 벤치마크
                    <br>
                    번역이 까다로운 문장 데이터셋을 바탕으로 높은 신뢰성을 목표로 합니다.
                </div>
                """
            )

            with gr.Tabs():
                with gr.TabItem("Leaderboard"):
                    self.leaderboard()
                with gr.TabItem("Raw Data"):
                    self.view_raw_data()
                with gr.TabItem("Evaluation Sentences"):
                    self.view_sentences()

        print("Launching Gradio App...")
        app.launch()
