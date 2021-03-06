# Proposal Generator (POC)

**This example demonstrates a new Co-op campaign proposal generation pipeline**

Use a list of search terms or urls to derive a set of related search terms and their benchmarks. This can be used to generate forecasts and proposals for the client and ultimately used to create a new AdWords Campaign.

Currently this POC demonstrates the inputs and outputs of the TargetingIdeaService & TrafficEstimatorService and logs output to stdout. The output from the TrafficEstimatorService can be used to create a proposal for new AdWords Campaigns.

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
