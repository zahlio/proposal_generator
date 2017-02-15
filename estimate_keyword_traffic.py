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


import logging

SERVICE = 'TrafficEstimatorService'
VERSION = 'v201609'

# Configure logging
logger = logging.getLogger(__name__)


def TrafficEstimatorService(client, selector, keywords):
  """TrafficEstimatorService.

  Args:
    client: instance of an adwords.AdWordsClient.
    selector: campaignEstimateRequests configuration dict
    keywords: list of keyword text strings.

  Returns:
    A list of tuples containing the KeywordCriterion and KeywordEstimate objects
  """
  # Initialize appropriate service.
  traffic_estimator_service = client.GetService(SERVICE, version=VERSION)

  # Get traffic estimates.
  selector, keyword_estimate_requests = _UpdateSelector(selector, keywords)
  estimates = traffic_estimator_service.get(selector)

  campaign_estimate = estimates['campaignEstimates'][0]

  # Display the campaign level estimates segmented by platform.
  if 'platformEstimates' in campaign_estimate:
    platform_template = ('Results for the platform with ID: "%d" and name: '
                         '"%s".')
    for platform_estimate in campaign_estimate['platformEstimates']:
      platform = platform_estimate['platform']
      DisplayEstimate(platform_template % (platform['id'],
                                           platform['platformName']),
                      platform_estimate['minEstimate'],
                      platform_estimate['maxEstimate'])

  # Display the keyword estimates.
  if 'adGroupEstimates' in campaign_estimate:
    ad_group_estimate = campaign_estimate['adGroupEstimates'][0]
    if 'keywordEstimates' in ad_group_estimate:
      keyword_estimates = ad_group_estimate['keywordEstimates']
      keyword_template = ('Results for the keyword with text "%s".')

      keyword_estimates_and_requests = zip(keyword_estimates,
                                           keyword_estimate_requests)

      for keyword_tuple in keyword_estimates_and_requests:
        keyword = keyword_tuple[1]['keyword']
        keyword_estimate = keyword_tuple[0]
        DisplayEstimate(keyword_template % (keyword['text']),
                        keyword_estimate['min'], keyword_estimate['max'])

  return keyword_estimates_and_requests

def _UpdateSelector(selector, keywords, negative_keywords=None):
  """Update a give selector with the provided keywords."""

  if negative_keywords == None:
    negative_keywords = []

  # Construct selector object and retrieve traffic estimates.
  # TODO(awonak) is there any way to use match types other than EXACT here?
  keywords = [{'text': kw, 'matchType': 'EXACT'} for kw in keywords]
  negative_keywords = [{'text': kw, 'matchType': 'EXACT'}
                       for kw in negative_keywords]

  keyword_estimate_requests = []

  for keyword in keywords:
    keyword_estimate_requests.append({
        'keyword': {
            'xsi_type': 'Keyword',
            'matchType': keyword['matchType'],
            'text': keyword['text']
        }
    })

  for keyword in negative_keywords:
    keyword_estimate_requests.append({
        'keyword': {
            'xsi_type': 'Keyword',
            'matchType': keyword['matchType'],
            'text': keyword['text']
        },
        'isNegative': 'true'
    })

  if selector['campaignEstimateRequests'][0]['adGroupEstimateRequests'] is None:
    selector['campaignEstimateRequests'][0]['adGroupEstimateRequests'] = [{}]

  # Create ad group estimate requests.
  selector['campaignEstimateRequests'][0]\
          ['adGroupEstimateRequests'][0]\
          ['keywordEstimateRequests'] = keyword_estimate_requests

  # Return the updated selector
  return selector, keyword_estimate_requests


def _CalculateMean(min_est, max_est):
  if min_est and max_est:
    return (float(min_est) + float(max_est)) / 2.0
  else:
    return None


def _FormatMean(mean):
  if mean:
    return '%.2f' % mean
  else:
    return 'N/A'


def DisplayEstimate(message, min_estimate, max_estimate):
  """Displays mean average cpc, position, clicks, and total cost for estimate.

  Args:
    message: str message to display for the given estimate.
    min_estimate: sudsobject containing a minimum estimate from the
      TrafficEstimatorService response.
    max_estimate: sudsobject containing a maximum estimate from the
      TrafficEstimatorService response.
  """
  # Find the mean of the min and max values.
  mean_avg_cpc = (_CalculateMean(min_estimate['averageCpc']['microAmount'],
                                 max_estimate['averageCpc']['microAmount'])
                  if 'averageCpc' in min_estimate else None)
  mean_avg_pos = (_CalculateMean(min_estimate['averagePosition'],
                                 max_estimate['averagePosition'])
                  if 'averagePosition' in min_estimate else None)
  mean_clicks = _CalculateMean(min_estimate['clicksPerDay'],
                               max_estimate['clicksPerDay'])
  mean_total_cost = _CalculateMean(min_estimate['totalCost']['microAmount'],
                                   max_estimate['totalCost']['microAmount'])

  logger.info(message)
  logger.info('  Estimated average CPC: %s' % _FormatMean((mean_avg_cpc or 0)/1000000.))
  logger.info('  Estimated ad position: %s' % _FormatMean(mean_avg_pos))
  logger.info('  Estimated daily clicks: %s' % _FormatMean(mean_clicks))
  logger.info('  Estimated daily cost: %s' % _FormatMean((mean_total_cost or 0)/1000000.))
