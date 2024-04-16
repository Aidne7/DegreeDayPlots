import WordTableFiller
import Plot
import DataGrabber
import geopandas as gpd

colors = [
    (179/255, 88/255, 6/255),
    (241/255, 163/255, 64/255),
    (254/255, 224/255, 182/255),
    (247/255, 247/255, 247/255),
    (216/255, 218/255, 235/255),
    (153/255, 142/255, 195/255),
    (84/255, 39/255, 136/255)
]

DateRange = '3', '1', '2024', '3', '31', '2024'
colors.reverse()
ddTable = DataGrabber.scraper(*DateRange)

WordTableFiller.fillWordTab(ddTable)

Plot.plot_departure_map(gpd.read_file('CONUS_CLIMATE_DIVISIONS.shp.zip'), ddTable, 'W_Percent', colors, "Heating Degree Day Percent of Normal (%)", DateRange)

Plot.plot_departure_map(gpd.read_file('CONUS_CLIMATE_DIVISIONS.shp.zip'), ddTable, 'C_Percent', colors, "Cooling Degree Day Percent of Normal (%)", DateRange)
