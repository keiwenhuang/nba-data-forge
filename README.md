# NBA Data Forge

A portfolio project showcasing data engineering and backend development through NBA statistics analysis.

## Project Overview
NBA Data Forge is a comprehensive data platform demonstrating:

- Historical NBA data collection (2003-2024)
- Automated data engineering pipeline with Airflow
- RESTful API with analytics capabilities
- Robust error handling and recovery systems

### Data Sources & Disclaimer
This project uses data from:
- [Basketball Reference](https://www.basketball-reference.com/) - Historical player and game data
- [basketball_reference_web_scraper](https://jaebradley.github.io/basketball_reference_web_scraper/) - Python client for Basketball Reference data

**Data Usage Disclaimer:**  
All NBA data used in this project is sourced from Basketball Reference for educational and demonstration purposes only. This project is not affiliated with or endorsed by Basketball Reference, the NBA, or any NBA teams. Please refer to Basketball Reference's terms of use for information about data usage rights and limitations.


## Current Project Status

### Completed
- Project structure and environment setup
- Data collection infrastructure with error handling
- Initial data quality analysis (523,825 game logs, 2003-2024)
- Database schema design and implementation
- Development environment with Docker and Airflow
- Data transformation pipeline implementation
- Team name and location standardization
- Data validation system
- Loading optimization

### In Progress
- API endpoint implementation
- Advanced analytics features
- Incremental update system

### Planned
- Performance optimization

## Technical Implementation
### Data Structure
#### Player Data
```
player_id,name,year_min,year_max,position,height,weight,birth_date,college,is_active
```
Note: `is_active` status is determined during data collection from Basketball Reference

#### GameLogs
```
date,team,location,opponent,outcome,seconds_played,points_scored,game_score,plus_minus,player_id
```
Enriched fields:
- player_id and name (added during collection)
- is_home, is_win (boolean flags)
- minutes_played (converted from seconds)
- team_abbrev, opponent_abbrev (match to current team name abbreviations)


### Technical Stack
- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ETL**: Apache Airflow
- **ORM**: SQLAlchemy
- **Data Collection**: BeautifulSoup, basketball_reference_web_scraper
- **Data Processing**: Pandas, NumPy
- **Schema Validation**: Pydantic
- **Development Tools**: pytest, Git

### Project Structure
```
nba_data_forge/
├── src/                          
│   └── nba_data_forge/             
│       ├── api/                    
│       │   ├── dependencies/       # FastAPI dependencies
│       │   ├── models/             # SQLAlchemy models             
│       │   ├── schemas/            # Pydantic schemas 
│       │   ├── services/           # Business logic
│       │   └── v1/                 # API v1 endpoints
│       ├── common/                 # Shared code
│       │   ├── config/             # Configuration management
│       │   ├── db/                 # Database utilities
│       │   └── utils/              # Shared utilities
│       └── etl/                    # ETL pipeline
│           ├── extractors/         # Data collection
│           ├── loaders/            # Database loading
│           └── transformers/       # Data processing
├── tests/                          # Integration tests
└── airflow/                        # Airflow configuration
    └── dags/                       # Airflow DAG definitions
```

## Features
### Data Collection
```
# Collect player data
python data_collection.py --players

# Collect game logs for specific seasons
python data_collection.py --game-logs --from-season 2019 --to-season 2022
```
Key features:
- Web scraping with rate limiting
- Season-based collection
- Checkpoint recovery system
- Rotating logs (10MB, 5 backups)
- Data validation

### API Endpoints
- `/api/v1/players` - Player statistics with filtering capabilities
- `/api/v1/teams` - Team-level statistics 
- `/api/v1/game_logs` - Detailed game-by-game data
- `/api/v1/boxscores` - Daily box score summaries

Features:
- Season-based filtering
- Date range queries
- Last N games analysis
- Team statistics aggregation
- Daily box score compilation

## Development Setup
### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- PostgreSQL 16+

### Configuration
1. Create PostgreSQL database
2. Configure `config.ini`:
```
[postgresql]
host=localhost
port=5432
database=your_database_name
user=your_username
password=your_password
```
3. Install dependencies:
```
pip install -r requirements.txt
```

## API Documentation
Once running, view the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Next Steps
### Short Term
- Expand API analytics capabilities
- Add advanced statistical analysis
- Implement incremental periodically updates
- Enhance data validation and quality checks

### Medium Term
- Implement caching and query optimization
- Performance monitoring and tuning

## Skills Demonstrated
- ETL pipeline development
- RESTful API design
- Database modeling
- Error handling and recovery
- Clean code practices
- Project organization

## Contributing
This is a portfolio project but suggestions and feedback are welcome. Please feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

Note: While this project uses publicly available data, it is important to respect Basketball Reference's terms of service and data usage guidelines when using their data.