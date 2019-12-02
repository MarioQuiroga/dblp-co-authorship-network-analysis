# dblp-co-authorship-network-analysis
Scripts to scrap, build and analyze dblp co-authorship network.
  
# Scraping

## Get google researchers

```
  python3  scrapers/google_researchers_scraper.py
```
This return:
* csv file `data/google/google_authors.csv`
* json file `data/google/google_authors_titles.json`

## Get co-authors of google authors

```
  python3  coauthor_scraper/google_coauthor.py
```
This return:
* csv file `data/google/authors_titles_google.csv`

# Analysis

## To get the analyzes run in jupyter-lab

```
jupyter-lab analyzer/communitiys_CNA.ipynb
jupyter-lab analyzer/homophilia.ipynb
jupyter-lab analyzer/jupyter-lab 
jupyter-lab analyzer/homophmost_importantilia.ipynb
jupyter-lab analyzer/structural_properties.ipynb
jupyther-lab analyzer/Authores_importantes.ipynb
```


