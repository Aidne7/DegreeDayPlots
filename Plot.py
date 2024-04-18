import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patheffects import withStroke
import geopandas as gpd

with open("MPL_Blues.rgb", 'r') as f:
    lines = f.readlines()
    colorsOne = []
    for line in lines:
        if not line.strip() or line.startswith('#') or line.startswith('ncolors='):
            continue
        r, g, b = map(float, line.split())
        colorsOne.append([r, g, b])

    # Check if the number of colors read is equal to ncolors
    if len(colorsOne) != 128:
        raise ValueError("Number of colors read does not match ncolors=128")

    # Convert to numpy array for colormap creation
    colorsOne = np.array(colorsOne)


    print("Number of colors read:", len(colorsOne))

    with open("MPL_Reds.rgb", 'r') as f:
        lines = f.readlines()
        colorsTwo = []
        for line in lines:
            if not line.strip() or line.startswith('#') or line.startswith('ncolors='):
                continue
            r, g, b = map(float, line.split())
            colorsTwo.append([r, g, b])

        # Check if the number of colors read is equal to ncolors
        if len(colorsTwo) != 128:
            raise ValueError("Number of colors read does not match ncolors=128")

        # Convert to numpy array for colormap creation
        colorsTwo = np.array(colorsTwo)


    print("Number of colors read:", len(colorsTwo))

with open("MPL_BG.rgb", 'r') as f:
    lines = f.readlines()
    colorsThree = []
    for line in lines:
        if not line.strip() or line.startswith('#') or line.startswith('ncolors='):
            continue
        r, g, b = map(float, line.split())
        colorsThree.append([r, g, b])

    # Check if the number of colors read is equal to ncolors
    if len(colorsThree) != 64:
        raise ValueError("Number of colors read does not match ncolors=64")

    # Convert to numpy array for colormap creation
    colorsThree = np.array(colorsThree)



    print("Number of colors read:", len(colorsThree))

    with open("MPL_Br.rgb", 'r') as f:
        lines = f.readlines()
        colorsFour = []
        for line in lines:
            if not line.strip() or line.startswith('#') or line.startswith('ncolors='):
                continue
            r, g, b = map(float, line.split())
            colorsFour.append([r, g, b])

        # Check if the number of colors read is equal to ncolors
        if len(colorsFour) != 64:
            raise ValueError("Number of colors read does not match ncolors=64")

        # Convert to numpy array for colormap creation
        colorsFour = np.array(colorsFour)


    print("Number of colors read:", len(colorsFour))






sf = gpd.read_file('CONUS_CLIMATE_DIVISIONS.shp.zip')


# Function to plot the degree days chart
def plot_departure_maps(ddTable, date_range):
    for x in range(0, 4):

        if x == 0:
            column_name = 'W_DD'
            title = "# of Heating Degree Days"
            cBarLabel = 'Heating Degree Days'
            nColors = colorsOne

        # elif x==2:
        #     column_name = 'C_DD'
        #     title = "# of Cooling Degree Days"
        #     cBarLabel = 'Cooling Degree Days'
        #     nColors = colorsTwo

        elif x==1:
            column_name = 'W_Departure'
            title = "Depature from Heating Degree Days"
            cBarLabel = 'Departure Heating Degree Days'
            nColors = colorsFour[::-1]

        elif x==3:
            column_name = 'C_Departure'
            title = "Depature from Cooling Degree Days"
            cBarLabel = 'Depature Cooling Degree Days'
            nColors = colorsThree

        # Creates a new table with only the columns that are needed
        newTable = ddTable[['cd', column_name]].copy()

        # Adds 3300 to all the values in the cd column
        newTable['cd'] = newTable['cd'] + 3300

        # Renames the cd column to CLIMDIV in order to match up with the Shape File
        newTable.rename(columns={'cd': 'CLIMDIV'}, inplace=True)

        # Merges the newTable with the shapefile
        mergedSF = sf.merge(newTable, on="CLIMDIV", how="left")

        # Calculate vmin as the minimum value in the data or -200 (whichever is smaller)
        vmin = mergedSF[column_name].min()
        # Calculate vmax as the maximum  value in the data or 200 (whichever is greater)
        vmax = mergedSF[column_name].max()

        vcenter = ((vmax - vmin) / 2) + vmin

        print(vmax)
        print(vcenter)
        print(vmin)
        # Create a colormap with white at the center for 0
        cmap = LinearSegmentedColormap.from_list("Custom", nColors, N=18)

        # Sets the conditions for the chart
        norm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        fig, ax = plt.subplots(1, 1)

        # Plots the chart with black edges
        mergedSF.plot(column=column_name, cmap=cmap, norm=norm, linewidth=0.8, ax=ax, edgecolor="black", legend=False)

        # Adds text labels for each CLIMDIV section with bigger white font
        for idx, row in mergedSF.iterrows():
            climdiv = row['CLIMDIV']
            if 3301 <= climdiv <= 3310:
                label = str(climdiv - 3300)
                centroid = row['geometry'].centroid
                ax.text(centroid.x, centroid.y, label, ha='center', va='center',
                        fontsize=12, color='white',
                        path_effects=[withStroke(linewidth=2, foreground='black')])  # Add black outline

        ax.axis('off')  # Disables the axis

        # Adds the date Range
        ax.text(0.5, -0.1,
                f"{date_range[0]}/{date_range[1]}/{date_range[2]} - {date_range[3]}/{date_range[4]}/{date_range[5]}",
                horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

        # Create a ScalarMappable for colorbar
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        # Manually create colorbar
        cbar = plt.colorbar(sm, ax=ax, ticks=ticker.MaxNLocator(5))
        cbar.set_label(cBarLabel)  # Set the colorbar label

        # Adds the title
        plt.title(title)

        # Saves the chart as an image
        plt.savefig(f'{title}.png')
