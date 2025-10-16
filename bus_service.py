"""
Bus Recommendation Service
Core business logic for bus route recommendations
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os

# Import translation dictionaries and helper functions from the main module
from bus_recommendations import (
    STATION_TRANSLATIONS, DAY_TRANSLATIONS, SEASON_TRANSLATIONS,
    STATION_REVERSE, DAY_REVERSE, SEASON_REVERSE,
    translate_station_to_french, translate_station_to_arabic,
    find_matching_station, get_current_date_info,
    get_available_seasons_from_data
)

class BusRecommendationService:
    """Service class for handling bus route recommendations"""
    
    def __init__(self, excel_file_path: str = "horaires-des-bus-de-la-srtgn.xlsx"):
        """Initialize the service with bus schedule data"""
        self.excel_file_path = excel_file_path
        self.df = None
        self.available_seasons = []
        self.available_stations = []
        self.data_loaded = False
        
        # Load data on initialization
        self.load_data()
    
    def load_data(self) -> bool:
        """Load and preprocess the bus data"""
        try:
            print(f"📊 Loading bus schedule data from: {self.excel_file_path}")
            
            if not os.path.exists(self.excel_file_path):
                raise FileNotFoundError(f"Excel file not found: {self.excel_file_path}")
            
            self.df = pd.read_excel(self.excel_file_path)
            self.df.columns = self.df.columns.str.strip()
            
            # Clean data
            if 'Unnamed: 19' in self.df.columns and 'Unnamed: 20' in self.df.columns:
                self.df.drop(columns=['Unnamed: 19', 'Unnamed: 20'], inplace=True, errors='ignore')
            
            for col in self.df.select_dtypes(include=['object']).columns:
                self.df[col] = self.df[col].astype(str).str.strip()
            
            # Convert time columns
            def convert_to_minutes(time_obj):
                if pd.isna(time_obj):
                    return None
                if isinstance(time_obj, str) and ':' in time_obj:
                    try:
                        h, m = map(int, time_obj.split(':'))
                        return h * 60 + m
                    except:
                        return None
                elif isinstance(time_obj, (int, float)):
                    return int(time_obj)
                return None
            
            self.df['durée_min'] = self.df['المدة'].apply(convert_to_minutes)
            self.df['depart_min'] = self.df['ساعة الإنطلاق'].apply(convert_to_minutes)
            self.df.dropna(subset=['durée_min', 'depart_min'], inplace=True)
            
            # Add French translations
            self.df['origin_french'] = self.df['محطة الانطلاق'].apply(translate_station_to_french)
            self.df['destination_french'] = self.df['محطة الوصول'].apply(translate_station_to_french)
            
            # Get available seasons and stations
            self.available_seasons = get_available_seasons_from_data(self.df)
            
            # Get all unique stations in French
            origins = self.df['محطة الانطلاق'].dropna().unique()
            destinations = self.df['محطة الوصول'].dropna().unique()
            all_stations_arabic = sorted(set(list(origins) + list(destinations)))
            self.available_stations = sorted(set([
                translate_station_to_french(station.strip()) 
                for station in all_stations_arabic
            ]))
            
            self.data_loaded = True
            print(f"✅ Data loaded: {len(self.df)} routes available")
            print(f"🇫🇷 French translations added for {len(self.available_stations)} stations")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            self.data_loaded = False
            return False
    
    def get_available_stations(self) -> List[str]:
        """Get list of available stations in French"""
        return self.available_stations.copy()
    
    def get_available_seasons(self) -> List[str]:
        """Get list of available seasons"""
        return self.available_seasons.copy()
    
    def find_direct_routes(self, origin_french: str, destination_french: str, 
                          preferred_time: Optional[str] = None) -> pd.DataFrame:
        """Find direct routes between origin and destination using French names"""
        if not self.data_loaded:
            return pd.DataFrame()
        
        # Normalize input station names (trim whitespace)
        origin_french = origin_french.strip()
        destination_french = destination_french.strip()
            
        # Convert French names to Arabic for data lookup with improved case-insensitive matching
        origin_arabic = translate_station_to_arabic(origin_french)
        destination_arabic = translate_station_to_arabic(destination_french)
        
        # Find matching stations in the dataset with fuzzy matching for misspellings
        origin_match = find_matching_station(self.df, origin_arabic, 'محطة الانطلاق')
        destination_match = find_matching_station(self.df, destination_arabic, 'محطة الوصول')
        
        if not origin_match:
            # Try direct search in French names for better matching
            for idx, row in self.df.iterrows():
                if row['origin_french'].lower() == origin_french.lower() or origin_french.lower() in row['origin_french'].lower():
                    origin_match = row['محطة الانطلاق']
                    break
        
        if not destination_match:
            # Try direct search in French names for better matching
            for idx, row in self.df.iterrows():
                if row['destination_french'].lower() == destination_french.lower() or destination_french.lower() in row['destination_french'].lower():
                    destination_match = row['محطة الوصول']
                    break
        
        if not origin_match or not destination_match:
            return pd.DataFrame()
        
        routes = self.df[
            (self.df['محطة الانطلاق'] == origin_match) &
            (self.df['محطة الوصول'] == destination_match)
        ].copy()
        
        # Apply time filter if specified
        if preferred_time and not routes.empty:
            try:
                if ':' in str(preferred_time):
                    h, m = map(int, str(preferred_time).split(':'))
                    preferred_min = h * 60 + m
                    routes = routes[routes['depart_min'] >= preferred_min]
            except:
                pass
        
        return routes
    
    def find_transfer_routes(self, origin_french: str, destination_french: str, 
                           preferred_time: Optional[str] = None, 
                           preferred_day: Optional[str] = None, 
                           preferred_season: Optional[str] = None) -> List[Dict]:
        """Find routes with one transfer using French names"""
        if not self.data_loaded:
            return []
        
        # Normalize input station names (trim whitespace)
        origin_french = origin_french.strip()
        destination_french = destination_french.strip()
            
        # Convert French names to Arabic for data lookup with improved case-insensitive matching
        origin_arabic = translate_station_to_arabic(origin_french)
        destination_arabic = translate_station_to_arabic(destination_french)
        
        # Find matching stations in the dataset with fuzzy matching for misspellings
        origin_match = find_matching_station(self.df, origin_arabic, 'محطة الانطلاق')
        destination_match = find_matching_station(self.df, destination_arabic, 'محطة الوصول')
        
        if not origin_match:
            # Try direct search in French names for better matching
            for idx, row in self.df.iterrows():
                if row['origin_french'].lower() == origin_french.lower() or origin_french.lower() in row['origin_french'].lower():
                    origin_match = row['محطة الانطلاق']
                    break
        
        if not destination_match:
            # Try direct search in French names for better matching
            for idx, row in self.df.iterrows():
                if row['destination_french'].lower() == destination_french.lower() or destination_french.lower() in row['destination_french'].lower():
                    destination_match = row['محطة الوصول']
                    break
        
        if not origin_match or not destination_match:
            return []
        
        # Find potential transfer stations
        from_origin = self.df[self.df['محطة الانطلاق'] == origin_match]['محطة الوصول'].unique()
        to_destination = self.df[self.df['محطة الوصول'] == destination_match]['محطة الانطلاق'].unique()
        transfer_stations = set(from_origin) & set(to_destination)
        
        if not transfer_stations:
            return []
        
        transfer_routes = []
        transfer_time = 15  # 15 minutes minimum transfer time
        
        for transfer_station in transfer_stations:
            # First leg: origin → transfer
            first_leg_options = self.df[
                (self.df['محطة الانطلاق'] == origin_match) &
                (self.df['محطة الوصول'] == transfer_station)
            ].copy()
            
            if first_leg_options.empty:
                continue
                
            # Apply time filter for first leg
            if preferred_time:
                try:
                    if ':' in str(preferred_time):
                        h, m = map(int, str(preferred_time).split(':'))
                        preferred_min = h * 60 + m
                        first_leg_options = first_leg_options[first_leg_options['depart_min'] >= preferred_min]
                except:
                    pass
                    
            if first_leg_options.empty:
                continue
            
            # Get best first leg (shortest duration)
            best_first_leg = first_leg_options.nsmallest(1, 'durée_min').iloc[0]
            
            # Calculate when second leg can start
            second_leg_start = best_first_leg['depart_min'] + best_first_leg['durée_min'] + transfer_time
            
            # Second leg: transfer → destination
            second_leg_options = self.df[
                (self.df['محطة الانطلاق'] == transfer_station) &
                (self.df['محطة الوصول'] == destination_match) &
                (self.df['depart_min'] >= second_leg_start)
            ].copy()
            
            if second_leg_options.empty:
                continue
                
            # Get best second leg
            best_second_leg = second_leg_options.nsmallest(1, 'durée_min').iloc[0]
            
            # Calculate journey metrics
            total_duration = (best_second_leg['depart_min'] + best_second_leg['durée_min']) - best_first_leg['depart_min']
            waiting_time = best_second_leg['depart_min'] - second_leg_start
            
            journey = {
                'transfer_station': transfer_station,
                'transfer_station_french': translate_station_to_french(transfer_station),
                'total_duration': total_duration,
                'first_leg': best_first_leg,
                'second_leg': best_second_leg,
                'waiting_time': waiting_time,
                'origin_french': origin_french,
                'destination_french': destination_french
            }
            
            transfer_routes.append(journey)
        
        # Sort by total duration
        transfer_routes.sort(key=lambda x: x['total_duration'])
        return transfer_routes
    
    def get_recommendations(self, origin_french: str, destination_french: str,
                          preferred_time: Optional[str] = None,
                          preferred_day: Optional[str] = None,
                          preferred_season: Optional[str] = None,
                          max_results: int = 5) -> List[Dict]:
        """Get comprehensive route recommendations with filtering"""
        
        if not self.data_loaded:
            raise Exception("Bus data not loaded. Please check if the Excel file exists.")
        
        # Normalize input station names (trim whitespace)
        origin_french = origin_french.strip()
        destination_french = destination_french.strip()
        
        # Convert to Arabic for data lookup with improved case-insensitive matching
        origin_arabic = translate_station_to_arabic(origin_french)
        destination_arabic = translate_station_to_arabic(destination_french)
        
        # Find matching stations with fuzzy matching for misspellings
        origin_match = find_matching_station(self.df, origin_arabic, 'محطة الانطلاق')
        destination_match = find_matching_station(self.df, destination_arabic, 'محطة الوصول')
        
        if not origin_match:
            # Try direct search in French names for better matching
            for idx, row in self.df.iterrows():
                if row['origin_french'].lower() == origin_french.lower() or origin_french.lower() in row['origin_french'].lower():
                    origin_match = row['محطة الانطلاق']
                    break
            
            if not origin_match:
                raise ValueError(f"Origin station '{origin_french}' not found in dataset")
        
        if not destination_match:
            # Try direct search in French names for better matching
            for idx, row in self.df.iterrows():
                if row['destination_french'].lower() == destination_french.lower() or destination_french.lower() in row['destination_french'].lower():
                    destination_match = row['محطة الوصول']
                    break
            
            if not destination_match:
                raise ValueError(f"Destination station '{destination_french}' not found in dataset")
        
        # Find direct routes
        direct_routes = self.df[
            (self.df['محطة الانطلاق'] == origin_match) &
            (self.df['محطة الوصول'] == destination_match)
        ].copy()
        
        recommendations = []
        
        if not direct_routes.empty:
            # Apply DAY filtering if specified
            if preferred_day:
                day_arabic = DAY_REVERSE.get(preferred_day, preferred_day)
                if day_arabic in direct_routes.columns:
                    day_filtered = direct_routes[direct_routes[day_arabic].str.strip() == 'X']
                    if not day_filtered.empty:
                        direct_routes = day_filtered
            
            # Apply SEASON filtering if specified
            if preferred_season:
                if 'الموسم' in direct_routes.columns:
                    season_arabic = None
                    for arabic_season, french_season in SEASON_TRANSLATIONS.items():
                        if french_season.lower() == preferred_season.lower():
                            season_arabic = arabic_season
                            break
                    
                    if season_arabic:
                        season_filtered = direct_routes[direct_routes['الموسم'].str.strip() == season_arabic.strip()]
                        if not season_filtered.empty:
                            direct_routes = season_filtered
            
            # Apply smart time filtering and scoring
            filtered_routes = direct_routes.copy()
            
            if preferred_time:
                try:
                    if ':' in str(preferred_time):
                        h, m = map(int, str(preferred_time).split(':'))
                        preferred_min = h * 60 + m
                        
                        # Smart time filtering
                        time_window_routes = direct_routes[
                            (direct_routes['depart_min'] >= preferred_min) &
                            (direct_routes['depart_min'] <= preferred_min + 240)  # Within 4 hours
                        ]
                        
                        if not time_window_routes.empty:
                            filtered_routes = time_window_routes
                        else:
                            next_routes = direct_routes[direct_routes['depart_min'] >= preferred_min]
                            if not next_routes.empty:
                                filtered_routes = next_routes.head(10)
                except:
                    pass
            
            # Calculate quality scores
            filtered_routes = filtered_routes.copy()
            filtered_routes['quality_score'] = 0
            
            # Service quality score
            filtered_routes['service_score'] = filtered_routes['نوع الخدمة'].apply(
                lambda x: 3 if x == 'رفاهة' else 1
            )
            
            # Duration efficiency score
            min_duration = filtered_routes['durée_min'].min()
            max_duration = filtered_routes['durée_min'].max()
            if max_duration > min_duration:
                filtered_routes['duration_score'] = 3 - 2 * (filtered_routes['durée_min'] - min_duration) / (max_duration - min_duration)
            else:
                filtered_routes['duration_score'] = 3
            
            # Time proximity score if preferred time specified
            if preferred_time:
                try:
                    if ':' in str(preferred_time):
                        h, m = map(int, str(preferred_time).split(':'))
                        preferred_min = h * 60 + m
                        
                        filtered_routes['time_diff'] = filtered_routes['depart_min'] - preferred_min
                        
                        def calculate_time_proximity(time_diff):
                            if time_diff < 0:
                                return 0.1
                            elif time_diff == 0:
                                return 3.0
                            elif time_diff <= 30:
                                return 3.0 - (time_diff / 30) * 0.5
                            elif time_diff <= 60:
                                return 2.5 - ((time_diff - 30) / 30) * 1.0
                            elif time_diff <= 120:
                                return 1.5 - ((time_diff - 60) / 60) * 1.0
                            else:
                                return 0.5 - min((time_diff - 120) / 480, 0.4)
                        
                        filtered_routes['time_proximity_score'] = filtered_routes['time_diff'].apply(calculate_time_proximity)
                        
                        # Weighted scoring with time priority
                        filtered_routes['quality_score'] = (
                            0.7 * filtered_routes['time_proximity_score'] +
                            0.15 * filtered_routes['service_score'] +
                            0.15 * filtered_routes['duration_score']
                        )
                except:
                    filtered_routes['quality_score'] = (
                        filtered_routes['service_score'] + filtered_routes['duration_score']
                    ) / 2
            else:
                # No preferred time - general scoring
                filtered_routes['hour'] = filtered_routes['depart_min'] // 60
                filtered_routes['time_score'] = filtered_routes['hour'].apply(
                    lambda x: 3 if x in [7,8,9,17,18,19] else 2 if x in [6,10,16,20] else 1
                )
                
                filtered_routes['quality_score'] = (
                    0.4 * filtered_routes['service_score'] +
                    0.3 * filtered_routes['time_score'] +
                    0.3 * filtered_routes['duration_score']
                )
            
            # Remove duplicates and get best routes
            filtered_routes['route_key'] = (
                filtered_routes['depart_min'].astype(str) + '_' +
                filtered_routes['نوع الخدمة'].astype(str) + '_' +
                filtered_routes['durée_min'].astype(str)
            )
            
            unique_routes = filtered_routes.loc[
                filtered_routes.groupby('route_key')['quality_score'].idxmax()
            ].copy()
            
            best_routes = unique_routes.nlargest(max_results, 'quality_score')
            
            for _, route in best_routes.iterrows():
                hour = int(route['depart_min'] // 60)
                minute = int(route['depart_min'] % 60)
                duration = int(route['durée_min'])
                service_french = "Luxe" if route['نوع الخدمة'] == 'رفاهة' else "Standard"
                
                # Calculate time difference info
                time_diff_info = ""
                if preferred_time and 'time_diff' in route:
                    time_diff_minutes = int(route['time_diff'])
                    if time_diff_minutes == 0:
                        time_diff_info = "Exact match!"
                    elif time_diff_minutes <= 30:
                        time_diff_info = f"+{time_diff_minutes}min from preferred"
                    else:
                        hours_diff = time_diff_minutes // 60
                        mins_diff = time_diff_minutes % 60
                        if hours_diff > 0:
                            time_diff_info = f"+{hours_diff}h{mins_diff:02d}m from preferred"
                        else:
                            time_diff_info = f"+{mins_diff}min from preferred"
                
                recommendation = {
                    'type': 'direct',
                    'departure_time': f"{hour:02d}:{minute:02d}",
                    'duration': duration,
                    'service_type': service_french,
                    'quality_score': float(route['quality_score']),
                    'route_details': f"{origin_french} → {destination_french}",
                    'total_duration': duration,
                    'transfers': 0,
                    'time_difference_info': time_diff_info if time_diff_info else None
                }
                recommendations.append(recommendation)
        
        else:
            # Find transfer routes if no direct routes
            transfer_routes = self.find_transfer_routes(
                origin_french, destination_french, preferred_time, preferred_day, preferred_season
            )
            
            for transfer in transfer_routes[:max_results]:
                # Extract transfer details
                f_hour = int(transfer['first_leg']['depart_min'] // 60)
                f_min = int(transfer['first_leg']['depart_min'] % 60)
                f_duration = int(transfer['first_leg']['durée_min'])
                f_service = "Luxe" if transfer['first_leg']['نوع الخدمة'] == 'رفاهة' else "Standard"
                
                s_hour = int(transfer['second_leg']['depart_min'] // 60)
                s_min = int(transfer['second_leg']['depart_min'] % 60)
                s_duration = int(transfer['second_leg']['durée_min'])
                s_service = "Luxe" if transfer['second_leg']['نوع الخدمة'] == 'رفاهة' else "Standard"
                
                transfer_details = {
                    'transfer_station': transfer['transfer_station_french'],
                    'first_leg_departure': f"{f_hour:02d}:{f_min:02d}",
                    'first_leg_duration': f_duration,
                    'first_leg_service': f_service,
                    'waiting_time': int(transfer['waiting_time']),
                    'second_leg_departure': f"{s_hour:02d}:{s_min:02d}",
                    'second_leg_duration': s_duration,
                    'second_leg_service': s_service
                }
                
                recommendation = {
                    'type': 'transfer',
                    'departure_time': f"{f_hour:02d}:{f_min:02d}",
                    'duration': int(transfer['total_duration']),
                    'service_type': 'Mixed',
                    'quality_score': 2.0,
                    'route_details': f"{origin_french} → {transfer['transfer_station_french']} → {destination_french}",
                    'total_duration': int(transfer['total_duration']),
                    'transfers': 1,
                    'time_difference_info': None,
                    'transfer_details': transfer_details
                }
                recommendations.append(recommendation)
        
        return recommendations
    
    def is_data_loaded(self) -> bool:
        """Check if data is loaded successfully"""
        return self.data_loaded
    
    def get_current_info(self) -> Dict:
        """Get current date and season information"""
        return get_current_date_info()