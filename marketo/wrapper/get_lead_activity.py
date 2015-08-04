
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
    t = response.text
    print t
    root = ET.fromstring(t)
    activities = []
    for activity_el in root.findall('.//activityRecord'):
        activity = lead_activity.unwrap(activity_el)
        activities.append(activity)
    return activities
