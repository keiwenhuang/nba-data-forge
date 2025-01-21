# NBA Data Forge

A FastAPI-powered analytics platform demonstrating backend development with planned data engineering capabilities through NBA statistics analysis.

## Project Overview

NBA Data Forge is a portfolio project that showcases the development of a robust API for NBA statistics analysis. The project currently focuses on:
- Backend development with FastAPI and SQLAlchemy
- Web scraping and data collection
- RESTful API design and implementation
- Database modeling with PostgreSQL
- Statistics and analytics processing

### Data Processing & Structure

The project uses processed NBA game statistics originally sourced from [Basketball Reference](https://www.basketball-reference.com/). The data was collected through web scraping and underwent several processing steps to create a clean, analyzed dataset suitable for the API.

#### Dataset Features
The processed dataset includes comprehensive game statistics with 28 fields per entry:
- Game metadata (date, location, teams)
- Player statistics (points, rebounds, assists, etc.)
- Advanced metrics (game score, plus/minus)
- Derived fields (is_home, is_win, minutes_played)

The complete data schema can be found in `game_logs.sql`, which defines the structure of:
- Player identification and game participation
- Standard box score statistics
- Advanced performance metrics
- Game context and outcomes

Note: The processed dataset is not included in this repository. The database schema and processing scripts are provided for reference.

## Current Features

### API Endpoints
- `/api/v1/players` - Player statistics with filtering capabilities
- `/api/v1/teams` - Team-level statistics 
- `/api/v1/game_logs` - Detailed game-by-game data
- `/api/v1/boxscores` - Daily box score summaries

### Analytics Capabilities
- Player performance metrics
- Team statistics aggregation
- Game-by-game analysis
- Flexible date range and season filtering

## Technical Stack

### Current Implementation
- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Data Collection**: Web scraping (Beautiful Soup/Selenium)
- **Data Processing**: Pandas
- **Schema Validation**: Pydantic
- **Development Tools**: pytest, Git

### Planned Additions
- **ETL Framework**: Apache Airflow
- **Data Validation**: Great Expectations
- **Data Processing**: Additional pandas and NumPy integrations
- **Monitoring**: Custom metrics and alerting

## Project Structure
```
├── alembic/                  # Database migrations
├── app/
│   ├── api/
│   │   ├── dependencies/     # API dependencies
│   │   │   ├── filters.py
│   │   │   └── __init__.py
│   │   └── v1/              # API route handlers
│   │       ├── boxscores.py
│   │       ├── game_logs.py
│   │       ├── players.py
│   │       ├── teams.py
│   │       └── __init__.py
│   ├── core/                # Core configurations
│   │   ├── config.py
│   │   ├── database.py
│   │   └── __init__.py
│   ├── models/              # SQLAlchemy models
│   │   ├── game_log.py
│   │   └── __init__.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── boxscore.py
│   │   ├── game_log.py
│   │   ├── Player_name_id.py
│   │   ├── team_names.py
│   │   └── __init__.py
│   ├── scripts/             # Utility scripts
│   │   ├── db_setup.py
│   │   ├── preprocessing.py
│   │   └── __init__.py
│   ├── services/           # Business logic
│   │   ├── boxscore_service.py
│   │   └── __init__.py
│   └── test/              # Test directory
│       └── __init__.py
├── database/             # Database definitions
│   └── game_logs.sql
├── .gitignore
├── alembic.ini         # Alembic configuration
└── config.ini          # Project configuration
```

## Key Components

### Data Models
- Comprehensive game log tracking with 28 statistical fields
- Player and team identification
- Game outcome and location tracking
- Performance metrics including plus/minus and game score

### API Features
- Season-based filtering
- Date range queries
- Last N games analysis
- Player and team statistics aggregation
- Daily box score compilation

## Development Status

### Currently Implemented
- Core database schema
- Basic API routing structure
- Simple data preprocessing
- Player and team statistics endpoints
- Box score generation service
- Basic filtering capabilities

### Planned Features

#### Advanced Analytics
- Enhanced player metrics
- Team performance analysis
- Prediction modeling
- Historical trend analysis

#### Data Engineering Pipeline
- Apache Airflow integration for ETL workflows
- Automated data validation and cleaning
- Data quality monitoring
- Error handling and recovery procedures
- Historical data processing

#### Performance Optimizations
- Query optimization
- Caching implementation
- Database indexing improvements
- Response compression

## Development Setup

This project is currently set up for development and demonstration purposes. To explore or work with this codebase:

### Prerequisites
- Python 3.8+
- PostgreSQL
- FastAPI
- SQLAlchemy
- Pydantic
- pandas

### Configuration
The project requires some configuration to run:

1. Database Configuration
   - Create a PostgreSQL database
   - Create a `config.ini` file in the project root with the following structure:
     ```ini
     [postgresql]
     host=localhost
     port=5432
     database=your_database_name
     user=your_username
     password=your_password
     ```

2. Dependencies
   The project requires the following main Python packages:
   ```
   fastapi
   uvicorn
   sqlalchemy
   psycopg2-binary
   pandas
   pydantic
   ```

For a complete setup guide or questions about running the project, please open an issue on GitHub.

## API Documentation

Once running, view the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Portfolio Notes

This project demonstrates proficiency in:
- Modern Python backend development
- RESTful API design and implementation
- Database modeling and optimization
- Clean code practices and project structure
- Documentation and maintenance considerations

The planned data engineering enhancements will showcase additional skills in:
- ETL pipeline development
- Data workflow automation
- Data quality management
- System scaling and optimization

For questions or discussions about this portfolio project, feel free to reach out through GitHub issues.