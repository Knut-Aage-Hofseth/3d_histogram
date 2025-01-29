import pandas as pd
import geopandas as gpd
import pydeck as pdk

df = pd.read_csv("./data/DECENNIALDHC2020.P1-2024-12-16T113140.csv")

df.drop(columns=['Label (Grouping)'], inplace=True)
df = df.T
df.columns = ['POPULATION']
df = df.rename_axis('Info').reset_index()

# Changing the col names and creating new columns from the titles
df["NAME"] = df.apply(lambda x: x['Info'].split(",")[0].split(" ")[2], axis=1)
df['COUNTY'] = df.apply(lambda x: x['Info'].split(",")[1], axis=1)

df.drop(columns=['Info'], inplace=True)

gdf = gpd.read_file("./data/tl_2020_01_tract.zip")

complete_df = gdf.merge(df, how="left")

complete_df.to_file("./data/connecticut_tracts.json", driver="GeoJSON")

ct_tracts = gpd.read_file("./data/connecticut_tracts.json")

ct_tracts['POPULATION'] = ct_tracts['POPULATION'].apply(lambda x: int(x.replace(",", "")))

ct_tracts["POPDEN"]=ct_tracts['POPULATION']/(ct_tracts['ALAND']*0.0000003861)

ct_tracts["POPDENNORM"] = ct_tracts['POPDEN'].apply(lambda x: (255+((x - ct_tracts['POPDEN'].min())*(255)) )/ (ct_tracts['POPDEN'].max() - ct_tracts['POPDEN'].min()) )

ct_tracts.fillna(0, inplace=True)

INITIAL_VIEW_STATE = pdk.ViewState(latitude=41.76375, 
                                   longitude=-72.69102, 
                                   zoom=9, max_zoom=16, pitch=60, bearing=0)

tracts = pdk.Layer(
    "GeoJsonLayer",
    ct_tracts,
    opacity=1,
    stroked=True,
    filled=True,
    extruded=True,
    wireframe=True,
    pickable=True,
    get_elevation="POPDEN", # Converting to population density per sq m to per sq mile
    get_fill_color="POPULATION==0?[0,0,0,0]:[POPDENNORM+95, POPDENNORM+95, POPDENNORM+95]",
    get_line_color="POPULATION==0?[0,0,0,0]:[POPDENNORM+50, POPDENNORM+50, POPDENNORM+50]",
)

# All together
# You can customize by adding more layers if you wish
r = pdk.Deck(layers=[tracts], initial_view_state=INITIAL_VIEW_STATE)

# Exporting as an html file
r.to_html("PATH/filename.html")