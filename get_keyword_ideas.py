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

SERVICE = 'TargetingIdeaService'
VERSION = 'v201609'
OFFSET = 0
PAGE_SIZE = 100
SEARCH_VOLUME_THRESHOLD = 0  # The minimum threshold of Search Volume for a Keyword
KEYWORD_IDEA_LIMIT = 10  # The number of KeywordIdeas to return

logger = logging.getLogger(__name__)


def TargetingIdeaService(client, selector):
  """TargetingIdeaService.

  Args:
    client: instance of an adwords.AdWordsClient
    selector: searchParameters configuration dict

  Returns:
    A list of KeywordIdea objects.
  """
  # Initialize appropriate service.
  targeting_idea_service = client.GetService(SERVICE, version=VERSION)

  # Construct selector object and retrieve related keywords.
  offset = OFFSET
  results = []

  more_pages = True
  while more_pages:
    page = targeting_idea_service.get(selector)

    # Display results.
    if 'entries' in page:
      for result in page['entries']:

        # Stop reading results after limit reached
        if len(results) >= KEYWORD_IDEA_LIMIT:
          more_pages = False
          offset = int(page['totalNumEntries'])
          break

        attributes = {}
        for attribute in result['data']:
          # Parse the appropriate value out of each row of data
          attributeValue = getattr(attribute['value'], 'value', '0')
          if getattr(attribute.value, 'Attribute.Type') == 'MoneyAttribute':
            attributes[attribute['key']] = getattr(attributeValue,
                                                   'microAmount', 0) / 1000000.
          else:
            attributes[attribute['key']] = attributeValue

        # Require a threshold of X search terms to be considered significant
        if attributes['SEARCH_VOLUME'] < SEARCH_VOLUME_THRESHOLD:
          continue

        results.append(attributes)
        DisplayIdea(attributes)

    else:
      logger.info('No related keywords were found.')

    offset += PAGE_SIZE
    selector['paging']['startIndex'] = str(offset)
    more_pages = offset < int(page['totalNumEntries'])

  return results


def DisplayIdea(keyword):
  """Displays text, search volume, average cpc and categories for idea.

  Args:
    keyword: dict attributes of Keyword Idea
  """
  logger.info('Found Keyword with text [%s]' % keyword['KEYWORD_TEXT'])
  logger.info('  Keyword Idea search volume: %s' % keyword['SEARCH_VOLUME'])
  logger.info('  Keyword Idea average CPC: %s' % keyword['AVERAGE_CPC'])
  logger.info('  Keyword Idea categories: %s' % keyword['CATEGORY_PRODUCTS_AND_SERVICES'])
