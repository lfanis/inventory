import streamlit as st
import sqlite3
from ppf.datamatrix import DataMatrix

st.set_page_config(
    page_title="Add a component",
    page_icon="🐞",
    layout="centered",
    initial_sidebar_state="auto",
)
st.title("🐞 components!")

st.sidebar.write(f"One day PInky, one day")

conn = sqlite3.connect("db/stocks.db")
cur = conn.cursor()

""" Generating a list of manufacturer as we know it """


@st.cache_data 
def loadManufacturerFile():
    ManufacturerFile = open("data/Manufacturer.txt", "r")
    lines = ManufacturerFile.read()
    ManufacturerList = lines.splitlines()
    ManufacturerFile.close()
    return ManufacturerList


ManufacturerList = loadManufacturerFile()


""" Now we do the actual Form stuff """
form = st.form(key="annotation")

with form:
    cols = st.columns((1, 1))
    ManufacturerPN = cols[0].text_input("Manufacturer PN:")
    Manufacturer = (cols[1].selectbox("Manufacturer: ", ManufacturerList),)
    Description = (cols[1].text_input("Description: "),)
    Stock_QTY = (cols[1].number_input("Stock QTY ", min_value=1),)
    Label = (cols[0].text_input("Label: "),)
    Value = (cols[0].text_input("Value: "),)
    Tolerance = (cols[0].text_input("Tolerance: "),)
    Package = cols[1].selectbox(
        "Package:",
        [
            "MELF",
            "SOD",
            "SOT",
            "TO-3",
            "TO-5",
            "TO-18",
            "TO-39",
            "TO-46",
            "TO-66",
            "TO-92",
            "TO-99",
            "TO-100",
            "TO-126",
            "TO-220",
            "TO-226",
            "TO-247",
            "TO-251",
            "TO-252",
            "TO-262",
            "TO-263",
            "TO-274",
            "SIP",
            "DIP",
            "CDIP ",
            "CERDIP",
            "QIP",
            "SKDIP",
            "SDIP",
            "ZIP",
            "MDIP",
            "PDIP",
        ],
        index=4,
    )

    Image_URL = (cols[1].text_input("Image URL"),)
    Datasheet = (cols[0].text_input("Datasheet URL"),)
    Storage = (cols[0].text_input("Storage"),)
    Seller = cols[1].text_input("Seller")
    cols = st.columns(2)

    submitted = st.form_submit_button(label="Submit")


if submitted:
    # st.write(type(ManufacturerPN) , Manufacturer , Description , Stock_QTY , Label , Value , Tolerance, Package, Image_URL , Datasheet , Storage, Seller)

    SQL = f'INSERT into ecomponents ("Manufacturer_PN","Manufacturer", "Description", "Label", "Value", "Tolerance" , "Package", "Storage","Stock QTY","Image URL", "Datasheet","Seller") VALUES ("{ManufacturerPN}","{Manufacturer[0]}","{Description[0]}","{Label[0]}","{Value[0]}","{Tolerance[0]}","{Package}","{Storage[0]}","{Stock_QTY[0]}","{Image_URL[0]}","{Datasheet[0]}","{Seller}")'
    # cursor.execute(SQL)
    cur.execute(SQL)
    conn.commit()
   
    st.write("Added")
