from datetime import datetime

from nba_data_forge.etl.transformers.game_log_transformer import GameLogTransformer


class DailyGameLogTransformer(GameLogTransformer):

    def transform(self, df):
        try:
            result = df.copy()
            result = result.rename(columns={"slug": "player_id"})
            result = super().transform(result)  # temporary filename
            current_date = datetime.now()
            result["season"] = (
                current_date.year + 1 if current_date.month >= 10 else current_date.year
            )

            # Calculate points_scored
            result["points_scored"] = (
                (df["made_field_goals"] - df["made_three_point_field_goals"]) * 2
                + df["made_three_point_field_goals"] * 3
                + df["made_free_throws"]
            )

            # Add active column for compatibility
            result["active"] = True

            self.logger.info(
                f"Transformed {len(result)} daily game logs with {len(result.columns)} columns"
            )

            return result

        except Exception as e:
            self.logger.error(f"Error transforming daily data: {str(e)}")
            raise
