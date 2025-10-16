"""
API Models for Bus Recommendation System
Pydantic models for request/response validation and documentation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import datetime

class RouteRecommendationRequest(BaseModel):
    """Request model for route recommendations"""
    origin: str = Field(..., description="Origin station name in French", example="Nabeul")
    destination: str = Field(..., description="Destination station name in French", example="Tunis")
    preferred_time: Optional[str] = Field(None, description="Preferred departure time in HH:MM format", example="08:30")
    preferred_day: Optional[str] = Field(
        None, description="Preferred day of week in French", example="Lundi"
    )
    preferred_season: Optional[str] = Field(
        None, description="Preferred season", example="Summer"
    )
    max_results: Optional[int] = Field(5, description="Maximum number of recommendations to return", ge=1, le=20)

    @validator('preferred_time')
    def validate_time_format(cls, v):
        if v is not None:
            try:
                # Validate HH:MM format
                parts = v.split(':')
                if len(parts) != 2:
                    raise ValueError("Time must be in HH:MM format")
                hour, minute = int(parts[0]), int(parts[1])
                if not (0 <= hour <= 23):
                    raise ValueError("Hour must be between 00 and 23")
                if not (0 <= minute <= 59):
                    raise ValueError("Minute must be between 00 and 59")
                return f"{hour:02d}:{minute:02d}"
            except (ValueError, IndexError):
                raise ValueError("Invalid time format. Use HH:MM (e.g., 08:30)")
        return v
        
    @validator('preferred_day')
    def normalize_day(cls, v):
        """Normalize day name to handle case-insensitivity"""
        if v is not None:
            v = v.strip()
            # Map common day names to standard format
            day_mapping = {
                'lundi': 'Lundi', 'mardi': 'Mardi', 'mercredi': 'Mercredi',
                'jeudi': 'Jeudi', 'vendredi': 'Vendredi', 'samedi': 'Samedi',
                'dimanche': 'Dimanche'
            }
            return day_mapping.get(v.lower(), v)
        return v
        
    @validator('preferred_season')
    def normalize_season(cls, v):
        """Normalize season name to handle case-insensitivity"""
        if v is not None:
            v = v.strip()
            # Map common season names to standard format
            season_mapping = {
                'summer': 'Summer', 'été': 'Summer', 'ete': 'Summer',
                'winter': 'Winter', 'hiver': 'Winter',
                'ramadan': 'Ramadan'
            }
            return season_mapping.get(v.lower(), v)
        return v

class TransferDetails(BaseModel):
    """Details for transfer routes"""
    transfer_station: str = Field(..., description="Transfer station name in French")
    first_leg_departure: str = Field(..., description="First leg departure time (HH:MM)")
    first_leg_duration: int = Field(..., description="First leg duration in minutes")
    first_leg_service: str = Field(..., description="First leg service type")
    waiting_time: int = Field(..., description="Waiting time at transfer station in minutes")
    second_leg_departure: str = Field(..., description="Second leg departure time (HH:MM)")
    second_leg_duration: int = Field(..., description="Second leg duration in minutes")
    second_leg_service: str = Field(..., description="Second leg service type")

class RouteRecommendation(BaseModel):
    """Individual route recommendation"""
    type: Literal["direct", "transfer"] = Field(..., description="Route type")
    departure_time: str = Field(..., description="Departure time (HH:MM)")
    duration: int = Field(..., description="Total journey duration in minutes")
    service_type: str = Field(..., description="Service type (Standard, Luxe, Mixed)")
    quality_score: float = Field(..., description="Route quality score (0-3)", ge=0, le=3)
    route_details: str = Field(..., description="Route description")
    transfers: int = Field(..., description="Number of transfers", ge=0)
    time_difference_info: Optional[str] = Field(None, description="Information about time difference from preferred time")
    transfer_details: Optional[TransferDetails] = Field(None, description="Transfer details if applicable")

class RouteRecommendationResponse(BaseModel):
    """Response model for route recommendations"""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Response message")
    recommendations: List[RouteRecommendation] = Field(..., description="List of route recommendations")
    total_found: int = Field(..., description="Total number of recommendations found")
    search_criteria: dict = Field(..., description="Search criteria used")
    metadata: dict = Field(..., description="Additional metadata")

class StationListResponse(BaseModel):
    """Response model for available stations"""
    success: bool = Field(..., description="Whether the request was successful")
    stations: List[str] = Field(..., description="List of available station names in French")
    total_stations: int = Field(..., description="Total number of stations")

class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    data_loaded: bool = Field(..., description="Whether bus data is loaded")

class ErrorResponse(BaseModel):
    """Response model for errors"""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    details: Optional[dict] = Field(None, description="Additional error details")