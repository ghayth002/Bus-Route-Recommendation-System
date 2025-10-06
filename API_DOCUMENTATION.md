# Bus Recommendation API Documentation

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
    "Bir Bouregba",
    "Cite Universitaire",
    "Hammamet",
    "Nabeul",
    "Tunis",
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

## Usage Examples

### 1. Basic Route Search

```bash
# Using curl
curl -X GET "http://localhost:8000/recommendations?origin=Nabeul&destination=Tunis"

# Using PowerShell
Invoke-WebRequest -Uri "http://localhost:8000/recommendations?origin=Nabeul&destination=Tunis" -Method GET
```

### 2. Time-specific Search

```bash
curl -X GET "http://localhost:8000/recommendations?origin=Hammamet&destination=Tunis&preferred_time=14:30"
```

### 3. Detailed Search with POST

```bash
curl -X POST "http://localhost:8000/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Nabeul",
    "destination": "Tunis",
    "preferred_time": "08:00",
    "preferred_day": "Lundi", 
    "preferred_season": "Summer",
    "max_results": 3
  }'
```

### 4. JavaScript/Fetch Example

```javascript
// Get recommendations
const response = await fetch('http://localhost:8000/recommendations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    origin: 'Nabeul',
    destination: 'Tunis',
    preferred_time: '08:00',
    preferred_day: 'Lundi',
    max_results: 5
  })
});

const data = await response.json();
console.log('Recommendations:', data.recommendations);
```

### 5. Python Example

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

## Response Fields Explained

### Route Recommendation Fields

- **type**: `"direct"` or `"transfer"` - Route type
- **departure_time**: Departure time in HH:MM format
- **duration**: Total journey duration in minutes
- **service_type**: Service quality (`"Standard"`, `"Luxe"`, `"Mixed"`)
- **quality_score**: AI-calculated quality score (0-3, higher is better)
- **route_details**: Human-readable route description  
- **transfers**: Number of transfers required (0 for direct)
- **time_difference_info**: Information about time difference from preferred time
- **transfer_details**: Detailed transfer information (if applicable)

### Quality Score Factors

The AI model considers multiple factors for quality scoring:

1. **Time Proximity** (70% weight when preferred time specified)
   - Exact match: 3.0 points
   - Within 30 minutes: 2.5-3.0 points
   - Within 1 hour: 1.5-2.5 points
   - Beyond 2 hours: 0.1-0.5 points

2. **Service Quality** (15% weight)
   - Luxe service: 3 points
   - Standard service: 1 point

3. **Duration Efficiency** (10% weight)
   - Shorter routes score higher

4. **Additional Factors** (5% weight)
   - Peak time bonuses
   - Business hours efficiency
   - Service combinations

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

### Example Error Responses

**Station Not Found:**
```json
{
  "detail": "Origin station 'InvalidStation' not found in dataset"
}
```

**Invalid Time Format:**
```json
{
  "detail": "Invalid time format. Use HH:MM (e.g., 08:30)"
}
```

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

## Interactive Documentation

The API provides interactive documentation that you can use to test endpoints directly:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all available endpoints
- See request/response schemas
- Test endpoints directly in the browser
- Download OpenAPI specification

## Integration Tips

1. **Station Names**: Always get available stations first using `/stations` endpoint
2. **Error Handling**: Implement proper error handling for network and API errors  
3. **Caching**: Consider caching station lists as they don't change frequently
4. **Time Format**: Always use HH:MM format for time parameters
5. **French Names**: Use French station names as shown in the stations endpoint
6. **Quality Scores**: Higher quality scores indicate better route recommendations

## Performance

- **Response Time**: Typically 200-800ms for recommendations
- **Concurrent Requests**: Supports multiple simultaneous requests
- **Data Size**: Handles 138 stations with thousands of routes efficiently
- **Memory Usage**: ~50-100MB for loaded bus data

## Support

For issues or questions about the API:
1. Check the interactive documentation at `/docs`
2. Verify your request format matches the examples
3. Ensure all station names exist in the `/stations` response
4. Check server logs for detailed error information

---

**API Version**: 1.0.0  
**Last Updated**: September 1, 2025  
**Status**: ✅ Production Ready