from .base_leaderboard import BaseLeaderBoard


class LeaderBoardText(BaseLeaderBoard):
    def __init__(self, input_dir):
        super().__init__(input_dir)

    def launch(self):
        sorted_data = sorted(
            self.leaderboard_data,
            key=lambda x: x["Overall Score"],
            reverse=True,
        )

        max_length = max(len(model["Model Name"]) for model in sorted_data)

        print("# KorT Leaderboard")
        print("## Models")
        print()
        print(
            " | ".join(
                key.ljust(max_length if i == 0 else 1)
                for i, key in enumerate(sorted_data[0].keys())
            )
        )
        print(
            " | ".join(
                [
                    "-"
                    * (max_length if i == 0 else len(list(sorted_data[0].keys())[i]))
                    for i in range(len(sorted_data[0]))
                ]
            )
        )
        for model in sorted_data:
            print(
                f"{model['Model Name']}".ljust(max_length)
                + " | "
                + " | ".join(
                    [
                        str(model[cat]).ljust(len(list(sorted_data[0].keys())[i + 1]))
                        for i, cat in enumerate(list(model.keys())[1:])
                    ]
                )
            )
        print()
