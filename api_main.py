"""
FastAPI Application for Bus Recommendation System
REST API endpoints to expose bus route recommendation functionality
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import uvicorn
from typing import Optional, List
import traceback
import logging

# Import models and service
from api_models import (
    RouteRecommendationRequest, RouteRecommendationResponse, RouteRecommendation,
    StationListResponse, HealthCheckResponse, ErrorResponse, TransferDetails
)
from bus_service import BusRecommendationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Bus Recommendation API",
    description="Enhanced Bus Recommendation System API for intelligent route suggestions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the bus recommendation service
bus_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize the bus recommendation service on startup"""
    global bus_service
    try:
        logger.info("🚀 Starting Bus Recommendation API...")
        bus_service = BusRecommendationService()
        if bus_service.is_data_loaded():
            logger.info("✅ Bus data loaded successfully")
        else:
            logger.error("❌ Failed to load bus data")
    except Exception as e:
        logger.error(f"❌ Error during startup: {str(e)}")
        bus_service = None

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "details": {"message": str(exc)}
        }
    )

@app.get("/", response_model=HealthCheckResponse)
async def root():
    """Root endpoint - Health check"""
    return await health_check()

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    global bus_service
    
    return HealthCheckResponse(
        status="healthy" if bus_service and bus_service.is_data_loaded() else "unhealthy",
        timestamp=datetime.now(),
        version="1.0.0",
        data_loaded=bus_service.is_data_loaded() if bus_service else False
    )

@app.get("/stations", response_model=StationListResponse)
async def get_stations():
    """Get list of available stations"""
    global bus_service
    
    if not bus_service or not bus_service.is_data_loaded():
        raise HTTPException(
            status_code=503,
            detail="Bus data service unavailable"
        )
    
    try:
        stations = bus_service.get_available_stations()
        return StationListResponse(
            success=True,
            stations=stations,
            total_stations=len(stations)
        )
    except Exception as e:
        logger.error(f"Error getting stations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving stations: {str(e)}"
        )

@app.get("/seasons")
async def get_seasons():
    """Get list of available seasons"""
    global bus_service
    
    if not bus_service or not bus_service.is_data_loaded():
        raise HTTPException(
            status_code=503,
            detail="Bus data service unavailable"
        )
    
    try:
        seasons = bus_service.get_available_seasons()
        return {
            "success": True,
            "seasons": seasons,
            "total_seasons": len(seasons)
        }
    except Exception as e:
        logger.error(f"Error getting seasons: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving seasons: {str(e)}"
        )

@app.get("/current-info")
async def get_current_info():
    """Get current date and season information"""
    global bus_service
    
    if not bus_service or not bus_service.is_data_loaded():
        raise HTTPException(
            status_code=503,
            detail="Bus data service unavailable"
        )
    
    try:
        current_info = bus_service.get_current_info()
        return {
            "success": True,
            "current_info": current_info
        }
    except Exception as e:
        logger.error(f"Error getting current info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving current info: {str(e)}"
        )

@app.post("/recommendations", response_model=RouteRecommendationResponse)
async def get_route_recommendations(request: RouteRecommendationRequest):
    """Get bus route recommendations based on search criteria"""
    global bus_service
    
    if not bus_service or not bus_service.is_data_loaded():
        raise HTTPException(
            status_code=503,
            detail="Bus data service unavailable"
        )
    
    try:
        logger.info(f"Processing recommendation request: {request.origin} → {request.destination}")
        
        # Get recommendations from service
        recommendations_data = bus_service.get_recommendations(
            origin_french=request.origin,
            destination_french=request.destination,
            preferred_time=request.preferred_time,
            preferred_day=request.preferred_day,
            preferred_season=request.preferred_season,
            max_results=request.max_results
        )
        
        # Convert to API model format
        recommendations = []
        for rec_data in recommendations_data:
            # Handle transfer details if present
            transfer_details = None
            if rec_data.get('transfer_details'):
                td = rec_data['transfer_details']
                transfer_details = TransferDetails(
                    transfer_station=td['transfer_station'],
                    first_leg_departure=td['first_leg_departure'],
                    first_leg_duration=td['first_leg_duration'],
                    first_leg_service=td['first_leg_service'],
                    waiting_time=td['waiting_time'],
                    second_leg_departure=td['second_leg_departure'],
                    second_leg_duration=td['second_leg_duration'],
                    second_leg_service=td['second_leg_service']
                )
            
            recommendation = RouteRecommendation(
                type=rec_data['type'],
                departure_time=rec_data['departure_time'],
                duration=rec_data['duration'],
                service_type=rec_data['service_type'],
                quality_score=rec_data['quality_score'],
                route_details=rec_data['route_details'],
                transfers=rec_data['transfers'],
                time_difference_info=rec_data.get('time_difference_info'),
                transfer_details=transfer_details
            )
            recommendations.append(recommendation)
        
        # Build search criteria
        search_criteria = {
            "origin": request.origin,
            "destination": request.destination,
            "preferred_time": request.preferred_time,
            "preferred_day": request.preferred_day,
            "preferred_season": request.preferred_season,
            "max_results": request.max_results
        }
        
        # Build metadata
        metadata = {
            "search_timestamp": datetime.now().isoformat(),
            "direct_routes_found": sum(1 for r in recommendations if r.type == "direct"),
            "transfer_routes_found": sum(1 for r in recommendations if r.type == "transfer"),
            "average_quality_score": sum(r.quality_score for r in recommendations) / len(recommendations) if recommendations else 0
        }
        
        message = f"Found {len(recommendations)} route recommendations"
        if not recommendations:
            message = "No routes found for the specified criteria"
        
        return RouteRecommendationResponse(
            success=True,
            message=message,
            recommendations=recommendations,
            total_found=len(recommendations),
            search_criteria=search_criteria,
            metadata=metadata
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting recommendations: {str(e)}"
        )

@app.get("/recommendations", response_model=RouteRecommendationResponse)
async def get_route_recommendations_get(
    origin: str = Query(..., description="Origin station name in French"),
    destination: str = Query(..., description="Destination station name in French"),
    preferred_time: Optional[str] = Query(None, description="Preferred departure time (HH:MM)"),
    preferred_day: Optional[str] = Query(None, description="Preferred day of week in French"),
    preferred_season: Optional[str] = Query(None, description="Preferred season"),
    max_results: int = Query(5, description="Maximum number of results", ge=1, le=20)
):
    """Get bus route recommendations using GET method (for easier testing)"""
    
    # Create request object and use the POST handler
    request_obj = RouteRecommendationRequest(
        origin=origin,
        destination=destination,
        preferred_time=preferred_time,
        preferred_day=preferred_day,
        preferred_season=preferred_season,
        max_results=max_results
    )
    
    return await get_route_recommendations(request_obj)

# Helper endpoint for testing
@app.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {
        "status": "OK", 
        "message": "Bus Recommendation API is running!",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "stations": "/stations",
            "seasons": "/seasons",
            "current_info": "/current-info",
            "recommendations_post": "/recommendations (POST)",
            "recommendations_get": "/recommendations (GET)",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    """Run the API server"""
    print("🚌 Starting Bus Recommendation API Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Alternative Docs: http://localhost:8000/redoc")
    print("🧪 Test Endpoint: http://localhost:8000/test")
    
    uvicorn.run(
        "api_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )