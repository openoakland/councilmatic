WebPage/website/scraped/year%.csv: run_calendar.py
	python run_calendar.py -d $(subst .csv,,$(subst WebPage/website/scraped/year,,$@)) > $@

.PHONY: clean

scrape: WebPage/website/scraped/year2019.csv WebPage/website/scraped/year2018.csv WebPage/website/scraped/year2017.csv WebPage/website/scraped/year2016.csv WebPage/website/scraped/year2015.csv WebPage/website/scraped/year2014.csv

generate: WebPage/src/main.py
	python WebPage/src/main.py

clean:
	$(shell rm -f WebPage/website/index.html)
	$(shell rm -rf WebPage/website/{2014..2019}/*)
