#!/usr/bin/env python3
"""
Test script for fuzzy matching and case-insensitive station name handling
"""

import requests
import json
from time import sleep

# API endpoint (adjust if your server runs on a different port/host)
BASE_URL = "http://localhost:8000"

def test_case_insensitive():
    """Test case-insensitive station name matching"""
    print("\n🧪 TESTING CASE-INSENSITIVE MATCHING")
    print("=" * 50)
    
    test_cases = [
        # Original, lowercase, uppercase, mixed case
        ("Nabeul", "nabeul", "NABEUL", "nAbEuL"),
        ("Tunis", "tunis", "TUNIS", "TuNiS"),
        ("Hammamet", "hammamet", "HAMMAMET", "hAmmAmEt"),
    ]
    
    for original, lowercase, uppercase, mixed_case in test_cases:
        print(f"\n🔍 Testing variations of '{original}':")
        
        # Test lowercase
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin={lowercase}&destination=Tunis")
            if response.status_code == 200:
                print(f"  ✅ Lowercase '{lowercase}' - SUCCESS")
            else:
                print(f"  ❌ Lowercase '{lowercase}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Lowercase '{lowercase}' - ERROR: {str(e)}")
        
        # Test uppercase
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin={uppercase}&destination=Tunis")
            if response.status_code == 200:
                print(f"  ✅ Uppercase '{uppercase}' - SUCCESS")
            else:
                print(f"  ❌ Uppercase '{uppercase}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Uppercase '{uppercase}' - ERROR: {str(e)}")
        
        # Test mixed case
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin={mixed_case}&destination=Tunis")
            if response.status_code == 200:
                print(f"  ✅ Mixed case '{mixed_case}' - SUCCESS")
            else:
                print(f"  ❌ Mixed case '{mixed_case}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Mixed case '{mixed_case}' - ERROR: {str(e)}")
        
        sleep(0.5)  # Small delay to avoid overwhelming the server

def test_fuzzy_matching():
    """Test fuzzy matching for misspelled station names"""
    print("\n🧪 TESTING FUZZY MATCHING FOR MISSPELLINGS")
    print("=" * 50)
    
    test_cases = [
        # Original, misspelling 1, misspelling 2
        ("Nabeul", "Nabel", "Nabul"),
        ("Hammamet", "Hamamet", "Hammamt"),
        ("Tunis", "Tunus", "Tunis"),
        ("Korba", "Corba", "Korb"),
    ]
    
    for original, misspell1, misspell2 in test_cases:
        print(f"\n🔍 Testing misspellings of '{original}':")
        
        # Test first misspelling
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin={misspell1}&destination=Tunis")
            if response.status_code == 200:
                print(f"  ✅ Misspelling '{misspell1}' - SUCCESS")
            else:
                print(f"  ❌ Misspelling '{misspell1}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Misspelling '{misspell1}' - ERROR: {str(e)}")
        
        # Test second misspelling
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin={misspell2}&destination=Tunis")
            if response.status_code == 200:
                print(f"  ✅ Misspelling '{misspell2}' - SUCCESS")
            else:
                print(f"  ❌ Misspelling '{misspell2}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Misspelling '{misspell2}' - ERROR: {str(e)}")
        
        sleep(0.5)  # Small delay to avoid overwhelming the server

def test_whitespace_handling():
    """Test handling of extra whitespace in station names"""
    print("\n🧪 TESTING WHITESPACE HANDLING")
    print("=" * 50)
    
    test_cases = [
        # Original, with leading space, with trailing space, with both
        ("Nabeul", " Nabeul", "Nabeul ", " Nabeul "),
        ("Tunis", " Tunis", "Tunis ", " Tunis "),
    ]
    
    for original, leading, trailing, both in test_cases:
        print(f"\n🔍 Testing whitespace variations of '{original}':")
        
        # Test leading whitespace
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin={leading}&destination=Tunis")
            if response.status_code == 200:
                print(f"  ✅ Leading whitespace '{leading}' - SUCCESS")
            else:
                print(f"  ❌ Leading whitespace '{leading}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Leading whitespace '{leading}' - ERROR: {str(e)}")
        
        # Test trailing whitespace
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin={trailing}&destination=Tunis")
            if response.status_code == 200:
                print(f"  ✅ Trailing whitespace '{trailing}' - SUCCESS")
            else:
                print(f"  ❌ Trailing whitespace '{trailing}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Trailing whitespace '{trailing}' - ERROR: {str(e)}")
        
        # Test both leading and trailing whitespace
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin={both}&destination=Tunis")
            if response.status_code == 200:
                print(f"  ✅ Both whitespaces '{both}' - SUCCESS")
            else:
                print(f"  ❌ Both whitespaces '{both}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Both whitespaces '{both}' - ERROR: {str(e)}")
        
        sleep(0.5)  # Small delay to avoid overwhelming the server

def test_day_and_season_normalization():
    """Test day and season name normalization"""
    print("\n🧪 TESTING DAY AND SEASON NORMALIZATION")
    print("=" * 50)
    
    # Test day normalization
    day_test_cases = [
        # Original, lowercase, uppercase
        ("Lundi", "lundi", "LUNDI"),
        ("Vendredi", "vendredi", "VENDREDI"),
    ]
    
    for original, lowercase, uppercase in day_test_cases:
        print(f"\n🔍 Testing day variations of '{original}':")
        
        # Test lowercase day
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin=Nabeul&destination=Tunis&preferred_day={lowercase}")
            if response.status_code == 200:
                print(f"  ✅ Lowercase day '{lowercase}' - SUCCESS")
            else:
                print(f"  ❌ Lowercase day '{lowercase}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Lowercase day '{lowercase}' - ERROR: {str(e)}")
        
        # Test uppercase day
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin=Nabeul&destination=Tunis&preferred_day={uppercase}")
            if response.status_code == 200:
                print(f"  ✅ Uppercase day '{uppercase}' - SUCCESS")
            else:
                print(f"  ❌ Uppercase day '{uppercase}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Uppercase day '{uppercase}' - ERROR: {str(e)}")
        
        sleep(0.5)  # Small delay to avoid overwhelming the server
    
    # Test season normalization
    season_test_cases = [
        # Original, lowercase, uppercase, alternative name
        ("Summer", "summer", "SUMMER", "été"),
        ("Winter", "winter", "WINTER", "hiver"),
    ]
    
    for original, lowercase, uppercase, alt_name in season_test_cases:
        print(f"\n🔍 Testing season variations of '{original}':")
        
        # Test lowercase season
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin=Nabeul&destination=Tunis&preferred_season={lowercase}")
            if response.status_code == 200:
                print(f"  ✅ Lowercase season '{lowercase}' - SUCCESS")
            else:
                print(f"  ❌ Lowercase season '{lowercase}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Lowercase season '{lowercase}' - ERROR: {str(e)}")
        
        # Test uppercase season
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin=Nabeul&destination=Tunis&preferred_season={uppercase}")
            if response.status_code == 200:
                print(f"  ✅ Uppercase season '{uppercase}' - SUCCESS")
            else:
                print(f"  ❌ Uppercase season '{uppercase}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Uppercase season '{uppercase}' - ERROR: {str(e)}")
        
        # Test alternative name
        try:
            response = requests.get(f"{BASE_URL}/recommendations?origin=Nabeul&destination=Tunis&preferred_season={alt_name}")
            if response.status_code == 200:
                print(f"  ✅ Alternative name '{alt_name}' - SUCCESS")
            else:
                print(f"  ❌ Alternative name '{alt_name}' - FAILED: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Alternative name '{alt_name}' - ERROR: {str(e)}")
        
        sleep(0.5)  # Small delay to avoid overwhelming the server

def run_all_tests():
    """Run all test cases"""
    print("\n🚀 STARTING FUZZY MATCHING AND CASE-INSENSITIVE TESTS")
    print("=" * 70)
    print("Make sure the API server is running at http://localhost:8000")
    print("=" * 70)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API server is running")
        else:
            print(f"❌ API server returned status code {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Could not connect to API server: {str(e)}")
        print("Please start the API server first with: python api_main.py")
        return
    
    # Run all test cases
    test_case_insensitive()
    test_fuzzy_matching()
    test_whitespace_handling()
    test_day_and_season_normalization()
    
    print("\n🎉 ALL TESTS COMPLETED!")

if __name__ == "__main__":
    run_all_tests()

