import leafmap
import bokeh.io
import bokeh.plotting

def add_data_to_map(df, popup, color_column):
    m = leafmap.Map(center=(0, 0), zoom=2)
    m.add_points_from_xy(df, 
                         x='lon', 
                         y='lat', 
                         popup=popup,
                        color_column=color_column, 
                        add_legend=False)
    return m



def index_plot(results_df):
    p = bokeh.plotting.figure(
        width=400,
        height=300,
        x_axis_label="Shannon Index",
        y_axis_label="Simpsons Diversity Index",
        toolbar_location=None,
        title="Brown Algae Microbiome Diversity"
    )
    p.circle(
        source=results_df,
        x="Shannon Index",
        y="Simpsons Index",
        color="color"
    )
    return p