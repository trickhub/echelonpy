import csv
import logging
import re
from itertools import chain

TOTAL = r'Stage_'
DISTANCE = r'distance'
TOTAL_END = r'KCal'


class Lap(object):
    def __init__(self, total_distance=None, total_calories=None, tracks=None):
        super(Lap, self).__init__()
        self.total_distance = total_distance
        self.total_calories = total_calories
        self.tracks = tracks

    @property
    def average_hr(self):
        return sum([track.hr for track in self.tracks]) / len(self.tracks)

    @property
    def average_cadence(self):
        return sum([track.cadence for track in self.tracks]) / len(self.tracks)


class Track(object):
    def __init__(self, distance=None, speed=None, power=None, hr=None, cadence=None):
        super(Track, self).__init__()
        self.distance = distance  # miles
        self.speed = speed  # mph
        self.power = power
        self.hr = hr
        self.cadence = cadence

    @classmethod
    def from_row(cls, row):
        r_time, r_distance, r_speed, r_power, r_hr, r_cadence = row

        return cls(distance=float(r_distance),
                   speed=float(r_speed),
                   power=int(r_power),
                   hr=int(r_hr),
                   cadence=int(r_cadence),
                   )


def read(file_path):
    with open(file_path, 'rb') as csv_file:
        rows = csv.reader(csv_file, delimiter=',')
        return [_read_lap(chain([row], rows)) for name, row in _safe_generate(rows) if _is_track_row(name)]


def _read_lap(rows):
    """
    The echelon spits out a dodgy format - a single lap sessions will only spit out Stage_Totals, so we need to cater
    for that.
    """
    logging.debug("parsing lap")
    tracks = []

    for name, row in _safe_generate(rows):
        if re.search(TOTAL, name):
            distance, calories = _read_lap_total(rows)
            logging.info("Parsed lap with {} tracks, Distance: {}, Calories: {}"
                         .format(len(tracks), distance, calories))
            return Lap(total_distance=distance, total_calories=calories, tracks=tracks)

        tracks.append(Track.from_row(row))


def _read_lap_total(rows):
    logging.debug("reading lap total")
    distance = None
    for name, row in _safe_generate(rows):
        if re.search(DISTANCE, name):
            distance = float(row[1])
        elif re.match(TOTAL_END, name):
            calories = float(row[1])
            return distance, calories


def _safe_generate(rows):
    while True:
        row = next(rows)
        name = row[0] if len(row) > 0 else None

        if name is None:
            continue

        logging.debug("in row {}:{}".format(name, row))
        yield name, row


def _is_track_row(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
