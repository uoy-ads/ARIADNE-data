# ARIADNE-data
This repository is used mostly to manage issues relating to data in the issue tracker. However, some scripts will be added as used to prepare or peocess data.  

## update_xml_dates
This script will find 13-digit long numbers and convert them to YYYY-MM-DD dates. It processes the files as text.  
Usage:  `python update_xml_dates.py input_file output_file`  

## add_country_code
This script will read latitute and longitude fields in a xlsx file and add the country code to the country_code field, add the Wikidata Qid for the country in the country_wikidata field, and create a new field for the three letters country code. The script queries the Wikidata SPARQL endpoint.  
Usage: `python add_country_code.py input.xlsx output.xlsx`  
