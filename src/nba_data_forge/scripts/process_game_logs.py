import shutil
from pathlib import Path

import pandas as pd

from nba_data_forge.common.utils.logger import setup_logger
from nba_data_forge.common.utils.paths import paths
from nba_data_forge.etl.loaders.database import DatabaseLoader
from nba_data_forge.etl.transformers.game_log_transformer import GameLogTransformer


class GameLogProcessor:
    def __init__(self, test=False):
        self.project_root = paths.root
        self.test = test
        self.transformer = GameLogTransformer()
        self.loader = DatabaseLoader(test=test)
        self.logger = setup_logger(__class__.__name__, log_dir=paths.get_path("logs"))

    def _get_raw_files(self):
        return list(paths.get_path("raw").glob("game_logs_*.csv"))

    def process_file(self, file_path: Path):
        filename = file_path.name
        processed_filename = file_path.stem + "_transformed" + file_path.suffix
        self.logger.info(f"Processing {filename}")

        try:
            # read data
            df = pd.read_csv(file_path)
            self.logger.info(f"Read {len(df)} records from {filename}")

            # transform data
            transformed_data = self.transformer.transform(df, filename)
            self.logger.info(f"Transformed {len(transformed_data)} records")

            # load data into database
            self.loader.load(transformed_data)
            self.logger.info(f"Loaded {len(transformed_data)} records to database")

            if self.test:  # if running for test, save transformed file into temp folder
                processed_path = paths.get_path("temp") / processed_filename
                transformed_data.to_csv(processed_path, index=False)
            else:
                # save transformed data into archive/transform
                processed_path = (
                    paths.get_path("transformed_archive") / processed_filename
                )
                transformed_data.to_csv(processed_path, index=False)

                # move raw files into archive folder
                archive_path = paths.get_path("raw_archive") / filename
                shutil.move(str(file_path), str(archive_path))

            self.logger.info(f"Successfully processed and archived {filename}")

            return {
                "filename": filename,
                "raw_records": len(df),
                "processed_records": len(transformed_data),
                "status": "success",
            }

        except Exception as e:
            self.logger.error(f"Error processing {filename}: {str(e)}")
            return {"filename": filename, "error": str(e), "status": "failed"}

    def process_all_files(self):
        raw_files = self._get_raw_files()
        if not raw_files:
            self.logger.warning(f"No CSV file found in raw directory")
            return []

        results = []
        for file_path in raw_files:
            result = self.process_file(file_path)
            results.append(result)

        return results


def main():
    processor = GameLogProcessor(test=False)
    results = processor.process_all_files()

    # Print summary
    success_count = sum(1 for r in results if r["status"] == "success")
    fail_count = sum(1 for r in results if r["status"] == "failed")
    print("\nProcessing Summary:")
    print(f"Successfully processed: {success_count} files")
    print(f"Failed to process: {fail_count} files")

    if fail_count > 0:
        print("\nFailed files:")
        for result in results:
            if result["status"] == "failed":
                print(f"- {result['filename']}: {result['error']}")


if __name__ == "__main__":
    main()
    # pass
