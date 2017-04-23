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

    etree.SubElement(track_point, 'Time').text = time
    hr_element = etree.SubElement(track_point, 'HeartRateBpm')
    etree.SubElement(hr_element, 'Value').text = str(hr)
    etree.SubElement(track_point, 'DistanceMeters').text = str(distance)
    etree.SubElement(track_point, 'Cadence').text = str(cadence)

    extensions_element = etree.SubElement(track_point, 'Extensions')
    tpx_element = etree.SubElement(extensions_element, 'TPX', xmlns=TPXNS)
    etree.SubElement(tpx_element, 'Speed').text = str(speed)
    etree.SubElement(tpx_element, 'Watts').text = str(power)


def add_lap(activity_element, lap, time):

    etree.SubElement(activity_element, 'Id').text = time.strftime(TCX_TIME_FORMAT)
    lap_element = etree.SubElement(activity_element, 'Lap', StartTime=time.strftime(TCX_TIME_FORMAT))
    etree.SubElement(lap_element, 'TotalTimeSeconds').text = str(len(lap.tracks) * 6)
    etree.SubElement(lap_element, 'DistanceMeters').text = str(lap.total_distance)
    etree.SubElement(lap_element, 'Calories').text = str(lap.total_calories)
    etree.SubElement(lap_element, 'AverageHeartRateBpm').text = str(lap.average_hr)
    etree.SubElement(lap_element, 'Cadence').text = str(lap.average_cadence)
    track_element = etree.SubElement(lap_element, 'Track')

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
    activities_element = etree.SubElement(page, 'Activities')
    activity_element = etree.SubElement(activities_element, 'Activity', Sport="Biking")

    for lap in laps:
        time = add_lap(activity_element, lap, time)

    return doc


def _to_meters_per_second(value):
    return _to_seconds(_to_meters(value))


def _to_seconds(value):
    return value / 60 / 60


def _to_meters(value):
    return value / 0.00062137
