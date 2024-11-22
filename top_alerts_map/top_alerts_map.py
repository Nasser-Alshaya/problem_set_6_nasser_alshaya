from shiny import App, ui, reactive, render
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

app_ui = ui.page_fluid(
   ui.input_select(
       id = "type_subtype",
       label = "Choose a combination:",
       choices = []),
   ui.output_plot("ts"),
)

def server(input, output, session):
    @reactive.calc
    def full_data():
        df = pd.read_csv("top_alerts_map.csv")
        df["type_subtype"] = df["updated_type"] + " - " + df["updated_subtype"]
        return df

    @reactive.calc
    def geo_data():
       file_path = "/Users/nasser.alshaya/Desktop/Fall-2024/PPHA-30538/PS6/top_alerts_map"
       return gpd.read_file(file_path)
    
    @reactive.effect
    def _():
        type_subtype = full_data()['type_subtype']
        type_subtype_list = type_subtype.tolist()
        ui.update_select('type_subtype', choices = type_subtype_list)

    @render.plot
    def ts():
        df = full_data()
        gdf = geo_data()
        selected_type_subtype = input.type_subtype.get()
        filtered_df = df[df["type_subtype"] == selected_type_subtype]
        fig, ax = plt.subplots(figsize=(10, 6))

        gdf.plot(ax=ax, color="lightgrey", edgecolor="black", alpha=0.8)

            
        scatter = ax.scatter(
            filtered_df["longitude"],
            filtered_df["latitude"],
            s=filtered_df["count"],  
            c=filtered_df["count"], 
            cmap="plasma",
            alpha=0.7,
            edgecolor="black",
            linewidth=0.5,
            )
        ax.set_title(f"Top Alerts for {selected_type_subtype}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True)

        ax.set_xlim(-87.94, -87.52)
        ax.set_ylim(41.64, 42.02)
        cbar = plt.colorbar(scatter, ax=ax, orientation="vertical")
        cbar.set_label('Number of Incidents')
        cbar.ax.set_position([0.85, 0.25, 0.03, 0.5])

        return fig
app = App(app_ui, server)