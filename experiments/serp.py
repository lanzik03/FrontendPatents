# SerpAPI scrapes Google sites like butter
# The 'clustered' parameter retrieves CPC classifications,
# and it got me thinking: Can this be useful?
# Mind you, only 100 searches per month are available

from serpapi import GoogleSearch

params = {
  "api_key": "1bcb58fa15b19a8edab48477134ac4a2e12c96f415b481354dc54e180e40920a",
  "engine": "google_patents",
  "q": "(Coffee)",
  "country": "US",
  "language": "ENGLISH",
  "clustered": "true"
}

search = GoogleSearch(params)
results = search.get_dict()
