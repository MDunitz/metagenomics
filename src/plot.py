import leafmap


def add_data_to_map(df, popup, color_column):
    m = leafmap.Map(center=(0, 0), zoom=2)
    m.add_points_from_xy(df, 
                         x='lon', 
                         y='lat', 
                         popup=popup,
                        color_column=color_column, 
                        add_legend=False)
    return m