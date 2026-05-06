#!/usr/bin/env python3
"""
Google Search Scraper for Software Companies
Uses SerpAPI to scrape Google search results legally and efficiently.

Requirements:
    pip install google-search-results

Usage:
    python google_scraper.py --api-key YOUR_API_KEY --query "software companies"
"""

import argparse
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

try:
    from serpapi import GoogleSearch
except ImportError:
    print("Please install required package: pip install google-search-results")
    exit(1)


def scrape_google_search(
    query: str,
    api_key: str,
    num_results: int = 10,
    location: str = "United States",
    language: str = "en"
) -> List[Dict]:
    """
    Scrape Google search results using SerpAPI.
    
    Args:
        query: Search query string
        api_key: SerpAPI key
        num_results: Number of results to retrieve
        location: Geographic location for search
        language: Language code for results
    
    Returns:
        List of dictionaries containing search result data
    """
    params = {
        "q": query,
        "api_key": api_key,
        "num": num_results,
        "location": location,
        "hl": language,
        "gl": "us"
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Extract organic search results
        organic_results = results.get("organic_results", [])
        
        return organic_results
    
    except Exception as e:
        print(f"Error during search: {e}")
        return []


def display_results(results: List[Dict]) -> None:
    """Display search results in a formatted manner."""
    if not results:
        print("No results found.")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(results)} results\n")
    print(f"{'='*80}\n")
    
    for idx, result in enumerate(results, 1):
        title = result.get("title", "N/A")
        link = result.get("link", "N/A")
        snippet = result.get("snippet", "N/A")
        
        print(f"{idx}. {title}")
        print(f"   URL: {link}")
        print(f"   Description: {snippet[:200]}{'...' if len(snippet) > 200 else ''}")
        print()


def save_results(results: List[Dict], filename: Optional[str] = None) -> str:
    """Save search results to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"google_search_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to: {filename}")
    return filename


def main():
    parser = argparse.ArgumentParser(
        description="Scrape Google search results for software companies"
    )
    parser.add_argument(
        "--api-key", 
        type=str,
        default=os.getenv("SERPAPI_KEY"),
        help="SerpAPI key (or set SERPAPI_KEY environment variable)"
    )
    parser.add_argument(
        "--query", 
        type=str, 
        default="software companies",
        help="Search query (default: 'software companies')"
    )
    parser.add_argument(
        "--num-results", 
        type=int, 
        default=10,
        help="Number of results to retrieve (default: 10)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default=None,
        help="Output JSON file (default: auto-generated filename)"
    )
    parser.add_argument(
        "--location", 
        type=str, 
        default="United States",
        help="Geographic location for search (default: United States)"
    )
    parser.add_argument(
        "--silent", 
        action="store_true",
        help="Don't display results, only save to file"
    )
    
    args = parser.parse_args()
    
    # Validate API key
    if not args.api_key:
        print("Error: API key is required!")
        print("Provide it via --api-key flag or SERPAPI_KEY environment variable")
        print("\nGet your API key at: https://serpapi.com/")
        exit(1)
    
    print(f"Searching for: '{args.query}'")
    print(f"Number of results: {args.num_results}")
    print(f"Location: {args.location}")
    print("-" * 50)
    
    # Perform search
    results = scrape_google_search(
        query=args.query,
        api_key=args.api_key,
        num_results=args.num_results,
        location=args.location
    )
    
    if not args.silent:
        display_results(results)
    
    # Save results
    save_results(results, args.output)
    
    print(f"\nTotal results retrieved: {len(results)}")


if __name__ == "__main__":
    main()
