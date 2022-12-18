# wikipedia-scraper
Wikipedia web scraper built in python to gather a list of all the link adjacencies of every published wikipedia page

Most of the time spent running this program is waiting for Wikipedia servers. From internal testing, each page fetch takes between 100 and 400ms depending on internet connectivity and the computation time (dictionary parsing mostly) is negligible compared to page fetching. This might change once the output json file nears the ~50GB size needed for all page adjacencies (has not been tested yet).

A numToFetch of ~1000 is reasonable, and runs in a few minutes on my machines
