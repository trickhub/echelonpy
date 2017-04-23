from datetime import timedelta, datetime
from lxml import etree

NSMAP = {
    None: 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
    'ax2': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'
}
TPXNS = 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'
TCX_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def add_track(track_element, time, hr, cadence, speed, distance, power):
    track_point = etree.SubElement(track_element, 'Trackpoint')
    _sub_element(track_point, 'Time', time)

    hr_el = _sub_element(track_point, 'HeartRateBpm')
    _sub_element(hr_el, 'Value', hr)

    _sub_element(track_point, 'DistanceMeters', distance)
    _sub_element(track_point, 'Cadence', cadence)

    extensions_el = _sub_element(track_point, 'Extensions')
    tpx_element = _sub_element(extensions_el, 'TPX', xmlns=TPXNS)
    _sub_element(tpx_element, 'Speed', speed)
    _sub_element(tpx_element, 'Watts', power)


def add_lap(activity_element, lap, time):
    _sub_element(activity_element, 'Id', time.strftime(TCX_TIME_FORMAT))

    lap_el = _sub_element(activity_element, 'Lap', StartTime=time.strftime(TCX_TIME_FORMAT))
    _sub_element(lap_el, 'TotalTimeSeconds', len(lap.tracks) * 6)
    _sub_element(lap_el, 'DistanceMeters', lap.total_distance)
    _sub_element(lap_el, 'Calories', lap.total_calories)
    _sub_element(lap_el, 'AverageHeartRateBpm', lap.average_hr)
    _sub_element(lap_el, 'Cadence', lap.average_cadence)

    track_element = _sub_element(lap_el, 'Track')
    for track in lap.tracks:
        time = time + timedelta(seconds=6)
        add_track(track_element,
                  time=time.strftime(TCX_TIME_FORMAT),
                  hr=track.hr,
                  cadence=track.cadence,
                  speed=_to_meters_per_second(track.speed),
                  distance=_to_meters(track.distance),
                  power=track.power,
                  )
    return time


def from_laps(laps):
    time = datetime.now()

    page = etree.Element('TrainingCenterDatabase', nsmap=NSMAP)
    doc = etree.ElementTree(page)
    activities_el = _sub_element(page, 'Activities')
    activity_el = _sub_element(activities_el, 'Activity', Sport="Biking")

    for lap in laps:
        time = add_lap(activity_el, lap, time)

    return doc


def _sub_element(el, name, value=None, **kwargs):
    sub_el = etree.SubElement(el, name, **kwargs)
    if value is not None:
        sub_el.text = str(value)
    return sub_el


def _to_meters_per_second(value):
    return _to_seconds(_to_meters(value))


def _to_seconds(value):
    return value / 3600


def _to_meters(value):
    return value / 0.00062137
