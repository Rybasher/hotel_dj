import xml.etree.ElementTree as ET
from hotel.settings import WSDL_CONFIG
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport


def session_auth():
    breakpoint()

    session = Session()
    session.auth = HTTPBasicAuth(WSDL_CONFIG["user"], WSDL_CONFIG["password"])
    client = Client(WSDL_CONFIG["url"], transport=Transport(session=session))
    service = client.service
    return client


def parseElements(elements):
    all_elements = {}
    for name, element in elements:
        all_elements[name] = {}
        all_elements[name]['optional'] = element.is_optional
        if hasattr(element.type, 'elements'):
            all_elements[name]['type'] = parseElements(
                element.type.elements)
        else:
            all_elements[name]['type'] = str(element.type)
    print(all_elements)
    return all_elements

def interface():
    interface = {}
    for service in session_auth().wsdl.services.values():
        interface[service.name] = {}
        for port in service.ports.values():
            interface[service.name][port.name] = {}
            operations = {}
            breakpoint()
            for operation in port.binding._operations.values():
                operations[operation.name] = {}
                operations[operation.name]['input'] = {}
                elements = operation.input.body.type.elements
                operations[operation.name]['input'] = parseElements(elements)
            interface[service.name][port.name]['operations'] = operations

    # print(interface)

def parseElements(elements):
    all_elements = {}
    for name, element in elements:
        all_elements[name] = {}
        all_elements[name]['optional'] = element.is_optional
        if hasattr(element.type, 'elements'):
            all_elements[name]['type'] = parseElements(
                element.type.elements)
        else:
            all_elements[name]['type'] = str(element.type)

    return all_elements


def xml_to_dict(xml_data):
    root = ET.fromstring(xml_data)
    result = []
    for hotel_xml in root:
        for category_xml in hotel_xml:
            result_item = {
                "attributes": {
                    "id": category_xml.attrib['id'],
                    "name": category_xml.attrib['name']
                },
                "hotelAttributes": {
                    "id": hotel_xml.attrib['id'],
                    "name": hotel_xml.attrib['name'],
                    "eci": hotel_xml.attrib['eci'],
                    "lco": hotel_xml.attrib['lco'],
                    "checkin": hotel_xml.attrib['ckeckin'],
                    "checkout": hotel_xml.attrib['checkout'],
                    "address": hotel_xml.attrib['Adres']
                },
                "room": [],
                "tarif": []
            }
            for category_item_xml in category_xml:
                if category_item_xml.tag == 'tarif':
                    tarif = {
                        "attributes": {
                            "id": category_item_xml.attrib['id'],
                            "name": category_item_xml.attrib['name'],
                            "name_eng": category_item_xml.attrib['nameENG'],
                            "address": category_item_xml.attrib['Adres'],
                            "description": category_item_xml.attrib['description'],
                            "eciprice": category_item_xml.attrib['eciprice'],
                            "lcoprice": category_item_xml.attrib['lcoprice']
                        },
                        "price": {
                            "attributes": {
                                "add_guest": category_item_xml[0].attrib["KvoDop"],
                                "bkf_price": category_item_xml[0].attrib["bkfprice"],
                                "arrival_date": category_item_xml[0].attrib["dateN"],
                                "departure_date": category_item_xml[0].attrib["dateK"],
                                "room_price": category_item_xml[0].attrib["roomprice"],
                                "twin_price": category_item_xml[0].attrib["twinprice"]
                            }
                        }
                    }
                    result_item["tarif"].append(tarif)
                if category_item_xml.tag == 'room':
                    room = {
                        "number": category_item_xml.attrib['num'],
                        "guests": category_item_xml.attrib['guests'],
                        "add_guests": category_item_xml.attrib['addguests'],
                        "twin": True if category_item_xml.attrib['twin'] == 'true' else False,
                        "bathroom": category_item_xml.attrib['bathroom'],
                        "level": category_item_xml.attrib['level'],
                        "category_id": category_xml.attrib['id'],
                        "hotel_id": hotel_xml.attrib['id'],
                        "option": ""
                    }
                    for option in category_item_xml:
                        room["option"] = option.text if hasattr(option, 'text') else ""
                    result_item["room"].append(room)
            result.append(result_item)
    return result


def xml_to_json_recursion(_xml):
    _tmp = {
        "attributes": _xml.attrib
    }
    for elem in _xml:
        if elem.tag not in _tmp:
            _tmp[elem.tag] = []
        _tmp[elem.tag].append(xml_to_json_recursion(elem))
    return _tmp

if __name__ == "__main__":
    interface()
