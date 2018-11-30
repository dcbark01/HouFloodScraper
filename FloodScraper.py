import json
import numpy as np
import requests
from bs4 import BeautifulSoup
from pprint import pprint


class QueryBuilder(object):

    def __init__(self):
        self._base_url = 'https://www.harriscountyfws.org/GageDetail/Index/'
        self._postfix_url = '&v=stream%20elevation'

    def _build_query_range(self, last):
        """ Private method for returning the length of time for the query.

        :param last: Length of time to query as string, case insensitive (only allow valid inputs per FWS website)
            1 Hour
            3 Hours
            6 Hours
            12 Hours
            24 Hours
            2 Days
            7 Days
            1 Month
            1 Year

        :return: url formatted as 'span=x hours' or 'span=x days' ... 'span=1 year'


        """
        last = last.lower()
        base_url_str = 'span='
        if last == '1 hour':
            return base_url_str + last
        elif last == '3 hours':
            return base_url_str + last
        elif last == '6 hours':
            return base_url_str + last
        elif last == '12 hours':
            return base_url_str + last
        elif last == '24 hours':
            return base_url_str + last
        elif last == '2 days':
            return base_url_str + last
        elif last == '7 days':
            return base_url_str + last
        elif last == '1 month':
            return base_url_str + last
        elif last == '1 year':
            return base_url_str + last
        else:
            print('Not a valid duration length!')
            return None

    def build_query(self, gage_number, reported_from, last):
        """ Returns a properly encoded URL for querying one of the FWS stream gages. """
        gage_number_str = str(gage_number)
        url = self._base_url + gage_number_str + '?' + 'From=' + reported_from + '&' + self._build_query_range(last) + self._postfix_url
        return url


class FloodScraper(object):

    def __init__(self):
        self.qb = QueryBuilder()

    def _parse_gage_table(self, soup):
        """ Parses the sensor metadata table from the soup. """
        sensorDict = {
            'sensorId': '',
            'sensorType': '',
            'installedDate': '',
            'topOfBankFt': ''
        }
        for tr in soup.find_all(class_='streamDetail'):
            tds = [i.text for i in tr.find_all('td')[1:] if i.text != '']
            tds = tds[0:18]  # Gets rid of the notes at the end of the table
            for i, td in enumerate(tds):
                # print(i, td)
                if td == "Sensor ID":
                    sensorDict['sensorId'] = tds[i + 1]
                elif td == "Sensor Type":
                    sensorDict['sensorType'] = tds[i + 1]
                elif td == "Installed":
                    sensorDict['installedDate'] = tds[i + 1]
                elif td == "Top of Bank (TOB)":
                    sensorDict['topOfBankFt'] = float(tds[i + 1].strip("'"))
        return sensorDict

    def _parse_data_table(self, soup, top_of_bank_ft):
        """ Parses the time-series data from the FWS gage page. """
        _default_units = 'ft'
        data_table = soup.find(id="StreamElevationCumulativeGridView_DXMainTable")
        data = []
        for tr in data_table.find_all('tr')[1:]:  # [1:] gets rid of header row
            tds = tr.find_all('td')[1:]
            # noinspection PyDictCreation
            data_dict = {
                'timestamp': '',
                'elevation': {
                    'value': np.nan,
                    'units': ''
                },
                'depth': {
                    'value': np.nan,
                    'units': ''
                },
                'aboveBank': bool
            }
            data_dict['timestamp'] = tds[0].text
            elev_val = float(tds[1].text.strip("'"))
            data_dict['elevation']['value'] = elev_val
            data_dict['elevation']['units'] = _default_units

            # Calculate the depth
            depth_val = top_of_bank_ft - elev_val
            if depth_val > 0:
                data_dict['depth']['value'] = 0
                data_dict['depth']['units'] = _default_units
                data_dict['aboveBank'] = False
            elif depth_val <= 0:
                data_dict['depth']['value'] = abs(top_of_bank_ft - elev_val)
                data_dict['depth']['units'] = _default_units
                data_dict['aboveBank'] = True

            # Append the data to the results dict
            data.append(data_dict)
        data = list(reversed(data))  # For some reason Houston FWS has time series reversed from typical ordering
        return data

    def lookup_gage(self, gage_number):
        """ Placeholder function for looking up up a gage and its street location. """
        raise NotImplementedError

    def query_gage(self, gage_number, reported_from, last):
        """ Query data from gage and return data as dict. """
        url = self.qb.build_query(gage_number, reported_from, last)

        # Request the page content
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Parse the content of interest
        sensor_metadata = self._parse_gage_table(soup)
        sensor_data = self._parse_data_table(soup, sensor_metadata['topOfBankFt'])

        # Calculate the depth


        # Create a dict for storing all the data and return
        data_dict = {
            "sensorMetaData": sensor_metadata,
            "sensorData": sensor_data
        }
        return data_dict

    def download_gage(self, filename, gage_number, reported_from, last, json_indent=4):
        """ Download the data into a JSON file. """
        data = self.query_gage(gage_number, reported_from, last)
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=json_indent)


if __name__ == "__main__":

    # User Inputs
    gage_number = 520
    reported_from = '09/02/2017 07:31:00 AM'
    last = '6 Hours'

    # Example of querying gage
    scraper = FloodScraper()
    data = scraper.query_gage(gage_number=gage_number, reported_from=reported_from, last=last)
    pprint(data, indent=4)

    # Example of downloading gage
    filename = 'gage_data.json'
    scraper.download_gage(filename, gage_number, reported_from, last)
