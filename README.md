# NBA Data Forge

A data engineering portfolio project showcasing ETL pipeline development, API implementation, and data visualization.

![alt text](screenshots/dashboard.png)

## Project Overview

NBA Data Forge demonstrates data engineering practices through:
- ETL pipeline with Airflow for NBA game statistics processing
- RESTful API with FastAPI for data access
- Interactive dashboard using Streamlit
- PostgreSQL database with SQLAlchemy ORM

## Features

### Data Pipeline
```
extract_games >> transform_games >> load_games >> validate_games
```

- **Historical Data Collection**
  - Rate-limited API requests with retry logic
  - Checkpoint system for resumable collection
  - Data validation and error handling
  - Progress tracking and recovery

- **Incremental Updates**
  - Airflow DAG for automation
  - Efficient upsert pattern for updates
  - Multi-stage validation
  - File archiving system

### API Implementation

Simple yet powerful endpoints for accessing NBA statistics:


`GET /api/v1/players/`
- List players for a given season (2004-2025)

`GET /api/v1/players/{player_id}/season/{season}`
- Get player's season statistics with optional home/away and win/loss filters

`GET /api/v1/players/{player_id}/vs-opponent-stats`
- Get player's statistics with opponent and recent game filters


### Interactive Dashboard

The Streamlit dashboard provides an interactive interface to explore player statistics across different contexts:

#### Filters
- Season selection (2004-2025)
- Player selection
- Opponent filter
- Last N games selection (3-82)

#### Statistics Views

1. Season Averages
    - Points, minutes, field goals
    - Three-point shots
    - Free throws and other key stats

2. VS Specific Team Analysis
    - Last N games averages against selected opponent
    - Detailed shooting and scoring statistics

3. Game Logs
    - Date, team, and opponent
    - Home/away and win/loss indicators
    - Minutes played
    - Complete game statistics

## Technical Stack

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **ETL**: Apache Airflow, Pandas
- **Frontend**: Streamlit
- **Development**: Python 3.12+, Docker

## Project Structure

```
nba_data_forge/
├── src/
│   └── nba_data_forge/
│       ├── api/                    # FastAPI implementation
│       │   ├── dependencies/       # Query params and filters
│       │   ├── models/            # SQLAlchemy models
│       │   ├── schemas/           # Pydantic schemas
│       │   ├── services/          # Business logic
│       │   └── v1/                # API endpoints
│       ├── common/                # Shared utilities
│       ├── dashboard/             # Streamlit implementation
│       └── etl/                   # Data pipeline
│           ├── extractors/        # Data collection
│           ├── loaders/           # Database operations
│           └── transformers/      # Data processing
├── tests/                         # Integration tests
└── config/                        # Configuration
```

## Local Development

### Prerequisites
- Python 3.12+
- PostgreSQL 16+
- Docker & Docker Compose

### Setup

- Clone repository
```
git clone https://github.com/yourusername/nba_data_forge.git
cd nba_data_forge
```

- Create virtual environment
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

- Install dependencies
```
pip install -r requirements.txt
```

- Configure database
```
createdb nba_data
```

- Update ./config.ini
```
[postgresql]
host=localhost
port=5432
database=nba_data_forge
user=your_username
password=your_password
```

- Start services
```
uvicorn nba_data_forge.api.main:app --reload
streamlit run nba_data_forge/dashboard/main.py
```


## Data Sources & Disclaimer

This project uses publicly available NBA statistics from:
- [Basketball Reference](https://www.basketball-reference.com/)
- [basketball_reference_web_scraper](https://jaebradley.github.io/basketball_reference_web_scraper/)

For educational and demonstration purposes only. Not affiliated with or endorsed by the NBA or Basketball Reference.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Testing Implementation
The project implements comprehensive testing across all layers:
### Test Structure
```
tests/
├── conftest.py                 # Test configuration and fixtures
├── test_player_stats.py        # API service tests
├── test_create_table.py        # Database schema tests
├── test_database.py            # Database connection tests
├── test_transformer.py         # Data transformation tests
└── test_upsert_functionality.py # Database operations tests
```
### Key Testing Features
- Database transaction isolation for tests
- Comprehensive fixture system
- Detailed service layer testing
- ETL pipeline validation
- Data integrity verification

### Test Coverage
- API endpoint validation
- Data transformation verification
- Database operation testing
- Player statistics calculation
- Error handling scenarios