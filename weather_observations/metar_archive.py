import datetime
import os
import time
import urllib2

ARCHIVE_PATH = os.environ.get('METAR_ARCHIVE_PATH', None) or os.getcwd()
NOAA_URL = "https://tgftp.nws.noaa.gov/data/observations/metar/cycles/*cycle*Z.TXT"

CYCLES = {
    '00': (datetime.time(23, 45), datetime.time(0, 45)),
    '01': (datetime.time(0, 45), datetime.time(1, 45)),
    '02': (datetime.time(1, 45), datetime.time(2, 45)),
    '03': (datetime.time(2, 45), datetime.time(3, 45)),
    '04': (datetime.time(3, 45), datetime.time(4, 45)),
    '05': (datetime.time(4, 45), datetime.time(5, 45)),
    '06': (datetime.time(5, 45), datetime.time(6, 45)),
    '07': (datetime.time(6, 45), datetime.time(7, 45)),
    '08': (datetime.time(7, 45), datetime.time(8, 45)),
    '09': (datetime.time(8, 45), datetime.time(9, 45)),
    '10': (datetime.time(9, 45), datetime.time(10, 45)),
    '11': (datetime.time(10, 45), datetime.time(11, 45)),
    '12': (datetime.time(11, 45), datetime.time(12, 45)),
    '13': (datetime.time(12, 45), datetime.time(13, 45)),
    '14': (datetime.time(13, 45), datetime.time(14, 45)),
    '15': (datetime.time(14, 45), datetime.time(15, 45)),
    '16': (datetime.time(15, 45), datetime.time(16, 45)),
    '17': (datetime.time(16, 45), datetime.time(17, 45)),
    '18': (datetime.time(17, 45), datetime.time(18, 45)),
    '19': (datetime.time(18, 45), datetime.time(19, 45)),
    '20': (datetime.time(19, 45), datetime.time(20, 45)),
    '21': (datetime.time(20, 45), datetime.time(21, 45)),
    '22': (datetime.time(21, 45), datetime.time(22, 45)),
    '23': (datetime.time(22, 45), datetime.time(23, 45)),
}

def determine_cycle(for_datetime, number_behind=0):
    """
        Look at the current UTC time and determine the current NOAA cycle.
        Cycle info taken from http://weather.noaa.gov/weather/metar.shtml
    """
    current_cycle = None

    lookup = for_datetime - datetime.timedelta(hours=number_behind)
    print('Using %s for lookup.' % lookup)

    for cycle in CYCLES:
        if lookup.time() >= CYCLES[cycle][0] and lookup.time() < CYCLES[cycle][1]:
            current_cycle = cycle
    if not current_cycle: # didn't find it - so it's almost assuredly cycle zero.
        if lookup.time().hour == 0:
            if lookup.time().minute >= 0 and lookup.time().minute < 45:
                current_cycle = '00'
        if lookup.time().hour == 23:
            if lookup.time().minute >= 45:
                lookup = lookup + datetime.timedelta(days=1) # have to add a day so it names the file right
                current_cycle = '00'

    return {'year': lookup.year, 'month': lookup.month, 'day': lookup.day, 'cycle': current_cycle}


def download_cycle(cycle, year, month, day):
    pull_url = NOAA_URL.replace('*cycle*', str(cycle))
    print pull_url
    try:
        request = urllib2.Request(pull_url, None)
        response = urllib2.urlopen(request)

        # make sure the path exists, create where necessary
        if not os.path.exists(ARCHIVE_PATH):
            print("The path you've specified for archives to be stored in (%s) does not exist. Either create it or change the path." % ARCHIVE_PATH)
        else:
            if not os.path.exists(os.path.join(ARCHIVE_PATH, str(year))):
                os.mkdir(os.path.join(ARCHIVE_PATH, str(year)))
            if not os.path.exists(os.path.join(ARCHIVE_PATH, '%s/%s' % (year, month))):
                os.mkdir(os.path.join(ARCHIVE_PATH, '%s/%s' % (year, month)))

        archive_file_path = os.path.join(ARCHIVE_PATH, '%s/%s/%s_%s.txt' % (year, month, day, cycle))
        print archive_file_path
        if not os.path.exists(archive_file_path): # isn't there already
            archive_file = open(archive_file_path, 'w')
            archive_file.write(response.read())
            archive_file.close()
            print('Downloaded.')
        else:
            print('Existed. exiting.')
    except:
        print('HTTP error, going to wait till the next pass')


if __name__ == '__main__':
    utc = datetime.datetime.utcnow()
    print('Currently %s' % utc)

    # figure out the current cycle - then download whatever happened two cycles back.
    # I'm not trying to get real-time data, just accurate data - and they're updating / changing things occasionally according to the file mod times - I've seen up to 4 hours but use 2 personally
    to_download = determine_cycle(utc, number_behind=2)

    print('Download cycle %s' % to_download)

    download_cycle(to_download['cycle'], to_download['year'], to_download['month'], to_download['day'])
