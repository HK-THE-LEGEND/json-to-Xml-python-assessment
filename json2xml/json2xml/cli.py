import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
import argparse


def create_typed_element(json_key, value):
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
            elem.append(handle_value(item))
    else:
        elem = ET.Element("string", name=json_key)
        elem.text = str(value)
    return elem


def handle_value(value):
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
    root = ET.Element("object")
    for k, v in json_obj.items():
        root.append(create_typed_element(k, v))
    return ET.tostring(root, encoding="unicode")


def pretty_print_xml(xml_str):
    dom = xml.dom.minidom.parseString(xml_str)
    return dom.toprettyxml(indent="  ")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a JSON file to typed XML."
    )
    parser.add_argument("input", nargs="?", help="Path to input JSON file")
    parser.add_argument("output", nargs="?", help="Path to output XML file")

    args = parser.parse_args()

    if not args.input or not args.output:
        parser.print_usage()
        return

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)

        raw_xml = json_to_custom_xml(data)
        pretty_xml = pretty_print_xml(raw_xml)

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

        print(f"✅ XML written to {args.output}")

    except FileNotFoundError:
        print(f"❌ Input file not found: {args.input}")
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON format in: {args.input}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")



if __name__ == "__main__":
    main()
