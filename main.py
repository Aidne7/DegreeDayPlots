import WordTableFiller
import Plot
import DataGrabber


DateRange = '3', '1', '2024', '3', '31', '2024'

ddTable = DataGrabber.scraper(*DateRange)

#WordTableFiller.fillWordTab(ddTable)

Plot.plot_departure_maps(ddTable, DateRange)
