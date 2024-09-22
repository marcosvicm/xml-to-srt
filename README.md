# TTML to SRT Converter

This Python script converts all TTML (Timed Text Markup Language) or XML subtitle files in a specified folder into the SRT (SubRip Subtitle) format. It extracts text, timing, and basic styling from the TTML files and outputs them in SRT format.

## Features
- Converts TTML and XML files to SRT.
- Supports basic styling (italic).
- Handles subtitle positioning (e.g., top of the screen).
- Creates the output folder if it doesn't exist.
- Error handling ensures the conversion process continues even if some files fail.

## Usage

1. Set the `input_folder` to the directory containing your TTML/XML files.
2. Set the `output_folder` to the directory where you want the SRT files to be saved.
3. Run the script.

```python
input_folder = '/path/to/input/folder'
output_folder = '/path/to/output/folder'

ttml_to_srt_folder(input_folder, output_folder)
```

## Requirements

- Python 3.x
- `xml.etree.ElementTree` (part of Python standard library)
