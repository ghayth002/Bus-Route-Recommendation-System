"""
Example Client for Bus Recommendation API
Demonstrates how to consume the API from another project
"""

import requests
import json
from typing import List, Dict, Optional

class BusRecommendationClient:
    """Client class for the Bus Recommendation API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the client with API base URL"""
        self.base_url = base_url.rstrip('/')
        
    def health_check(self) -> Dict:
        """Check if the API is healthy and running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def get_available_stations(self) -> List[str]:
        """Get list of available bus stations"""
        try:
            response = requests.get(f"{self.base_url}/stations", timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('stations', [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting stations: {e}")
            return []
    
    def get_available_seasons(self) -> List[str]:
        """Get list of available seasons"""
        try:
            response = requests.get(f"{self.base_url}/seasons", timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('seasons', [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting seasons: {e}")
            return []
    
    def get_current_info(self) -> Dict:
        """Get current date and season information"""
        try:
            response = requests.get(f"{self.base_url}/current-info", timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('current_info', {})
        except requests.exceptions.RequestException as e:
            print(f"Error getting current info: {e}")
            return {}
    
    def get_recommendations(self, 
                          origin: str, 
                          destination: str,
                          preferred_time: Optional[str] = None,
                          preferred_day: Optional[str] = None,
                          preferred_season: Optional[str] = None,
                          max_results: int = 5) -> Dict:
        """
        Get bus route recommendations
        
        Args:
            origin: Origin station name in French
            destination: Destination station name in French  
            preferred_time: Preferred time in HH:MM format (optional)
            preferred_day: Day of week in French (optional)
            preferred_season: Season filter (optional)
            max_results: Maximum number of results (1-20)
            
        Returns:
            Dictionary with recommendations and metadata
        """
        try:
            payload = {
                "origin": origin,
                "destination": destination,
                "max_results": max_results
            }
            
            # Add optional parameters
            if preferred_time:
                payload["preferred_time"] = preferred_time
            if preferred_day:
                payload["preferred_day"] = preferred_day  
            if preferred_season:
                payload["preferred_season"] = preferred_season
            
            response = requests.post(
                f"{self.base_url}/recommendations",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "recommendations": [],
                "total_found": 0
            }
    
    def find_best_route(self, origin: str, destination: str, 
                       preferred_time: Optional[str] = None) -> Optional[Dict]:
        """
        Find the single best route recommendation
        
        Returns the highest quality scoring route or None if no routes found
        """
        result = self.get_recommendations(
            origin=origin,
            destination=destination, 
            preferred_time=preferred_time,
            max_results=1
        )
        
        if result.get('success') and result.get('recommendations'):
            return result['recommendations'][0]
        return None
    
    def search_routes_by_time_range(self, origin: str, destination: str,
                                   start_time: str, end_time: str) -> List[Dict]:
        """
        Find all routes within a time range
        
        Args:
            origin: Origin station
            destination: Destination station
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            
        Returns:
            List of routes within the time range
        """
        # Get more results to filter by time range
        result = self.get_recommendations(
            origin=origin,
            destination=destination,
            max_results=20
        )
        
        if not result.get('success'):
            return []
        
        # Filter by time range
        filtered_routes = []
        for route in result.get('recommendations', []):
            route_time = route.get('departure_time', '')
            if start_time <= route_time <= end_time:
                filtered_routes.append(route)
        
        return filtered_routes

def demo_basic_usage():
    """Demonstrate basic API usage"""
    print("🚌 Bus Recommendation API Client Demo")
    print("=" * 50)
    
    # Initialize client
    client = BusRecommendationClient()
    
    # 1. Health check
    print("1. Health Check:")
    health = client.health_check()
    print(f"   Status: {health.get('status', 'unknown')}")
    print(f"   Data Loaded: {health.get('data_loaded', False)}")
    print()
    
    # 2. Get available stations
    print("2. Available Stations:")
    stations = client.get_available_stations()
    print(f"   Found {len(stations)} stations")
    print(f"   Sample: {', '.join(stations[:5])}")
    print()
    
    # 3. Get current info
    print("3. Current Information:")
    current_info = client.get_current_info()
    print(f"   Today: {current_info.get('day_french', 'N/A')}")
    print(f"   Season: {current_info.get('season', 'N/A')}")
    print()
    
    # 4. Basic route search
    print("4. Basic Route Search (Nabeul → Tunis):")
    recommendations = client.get_recommendations("Nabeul", "Tunis")
    
    if recommendations.get('success'):
        print(f"   Found {recommendations['total_found']} recommendations")
        
        for i, route in enumerate(recommendations['recommendations'][:3], 1):
            print(f"   {i}. {route['departure_time']} | {route['duration']}min | {route['service_type']} | Score: {route['quality_score']:.1f}")
    else:
        print(f"   Error: {recommendations.get('error', 'Unknown error')}")
    print()
    
    # 5. Time-specific search
    print("5. Time-specific Search (Nabeul → Tunis at 08:00):")
    timed_recommendations = client.get_recommendations(
        origin="Nabeul",
        destination="Tunis", 
        preferred_time="08:00"
    )
    
    if timed_recommendations.get('success'):
        best_route = timed_recommendations['recommendations'][0]
        print(f"   Best Match: {best_route['departure_time']} ({best_route['time_difference_info'] or 'No time info'})")
        print(f"   Duration: {best_route['duration']} minutes")
        print(f"   Service: {best_route['service_type']}")
    print()
    
    # 6. Find best route shortcut
    print("6. Find Best Route (Hammamet → Nabeul):")
    best_route = client.find_best_route("Hammamet", "Nabeul")
    
    if best_route:
        print(f"   Best Route: {best_route['departure_time']} | {best_route['duration']}min | Score: {best_route['quality_score']:.1f}")
        if best_route['transfers'] > 0:
            print(f"   Transfers: {best_route['transfers']}")
    else:
        print("   No routes found")

def demo_advanced_usage():
    """Demonstrate advanced API usage patterns"""
    print("\n🔧 Advanced Usage Examples")
    print("=" * 50)
    
    client = BusRecommendationClient()
    
    # 1. Station validation
    print("1. Station Name Validation:")
    stations = client.get_available_stations()
    
    def validate_station(station_name: str) -> bool:
        return station_name in stations
    
    test_stations = ["Nabeul", "Tunis", "InvalidStation"]
    for station in test_stations:
        valid = validate_station(station)
        print(f"   '{station}': {'✅ Valid' if valid else '❌ Invalid'}")
    print()
    
    # 2. Error handling
    print("2. Error Handling Example:")
    try:
        result = client.get_recommendations("InvalidOrigin", "InvalidDestination")
        if not result.get('success'):
            print(f"   Handled error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   Exception caught: {e}")
    print()
    
    # 3. Bulk route checking
    print("3. Bulk Route Checking:")
    route_pairs = [
        ("Nabeul", "Tunis"),
        ("Hammamet", "Nabeul"),
        ("Tunis", "Korba")
    ]
    
    for origin, destination in route_pairs:
        best = client.find_best_route(origin, destination)
        if best:
            print(f"   {origin} → {destination}: {best['departure_time']} ({best['duration']}min)")
        else:
            print(f"   {origin} → {destination}: No routes found")
    print()
    
    # 4. Time range search
    print("4. Time Range Search (Nabeul → Tunis, 07:00-10:00):")
    time_filtered = client.search_routes_by_time_range(
        "Nabeul", "Tunis", "07:00", "10:00"
    )
    
    print(f"   Found {len(time_filtered)} routes in time range:")
    for route in time_filtered[:3]:
        print(f"   - {route['departure_time']} | {route['service_type']} | Score: {route['quality_score']:.1f}")

if __name__ == "__main__":
    """Run the demo"""
    try:
        # Basic usage demo
        demo_basic_usage()
        
        # Advanced usage demo  
        demo_advanced_usage()
        
        print("\n✅ Demo completed successfully!")
        print("\n💡 Integration Tips:")
        print("   - Always validate station names against /stations endpoint")
        print("   - Implement error handling for network issues")
        print("   - Cache station lists since they don't change often")
        print("   - Use quality scores to rank recommendations")
        print("   - Consider time preferences for better user experience")
        
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("   Make sure the API server is running on http://localhost:8000")