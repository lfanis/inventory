import streamlit as st
import sqlite3
import pandas as pd
from streamlit_option_menu import option_menu
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
#from ppf.datamatrix import DataMatrix

columns = [
    "id",
    "Manufacturer_PN",
    "Manufacturer",
    "Description",
    "Label",
    "Value",
    "Tolerance",
    "Package",
    "Storage",
    "Stock QTY",
    "Image URL",
    "Datasheet",
    "Seller",
]

conn = sqlite3.connect("db/stocks.db")
cur = conn.cursor()


def create_table():
    # cur.execute('CREATE TABLE IF NOT EXISTS ecomponents(id integer PRIMARY KEY, name TEXT, count integer)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS ecomponents(id integer PRIMARY KEY autoincrement, "Manufacturer_PN" TEXT,"Manufacturer" TEXT,"Description" TEXT,"Label" TEXT ,"Value" TEXT,"Tolerance" TEXT,"Package" TEXT ,"Storage" TEXT,"Stock QTY" integer,"Image URL" TEXT ,"Datasheet" TEXT,"Seller" TEXT)'
    )


def add(name, count):
    cur.execute("INSERT INTO ecomponents(name, count) VALUES (?,?)", (name, count))
    conn.commit()


def update(id, count):
    cur.execute("UPDATE product SET count=? WHERE id=?", (count, id))
    conn.commit()


### XXX called every load, i should feel bad
create_table()


def convert_df_csv(df):
    return df.to_csv(index=False).encode("utf-8")

# def convert_df_excel(df):
#     return df.to_excel(index=False).encode("utf-8")

# @st.cache()  # Behavior of caching has changed in 1.18.1, i should do better but yolo https://docs.streamlit.io/library/advanced-features/caching
def fetch_data():
    return pd.read_sql("SELECT * FROM ecomponents", con=conn)


# Use the full page instead of a narrow central column and close the side bar
# Probably a bug in this version but yeah ignore it
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
try:
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
except st.errors.StreamlitAPIException as e:
    pass 

## Side bar var
grid_height = st.sidebar.number_input(
    "Grid height", min_value=300, max_value=1208, value=500
)
return_mode = st.sidebar.selectbox(
    "Return Mode", list(DataReturnMode.__members__), index=1
)
return_mode_value = DataReturnMode.__members__[return_mode]

update_mode = st.sidebar.selectbox(
    "Update Mode",
    list(GridUpdateMode.__members__),
    index=len(GridUpdateMode.__members__) - 1,
)
update_mode_value = GridUpdateMode.__members__[update_mode]

# enterprise modules
enable_enterprise_modules = st.sidebar.checkbox("Enable Enterprise Modules")
if enable_enterprise_modules:
    enable_sidebar = st.sidebar.checkbox("Enable grid sidebar", value=False)
else:
    enable_sidebar = False

# enable_pagination = st.sidebar.checkbox("Enable pagination", value=False)
fit_columns_on_grid_load = st.sidebar.checkbox("Fit Grid Columns on Load", value=True)

# XXX Fetch data wrapped in caching
st.write("# Component in the shop")
df = fetch_data()
st.write(df)


# All the grid options for edit go here
# Infer basic colDefs from dataframe types
gb = GridOptionsBuilder.from_dataframe(df)

# customize gridOptions
gb.configure_default_column(
    groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True
)

gb.configure_auto_height(autoHeight=True)

if enable_sidebar:
    gb.configure_side_bar()

gb.configure_grid_options(domLayout="normal")
gridOptions = gb.build()

# Display the grid
st.header("Edit inventory")
st.markdown(
    """
    Simply edit the grid and update the elements you care about. 
"""
)

grid_response = AgGrid(
    df,
    gridOptions=gridOptions,
    height=grid_height,
    width="100%",
    data_return_mode=return_mode_value,
    update_mode=update_mode_value,
    fit_columns_on_grid_load=fit_columns_on_grid_load,
    allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
    enable_enterprise_modules=enable_enterprise_modules,
)

df2 = grid_response["data"].copy()

try:
    st.write("The following changes will be applied", df.compare(grid_response["data"]))
    if st.button("Update db", key=1):
        df2.to_sql(
            "ecomponents", conn, if_exists="replace", index_label="id", index=False
        )
        st.write("##### Updated db")
        # df_update = pd.read_sql('SELECT * FROM product', con=conn)
        df_update = fetch_data()
        st.write(df_update)
        # this forces a reload, are we loosing something else? probably as it is session based
        st.experimental_rerun()

except ValueError:
    st.error("Please clear the filter before can see and commit changes")


# Download the inventory
st.header("Download inventory in csv format ")
st.markdown(
    """
    Export inventory as a CSV
"""
)

st.download_button(
    "Export to CSV", convert_df_csv(df), "inventory.csv", "text/csv", key="download-csv"
)

# XXX Add inventory upload
# inventoryLoad = st.file_uploader("upload file", type={"csv", "txt"})
# if inventoryLoad is not None:
#     df_inventoryLoad = pd.read_csv(inventoryLoad)
#     # st.experimental_rerun()
# st.write(df_inventoryLoad)

# Search / filtering: https://discuss.streamlit.io/t/how-can-i-add-a-user-input-box-that-gives-an-auto-complete-suggestion-from-a-list-but-also-allows-user-too-input-its-own-query/15502/15
# col_one_list = df['Description'].tolist()
# selectbox_01 = st.selectbox('Select', col_one_list)

cur.close()
conn.close()
