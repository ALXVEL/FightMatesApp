import bs4 as bs
import urllib.request

current_previous_sauce = urllib.request.urlopen('http://ufcstats.com/statistics/events/completed').read()
current_previous_soup = bs.BeautifulSoup(current_previous_sauce, 'lxml')

class events:

    def __init__(self):
        self.previous_events = []
        self.upcoming_events = []
        self.current_event = 0

    def get_current_event(self):
        first_event = current_previous_soup.find('a', class_='b-link b-link_style_white')
        first_event_url = first_event.getText().replace('\n', '').replace('            ', ' ').strip()
        first_event_date = current_previous_soup.find('span', class_='b-statistics__date').getText().replace('\n', '').replace('            ', ' ').strip()
        first_event_location = current_previous_soup.find('td', class_='b-statistics__table-col b-statistics__table-col_style_big-top-padding').getText().replace('\n', '').replace('            ', ' ').strip()
        return (first_event_url, first_event_date,first_event_location)

    def get_current_event_fights(self):
        first_event = current_previous_soup.find('a', class_='b-link b-link_style_white')
        first_event_url = first_event.get('href')

        events_sauce = urllib.request.urlopen(first_event_url).read()
        events_soup = bs.BeautifulSoup(events_sauce,'lxml')
        table = events_soup.find('table')

        row_list = table.find_all('tr', class_='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click')  # list of rows in the sauce
        td_list = row_list[1].find('td', class_='b-fight-details__table-col l-page_align_left')
        td_list_a = td_list.find_all('a')

        fight_list = []
        for i in range(0, len(row_list)):
            matchup = row_list[i].find_all('a', class_='b-link b-link_style_black')
            fighter_1 = matchup[0].getText().strip()
            fighter_2 = matchup[1].getText().strip()
            # date = row_list[i].find('span', class_='b-statistics__date').getText().strip()
            weight = row_list[i].find_all('p', class_='b-fight-details__table-text')[3].getText().strip()
            fight_list.append((fighter_1,fighter_2,weight))

        return fight_list
    def get_previous_events(self):
        tr_list = current_previous_soup.findAll('tr', class_='b-statistics__table-row')
        tr_list.pop(0)
        tr_list.pop(0)

        list_of_upcoming_events = []
        for i in range(0, len(tr_list)):
            if len(list_of_upcoming_events) == 5:
                break
            event_name = tr_list[i].find('a', class_='b-link b-link_style_black').getText().strip()
            date = tr_list[i].find('span', class_='b-statistics__date').getText().strip()
            location = tr_list[i].find('td',
                                       class_='b-statistics__table-col b-statistics__table-col_style_big-top-padding').getText().replace(
                '            ', ' ').strip()

            tuple2 = (event_name, date, location)
            list_of_upcoming_events.append(tuple2)

        for event in list_of_upcoming_events:
            s = '{}\n'.format(event)
            print(s)

    def get_upcoming_events(self):
        upcoming_sauce = urllib.request.urlopen('http://ufcstats.com/statistics/events/upcoming').read()
        upcoming_soup = bs.BeautifulSoup(upcoming_sauce, 'lxml')

        tr_list = upcoming_soup.findAll('tr', class_='b-statistics__table-row')
        tr_list.pop(0)
        tr_list.pop(0)
        tr_list.pop(0)

        upcoming_events_list = []
        for e in range(0, len(tr_list)):
            event_name = tr_list[e].find('a', class_='b-link b-link_style_black').getText().strip()
            date = tr_list[e].find('span', class_='b-statistics__date').getText().strip()
            location = tr_list[e].find('td',
                                       class_='b-statistics__table-col b-statistics__table-col_style_big-top-padding').getText().strip()
            tuple3 = (event_name, date, location)
            upcoming_events_list.append(tuple3)

        return upcoming_events_list

# events.get_previous_events(None)
# events.get_upcoming_events(None)
print(events.get_current_event(None))
print(events.get_current_event_fights(None))