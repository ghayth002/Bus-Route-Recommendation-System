# Quick Start Guide: Bus Recommendation API

## 🚀 Quick Setup

### 1. Start the API Server

```bash
cd /path/to/rima-ghayth
python api_main.py
```

The server will start on `http://localhost:8000`

### 2. Test the API

Open your browser and visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Test Endpoint**: http://localhost:8000/test
- **Health Check**: http://localhost:8000/health

## 🔥 Common Use Cases

### Get Available Stations

```bash
curl http://localhost:8000/stations
```

### Basic Route Search

```bash
curl "http://localhost:8000/recommendations?origin=Nabeul&destination=Tunis"
```

### Time-Specific Search

```bash  
curl "http://localhost:8000/recommendations?origin=Hammamet&destination=Tunis&preferred_time=14:30"
```

### Complete Search with Filters

```bash
curl -X POST http://localhost:8000/recommendations \
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

## 🐍 Python Integration

### Simple Example

```python
import requests

# Get recommendations
response = requests.get(
    "http://localhost:8000/recommendations",
    params={
        "origin": "Nabeul",
        "destination": "Tunis",
        "preferred_time": "08:00"
    }
)

data = response.json()
print(f"Found {data['total_found']} recommendations")

# Display best route
if data['recommendations']:
    best = data['recommendations'][0]
    print(f"Best: {best['departure_time']} | {best['duration']}min | {best['service_type']}")
```

### Using the Client Class

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

## 🌐 JavaScript/Frontend Integration

### Fetch API

```javascript
// Get recommendations
async function getRoutes(origin, destination, time) {
  try {
    const response = await fetch('http://localhost:8000/recommendations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        origin: origin,
        destination: destination,
        preferred_time: time,
        max_results: 5
      })
    });
    
    const data = await response.json();
    
    if (data.success) {
      return data.recommendations;
    } else {
      console.error('API Error:', data.error);
      return [];
    }
  } catch (error) {
    console.error('Network Error:', error);
    return [];
  }
}

// Usage
const routes = await getRoutes('Nabeul', 'Tunis', '08:00');
routes.forEach(route => {
  console.log(`${route.departure_time} | ${route.duration}min | ${route.service_type}`);
});
```

### React Hook Example

```javascript
import { useState, useEffect } from 'react';

function useBusRecommendations(origin, destination, preferredTime) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    if (!origin || !destination) return;
    
    setLoading(true);
    setError(null);
    
    fetch('http://localhost:8000/recommendations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        origin,
        destination,
        preferred_time: preferredTime,
        max_results: 10
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        setRecommendations(data.recommendations);
      } else {
        setError(data.error || 'Unknown error');
      }
    })
    .catch(err => {
      setError(err.message);
    })
    .finally(() => {
      setLoading(false);
    });
  }, [origin, destination, preferredTime]);
  
  return { recommendations, loading, error };
}

// Usage in component
function BusSearch() {
  const { recommendations, loading, error } = useBusRecommendations(
    'Nabeul', 'Tunis', '08:00'
  );
  
  if (loading) return <div>Loading routes...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div>
      <h3>Route Recommendations</h3>
      {recommendations.map((route, index) => (
        <div key={index}>
          {route.departure_time} | {route.duration}min | {route.service_type}
        </div>
      ))}
    </div>
  );
}
```

## 📱 Mobile App Integration

### Flutter/Dart Example

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class BusApiService {
  static const String baseUrl = 'http://localhost:8000';
  
  static Future<List<dynamic>> getRecommendations({
    required String origin,
    required String destination,
    String? preferredTime,
    int maxResults = 5,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/recommendations'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'origin': origin,
          'destination': destination,
          'preferred_time': preferredTime,
          'max_results': maxResults,
        }),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['success']) {
          return data['recommendations'];
        }
      }
      return [];
    } catch (e) {
      print('Error getting recommendations: $e');
      return [];
    }
  }
}

// Usage
final routes = await BusApiService.getRecommendations(
  origin: 'Nabeul',
  destination: 'Tunis',
  preferredTime: '08:00',
);
```

## 🧪 Testing the API

### Run the Example Client

```bash
python example_client.py
```

### Manual Testing with curl

```bash
# Test health
curl http://localhost:8000/health

# Get stations  
curl http://localhost:8000/stations | jq .

# Test recommendations
curl "http://localhost:8000/recommendations?origin=Nabeul&destination=Tunis&max_results=3" | jq .
```

### Using PowerShell (Windows)

```powershell
# Test basic endpoint
Invoke-WebRequest -Uri "http://localhost:8000/test" -Method GET

# Get recommendations
$body = @{
    origin = "Nabeul"
    destination = "Tunis"  
    preferred_time = "08:00"
    max_results = 3
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/recommendations" -Method POST -Body $body -ContentType "application/json"
```

## 🚨 Troubleshooting

### API Not Starting

1. **Check dependencies**: `pip install -r requirements.txt`
2. **Check Excel file**: Ensure `horaires-des-bus-de-la-srtgn.xlsx` exists
3. **Check port**: Make sure port 8000 is not in use

### Station Not Found Errors

1. **Get station list**: Use `/stations` endpoint to see valid names
2. **Use French names**: Station names must be in French (e.g., "Nabeul" not "نابل")
3. **Check spelling**: Station names are case-sensitive

### No Routes Found

1. **Check station names**: Ensure both origin and destination exist
2. **Try different time**: Some routes may not operate at all times
3. **Remove filters**: Try without day/season filters first

### Connection Errors

1. **Check server**: Ensure API server is running
2. **Check URL**: Verify `http://localhost:8000` is accessible
3. **Check firewall**: Ensure port 8000 is not blocked

## 📋 Station Names Reference

Common stations (use exact French names):
- Nabeul
- Tunis  
- Hammamet
- Korba
- Zaghouan
- Kairouan
- Aeroport Tunis Carthage
- Yasmine Hammamet
- Cite Universitaire

Get the complete list: `curl http://localhost:8000/stations`

## 🔗 API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Check API status |
| GET | `/stations` | Get available stations |
| GET | `/seasons` | Get available seasons |  
| GET | `/current-info` | Get current date info |
| POST | `/recommendations` | Get route recommendations |
| GET | `/recommendations` | Get recommendations (query params) |
| GET | `/test` | Test endpoint |
| GET | `/docs` | Interactive documentation |

---

**Need Help?** 
- 📖 Full docs: http://localhost:8000/docs
- 🔍 Detailed guide: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- 🧪 Example code: [example_client.py](example_client.py)