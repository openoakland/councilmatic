WebPage/website/scraped/Scraper%.json: run_calendar.py
	python run_meeting_json.py --year $(subst .json,,$(subst WebPage/website/scraped/Scraper,,$@)) --output $@

.PHONY: clean

serve:
	cd WebPage/website && python -m http.server

scrape: WebPage/website/scraped/Scraper2019.json WebPage/website/scraped/Scraper2018.json WebPage/website/scraped/Scraper2017.json WebPage/website/scraped/Scraper2016.json WebPage/website/scraped/Scraper2015.json WebPage/website/scraped/Scraper2014.json

generate: WebPage/src/main.py
	python WebPage/src/main.py

clean:
	$(shell rm -f WebPage/website/index.html)
	$(shell rm -rf WebPage/website/{2014..2019}/*)
