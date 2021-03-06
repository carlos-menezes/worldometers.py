from bs4 import BeautifulSoup
from urllib.request import urlopen


class Worldometers():
    url = 'https://countrymeters.info/en/World'
    # html = requests.get(url).text
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    # World Population
    def current_world_population(self, option='total'):
        """
        Parses through the HTML page to gather information about the current world population.

        :param option: Choose between three types of return values. 'total', the default value for this parameter, returns the total world population. 'male' and 'female' returns the current population for each gender.
        :return: Integer with the current population.
        """
        if option.lower() == 'total':
            return int(Worldometers.soup.find(id='cp1').getText().replace(',', ''))
        
        elif option.lower() == 'male':
            return int(Worldometers.soup.find(id='cp2').getText().replace(',', ''))
        
        elif option.lower() == 'female':
            return int(Worldometers.soup.find(id='cp3').getText().replace(',', ''))

    def population_growth(self, timescale):
        """
        Parses through the HTML page to gather information about the population growth based on the chosen timescale.

        :param timescale: Choose between two types — 'day' or 'year' — that will return results accordingly. 
        :return: Integer with the population growth based on the chosen timescale.
        """

        if timescale.lower() == 'day':
            return int(Worldometers.soup.find(id='cp13').getText().replace(',', ''))
        
        elif timescale.lower() == 'year':
            return int(Worldometers.soup.find(id='cp12').getText().replace(',', ''))

    def population_history(self):
        """
        Parses through the HTML page to gather information about the population history.

        :return: Dictionary with the population history in the format {'year': value, 'population': value, 'growth': value}.
        """
        population_history = Worldometers.soup.find_all(class_='years')[0]
        year_rows = population_history.find_all('tr')

        population_history_dict = {}
        for x in range(1, len(year_rows)):
            columns = year_rows[x].find_all('td')
            population_history_dict[x-1] = {
                'year': columns[0].getText().replace(',', ''),
                'population': columns[1].getText().replace(',', ''),
                'growth': columns[2].getText().replace(' %', '')
            }

        return population_history_dict

    def population_projection(self):
        """
        Parses through the HTML page to gather information about the population projection.

        :return: Dictionary with the population growth in the format {'year': value, 'population': value, 'growth': value}.
        """
        population_projection = Worldometers.soup.find_all(class_='years')[1]
        year_rows = population_projection.find_all('tr')

        population_projection_dict = {}
        for x in range(1, len(year_rows)):
            columns = year_rows[x].find_all('td')
            population_projection_dict[x-1] = {
                'year': columns[0].getText().replace(',', ''),
                'population': columns[1].getText().replace(',', ''),
                'growth': columns[2].getText().replace(' %', '')
            }

        return population_projection_dict

    # Births
    def births(self, timescale):
        """
        Parses through the HTML page to gather information about births.

        :param timescale: Choose between two types — 'day' or 'year' — that will return results accordingly.
        :return: Integer with the number of births.
        """
        if timescale.lower() == 'year':
            return int(Worldometers.soup.find(id='cp6').getText().replace(',', ''))

        if timescale.lower() == 'day':
            return int(Worldometers.soup.find(id='cp7').getText().replace(',', ''))

    # Deaths
    def deaths(self, timescale):
        """
        Parses through the HTML page to gather information about deaths based on the chosen timescale..

        :param timescale: Choose between two types — 'day' or 'year' — that will return results accordingly.
        :return: Integer with the number of deaths.
        """
        if timescale.lower() == 'year':
            return int(Worldometers.soup.find(id='cp8').getText().replace(',', ''))

        if timescale.lower() == 'day':
            return int(Worldometers.soup.find(id='cp9').getText().replace(',', ''))

    def top_death_causes(self, timescale):
        """
        Parses through the HTML page to gather information about top death causes based on the chosen timescale.

        :param timescale: Choose between two types — 'day' or 'year' — that will return results accordingly.
        :return: Integer with the number of deaths.
        """

        top_deaths = Worldometers.soup.find('div', class_='death_top')
        top_deaths = top_deaths.text.replace(" %", "").splitlines()[4:-4]
        top_deaths = list(filter(None, top_deaths))
        while 'Connecting . . .' in top_deaths: top_deaths.remove('Connecting . . .')

        deaths = self.deaths(timescale=timescale)

        deaths_in_timescale = []

        for element in top_deaths[1::2]:
            deaths_in_timescale.append(int(float(element)*(deaths/100)))

        top_deaths_causes_timescale = dict(zip(top_deaths[0::2], deaths_in_timescale))

        return top_deaths_causes_timescale
