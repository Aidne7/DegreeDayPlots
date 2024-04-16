import WordTableFiller
import Plot
import DataGrabber
import geopandas as gpd


DateRange = '3', '1', '2024', '3', '31', '2024'

ddTable = DataGrabber.scraper(*DateRange)

#WordTableFiller.fillWordTab(ddTable)

Plot.plot_departure_map(gpd.read_file('CONUS_CLIMATE_DIVISIONS.shp.zip'), ddTable, 'W_DD', "# of Heating Degree Days", DateRange)

#Plot.plot_departure_map(gpd.read_file('CONUS_CLIMATE_DIVISIONS.shp.zip'), ddTable, 'C_DD', "# of Cooling Degree Days", DateRange)

Plot.plot_departure_map(gpd.read_file('CONUS_CLIMATE_DIVISIONS.shp.zip'), ddTable, 'W_Departure', "Depature from Heating Degree Day", DateRange)

Plot.plot_departure_map(gpd.read_file('CONUS_CLIMATE_DIVISIONS.shp.zip'), ddTable, 'C_Departure', "Depature from Cooling Degree Day", DateRange)