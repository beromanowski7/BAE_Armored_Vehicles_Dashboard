# BAE Systems Armored Vehicles Dashboard
### Author: Blake Romanowski
### Script: Final_Project_Romanowski.py

## Overview
This interactive Streamlit dashboard visualizes the global distribution of armored vehicle sales by BAE Systems Inc. from publiclly available sources (see 'References.xlsx' file included in the project folder). This dashboard uses an interactive Folium map to display vehicle deliveries by country, allowing users to filter by country, vehicle type, and map style. Clicking on a country reveals vehicle number data along with the associated vehicle images.

## Features
- Interactive Map: Allows you to explore an overview of global BAE Systems armored vehicle numbers by country with a Folium map, with selectable list of different map styles. Map is able to move around on click & drag, or zoom using the scroll wheel.

- Filter Options: Sidebar filters for country, vehicle type, and map style.

- Detailed Popups: Clickable country markers with formatted "tooltip" tables showing vehicles delivered to each country.

- Download PDF Report: Button that allows for the generation of a report view by the selected country. Button only appears after a country is first selected on the map.

- Vehicle Gallery: Displays images and quantities for each vehicle type delivered to a selected country.

- User-Friendly UI: Wide layout to use the full webpage, clean table formatting in the tooltips, and customizable map styles.

## Requirements
- Python 3.8+
- Streamlit
- pandas
- folium
- streamlit-folium
- logging
- import html
- fpdf
- BytesIO
- datetime


## Dataset & Image Files
- dataset.xlsx: The data file with country, vehicle, quantity, and coordinates.

- Vehicle Images: All referenced vehicle image files (e.g., RG-31.jpg, Warrior_IFV.jpeg, etc.) are located in the same directory as the script.

## How to Run
1. Ensure your working directory contains:
    - Final_Project_Romanowski.py
    - dataset.xlsx
    - All vehicle image files

**2. Start the Streamlit app using the following command on the command prompt:**

    streamlit run Final_Project_Romanowski.py

3. Use the sidebar to:
    - Filter by Country
    - Filter by Vehicle Type
    - Change the Map Style

4. Click any country marker on the map to view detailed delivery info and images.
5. Click the 'Download PDF Report' button after a country is selected on the map.

## Customization
Map Tiles: Choose from OpenStreetMap, CartoDB, or Esri WorldStreetMap.

Data: Update dataset.xlsx for new deliveries or additional vehicles.

Images: Add or change the vehicle images by editing the vehicle_images dictionary and ensuring image files exist.

## Troubleshooting
If images do not display, check that file names match exactly and are present in the directory. 

If the map does not load, confirm all required Python packages are installed. 

***If adding new map styles/tiles, ensure proper attribution is provided in the Folium map settings or the map style will not load on the dashboard.***

### License
This project is for educational purposes.

### Questions?
Contact: **beromanowski7** (GitHub profile)


"# BAE_Armored_Vehicles_Dashboard" 
