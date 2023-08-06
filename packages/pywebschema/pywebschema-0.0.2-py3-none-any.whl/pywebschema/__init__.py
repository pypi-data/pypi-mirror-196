#!/usr/bin/env python
# -*- coding: utf-8 -*- #

"""
pywebschema: A Python Package for Website Schema

MIT License
Copyright (c) 2023 SERP Wings www.serpwings.com
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS Standard Library
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

import json
from datetime import datetime
from xml.dom import minidom
from unittest.mock import Mock

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS 3rd Party Libraries
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

import requests
from requests.adapters import HTTPAdapter
from requests.models import Response
from bs4 import BeautifulSoup


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# DATABASE/CONSTANTS LIST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# Utility Functions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


def mock_requests_object(url: str) -> Response:
    """generate moked request objet

    Args:
        url (str): url needed to be fetched

    Returns:
        Response: request response object.
    """
    response = Mock(spec=Response)
    response.text = ""
    response.status_code = 9999
    response.url = url
    return response


def get_remote_content(url: str, max_retires: int = 5) -> Response:
    """get remote content using request library

    Args:
        url (str): url needed to be fetched
        max_retires (int, optional): maximum tries to fetch the content. Defaults to 5.

    Returns:
        Response: request response object.
    """
    try:
        s = requests.Session()
        s.mount(url, HTTPAdapter(max_retries=max_retires))
        return s.get(url, headers=HEADER)
    except:
        return mock_requests_object(url)


def get_corrected_url(url: str, fix_slash: str = "/") -> str:
    """correct url for missing slash and scheme

    Args:
        url (str): input url
        fix_slash (str, optional): text to append at the end of url. Defaults to "/".

    Returns:
        str: corrected url
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"http://{url}"

    if not url.endswith(fix_slash):
        url = f"{url}{fix_slash}"

    return url


def extract_schemas(soup):
    """extract schemas form soup object

    Args:
        soup (bs4): soup from bs4

    Returns:
        list: list of schemas on a given page
    """
    all_schemas = []
    for current_link in soup.find_all("script"):
        if "type" in current_link.attrs:
            if current_link["type"] == "application/ld+json":
                all_schemas += [json.loads(current_link.text)]
    return all_schemas


def extract_sub_schemas(schema, root):
    """extrac sub-schemas from root schema

    Args:
        schema: any schema object
        root: root

    Returns:
        list: list of schemas
    """
    all_schemas = []
    if not isinstance(schema, dict):
        all_schemas.append({root: schema})
        return all_schemas

    for s_key, s_value in schema.items():
        if s_key == "@type":
            all_schemas.append({root: schema})
        elif isinstance(s_value, dict):
            results = extract_sub_schemas(s_value, s_key)
            for result in results:
                all_schemas.append(result)

        elif isinstance(s_value, list):
            for item in s_value:
                if isinstance(item, dict):
                    more_results = extract_sub_schemas(item, s_key)
                    for another_result in more_results:
                        all_schemas.append(another_result)
    return all_schemas


def aggregate_schemas(all_schemas):
    """function to all schmea present at a page.

    Args:
        all_schemas (schemas): all schemas (single or mutlples)

    Returns:
        list: list of aggregated schemas
    """
    results = {}

    for schema in all_schemas:
        for s_key, s_value in schema.items():
            if s_key in results:
                results[s_key] += [s_value]
            else:
                results[s_key] = [s_value]
    return results


def get_schemas(url):
    """get schemas from url

    Args:
        url (str): url for which schema is required

    Returns:
        list: list of all aggregated schemas
    """
    url = get_corrected_url(url, fix_slash="/")
    response = get_remote_content(url)

    soup_xml = BeautifulSoup(response.text, "lxml")
    schemas = extract_schemas(soup_xml)

    sub_schemas = []
    for schema in schemas:
        sub_schemas += extract_sub_schemas(schema, "root")

    return aggregate_schemas(sub_schemas)
