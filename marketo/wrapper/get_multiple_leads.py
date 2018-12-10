
import xml.etree.ElementTree as ET
import lead_record


def wrap(lead_selector="LastUpdateAtSelector", oldest_updated_at=None,
         latest_updated_at=None, batch_size=100, steam_position=False):
    if lead_selector == "LastUpdateAtSelector":
        return  ('<ns1:paramsGetMultipleLeads>' +
                    '<leadSelector xsi:type="ns1:LastUpdateAtSelector">' +
                        '<oldestUpdatedAt>' + oldest_updated_at.strftime('%Y-%m-%dT%H:%M:%SZ') + '</oldestUpdatedAt>' +
                        '<latestUpdatedAt>' + latest_updated_at.strftime('%Y-%m-%dT%H:%M:%SZ') + '</latestUpdatedAt>' +
                    '</leadSelector>' +
                    '<batchSize>' + str(batch_size) + '</batchSize>' +
                    '' if not steam_position else '<streamPosition>{}</streamPosition>'.format(steam_position) +
                    '</ns1:paramsGetMultipleLeads>')
    else:
        raise NotImplementedError("Only LastUpdateAtSelector lead selector is currently supported")


def unwrap(response):
    root = ET.fromstring(response.text.encode("utf-8"))
    new_position = root.find('.//newStreamPosition').text
    lead_records_xml = root.findall('.//leadRecord')
    return new_position, [lead_record.unwrap(lead_record_xml) for lead_record_xml in lead_records_xml]
