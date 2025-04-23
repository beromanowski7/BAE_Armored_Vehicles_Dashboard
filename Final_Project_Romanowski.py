# Final_Project_Romanowski.py
## Blake Romanowski

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import logging
from streamlit.components.v1 import html
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

# Loading in the dataset
df = pd.read_excel("dataset.xlsx")

# Vehicle images
vehicle_images = {
    "RG31 Nyala": "RG-31.jpg",
    "RG33 MRAP": "RG-33.jpg",
    "Caiman MRAP": "Caiman.jpg",
    "Panther CLV": "Panther_CLV.jpg",
    "Warrior IFV": "Warrior_IFV.jpeg",
    "Terrier CEV": "Terrier_CEV.jpg",
    "Trojan AEV": "Trojan_AEV.jpg",
    "Titan AVLB": "Titan_AVLB.jpg",
    "Stormer HVM": "Stormer_HVM.jpg",
    "FV432 APC": "FV432_APC.jpg",
    "Challenger 2 MBT": "Challenger_2_MBT.jpg",
    "Challenger 3 MBT": "Challenger_3_MBT.jpeg",
    "Boxer AFV": "Boxer_AFV.jpg",
    "Armored Multi-Purpose Vehicle (AMPV)": "AMPV.jpg",
    "Paladin Integrated Management (PIM)": "PIM.jpg",
    "M88A3 Hercules Recovery Vehicle": "M88A3.jpg",
    "Multi-Domain Artillery Cannon (MDAC)": "MDAC.jpg",
    "ARCHER Artillery System": "ARCHER.jpg", 
    "CV90": "CV90.jpg",
    "BvS10 MkIIB": "BvS10_MkIIB.jpg",
    "BvS10 MkII (VHM)": "BvS10_MkII_VHM.jpg",
    "BvS10": "BvS10.jpg",
    "CV90 Mk IV": "CV90_Mk_IV.jpg",
    "BvS10 Viking": "BvS10_Viking.jpeg",
    "Bradley Fighting Vehicle (A4 variant)": "Bradley.jpeg",
    "Amphibious Combat Vehicle (ACV)": "ACV.jpg",
    "BvS10 Beowulf (CATV Program)": "BvS10_Beowulf.jpeg"
}

# Page Details
st.set_page_config(page_title="Final_Project_Romanowski", layout="wide")
st.title("BAE Systems Armored Vehicles Dashboard")
st.markdown("Explore the global distribution of publically available armored vehicle sales by BAE Systems Inc.")
st.markdown("*Click on a country marker on the map below to view details and download a PDF report.*")

tile_options = {
    "OpenStreetMap (default)": "OpenStreetMap",
    "CartoDB Positron (clean & modern)": "CartoDB positron",
    "CartoDB Dark Matter (dark theme)": "CartoDB dark_matter",
    "Esri WorldStreetMap (professional look)": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
}

# Filters Options for the left sidebar selection pane
with st.sidebar:
    st.header("Filter Options")
    selected_country = st.selectbox("Country", options=["All"] + sorted(df["Country"].unique()))
    selected_vehicle = st.selectbox("Vehicle Type", options=["All"] + sorted(df["Vehicle Model"].unique()))
    selected_tile_label = st.selectbox("Map Style", options=list(tile_options.keys()))
    selected_tile = tile_options[selected_tile_label]

# Filtered DataFrame
filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]
if selected_vehicle != "All":
    filtered_df = filtered_df[filtered_df["Vehicle Model"] == selected_vehicle]

# Creating the Folium Map
m = folium.Map(location=[20, 20], zoom_start=2, tiles=selected_tile, attr="Esri" if "Esri" in selected_tile_label else None)

for _, group in filtered_df.groupby("Country"):
    lat = float(group.iloc[0]['Latitude'][:-2]) * (1 if 'N' in group.iloc[0]['Latitude'] else -1)
    lng = float(group.iloc[0]['Longitude'][:-2]) * (1 if 'E' in group.iloc[0]['Longitude'] else -1)

# Fixing the formatting for the tooltip popups on the map
    html_content = f"""
    <div style="font-family: Arial; font-size: 14px; max-width: 300px;">
        <strong>{group.iloc[0]['Country']}</strong><br><br>
        <table style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr>
                    <th style="text-align: left; padding: 4px;">Vehicle Model</th>
                    <th style="text-align: right; padding: 4px;">Quantity</th>
                </tr>
            </thead>
            <tbody>
                {''.join(f"<tr><td style='padding: 4px;'>{row['Vehicle Model']}</td><td style='padding: 4px; text-align: right;'>{row['Quantity']}</td></tr>" for _, row in group.iterrows())}
            </tbody>
        </table>
    </div>
"""
    iframe = folium.IFrame(html_content, width=300, height=200)
    popup = folium.Popup(iframe, max_width=350)

    folium.Marker(
        [lat, lng],
        popup=popup,
        tooltip=group.iloc[0]['Country'],
        icon=folium.Icon(icon="fa-flag", prefix='fa', color='darkblue')
    ).add_to(m)

# Set the size of the map
st_data = st_folium(m, width=1000, height=550)

def render_pdf_button(display_df, sel_country):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "BAE Systems - Vehicle Report", ln=True, align="C")
            self.set_font("Arial", "", 12)
            self.cell(0, 10, f"Country: {sel_country}", ln=True, align="C")
            self.cell(0, 10, f"Date: {datetime.today().strftime('%B %d, %Y')}", ln=True, align="C")
            self.ln(5)
            self.set_draw_color(0, 0, 0)
            self.set_line_width(0.5)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    # Download PDF Button
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_fill_color(240, 240, 240)

    for _, row in display_df.iterrows():
        vehicle = row["Vehicle Model"]
        quantity = row["Quantity"]
        text = f"{vehicle} - Quantity: {quantity}"
        pdf.multi_cell(0, 10, text, border=0, align="L", fill=True)
        pdf.ln(1)

    pdf_buffer = BytesIO()
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    pdf_buffer.write(pdf_bytes)
    pdf_buffer.seek(0)

    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name=f"{sel_country}_delivery_report.pdf",
        mime="application/pdf",
        key=f"download_{sel_country}_{len(display_df)}" # Needed this to fix a duplication error with the Download PDF Button
    )

if st_data["last_object_clicked"]:
    clicked_lat = round(st_data["last_object_clicked"]["lat"], 4)
    clicked_lng = round(st_data["last_object_clicked"]["lng"], 4)

    def parse_coord(coord_str):
        value = float(coord_str[:-2])
        return value if "N" in coord_str or "E" in coord_str else -value

    df["Lat_float"] = df["Latitude"].apply(parse_coord).round(4)
    df["Lng_float"] = df["Longitude"].apply(parse_coord).round(4)

    match = df[(df["Lat_float"] == clicked_lat) & (df["Lng_float"] == clicked_lng)]

    if not match.empty:
        sel_country = match.iloc[0]["Country"]
        st.markdown("""<hr style='margin-top:40px;margin-bottom:20px;'>""", unsafe_allow_html=True)
        st.subheader(f"Vehicle Deliveries to **{sel_country}**")
        
        display_df = df[df["Country"] == sel_country][["Vehicle Model", "Quantity"]]
        render_pdf_button(display_df, sel_country) # Placed the 'Download PDF button' here to show up above the details/images below only after a country is selected on the map first.

        for _, row in display_df.iterrows():
            vehicle = row["Vehicle Model"]
            quantity = row["Quantity"]
            img_path = f"images/{vehicle_images.get(vehicle, 'default.jpg')}" # All of the applicable image files are in the "images" folder within the project folder
            st.markdown(f"#### {vehicle} (Qty: {quantity})")
            st.image(img_path, use_container_width=True)
    else:
        st.info("No matching country found for the clicked marker.")
        st.warning("Click on a country above to enable the Download PDF Report option.")

