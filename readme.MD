# Houston Flood Data Scraper

A simple scraper for getting historical data from the Harris County (Houston, Texas) Flood Warning System (FDS).
For more info on FWS, [see the FWS site at this link](https://www.harriscountyfws.org/).

## Quickstart

### Prerequisites / Installation

To use this scraper, you can install the requirements from the requirements.txt file by typing the following command 
into your activated virtual environment command prompt:

    pip install -r requirements.txt

### Usage Example

The Harris County FWS obtains its data from stream gages maintained by the US Geological Survey (USGS). To get 
historical data from a gage, you'll need the following as inputs:

1. Gage Number - You can get this from the FWS main page (hover over the gage to see number)
2. Reported From - The date of interest for your query, formatted as 'mm/dd/yyyy hh:mm:ss XM'
3. Last - Number of preceding hours/mins/days/months/year to query (see code for valid inputs)

![alt text](https://s3.amazonaws.com/phin-flood-images-db/static/fws_main_page.png "FWS Website")

#### Example Query

Querying data is as simple as the following:

```python
# Import the FloodScraper Module
from FloodScraper import FloodScraper

# User inputs
gage_number = 520
reported_from = '09/02/2017 07:31:00 AM'
last = '6 Hours'

# Create scraper interest and run a query
scraper = FloodScraper()
data = scraper.query_gage(gage_number=gage_number, reported_from=reported_from, last=last)
```


The data is returned as a Python dictionary, for example:

    {   'sensorData': [   {   'aboveBank': True,
                          'depth': {'units': 'ft', 'value': 7.490000000000002},
                          'elevation': {'units': 'ft', 'value': 39.49},
                          'timestamp': '8/27/2017 5:43 AM'},
                      {   'aboveBank': False,
                          'depth': {'units': 'ft', 'value': 0},
                          'elevation': {'units': 'ft', 'value': 9.25},
                          'timestamp': '9/7/2017 6:00 PM'}],
    'sensorMetaData': {   'installedDate': '3/27/1984',
                          'sensorId': '519',
                          'sensorType': 'USGS Radar',
                          'topOfBankFt': 32.0}}
                          
The 'elevation' field contains a record of the depth of the water above the stream bottom. The 'depth' field
is a calculated field that records the height of the water <u>above</u> the Top of Bank (TOB). If the depth of 
water is above the TOB, then the 'aboveBank' key holds the value 'True', otherwise it is 'False'.


#### Example Download to JSON

Data can also be downloaded in JSON format using the following method:

```python
# Import the FloodScraper Module
from FloodScraper import FloodScraper

# User inputs
gage_number = 520
reported_from = '09/02/2017 07:31:00 AM'
last = '7 Days'
filename = 'gage_data.json'

# Create scraper interest and run a query
scraper = FloodScraper()
data = scraper.download_gage(filename=filename, gage_number=gage_number, reported_from=reported_from, last=last)
```

The JSON output is formatted like this:

```json
{
    "sensorMetaData": {
        "sensorId": "519",
        "sensorType": "USGS Radar",
        "installedDate": "3/27/1984",
        "topOfBankFt": 32.0
    },
    "sensorData": [
        {
            "timestamp": "8/26/2017 7:31 AM",
            "elevation": {
                "value": 21.69,
                "units": "ft"
            },
            "depth": {
                "value": 0,
                "units": "ft"
            },
            "aboveBank": false
        },
        {
            "timestamp": "8/27/2017 5:43 AM",
            "elevation": {
                "value": 39.49,
                "units": "ft"
            },
            "depth": {
                "value": 7.490000000000002,
                "units": "ft"
            },
            "aboveBank": true
        }
    ]
}
```


## Authors

* **[Daniel Barker](https://www.linkedin.com/in/danielchristopherbarker/)** - *Initial work*


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

