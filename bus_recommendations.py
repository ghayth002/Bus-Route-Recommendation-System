#!/usr/bin/env python3
"""
Simple Bus Recommendation System with Multi-leg Support
Enhanced with French translations for stations and days
"""

import pandas as pd
import numpy as np

# Complete Translation Dictionary for ALL stations in the dataset
STATION_TRANSLATIONS = {
    # Main cities and towns
    'نابل': 'Nabeul',
    'القيروان': 'Kairouan',
    'تونس': 'Tunis',
    'زغوان': 'Zaghouan',

    # Nabeul area stations
    'نابل الورشة': 'Nabeul Atelier',
    'نابل  الورشة': 'Nabeul Atelier',
    'نابل الورشه': 'Nabeul Atelier',
    'الحي الجامعي': 'Cite Universitaire',
    'الحي الجامعي"الحزامية"': 'Cite Universitaire Hzamia',
    'الحي الصناعي': 'Zone Industrielle',
    'دار شعبان الفهري': 'Dar Chaabane Fehri',
    'دار شعبان': 'Dar Chaabane',
    'ديار بن سالم': 'Diar Ben Salem',
    'المعهد النموذجي': 'Institut Modele',
    'مبيتات طريق تونس': 'Mabitat Route Tunis',

    # Hammamet area
    'الحمامات': 'Hammamet',
    'الحمامات  الجنوبية': 'Hammamet Sud',
    'الحمامات الجنوبية': 'Hammamet Sud',
    'ياسمين الحمامات': 'Yasmine Hammamet',

    # Coastal towns
    'بئر بورقبة': 'Bir Bouregba',
    'براكة الساحل': 'Baraka Sahel',
    'تافرنين': 'Taferinine',
    'حمام بنت الجديدي': 'Hammam Bent Jdidi',
    'سيدي الجديدي': 'Sidi Jdidi',
    'حتوس': 'Htous',
    'جبنون': 'Jebnoun',
    'بني خيار': 'Beni Khiar',
    'بني وائل': 'Beni Wail',
    'قرمبالية': 'Korba',

    # Rural areas
    'المعمورة': 'Maamoura',
    'معمورة': 'Maamoura',
    'الصمعة': 'Somaa',
    'الصمعة حزاميه': 'Somaa Hzamia',
    'العامره': 'Amra',
    'العامره ': 'Amra',
    'المرازقة': 'Mrazga',
    'المزيرعة': 'Mziraa',
    'الأطرش': 'Atrach',
    'البسباسية': 'Basbassia',
    'الفحص': 'Fahs',
    'الفرينين': 'Freineine',
    'تازركة': 'Tazarka',
    'بيوب': 'Biyoub',
    'بوفيشة': 'Bouficha',
    'مزنين': 'Mznine',
    'واد الزيت': 'Oued Zeit',
    'بو علي': 'Bou Ali',

    # Airport
    'مطار تونس قرطاج': 'Aeroport Tunis Carthage',

    # Industrial/Commercial
    'SIPHAT': 'SIPHAT',

    # Complex route names (combinations)
    'الحمامات - بئر بورقبة - بني وائل': 'Hammamet - Bir Bouregba - Beni Wail',
    'الحمامات - ياسمين الحمامات': 'Hammamet - Yasmine Hammamet',
    'الفرينين - نابل  الورشة': 'Freineine - Nabeul Atelier',
    'المعمورة - ديار بن سالم': 'Maamoura - Diar Ben Salem',
    'براكة الساحل - الحمامات': 'Baraka Sahel - Hammamet',
    'براكة الساحل - بني وائل': 'Baraka Sahel - Beni Wail',
    'براكة الساحل - تافرنين - حمام بنت الجديدي': 'Baraka Sahel - Taferinine - Hammam Bent Jdidi',
    'براكة الساحل - تافرنين - حمام بنت الجديدي - حتوس': 'Baraka Sahel - Taferinine - Hammam Bent Jdidi - Htous',
    'براكة الساحل - حتوس': 'Baraka Sahel - Htous',
    'بني خيار - المعهد النموذجي': 'Beni Khiar - Institut Modele',
    'بني خيار- المعمورة': 'Beni Khiar - Maamoura',
    'بني وائل -  بئر بورقبة': 'Beni Wail - Bir Bouregba',
    'تافرنين - سيدي حمّاد - براكة الساحل': 'Taferinine - Sidi Hammad - Baraka Sahel',
    'جبنون - المنشار - تافرنين': 'Jebnoun - Menchar - Taferinine',
    'جبنون - براكة الساحل': 'Jebnoun - Baraka Sahel',
    'حتوس - حمام بنت الجديدي': 'Htous - Hammam Bent Jdidi',
    'حتوس - سيدي الجديدي - البسباسية - جبنون': 'Htous - Sidi Jdidi - Basbassia - Jebnoun',
    'حمام بنت الجديدي - سيدي الجديدي': 'Hammam Bent Jdidi - Sidi Jdidi',
    'دار شعبان الفهري - الحي الجامعي': 'Dar Chaabane Fehri - Cite Universitaire',
    'دار شعبان – المعهد النموذجي': 'Dar Chaabane - Institut Modele',
    'ديار بن سالم - بني خيار': 'Diar Ben Salem - Beni Khiar',
    'سيدي الجديدي - حتوس': 'Sidi Jdidi - Htous',
    'نابل -  بيوب -الفرينين': 'Nabeul - Biyoub - Freineine',
    'نابل - الصمعة': 'Nabeul - Somaa',
    'نابل - المعمورة': 'Nabeul - Maamoura',
    'نابل - دار شعبان': 'Nabeul - Dar Chaabane',
    'نابل - ديار بن سالم': 'Nabeul - Diar Ben Salem',
    'نابل الورشة - الحي الجامعي': 'Nabeul Atelier - Cite Universitaire',
    'نابل الورشة - المعهد النموذجي': 'Nabeul Atelier - Institut Modele',
    'نابل الورشة - ديار بن سالم': 'Nabeul Atelier - Diar Ben Salem',
    'ياسمين الحمامات - براكة الساحل': 'Yasmine Hammamet - Baraka Sahel',
    'بئر بورقبة - الحمامات': 'Bir Bouregba - Hammamet',

    # Additional stations found in dataset (completing the 138 stations)
    'الحي الجامعي"الحزامية"': 'Cite Universitaire Hzamia',
    'الصمعة حزاميه': 'Somaa Hzamia',
    'مبيتات طريق تونس': 'Mabitat Route Tunis',
    'الحمامات  الجنوبية': 'Hammamet Sud',
    'معمورة': 'Maamoura',
    'العامره ': 'Amra',
    'نابل  الورشة': 'Nabeul Atelier',
    'نابل الورشه': 'Nabeul Atelier',
    'المزيرعة': 'Mziraa',
    'بوفيشة': 'Bouficha',
    'بو علي': 'Bou Ali',

    # Additional complex routes and variations
    'الحي الجامعي"الحزامية" - نابل الورشة': 'Cite Universitaire Hzamia - Nabeul Atelier',
    'الصمعة - نابل': 'Somaa - Nabeul',
    'الصمعة حزاميه - نابل الورشة': 'Somaa Hzamia - Nabeul Atelier',
    'العامره  - نابل الورشة': 'Amra - Nabeul Atelier',
    'المرازقة - نابل الورشة': 'Mrazga - Nabeul Atelier',
    'المزيرعة - نابل الورشة': 'Mziraa - Nabeul Atelier',
    'الأطرش - نابل الورشة': 'Atrach - Nabeul Atelier',
    'البسباسية - نابل الورشة': 'Basbassia - Nabeul Atelier',
    'الفحص - نابل الورشة': 'Fahs - Nabeul Atelier',
    'تازركة - نابل الورشة': 'Tazarka - Nabeul Atelier',
    'بوفيشة - نابل الورشة': 'Bouficha - Nabeul Atelier',
    'مزنين - نابل الورشة': 'Mznine - Nabeul Atelier',
    'واد الزيت - نابل الورشة': 'Oued Zeit - Nabeul Atelier',
    'بو علي - نابل الورشة': 'Bou Ali - Nabeul Atelier',
    'قرمبالية - نابل الورشة': 'Korba - Nabeul Atelier',
    'قرمبالية - نابل': 'Korba - Nabeul',
    'قرمبالية - تونس': 'Korba - Tunis',
    'قرمبالية - زغوان': 'Korba - Zaghouan',
    'نابل - قرمبالية': 'Nabeul - Korba',
    'تونس - قرمبالية': 'Tunis - Korba',
    'زغوان - قرمبالية': 'Zaghouan - Korba',
    'زغوان - نابل': 'Zaghouan - Nabeul',
    'زغوان - تونس': 'Zaghouan - Tunis',
    'نابل - زغوان': 'Nabeul - Zaghouan',
    'تونس - زغوان': 'Tunis - Zaghouan',
    'القيروان - نابل': 'Kairouan - Nabeul',
    'القيروان - تونس': 'Kairouan - Tunis',
    'نابل - القيروان': 'Nabeul - Kairouan',
    'تونس - القيروان': 'Tunis - Kairouan',
    'تونس - نابل': 'Tunis - Nabeul',
    'نابل - تونس': 'Nabeul - Tunis',
    'مطار تونس قرطاج - نابل': 'Aeroport Tunis Carthage - Nabeul',
    'نابل - مطار تونس قرطاج': 'Nabeul - Aeroport Tunis Carthage',
    'SIPHAT - نابل الورشة': 'SIPHAT - Nabeul Atelier',
    'نابل الورشة - SIPHAT': 'Nabeul Atelier - SIPHAT',

    # Additional missing stations (whitespace variations and new ones)
    'برج السدرية': 'Borj Sedria',
    'الحي الجامعي" الحزامية"': 'Cite Universitaire Hzamia',

    # Handle whitespace variations by mapping them to existing translations
    '  الحمامات  الجنوبية': 'Hammamet Sud',
    '  العامره ': 'Amra',
    '  بيوب': 'Biyoub',
    '  نابل الورشه': 'Nabeul Atelier',
    '  ياسمين الحمامات': 'Yasmine Hammamet',
    ' الحمامات': 'Hammamet',
    ' بئر بورقبة': 'Bir Bouregba',
    ' معمورة': 'Maamoura',
    ' نابل الورشة': 'Nabeul Atelier',
    'الأطرش ': 'Atrach',
    'البسباسية ': 'Basbassia',
    'الحمامات ': 'Hammamet',
    'الحي الجامعي ': 'Cite Universitaire',
    'الحي الصناعي ': 'Zone Industrielle',
    'الصمعة ': 'Somaa',
    'العامره ': 'Amra',
    'المرازقة ': 'Mrazga',
    'المزيرعة ': 'Mziraa',
    'المعمورة ': 'Maamoura',
    'المعهد النموذجي ': 'Institut Modele',
    'بئر بورقبة ': 'Bir Bouregba',
    'براكة الساحل ': 'Baraka Sahel',
    'بني خيار ': 'Beni Khiar',
    'بني وائل ': 'Beni Wail',
    'بوفيشة ': 'Bouficha',
    'بيوب ': 'Biyoub',
    'تازركة ': 'Tazarka',
    'تافرنين ': 'Taferinine',
    'تونس ': 'Tunis',
    'جبنون ': 'Jebnoun',
    'حتوس ': 'Htous',
    'حمام بنت الجديدي ': 'Hammam Bent Jdidi',
    'دار شعبان ': 'Dar Chaabane',
    'دار شعبان الفهري ': 'Dar Chaabane Fehri',
    'ديار بن سالم ': 'Diar Ben Salem',
    'سيدي الجديدي ': 'Sidi Jdidi',
    'قرمبالية ': 'Korba',
    'مبيتات طريق تونس ': 'Mabitat Route Tunis',
    'مزنين ': 'Mznine',
    'نابل ': 'Nabeul',
    'نابل الورشة ': 'Nabeul Atelier',
    'نابل الورشه ': 'Nabeul Atelier',
    'واد الزيت ': 'Oued Zeit',
    'ياسمين الحمامات ': 'Yasmine Hammamet'
}

DAY_TRANSLATIONS = {
    # Arabic to French
    'إثنين': 'Lundi',
    'ثلاثاء': 'Mardi',
    'اربعاء': 'Mercredi',
    'خميس': 'Jeudi',
    'جمعة': 'Vendredi',
    'سبت': 'Samedi',
    'أحد': 'Dimanche'
}

# Reverse translations (French to Arabic) for internal processing
STATION_REVERSE = {v: k for k, v in STATION_TRANSLATIONS.items()}
DAY_REVERSE = {v: k for k, v in DAY_TRANSLATIONS.items()}

def translate_station_to_french(arabic_name):
    """Translate Arabic station name to French"""
    return STATION_TRANSLATIONS.get(arabic_name, arabic_name)

def translate_station_to_arabic(french_name):
    """Translate French station name to Arabic for data lookup"""
    return STATION_REVERSE.get(french_name, french_name)

def find_matching_station(df, station_name, column_name):
    """Find matching station name handling whitespace variations"""
    # Get all unique stations from the column
    all_stations = df[column_name].dropna().unique()

    # First try exact match
    if station_name in all_stations:
        return station_name

    # Try with stripped whitespace
    station_stripped = station_name.strip()
    for station in all_stations:
        if station.strip() == station_stripped:
            return station

    # Try partial match
    for station in all_stations:
        if station_stripped in station.strip() or station.strip() in station_stripped:
            return station

    return None

def translate_day_to_french(arabic_day):
    """Translate Arabic day to French"""
    return DAY_TRANSLATIONS.get(arabic_day, arabic_day)

def translate_day_to_arabic(french_day):
    """Translate French day to Arabic for data lookup"""
    return DAY_REVERSE.get(french_day, french_day)

def load_data():
    """Load and preprocess the bus data with French translations"""
    print("📊 Loading bus schedule data...")

    df = pd.read_excel("horaires-des-bus-de-la-srtgn.xlsx")
    df.columns = df.columns.str.strip()

    # Clean data
    if 'Unnamed: 19' in df.columns and 'Unnamed: 20' in df.columns:
        df.drop(columns=['Unnamed: 19', 'Unnamed: 20'], inplace=True, errors='ignore')

    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

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

    df['durée_min'] = df['المدة'].apply(convert_to_minutes)
    df['depart_min'] = df['ساعة الإنطلاق'].apply(convert_to_minutes)
    df.dropna(subset=['durée_min', 'depart_min'], inplace=True)

    # Add French translations
    df['origin_french'] = df['محطة الانطلاق'].apply(translate_station_to_french)
    df['destination_french'] = df['محطة الوصول'].apply(translate_station_to_french)

    print(f"✅ Data loaded: {len(df)} routes available")
    print("🇫🇷 French translations added for stations")
    return df



def find_direct_routes(df, origin_french, destination_french, preferred_time=None):
    """Find direct routes between origin and destination using French names"""
    # Convert French names to Arabic for data lookup
    origin_arabic = translate_station_to_arabic(origin_french)
    destination_arabic = translate_station_to_arabic(destination_french)

    # Find matching stations in the dataset (handles whitespace issues)
    origin_match = find_matching_station(df, origin_arabic, 'محطة الانطلاق')
    destination_match = find_matching_station(df, destination_arabic, 'محطة الوصول')

    if not origin_match or not destination_match:
        print(f"⚠️  Station matching issue:")
        print(f"   Origin: {origin_french} → {origin_arabic} → {origin_match}")
        print(f"   Destination: {destination_french} → {destination_arabic} → {destination_match}")
        return pd.DataFrame()

    routes = df[
        (df['محطة الانطلاق'] == origin_match) &
        (df['محطة الوصول'] == destination_match)
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

def find_transfer_routes(df, origin_french, destination_french, preferred_time=None):
    """Find routes with one transfer using French names"""
    # Convert French names to Arabic for data lookup
    origin_arabic = translate_station_to_arabic(origin_french)
    destination_arabic = translate_station_to_arabic(destination_french)

    # Find matching stations in the dataset
    origin_match = find_matching_station(df, origin_arabic, 'محطة الانطلاق')
    destination_match = find_matching_station(df, destination_arabic, 'محطة الوصول')

    if not origin_match or not destination_match:
        return []

    # Find potential transfer stations
    from_origin = df[df['محطة الانطلاق'] == origin_match]['محطة الوصول'].unique()
    to_destination = df[df['محطة الوصول'] == destination_match]['محطة الانطلاق'].unique()
    transfer_stations = set(from_origin) & set(to_destination)
    
    if not transfer_stations:
        return []
    
    transfer_routes = []
    transfer_time = 15  # 15 minutes minimum transfer time
    
    for transfer_station in transfer_stations:
        # First leg: origin → transfer
        first_leg_options = df[
            (df['محطة الانطلاق'] == origin_match) &
            (df['محطة الوصول'] == transfer_station)
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
        second_leg_options = df[
            (df['محطة الانطلاق'] == transfer_station) &
            (df['محطة الوصول'] == destination_match) &
            (df['depart_min'] >= second_leg_start)
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



def get_route_recommendations(df, origin_french, destination_french, preferred_time=None, max_results=5):
    """Get comprehensive route recommendations"""
    print(f"\n🔍 Finding routes: {origin_french} → {destination_french}")

    # Convert to Arabic
    origin_arabic = translate_station_to_arabic(origin_french)
    destination_arabic = translate_station_to_arabic(destination_french)

    # Find matching stations
    origin_match = find_matching_station(df, origin_arabic, 'محطة الانطلاق')
    destination_match = find_matching_station(df, destination_arabic, 'محطة الوصول')

    if not origin_match:
        print(f"❌ Origin station '{origin_french}' not found in dataset")
        return []

    if not destination_match:
        print(f"❌ Destination station '{destination_french}' not found in dataset")
        return []

    # Find direct routes
    direct_routes = df[
        (df['محطة الانطلاق'] == origin_match) &
        (df['محطة الوصول'] == destination_match)
    ].copy()

    recommendations = []

    if not direct_routes.empty:
        print(f"✅ Found {len(direct_routes)} direct routes")

        # Apply time filter if specified
        filtered_routes = direct_routes.copy()
        if preferred_time:
            try:
                if ':' in str(preferred_time):
                    h, m = map(int, str(preferred_time).split(':'))
                    preferred_min = h * 60 + m
                    filtered_routes = direct_routes[direct_routes['depart_min'] >= preferred_min]
                    if filtered_routes.empty:
                        print(f"⚠️  No routes after {preferred_time}, showing all routes")
                        filtered_routes = direct_routes
            except:
                filtered_routes = direct_routes

        # Score and rank routes
        filtered_routes = filtered_routes.copy()

        # Calculate route quality score
        filtered_routes['quality_score'] = 0

        # Service quality (Luxe > Standard)
        filtered_routes['service_score'] = filtered_routes['نوع الخدمة'].apply(
            lambda x: 3 if x == 'رفاهة' else 1
        )

        # Time preference (morning and evening preferred)
        filtered_routes['hour'] = filtered_routes['depart_min'] // 60
        filtered_routes['time_score'] = filtered_routes['hour'].apply(
            lambda x: 3 if x in [7,8,9,17,18,19] else 2 if x in [6,10,16,20] else 1
        )

        # Duration efficiency (shorter is better)
        min_duration = filtered_routes['durée_min'].min()
        max_duration = filtered_routes['durée_min'].max()
        if max_duration > min_duration:
            filtered_routes['duration_score'] = 3 - 2 * (filtered_routes['durée_min'] - min_duration) / (max_duration - min_duration)
        else:
            filtered_routes['duration_score'] = 3

        # Combined score
        filtered_routes['quality_score'] = (
            filtered_routes['service_score'] +
            filtered_routes['time_score'] +
            filtered_routes['duration_score']
        ) / 3

        # Sort by quality score and departure time
        best_routes = filtered_routes.nlargest(max_results, ['quality_score', 'depart_min'])

        for _, route in best_routes.iterrows():
            hour = int(route['depart_min'] // 60)
            minute = int(route['depart_min'] % 60)
            duration = int(route['durée_min'])
            service_french = "Luxe" if route['نوع الخدمة'] == 'رفاهة' else "Standard"

            recommendation = {
                'type': 'direct',
                'departure_time': f"{hour:02d}:{minute:02d}",
                'duration': duration,
                'service_type': service_french,
                'quality_score': route['quality_score'],
                'route_details': f"{origin_french} → {destination_french}",
                'total_duration': duration,
                'transfers': 0
            }
            recommendations.append(recommendation)

    else:
        print("❌ No direct routes found")
        print("🔄 Searching for routes with transfers...")

        # Find transfer routes using existing function
        transfer_routes = find_transfer_routes(df, origin_french, destination_french, preferred_time)

        for transfer in transfer_routes[:max_results]:
            recommendation = {
                'type': 'transfer',
                'departure_time': f"{int(transfer['first_leg']['depart_min'] // 60):02d}:{int(transfer['first_leg']['depart_min'] % 60):02d}",
                'duration': int(transfer['total_duration']),
                'service_type': "Mixed",
                'quality_score': 2.0,
                'route_details': f"{origin_french} → {transfer['transfer_station_french']} → {destination_french}",
                'total_duration': int(transfer['total_duration']),
                'transfers': 1,
                'transfer_details': transfer
            }
            recommendations.append(recommendation)

    return recommendations

def display_recommendations(recommendations):
    """Display route recommendations in a user-friendly format"""
    if not recommendations:
        print("\n❌ No routes found")
        return

    print(f"\n🎯 ROUTE RECOMMENDATIONS ({len(recommendations)} options)")
    print("=" * 60)

    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. 🚌 OPTION {i} - {rec['type'].upper()} ROUTE")
        print(f"   🕐 Departure: {rec['departure_time']}")
        print(f"   ⏱️  Total Duration: {rec['duration']} minutes")
        print(f"   🚌 Service: {rec['service_type']}")
        print(f"   📍 Route: {rec['route_details']}")
        print(f"   ⭐ Quality Score: {rec['quality_score']:.1f}/3.0")

        if rec['type'] == 'transfer' and 'transfer_details' in rec:
            transfer = rec['transfer_details']
            print(f"   🔄 Transfers: {rec['transfers']}")
            print(f"   📋 Journey Details:")

            f_hour = int(transfer['first_leg']['depart_min'] // 60)
            f_min = int(transfer['first_leg']['depart_min'] % 60)
            f_duration = int(transfer['first_leg']['durée_min'])
            f_service = "Luxe" if transfer['first_leg']['نوع الخدمة'] == 'رفاهة' else "Standard"

            s_hour = int(transfer['second_leg']['depart_min'] // 60)
            s_min = int(transfer['second_leg']['depart_min'] % 60)
            s_duration = int(transfer['second_leg']['durée_min'])
            s_service = "Luxe" if transfer['second_leg']['نوع الخدمة'] == 'رفاهة' else "Standard"

            print(f"      Leg 1: {f_hour:02d}:{f_min:02d} | {f_duration}min | {f_service}")
            print(f"      Transfer: 15min wait at {transfer['transfer_station_french']}")
            print(f"      Leg 2: {s_hour:02d}:{s_min:02d} | {s_duration}min | {s_service}")

def main():
    """Main interactive function with French interface"""
    print("🚌 SYSTÈME DE RECOMMANDATION DE ROUTES DE BUS")
    print("="*50)
    print("🇫🇷 Interface en Français - French Interface")
    print("✅ Provides actual route recommendations!")
    print("="*50)

    # Load data
    df = load_data()

    # Show available stations in French
    origins = df['محطة الانطلاق'].dropna().unique()
    destinations = df['محطة الوصول'].dropna().unique()
    all_stations = sorted(set(list(origins) + list(destinations)))

    print(f"\n📍 Available Stations ({len(all_stations)} total)")
    print("Sample French names:")
    for i, station in enumerate(all_stations[:15], 1):
        french_name = translate_station_to_french(station.strip())
        print(f"   {i:2d}. {french_name}")

    if len(all_stations) > 15:
        print(f"   ... and {len(all_stations)-15} more stations")

    print(f"\n📅 Available Days - Jours Disponibles:")
    french_days = list(DAY_TRANSLATIONS.values())
    print("   " + " | ".join(french_days))
    
    while True:
        print("\n" + "-"*50)
        print("🔍 OBTENIR DES RECOMMANDATIONS - GET ROUTE RECOMMENDATIONS")
        print("-"*50)

        origin_french = input("📍 Enter origin station (French name): ").strip()
        if not origin_french:
            break

        destination_french = input("🎯 Enter destination station (French name): ").strip()
        if not destination_french:
            break

        preferred_time = input("⏰ Enter preferred time (HH:MM, or Enter for any): ").strip()
        if not preferred_time:
            preferred_time = None

        # Get recommendations
        recommendations = get_route_recommendations(df, origin_french, destination_french, preferred_time)

        # Display results
        display_recommendations(recommendations)

        another = input("\n🔄 Search for another route? (y/n): ").strip().lower()
        if another not in ['y', 'yes', 'o', 'oui']:
            break
    
    print("\n🎉 Merci d'avoir utilisé le Système de Recommandation de Bus!")
    print("🎉 Thank you for using the Bus Recommendation System!")
    print("🚌 Bon voyage! Safe travels! ✨")

if __name__ == "__main__":
    main()
