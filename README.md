# my-first-scraper

## What is does?

1. It queries a given API to get a list of countries and leaders per country.
2. This list contains structured data such as ID, first name, last name, birth date, place of birth, etc. for each leader.
3. It then scrapes wikipedia for the very first paragraph describing each leader and adds it to this list.
4. Finally it prints the list of leaders per country to a json file.

## How it works?

1. Run `$ python3 leaders_scraper.py`
2. A new json file is created in your current directory
---
With big thanks to the Brussels BeCode Bouman 5 Team!
