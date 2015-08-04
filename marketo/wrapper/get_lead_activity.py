
import xml.etree.ElementTree as ET
import lead_activity


def wrap(email=None):
    return (
        '<ns1:paramsGetLeadActivity>' +
            '<leadKey>' +
                '<keyType>EMAIL</keyType>' +
                '<keyValue>' + email + '</keyValue>' +
            '</leadKey>' +
        '</ns1:paramsGetLeadActivity>')


def unwrap(response):
    print response
    root = ET.fromstring(response.decode("utf-8"))
    activities = []
    for activity_el in root.findall('.//activityRecord'):
        activity = lead_activity.unwrap(activity_el)
        activities.append(activity)
    return activities
