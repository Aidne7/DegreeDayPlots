import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patheffects import withStroke


# Function to plot the degree days chart
def plot_departure_map(sf, ddTable, column_name, colors, title, date_range):
    # Creates a new table with only the columns that are needed
    newTable = ddTable[['cd', column_name]].copy()

    # Adds 3300 to all the values in the cd column
    newTable['cd'] = newTable['cd'] + 3300

    # Renames the cd column to CLIMDIV in order to match up with the Shape File
    newTable.rename(columns={'cd': 'CLIMDIV'}, inplace=True)

    # Merges the newTable with the shapefile
    mergedSF = sf.merge(newTable, on="CLIMDIV", how="left")

    mergedSF[column_name] = mergedSF[column_name].apply(lambda x: 100 if x == 0 else x)
    # Calculate vmin as the minimum value in the data or -200 (whichever is smaller)
    vmin = 50
    # Calculate vmax as the maximum value in the data or 200 (whichever is greater)
    vmax = 150

    # Create a colormap with white at the center for 0
    cmap = LinearSegmentedColormap.from_list("Custom", colors, N=256)

    # Sets the conditions for the chart
    norm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter=100, vmax=vmax)
    fig, ax = plt.subplots(1, 1)

    # Plots the chart with black edges
    mergedSF.plot(column=column_name, cmap=cmap, norm=norm, linewidth=0.8, ax=ax, edgecolor="black", legend=True)

    # Adds text labels for each CLIMDIV section with bigger white font
    for idx, row in mergedSF.iterrows():
        climdiv = row['CLIMDIV']
        if 3301 <= climdiv <= 3310:
            label = str(climdiv - 3300)
            centroid = row['geometry'].centroid
            ax.text(centroid.x, centroid.y, label, ha='center', va='center',
                    fontsize=12, color='white',
                    path_effects=[withStroke(linewidth=2, foreground='black')])  # Add black outline

            plt.title(title)  # Adds the title
    ax.axis('off')  # Disables the axis

    #Adds the date Range
    ax.text(0.5, -0.1,
            f"{date_range[0]}/{date_range[1]}/{date_range[2]} - {date_range[3]}/{date_range[4]}/{date_range[5]}",
            horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

    # Saves the chart as an image
    plt.savefig(f'{title}.png')