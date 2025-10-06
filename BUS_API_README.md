# Bus Recommendation API

## Overview

The Bus Recommendation API provides intelligent bus route recommendations for the Enhanced Bus Recommendation System. It exposes the AI model through RESTful endpoints, allowing other projects to consume the bus recommendation functionality.

## Features

- 🚌 **Intelligent Route Recommendations**: Get optimized bus routes with quality scoring
- 🔄 **Multi-leg Journey Support**: Find routes with transfers when direct routes aren't available
- 🕐 **Time-aware Filtering**: Smart filtering based on preferred departure times
- 📅 **Day & Season Filtering**: Filter routes by day of week and seasonal schedules
- 🇫🇷 **French Interface**: Station names and days in French for user convenience
- ⚡ **Fast Response**: Optimized for quick recommendation generation
- 📖 **Auto-generated Docs**: Interactive API documentation with Swagger/OpenAPI

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required for this version.

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API service is running and data is loaded.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2025-09-01T20:45:20.852898",
  "version": "1.0.0",
  "data_loaded": true
}
```

### 2. Get Available Stations

**GET** `/stations`

Retrieve list of all available bus stations in French.

**Response:**

```json
{
  "success": true,
  "stations": [
    "Aeroport Tunis Carthage",
    "Amra",
    "Atrach",
    "Baraka Sahel",
    "Beni Khiar",
    "...more stations"
  ],
  "total_stations": 138
}
```

### 3. Get Available Seasons

**GET** `/seasons`

Retrieve list of available seasons for route filtering.

**Response:**

```json
{
  "success": true,
  "seasons": ["Summer", "Winter", "Ramadan"],
  "total_seasons": 3
}
```

### 4. Get Current Information

**GET** `/current-info`

Get current date, day, and season information for automatic filtering.

**Response:**

```json
{
  "success": true,
  "current_info": {
    "date": "2025-09-01",
    "day_french": "Lundi",
    "day_arabic": "إثنين",
    "season": "Summer",
    "month": 9,
    "formatted_date": "Monday, September 01, 2025"
  }
}
```

### 5. Get Route Recommendations

#### POST Method (Recommended)

**POST** `/recommendations`

**Content-Type:** `application/json`

**Request Body:**

```json
{
  "origin": "Nabeul",
  "destination": "Tunis",
  "preferred_time": "08:00",
  "preferred_day": "Lundi",
  "preferred_season": "Summer",
  "max_results": 5
}
```

#### GET Method (For Easy Testing)

**GET** `/recommendations?origin=Nabeul&destination=Tunis&preferred_time=08:00&preferred_day=Lundi&preferred_season=Summer&max_results=5`

**Parameters:**

- `origin` (required): Origin station name in French
- `destination` (required): Destination station name in French
- `preferred_time` (optional): Preferred departure time in HH:MM format
- `preferred_day` (optional): Day of week in French (Lundi, Mardi, Mercredi, Jeudi, Vendredi, Samedi, Dimanche)
- `preferred_season` (optional): Season (Summer, Winter, Ramadan)
- `max_results` (optional): Maximum results to return (1-20, default: 5)

**Response:**

```json
{
  "success": true,
  "message": "Found 5 route recommendations",
  "recommendations": [
    {
      "type": "direct",
      "departure_time": "08:00",
      "duration": 60,
      "service_type": "Luxe",
      "quality_score": 3.0,
      "route_details": "Nabeul → Tunis",
      "transfers": 0,
      "time_difference_info": "Exact match!",
      "transfer_details": null
    },
    {
      "type": "transfer",
      "departure_time": "08:15",
      "duration": 85,
      "service_type": "Mixed",
      "quality_score": 2.0,
      "route_details": "Nabeul → Hammamet → Tunis",
      "transfers": 1,
      "time_difference_info": "+15min from preferred",
      "transfer_details": {
        "transfer_station": "Hammamet",
        "first_leg_departure": "08:15",
        "first_leg_duration": 30,
        "first_leg_service": "Standard",
        "waiting_time": 15,
        "second_leg_departure": "09:00",
        "second_leg_duration": 40,
        "second_leg_service": "Luxe"
      }
    }
  ],
  "total_found": 5,
  "search_criteria": {
    "origin": "Nabeul",
    "destination": "Tunis",
    "preferred_time": "08:00",
    "preferred_day": "Lundi",
    "preferred_season": "Summer",
    "max_results": 5
  },
  "metadata": {
    "search_timestamp": "2025-09-01T20:45:36.123456",
    "direct_routes_found": 4,
    "transfer_routes_found": 1,
    "average_quality_score": 2.6
  }
}
```

### 6. Test Endpoint

**GET** `/test`

Simple endpoint to verify API is running with endpoint information.

## Documentation Endpoints

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## How to Use the API

### 1. Starting the API Server

```bash
cd /path/to/rima-ghayth
python api_main.py
```

### 2. Basic Usage Examples

#### Python Example

```python
import requests

# Get available stations first
stations_response = requests.get('http://localhost:8000/stations')
stations = stations_response.json()['stations']
print(f"Available stations: {stations[:5]}...")

# Get recommendations
payload = {
    "origin": "Nabeul",
    "destination": "Tunis",
    "preferred_time": "08:00",
    "preferred_day": "Lundi",
    "max_results": 3
}

response = requests.post('http://localhost:8000/recommendations', json=payload)
recommendations = response.json()

print(f"Found {len(recommendations['recommendations'])} recommendations:")
for rec in recommendations['recommendations']:
    print(f"- {rec['departure_time']} | {rec['duration']}min | {rec['service_type']} | Score: {rec['quality_score']}")
```

#### JavaScript/Fetch Example

```javascript
// Get recommendations
const response = await fetch("http://localhost:8000/recommendations", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    origin: "Nabeul",
    destination: "Tunis",
    preferred_time: "08:00",
    preferred_day: "Lundi",
    max_results: 5,
  }),
});

const data = await response.json();
console.log("Recommendations:", data.recommendations);
```

#### Using the Client Class

```python
from example_client import BusRecommendationClient

# Initialize client
client = BusRecommendationClient()

# Check API health
health = client.health_check()
print(f"API Status: {health['status']}")

# Get recommendations
recommendations = client.get_recommendations(
    origin="Nabeul",
    destination="Tunis",
    preferred_time="08:00"
)

# Find best route
best_route = client.find_best_route("Hammamet", "Nabeul")
if best_route:
    print(f"Best route: {best_route['departure_time']} ({best_route['duration']}min)")
```

### 3. AI Features in the API

The API incorporates AI-inspired intelligent algorithms that:

1. **Intelligent Route Scoring**: Uses multi-criteria scoring to rank routes
2. **Time Proximity Analysis**: Finds routes closest to your preferred time
3. **Service Quality Assessment**: Evaluates luxury vs standard services
4. **Peak Time Recognition**: Identifies and prioritizes optimal travel times
5. **Efficiency Detection**: Identifies short trips during business hours

The AI scoring system considers multiple factors with weighted importance:

- Time proximity (50% weight when time specified)
- Service quality (15-35% weight)
- Duration efficiency (10-20% weight)
- Peak time bonuses (10% weight)
- Special combinations like luxury service during peak times (5% weight)

### 4. Best Practices for Using the API

1. **Always check available stations first** using the `/stations` endpoint
2. **Use French station names** exactly as returned by the `/stations` endpoint
3. **Implement error handling** for network and API errors
4. **Consider caching station lists** as they don't change frequently
5. **Use the POST method** for production applications
6. **Always use HH:MM format** for time parameters
7. **Pay attention to quality scores** - higher scores indicate better recommendations

### 5. Troubleshooting

- If you get "Station not found" errors, check the spelling and use the exact French names
- If no routes are found, try removing filters (day/season) or try different times
- For connection errors, ensure the API server is running and port 8000 is accessible

## Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": "Error message description",
  "error_code": "ERROR_CODE",
  "details": {
    "message": "Additional error details"
  }
}
```

### Common Error Codes

- **400 Bad Request**: Invalid parameters or request format
- **404 Not Found**: Station not found in database
- **500 Internal Server Error**: Server processing error
- **503 Service Unavailable**: Bus data not loaded

## Running the API

### Prerequisites

1. Python 3.7+ installed
2. Bus schedule Excel file: `horaires-des-bus-de-la-srtgn.xlsx`

### Installation & Setup

```bash
# Navigate to project directory
cd /path/to/rima-ghayth

# Install dependencies
pip install -r requirements.txt

# Or install manually:
pip install fastapi uvicorn pandas numpy openpyxl

# Start the API server
python api_main.py
```

### Server Information

- **Port**: 8000
- **Host**: 0.0.0.0 (accessible from network)
- **Reload**: Enabled for development
- **Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc



