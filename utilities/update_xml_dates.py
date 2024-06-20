import sys
import re
from datetime import datetime

def convert_unix_to_date(match):
    try:
        unix_timestamp = match.group(1)
        timestamp = int(unix_timestamp) // 1000  # Convert milliseconds to seconds
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except ValueError:
        return match.group(0)  # Return original value if conversion fails

def process_xml(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regular expression to find 13-digit Unix timestamps between ><
        pattern = r'>(\d{13})<'
        updated_content = re.sub(pattern, lambda match: f'>{convert_unix_to_date(match)}<', content)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"Successfully updated timestamps in {input_file}. Saved as {output_file}")
    except Exception as e:
        print(f"Error processing XML file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_xml_dates.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_xml(input_file, output_file)
