import json
import xml.etree.ElementTree as ET
import sys

def create_typed_element(json_key, value):
    """
    Create an XML element with a tag based on the JSON value's type.
    If it's a key-value pair, the key becomes a `name` attribute.
    """
    if value is None:
        elem = ET.Element("null", name=json_key)
    elif isinstance(value, bool):
        elem = ET.Element("boolean", name=json_key)
        elem.text = "true" if value else "false"
    elif isinstance(value, int) or isinstance(value, float):
        elem = ET.Element("number", name=json_key)
        elem.text = str(value)
    elif isinstance(value, str):
        elem = ET.Element("string", name=json_key)
        elem.text = value
    elif isinstance(value, dict):
        elem = ET.Element("object", name=json_key)
        for k, v in value.items():
            child = create_typed_element(k, v)
            elem.append(child)
    elif isinstance(value, list):
        elem = ET.Element("array", name=json_key)
        for item in value:
            elem.append(handle_value(item))  # no key, just value
    else:
        elem = ET.Element("string", name=json_key)
        elem.text = str(value)
    return elem

def handle_value(value):
    """
    Handles unnamed values inside arrays (no 'name' attribute).
    """
    if value is None:
        return ET.Element("null")
    elif isinstance(value, bool):
        elem = ET.Element("boolean")
        elem.text = "true" if value else "false"
    elif isinstance(value, int) or isinstance(value, float):
        elem = ET.Element("number")
        elem.text = str(value)
    elif isinstance(value, str):
        elem = ET.Element("string")
        elem.text = value
    elif isinstance(value, dict):
        elem = ET.Element("object")
        for k, v in value.items():
            child = create_typed_element(k, v)
            elem.append(child)
    elif isinstance(value, list):
        elem = ET.Element("array")
        for item in value:
            elem.append(handle_value(item))
    else:
        elem = ET.Element("string")
        elem.text = str(value)
    return elem

def json_to_custom_xml(json_obj):
    """
    Converts the JSON root object to XML, wrapping everything inside <object>.
    """
    root = ET.Element("object")
    for k, v in json_obj.items():
        root.append(create_typed_element(k, v))
    return ET.tostring(root, encoding="unicode")

def pretty_print_xml(xml_str):
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(xml_str)
    return dom.toprettyxml(indent="  ")

def main():
    if len(sys.argv) != 3:
        print("Usage: python json_to_xml.py input.json output.xml")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        raw_xml = json_to_custom_xml(data)
        pretty_xml = pretty_print_xml(raw_xml)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

        print(f"✅ XML written to {output_file}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
