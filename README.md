# ICY Metadata Extractor for Shoutcast/Icecast Streams

## Overview

What if you don't want to listen to the radio but only want a list of songs played? This Python script extracts ICY metadata from Shoutcast or Icecast streams and saves it to a text file, allowing you to track song titles, artists, or radio program names without needing to stream the audio. It's perfect for monitoring playlists, logging music, or analyzing radio programming.

The script connects to a streaming audio source, reads metadata embedded in the stream, and logs it with timestamps to a specified output file. It supports all audio codecs used by Shoutcast and Icecast servers, including MP3, AAC, and others, as long as the stream provides ICY metadata.

## Features

- Extracts ICY metadata (e.g., song titles, artists, or program names) from Shoutcast/Icecast streams.
- Saves metadata with timestamps to a user-specified text file.
- Supports all codecs used by Icecast/Shoutcast, such as MP3, AAC, AAC+, Ogg Vorbis, and more.
- Runs for a user-defined duration (in seconds).
- Handles errors gracefully, logging issues to the output file.

## What is ICY Metadata?

ICY metadata is a protocol used by Shoutcast and Icecast servers to embed information in audio streams. This metadata is sent at regular intervals, specified by the `icy-metaint` header in the stream's HTTP response. The `icy-metaint` value indicates how many bytes of audio data are sent between each metadata block. For example, an `icy-metaint` of 16000 means metadata is sent after every 16000 bytes of audio.

Metadata typically includes:
- **Song titles and artists**: Common for music streams, e.g., `StreamTitle='Artist - Song Title'`.
- **Radio program names**: For talk radio or shows, metadata might only contain the program title, e.g., `StreamTitle='Morning Talk Show'`.
- **Other information**: Some streams include URLs or additional details in fields like `StreamUrl`.

The script reads these metadata blocks and parses them into a dictionary, saving the results to a text file.

## Supported Codecs

The script is codec-agnostic and works with any audio format supported by Shoutcast or Icecast, as long as the stream includes ICY metadata. Common codecs include:
- **MP3**: The most widely used format for streaming.
- **AAC/AAC+**: Popular for high-quality, low-bitrate streams.
- **Ogg Vorbis**: Often used for open-source or high-fidelity streams.
- Other formats supported by Icecast (e.g., Opus) may also work if ICY metadata is provided.

Note: Some Icecast streams (e.g., Ogg Vorbis) may use alternative metadata formats like Vorbis comments. This script is designed for ICY metadata, which is standard for MP3 and AAC streams and commonly used across codecs.

## Requirements

- Python 3.x
- `requests` library (`pip install requests`)

## Installation

1. Clone or download this repository.
2. Install the required library:
   ```bash
      pip install requests

## Usage

Run the script from the command line, providing three arguments:
- stream_url: The URL of the Shoutcast/Icecast stream (e.g., http://example.com:8000/stream or http://example.com:8000/stream.aac).
- output_file: The path to the text file where metadata will be saved (e.g., metadata.txt).
- duration: The duration (in seconds) to run the extraction (e.g., 60 for 1 minute).

Example:

python icy_meta.py http://example.com:8000/stream metadata.txt 3600


This will:

- Connect to the stream at http://example.com:8000/stream.
- Extract metadata for 60 seconds.
- Save the results to metadata.txt.

Example Output File (metadata.txt)

Metadata extraction started at 2025-07-31 07:05:00
Stream URL: http://example.com:8000/stream

[2025-07-31 07:05:01] {'StreamTitle': 'Artist - Song Title', 'StreamUrl': ''}
[2025-07-31 07:05:15] {'StreamTitle': 'Morning Talk Show', 'StreamUrl': ''}


## Finding Streams

To test the script, find public Shoutcast or Icecast streams at:

- Shoutcast Directory
- Xiph.org Directory

Ensure the stream supports ICY metadata by checking for the icy-metaint header in the HTTP response (e.g., using curl -I -H "Icy-MetaData: 1" <stream_url>).

## Notes

- The script appends to the output file if it already exists.
- If a stream doesn't support ICY metadata, the script will log an error to the output file and exit.
- For non-ICY metadata formats (e.g., Ogg Vorbis comments), the script would need modification.
- The script uses the requests library for HTTP streaming, which is reliable for most streams but may require adjustments for specific edge cases.

## Troubleshooting

- Error: "Stream does not support metadata": The stream may not provide ICY metadata. Verify with curl or try another stream.
- Connection errors: Ensure the stream URL is valid and accessible.
- Empty metadata: Some streams send sparse or incomplete metadata (e.g., only StreamTitle).

## License

This project is licensed under the MIT License. See the LICENSE file for details.ContributingContributions are welcome! Submit issues or pull requests on the repository for bug fixes or enhancements.ContactFor questions or support, open an issue on the repository or contact the maintainer.




