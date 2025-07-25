#!/usr/bin/env python3
"""
Script to generate compressed airport data from JSON source.
This script compresses the airports.json file into airports.gz for efficient distribution.
"""

import gzip
import json
import os
import argparse
import sys
from pathlib import Path

def compress_airport_data(source_file: str, output_file: str, compression_level: int = 9) -> bool:
    """
    Compress airport JSON data to gzipped format.
    
    Args:
        source_file: Path to source JSON file
        output_file: Path to output gzipped file
        compression_level: Compression level (1-9, default 9 for best compression)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Check if source file exists
        if not os.path.exists(source_file):
            print(f"Error: Source file '{source_file}' not found.")
            return False
        
        # Read JSON data
        print(f"Reading source file: {source_file}")
        with open(source_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate data structure
        if not isinstance(data, list):
            print("Error: Source data must be a list of airport objects.")
            return False
        
        if len(data) == 0:
            print("Warning: Source data is empty.")
        
        print(f"Loaded {len(data)} airport records")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            print(f"Created directory: {output_dir}")
        
        # Write compressed data
        print(f"Compressing data with level {compression_level}...")
        with gzip.open(output_file, 'wt', encoding='utf-8', compresslevel=compression_level) as f:
            json.dump(data, f, separators=(',', ':'), ensure_ascii=False)
        
        # Calculate file sizes and compression ratio
        original_size = os.path.getsize(source_file)
        compressed_size = os.path.getsize(output_file)
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        print(f"Compression complete!")
        print(f"Original size: {original_size:,} bytes ({original_size / 1024 / 1024:.2f} MB)")
        print(f"Compressed size: {compressed_size:,} bytes ({compressed_size / 1024:.2f} KB)")
        print(f"Compression ratio: {compression_ratio:.1f}%")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in source file: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def verify_compressed_data(compressed_file: str) -> bool:
    """
    Verify that the compressed file can be read and contains valid data.
    
    Args:
        compressed_file: Path to compressed file
    
    Returns:
        True if verification successful, False otherwise
    """
    try:
        print(f"Verifying compressed file: {compressed_file}")
        
        if not os.path.exists(compressed_file):
            print(f"Error: Compressed file '{compressed_file}' not found.")
            return False
        
        # Try to read and parse the compressed data
        with gzip.open(compressed_file, 'rt', encoding='utf-8') as f:
            data = json.load(f)
        
        # Basic validation
        if not isinstance(data, list):
            print("Error: Compressed data is not a list.")
            return False
        
        if len(data) == 0:
            print("Warning: Compressed data is empty.")
            return True
        
        # Check first record structure
        first_record = data[0]
        required_fields = ['iata', 'icao', 'airport']
        missing_fields = [field for field in required_fields if field not in first_record]
        
        if missing_fields:
            print(f"Warning: First record missing fields: {missing_fields}")
        
        print(f"Verification successful! Found {len(data)} airport records.")
        print(f"Sample record: {first_record.get('airport', 'Unknown')} ({first_record.get('iata', 'N/A')})")
        
        return True
        
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

def main():
    """Main function to handle command line arguments and execute compression."""
    parser = argparse.ArgumentParser(
        description="Generate compressed airport data from JSON source",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate with default settings
  python scripts/generate_airports_gz.py
  
  # Generate with custom compression level
  python scripts/generate_airports_gz.py --compression 6
  
  # Generate with custom files
  python scripts/generate_airports_gz.py --source data/custom.json --output data/custom.gz
  
  # Only verify existing compressed file
  python scripts/generate_airports_gz.py --verify-only
        """
    )
    
    parser.add_argument(
        '--source',
        default='airports/data/airports.json',
        help='Source JSON file path (default: airports/data/airports.json)'
    )
    
    parser.add_argument(
        '--output',
        default='airports/data/airports.gz',
        help='Output compressed file path (default: airports/data/airports.gz)'
    )
    
    parser.add_argument(
        '--compression',
        type=int,
        choices=range(1, 10),
        default=9,
        help='Compression level 1-9 (default: 9 for best compression)'
    )
    
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify existing compressed file, do not generate'
    )
    
    parser.add_argument(
        '--no-verify',
        action='store_true',
        help='Skip verification after compression'
    )
    
    args = parser.parse_args()
    
    # Handle verify-only mode
    if args.verify_only:
        success = verify_compressed_data(args.output)
        sys.exit(0 if success else 1)
    
    # Generate compressed file
    print("Airport Data Compression Tool")
    print("=" * 40)
    
    success = compress_airport_data(args.source, args.output, args.compression)
    
    if not success:
        print("Compression failed!")
        sys.exit(1)
    
    # Verify unless disabled
    if not args.no_verify:
        print("\nVerifying compressed file...")
        verify_success = verify_compressed_data(args.output)
        if not verify_success:
            print("Verification failed!")
            sys.exit(1)
    
    print("\nAll operations completed successfully!")

if __name__ == '__main__':
    main()