import requests
import time
import re
import sys
from datetime import datetime

def extract_icy_metadata(stream_url, output_file, duration):
    """
    Extract ICY metadata from a Shoutcast/Icecast stream and save to a text file.
    
    Args:
        stream_url (str): URL of the Shoutcast/Icecast stream
        output_file (str): Path to the output text file
        duration (int): Duration to run the extraction in seconds
    """
    # Headers to request metadata
    headers = {'Icy-MetaData': '1'}
    
    try:
        # Open the stream
        response = requests.get(stream_url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()

        # Get metadata interval from headers
        metaint = int(response.headers.get('icy-metaint', 0))
        if metaint == 0:
            print("Stream does not support metadata.")
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now()}] Stream does not support metadata.\n")
            return

        # Open output file
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"Metadata extraction started at {datetime.now()}\n")
            f.write(f"Stream URL: {stream_url}\n\n")

            # Initialize variables
            buffer = b''
            bytes_read = 0
            start_time = time.time()

            # Read stream for specified duration
            for chunk in response.iter_content(chunk_size=8192):
                if time.time() - start_time > duration:
                    break

                buffer += chunk
                bytes_read += len(chunk)

                # Process metadata when enough bytes are read
                while bytes_read >= metaint:
                    # Extract metadata block
                    metadata_length = buffer[metaint] * 16
                    if len(buffer) < metaint + 1 + metadata_length:
                        break

                    metadata = buffer[metaint + 1:metaint + 1 + metadata_length].decode('utf-8', errors='ignore')
                    buffer = buffer[metaint + 1 + metadata_length:]
                    bytes_read -= (metaint + 1 + metadata_length)

                    # Parse metadata
                    metadata_dict = parse_metadata(metadata)
                    if metadata_dict:
                        # Write to file
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        f.write(f"[{timestamp}] {metadata_dict}\n")
                        print(f"[{timestamp}] {metadata_dict}")

    except requests.RequestException as e:
        print(f"Error connecting to stream: {e}")
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now()}] Error connecting to stream: {e}\n")
    except Exception as e:
        print(f"Unexpected error: {e}")
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now()}] Unexpected error: {e}\n")

def parse_metadata(metadata):
    """
    Parse ICY metadata string into a dictionary.
    
    Args:
        metadata (str): Raw metadata string
    
    Returns:
        dict: Parsed metadata
    """
    metadata_dict = {}
    try:
        # Split metadata into key-value pairs
        pairs = re.findall(r"(\w+?)='([^']*)'", metadata)
        for key, value in pairs:
            metadata_dict[key] = value
        return metadata_dict
    except Exception as e:
        print(f"Error parsing metadata: {e}")
        return {}

if __name__ == "__main__":
    # Check for correct number of command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python script.py <stream_url> <output_file> <duration_in_seconds>")
        sys.exit(1)

    # Get command-line arguments
    stream_url = sys.argv[1]
    output_file = sys.argv[2]
    try:
        duration = int(sys.argv[3])
        if duration <= 0:
            raise ValueError("Duration must be a positive integer.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Starting metadata extraction from {stream_url}")
    extract_icy_metadata(stream_url, output_file, duration)
    print(f"Metadata saved to {output_file}")
