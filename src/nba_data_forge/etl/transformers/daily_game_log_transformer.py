from nba_data_forge.etl.transformers.base import BaseTransformer


class DailyGameLogTransformer(BaseTransformer):
    def __init__(self, log_dir=None):
        super().__init__(log_dir)

    def transform(self, df):
        try:
            pass
        except Exception as e:
            self.logger.error(f"Error transforming: {str(e)}")
