import pyproj
import xml.etree.ElementTree as ET
import ezdxf

def read_coordinates(file_path):
    if file_path.lower().endswith('.dxf'):
        return read_coordinates_dxf(file_path)
    elif file_path.lower().endswith('.txt'):
        return read_coordinates_txt(file_path)
    else:
        print("Nieobsługiwany format pliku.")
        return []

def read_coordinates_dxf(file_path):
    points = []
    lines = []
    doc = ezdxf.readfile(file_path)
    for entity in doc.modelspace():
        if entity.dxftype() == 'POINT':
            x, y, _ = entity.dxf.location
            points.append((str(len(points) + 1), x, y))
        elif entity.dxftype() == 'LINE':
            start_point = entity.dxf.start
            end_point = entity.dxf.end
            lines.append(((start_point[0], start_point[1]), (end_point[0], end_point[1])))
    return points, lines

def read_coordinates_txt(file_path):
    with open(file_path) as stream:
        content = stream.read()
        cleaned_lines = [line.split() for line in content.split('\n')]
    return [(str(line[0]), float(line[1]), float(line[2])) for line in cleaned_lines if len(line) > 2]

def convert_coordinates(points):
    transformer = pyproj.Transformer.from_crs("EPSG:2178", "EPSG:4326", always_xy=True)
    lat_lon_list = []
    for nr, xi, yi in points:
        if yi < 0:
            yi = abs(yi)
        lat, lon = transformer.transform(yi, xi)
        lat_lon_list.append((nr, lat, lon))
    return lat_lon_list

def convert_to_gpx(lat_lon_list, lines):
    gpx = ET.Element(
        "gpx", 
        attrib={
            "version": "1.1", 
            "xmlns": "http://www.topografix.com/GPX/1/1", 
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance", 
            "xsi:schemaLocation": "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"
        }
    )

    for line in lines:
        trk = ET.SubElement(gpx, "trk")
        trkseg = ET.SubElement(trk, "trkseg")
        for segment in line:
            start = segment[0]
            trkpt_start = ET.SubElement(trkseg, "trkpt", lat=str(lat_lon_list[int(start)][1]), lon=str(lat_lon_list[int(start)][2]))
            ET.SubElement(trkpt_start, "name").text = "Line Segment"

    return ET.ElementTree(gpx)



def save_to_gpx(gpx_tree, file_path):
    gpx_tree.write(file_path, encoding='utf-8', xml_declaration=True)
    print(f"Dane zapisane do pliku GPX: {file_path}")

def main():
    FILES_PATTERN = 'D:/ROBOTA/python/gpx/dw513_pp_kreski2.dxf'
    gpx_filename = 'D:/ROBOTA/python/gpx/poprzeczki.gpx'

    points, lines = read_coordinates(FILES_PATTERN)

    lat_lon_list = convert_coordinates(points)
    gpx_tree = convert_to_gpx(lat_lon_list, lines)
    save_to_gpx(gpx_tree, gpx_filename)

if __name__ == "__main__":
    main()
