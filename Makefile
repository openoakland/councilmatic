WebPage/website/scraped/year%.json: run_calendar.py
	python run_meeting_json.py --year $(subst .json,,$(subst WebPage/website/scraped/year,,$@)) --output $@

.PHONY: clean

scrape: WebPage/website/scraped/year2019.json WebPage/website/scraped/year2018.json WebPage/website/scraped/year2017.json WebPage/website/scraped/year2016.json WebPage/website/scraped/year2015.json WebPage/website/scraped/year2014.json

generate: WebPage/src/main.py
	python WebPage/src/main.py

clean:
	$(shell rm -f WebPage/website/index.html)
	$(shell rm -rf WebPage/website/{2014..2019}/*)
