import pandas as pd
import reverse_geocode
from SPARQLWrapper import SPARQLWrapper, JSON
import argparse
import time

def get_country_info(country_code_alpha2, timeout=10):
    print(f"Fetching country info for country code: {country_code_alpha2}")
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = f"""
    SELECT ?country ?countryLabel ?isoAlpha3 WHERE {{
      ?country wdt:P297 "{country_code_alpha2}".
      ?country wdt:P298 ?isoAlpha3.
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(timeout)

    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            q_code = result["country"]["value"].split('/')[-1]  # Extract the Q code from the URL
            iso_alpha3 = result["isoAlpha3"]["value"]
            print(f"Found Q code: {q_code}, ISO alpha-3: {iso_alpha3} for country code: {country_code_alpha2}")
            return q_code, iso_alpha3
    except Exception as e:
        print(f"Error fetching info for {country_code_alpha2}: {e}")
        return None, None

    print(f"No info found for country code: {country_code_alpha2}")
    return None, None

def add_country_info_to_excel(input_file_path, output_file_path):
    print(f"Loading Excel file: {input_file_path}")
    xls = pd.ExcelFile(input_file_path)
    sheet_name = xls.sheet_names[0]

    print(f"Reading sheet: {sheet_name}")
    df = pd.read_excel(input_file_path, sheet_name=sheet_name)

    if 'latitude' in df.columns and 'longitude' in df.columns:
        if 'country_code' not in df.columns:
            df['country_code'] = ''
        if 'country_wikidata' not in df.columns:
            df['country_wikidata'] = ''
        if 'country_code_alpha3' not in df.columns:
            df['country_code_alpha3'] = ''

        # Explicitly set the type of 'country_wikidata' and 'country_code_alpha3' to string
        df['country_wikidata'] = df['country_wikidata'].astype(str)
        df['country_code_alpha3'] = df['country_code_alpha3'].astype(str)

        for idx, row in df.iterrows():
            lat, lon = row['latitude'], row['longitude']
            print(f"Processing row {idx}: Latitude = {lat}, Longitude = {lon}")
            if pd.notna(lat) and pd.notna(lon):
                coordinates = [(lat, lon)]
                result = reverse_geocode.search(coordinates)[0]
                country_code_alpha2 = result['country_code']
                print(f"Found country code (alpha-2): {country_code_alpha2} for coordinates: {lat}, {lon}")
                wikidata_q_code, country_code_alpha3 = get_country_info(country_code_alpha2)
                df.at[idx, 'country_code'] = country_code_alpha2
                df.at[idx, 'country_wikidata'] = wikidata_q_code
                df.at[idx, 'country_code_alpha3'] = country_code_alpha3
                print(f"Updated row {idx}: country_code = {country_code_alpha2}, country_wikidata = {wikidata_q_code}, country_code_alpha3 = {country_code_alpha3}")
            else:
                print(f"Invalid or missing coordinates for row {idx}, leaving fields empty.")
                df.at[idx, 'country_code'] = ''
                df.at[idx, 'country_wikidata'] = ''
                df.at[idx, 'country_code_alpha3'] = ''

        print(f"Saving updated data to: {output_file_path}")
        with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
            for sheet in xls.sheet_names:
                if sheet == sheet_name:
                    df.to_excel(writer, sheet_name=sheet, index=False)
                else:
                    xls.parse(sheet).to_excel(writer, sheet_name=sheet, index=False)

    else:
        print("The required columns 'latitude' and 'longitude' are not in the DataFrame.")

def main():
    parser = argparse.ArgumentParser(description="Add country information to Excel file based on latitude and longitude.")
    parser.add_argument("input_file", help="Path to the input Excel file")
    parser.add_argument("output_file", help="Path to the output Excel file")
    args = parser.parse_args()

    print(f"Input file: {args.input_file}")
    print(f"Output file: {args.output_file}")

    start_time = time.time()
    add_country_info_to_excel(args.input_file, args.output_file)
    end_time = time.time()

    print(f"Script completed in {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
