#!/usr/bin/python
#
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example demonstrates a new Co-op campaign creation pipeline

Given an input of search term or url, fetch a list of keyword ideas. Then, use
the results as input to the estimate keyword traffic service. If that estimate
meets some threshold set in configuration, then create a new campaign based off
of the keyword results from first step.

AUTHOR: Project Raven Team [raven-faq@googlegroups.com]

VERSION: 1.0

CHANGELOG:
- version 1.0
  - Released initial version.

USAGE:
  main.py <config> [--search_terms <search_terms>] [--search_url <search_url>]

Example:
  $ python main.py default.yaml --search_terms advil
  $ python main.py default.yaml --search_url https://www.advil.com/advil
"""

import argparse
import logging
import os, sys

import yaml
from googleads import adwords

from get_keyword_ideas import TargetingIdeaService
from estimate_keyword_traffic import TrafficEstimatorService


# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure args
parser = argparse.ArgumentParser()
parser.add_argument("config", help="path to YAML configuration file")
parser.add_argument("--search_terms", help="comma separated list of search terms")
parser.add_argument("--search_url", help="a url used to search for related keywords")
args = parser.parse_args()

class MissingSearchTermOrDomain(Exception):
  pass


def main(client, config):
  logger.info('Execute Keyword Idea Service.')
  results = TargetingIdeaService(client, config['targetingIdeaServiceConfig'])

  logger.info('Pass Keywords to Traffic Estimator Service.')
  keywords = [row['KEYWORD_TEXT'] for row in results]
  keyword_estimates_and_requests = TrafficEstimatorService(client,
                              config['trafficEstimatorServiceConfig'], keywords)

  # TODO: use the combined results from both services and output the data in
  # a useful format.
  # WriteResults(keyword_estimates_and_requests)
  logger.info('All Done!')

if __name__ == '__main__':
  # Initialize AdWords API client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  # parse config file
  logger.info('Load configuration.')
  with open(args.config, 'r') as config_file:
    config = yaml.load(config_file.read())

  # parse search keyword
  if args.search_terms:
    config['targetingIdeaServiceConfig']['searchParameters'].append({
      'xsi_type': 'RelatedToQuerySearchParameter',
      'queries': args.search_terms.split(',')
    })

  # parse search url
  if args.search_url:
    config['targetingIdeaServiceConfig']['searchParameters'].append({
      'xsi_type': 'RelatedToUrlSearchParameter',
      'urls': [args.search_url]
    })

  # validate either search keyword or search url were provided
  if args.search_url is None and args.search_terms is None:
    raise MissingSearchTermOrDomain('Must provide either search_terms or '
                                    'search_url')

  main(adwords_client, config)
