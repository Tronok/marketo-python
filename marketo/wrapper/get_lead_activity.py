
import xml.etree.ElementTree as ET
import lead_activity
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


def wrap(email=None):
    return (
        '<ns1:paramsGetLeadActivity>' +
            '<leadKey>' +
                '<keyType>EMAIL</keyType>' +
                '<keyValue>' + email + '</keyValue>' +
            '</leadKey>' +
        '</ns1:paramsGetLeadActivity>')


def unwrap(response):
    root = ET.fromstring(response.text.encode("utf-8"))
    activities = []
    for activity_el in root.findall('.//activityRecord'):
        activity = lead_activity.unwrap(activity_el)
        activities.append(activity)
    return activities
