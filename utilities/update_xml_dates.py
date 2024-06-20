import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

def convert_unix_to_date(unix_timestamp):
    try:
        timestamp = int(unix_timestamp) // 1000  # Convert milliseconds to seconds
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Failed to convert Unix timestamp: {unix_timestamp}. Error: {e}")
        return unix_timestamp  # Return original value if conversion fails

def process_xml(input_file, output_file):
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()

        def update_elements(elem):
            if elem.text and elem.text.isdigit() and len(elem.text) == 13:
                elem.text = convert_unix_to_date(elem.text)
            for child in elem:
                update_elements(child)

        update_elements(root)
        tree.write(output_file)
        print(f"Successfully updated timestamps in {input_file}. Saved as {output_file}")
    except Exception as e:
        import traceback
        print(f"Error processing XML file: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_xml_dates.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_xml(input_file, output_file)
