import WordTableFiller
import Plot
import DataGrabber


DateRange = '7', '1', '2023', '7', '31', '2023'

ddTable = DataGrabber.scraper(*DateRange)

#WordTableFiller.fillWordTab(ddTable)

Plot.plot_departure_maps(ddTable, DateRange)
