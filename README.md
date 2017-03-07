# Proposal Generator (POC)

**This example demonstrates a new Co-op campaign proposal generation pipeline**

Given an input of search term or url, fetch a list of keyword ideas. Then, use the results as input to the estimate keyword traffic service. If that estimate meets some threshold set in configuration, then create a new campaign based off of the keyword results from first step.

### Getting Started

After cloning the repository, you will need to install the required python libraries using pip.

```
$ pip install requirements.txt
```

Using the Python client for the AdWords API, you will need to follow the steps to configure your credentials. Follow the instructions here:

https://github.com/googleads/googleads-python-lib#getting-started

Once everything is configured correctly, you are ready to run the script.

Usage:
```
main.py <config> [--search_terms <search_terms>] [--search_url <search_url>]
```

Example:
```
$ python main.py default.yaml --search_terms advil
$ python main.py default.yaml --search_url https://www.advil.com/advil
```
