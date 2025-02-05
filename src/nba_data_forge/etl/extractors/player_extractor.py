import pandas as pd
from bs4 import BeautifulSoup

from nba_data_forge.etl.extractors.base import BaseExtractor


class PlayerExtractor(BaseExtractor):
    def extract(self):
        print(self.base_url)
        self.logger.info(f"Extracting players...")
        all_player_data = []
        for letter in "abcdefghijklmnopqrstuvwxyz":
            self.logger.info(f"Extracting players with letter {letter}...")
            player_data = []
            response = self._safe_request(
                f"{self.base_url}/players/{letter}", max_retries=3
            )

            if response and response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                player_table = soup.find("table", id="players")
                self.expected_count = player_table.find("caption").text.split()[0]

                for player in player_table.find_all("tr")[1:]:  # skipping header row
                    player_info = self._parse_player_row(player)
                    player_data.append(player_info)

            if self.validate(player_data):
                self.logger.info(
                    f"Extracted {len(player_data)} players for letter {letter}"
                )
                all_player_data.extend(player_data)

        df = pd.DataFrame(all_player_data)
        return df

    def validate(self, player_data):
        expected = int(self.expected_count)
        actual = len(player_data)

        if expected != actual:
            self.logger.warning(
                f"Extracted fewer players than expected. Expected: {expected}, Actual: {actual}"
            )
            return False

        return True

    def _parse_player_row(self, player: BeautifulSoup):
        try:
            player_header = player.find("th")
            player_id = player_header.get("data-append-csv", "")
            is_active = bool(player_header.find("strong"))
            name = player_header.find("a")
            name = name.text.strip()
            year_min = player.find("td", {"data-stat": "year_min"})
            year_max = player.find("td", {"data-stat": "year_max"})
            position = player.find("td", {"data-stat": "pos"})
            height = player.find("td", {"data-stat": "height"})
            weight = player.find("td", {"data-stat": "weight"})
            birth_date = player.find("td", {"data-stat": "birth_date"})
            college = player.find("td", {"data-stat": "colleges"})

            return {
                "player_id": player_id,
                "name": name,
                "year_min": year_min.text.strip() if year_min else "",
                "year_max": year_max.text.strip() if year_max else "",
                "position": position.text.strip() if position else "",
                "height": height.text.strip() if height else "",
                "weight": weight.text.strip() if weight else "",
                "birth_date": (
                    birth_date.find("a").text.strip()
                    if birth_date and birth_date.find("a")
                    else ""
                ),
                "college": (
                    college.find("a").text.strip()
                    if college and college.find("a")
                    else ""
                ),
                "is_active": is_active,
            }

        except Exception as e:
            self.logger.info(f"Error parsing {player}: {str(e)}")
