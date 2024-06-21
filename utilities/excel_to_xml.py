import pandas as pd
import xml.etree.ElementTree as ET
import argparse
import os

def df_to_xml(df, root_tag, row_tag):
    root = ET.Element(root_tag)
    for _, row in df.iterrows():
        row_elem = ET.SubElement(root, row_tag)
        for field in df.columns:
            field_elem = ET.SubElement(row_elem, field)
            field_elem.text = str(row[field]) if pd.notna(row[field]) else ''
    return root

def save_xml_to_file(root, output_file_path):
    tree = ET.ElementTree(root)
    tree.write(output_file_path, encoding='utf-8', xml_declaration=True)

def excel_to_xml(input_file_path, output_file_path, sheet_name=None):
    print(f"Loading Excel file: {input_file_path}")
    xls = pd.ExcelFile(input_file_path)

    if sheet_name is None:
        sheet_name = xls.sheet_names[0]  # Default to the first sheet
    print(f"Reading sheet: {sheet_name}")
    df = pd.read_excel(input_file_path, sheet_name=sheet_name)

    root_tag = os.path.splitext(os.path.basename(input_file_path))[0]  # Use file name (without extension) as root tag
    row_tag = 'row'  # Use 'row' as the row tag

    print("Converting DataFrame to XML...")
    root = df_to_xml(df, root_tag, row_tag)

    print(f"Saving XML to file: {output_file_path}")
    save_xml_to_file(root, output_file_path)
    print("Conversion completed successfully.")

def main():
    parser = argparse.ArgumentParser(description="Convert an Excel file to an XML file.")
    parser.add_argument("input_file", help="Path to the input Excel file")
    parser.add_argument("output_file", help="Path to the output XML file")
    parser.add_argument("--sheet", help="Name of the sheet to convert (default is the first sheet)", default=None)
    args = parser.parse_args()

    print(f"Input file: {args.input_file}")
    print(f"Output file: {args.output_file}")
    if args.sheet:
        print(f"Sheet name: {args.sheet}")

    excel_to_xml(args.input_file, args.output_file, args.sheet)

if __name__ == "__main__":
    main()
