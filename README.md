# command-line-csv

**NOTE**: KNOWN ISSUES, cannot process non UTF-8 CSVs. For example `./normalizer < sample-with-broken-utf-8.csv > output.csv` does not work. I tried parsing it, but was struggling with it and reverted back to the original method + assumption with non broken UTF-8.

1. `pip3 install -r requirements.txt` (if I had the time, I would've Dockerized it so the user wouldn't have to install everything themselves - sorry!)
2. `./normalizer < sample.csv > output.csv` (./normalizer < sample.csv (sets as stdin) > output.csv (stdout) -- redirection sets up stdin and stdout)

