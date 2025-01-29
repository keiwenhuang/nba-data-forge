# NBA Data Forge

A portfolio project showcasing data engineering and backend development through NBA statistics analysis.

## Project Overview
Starting from an existing NBA analytics project, NBA Data Forge evolved into a comprehensive platform demonstrating:

- Historical NBA data collection
- Automated data engineering pipeline
- RESTful API with analytics capabilities
- Robust error handling and recovery systems

### Data Sources
- [Basketball Reference](https://www.basketball-reference.com/) - Web scraping for player data
- [basketball_reference_web_scraper](https://jaebradley.github.io/basketball_reference_web_scraper/) - Python client for Basketball Reference data

## Project Timeline & Status
### Phase 1: API Development
- Utilized existing NBA dataset
- Implemented basic FastAPI endpoints
- Created database models and schemas
- Set up initial analytics features

### Phase 2: Data Engineering (Current)
- Implemented web scraping infrastructure
- Built data collection pipeline with recovery system
- Currently collecting historical data (past 20 seasons)
- Developed checkpoint-based recovery mechanism

### Phase 3: Planned
- Complete historical data collection
- Implement incremental data updates
- Enhance API analytics capabilities
- Add advanced statistical analysis

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
Additional fields:
- `player_id` and `name` are added during data collection
- Preprocessing adds: `is_home`, `is_win`, `minutes_played`

Dataset includes 28 fields per game entry:
- Game metadata (date, location, teams)
- Player statistics (points, rebounds, assists)
- Advanced metrics (game score, plus/minus)
- Enriched data (player identification, derived statistics)

### Technical Stack
- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Data Collection**: BeautifulSoup, basketball_reference_web_scraper
- **Data Processing**: Pandas
- **Schema Validation**: Pydantic
- **Development Tools**: pytest, Git

### Project Structure
```
nba_data_forge/
├── app/                            # FastAPI application
│   ├── api/                        # API endpoints
│   ├── core/                       # Core configurations
│   ├── models/                     # SQLAlchemy models
│   ├── schemas/                    # Pydantic schemas
│   └── services/                   # Business logic
├── data_engineering/               # Data collection
│   ├── extractors/                 # Web scraping
│   └── utils/                      # Shared utilities
├── airflow/ 
│   ├── dags/                       
├── data/                           # Data storage
│   ├── raw/                        # Collected data
│   ├── processed/                  # Transformed data
│   └── checkpoints/                # Recovery points
└── logs/                           # Application logs
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
- PostgresSQL

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
- Complete historical data collection
- Implement incremental periodically updates
- Enhance data validation and quality checks

### Medium Term
- Expand API analytics capabilities
- Add advanced statistical analysis
- Implement caching and query optimization
- Performance monitoring and tuning

## Skills Demonstrated
- ETL pipeline development
- RESTful API design
- Database modeling
- Error handling and recovery
- Clean code practices
- Project organization

For questions about this portfolio project, please open an issue on GitHub.