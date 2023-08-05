import requests

# url = 'https://api.openweathermap.org/data/2.5/forecast?q=Madrid&appid=d8c633a565504da84221459cd224eedd'
# url = 'https://api.openweathermap.org/data/2.5/forecast?lat=44.34&lon=10.99&appid=d8c633a565504da84221459cd224eedd'

class Weather:
    """Creates a weather object using apikey, either
    a city name or lat and lon coordinates as inputs.

    Package use example:

    # Create a weather object using city name
    # Get your own Apikey from https://openweathermap.org
    # Wait until the Apikey is activated.

    >> weather1 = Weather(apikey='d8c633a565504da84221459cd224eedd', city = 'Garland')

    # Using latitude and longitude coordinates
    >> weather2 = Weather(apikey='d8c633a565504da84221459cd224eedd', lat = '45', lon = 20)

    # Using latitude and longitude coordinates with count days.
    >> weather2 = Weather(apikey='d8c633a565504da84221459cd224eedd', lat = '45', lon = 20, cnt = 7)

    # Get complete weather data for next 12 hours
    >> weather1.next_12h_detail()

    # Simplified data for the next 12 hours.
    >> weather1.next12h_simplified()
    """
    def __init__(self, apikey, city=None, lat=None, lon=None):

        if city and (not lat and not lon):
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}"
            r = requests.get(url)
            self.data = r.json()
        elif (lat and lon) and (not city):
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}"
            r = requests.get(url)
            self.data = r.json()
        elif city and (lat and lon):
            raise TypeError("Provide only city or lat and lon values, not all three")
        else:
            raise TypeError("Please provide either city or lat and lon values")
        if self.data['cod'] != '200':
            raise ValueError(self.data['message'])

    def next_12h_detail(self):
        """Returns every 3-hour data for the next 12 hours as a dict
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """Returns date, time, temperature, sky condition, and icon for every
        3-hours for next 12 hours as a tuple of tuples.
        """
        simple_data = []
        for dicty in self.data['list'][:4]:
            simple_data.append((dicty['dt_txt'],dicty['main']['temp'],
                                dicty['weather'][0]['description'],
                                dicty['weather'][0]['icon']))
        return simple_data


