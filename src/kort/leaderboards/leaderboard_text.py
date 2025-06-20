from .base_leaderboard import BaseLeaderBoard


class LeaderBoardText(BaseLeaderBoard):
    def __init__(self, input_dir):
        super().__init__(input_dir)

    def launch(self):
        max_length = max(
            len(str(model["Model Name"])) for model in self.leaderboard_data
        )

        print("# KorT Leaderboard")
        print("## Models")
        print()
        print(
            " | ".join(
                key.ljust(max_length if i == 0 else 1)
                for i, key in enumerate(self.leaderboard_data[0].keys())
            )
        )
        print(
            " | ".join(
                [
                    "-"
                    * (
                        max_length
                        if i == 0
                        else len(list(self.leaderboard_data[0].keys())[i])
                    )
                    for i in range(len(self.leaderboard_data[0]))
                ]
            )
        )
        for model in self.leaderboard_data:
            print(
                f"{model['Model Name']}".ljust(max_length)
                + " | "
                + " | ".join(
                    [
                        str(model[cat]).ljust(
                            len(list(self.leaderboard_data[0].keys())[i + 1])
                        )
                        for i, cat in enumerate(list(model.keys())[1:])
                    ]
                )
            )
        print()
