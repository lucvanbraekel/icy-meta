# ICY Metadata Extractor for Shoutcast/Icecast Streams

A Python script to extract ICY metadata (e.g., song titles) from Icecast or SHOUTcast streaming audio sources.

## Overview

This Python script extracts ICY metadata from Shoutcast or Icecast streams. It outputs the metadata to standard output (stdout) and includes robust error handling for network issues, malformed metadata, or stream termination. 

The script can run in a single mode to fetch metadata once, or in continuous mode to poll for metadata changes. 

Using this script allows you to track song titles, artists, or radio program names without needing to stream the audio. It's perfect for monitoring playlists, logging music, or analyzing radio programming.

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

Run the script with a stream URL to extract ICY metadata (e.g., song titles) from an Icecast or SHOUTcast stream. The script outputs metadata to standard output (stdout) and supports both single-run and continuous polling modes, with an option to limit the duration of continuous mode.

### Command-Line Syntax

```
icy_meta.py [-h] [--timeout TIMEOUT] [--continuous] [--duration DURATION] url
```

### Arguments

- `url`: The URL of the Icecast or SHOUTcast stream (required). Example: `http://example.com:8000/stream`.
- `--timeout TIMEOUT`: Timeout for the initial connection in seconds (optional, default: 10).
- `--continuous`: Enable continuous mode to poll for metadata changes every second (optional).
- `--duration DURATION`: Duration in seconds for continuous mode (optional, default: run until interrupted).
- `-h, --help`: Show help message and exit.

### Examples

1. **Single-run mode** (fetch metadata once):
   ```bash
   python3 icy_meta.py http://example.com:8000/stream
   ```
   Output (to stdout):
   ```
   Metadata: Artist - Song Title
   ```
   If no metadata is retrieved:
   ```
   No metadata retrieved
   ```

2. **Continuous mode** (poll for metadata changes until interrupted):
   ```bash
   python3 icy_meta.py http://example.com:8000/stream --continuous
   ```
   Output (to stdout, only when metadata changes):
   ```
   Metadata: Artist - Song Title
   Metadata: Artist - New Song Title
   ```
   Stop with `Ctrl+C`:
   ```
   Stopped by user
   ```

3. **Continuous mode with duration** (poll for 3600 seconds):
   ```bash
   python3 icy_meta.py http://example.com:8000/stream --continuous --duration 3600
   ```
   Output (to stdout, only when metadata changes, stops after 3600 seconds):
   ```
   Metadata: Artist - Song Title
   Metadata: Artist - New Song Title
   Stopped: Reached duration limit of 3600 seconds
   ```

4. **Specify a custom timeout**:
   ```bash
   python3 icy_meta.py http://example.com:8000/stream --timeout 15
   ```
   Output (same as single-run mode).

5. **Redirect output to a file**:
   ```bash
   python3 icy_meta.py http://example.com:8000/stream --continuous --duration 3600 > metadata.txt
   ```

### Error and Warning Messages

The script outputs errors or warnings to stdout for issues such as:
- Invalid or missing `icy-metaint` header.
- Empty stream chunks or stream termination.
- Malformed metadata (e.g., no `StreamTitle`).
- Network errors (e.g., connection timeout).

Example:
```
Error: No icy-metaint header found in response
Warning: Malformed metadata: StreamTitle='Invalid'
```

### Notes
- The `--duration` argument only affects continuous mode (`--continuous`). If used without `--continuous`, it has no effect, as single-run mode exits after one metadata fetch.
- 

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




