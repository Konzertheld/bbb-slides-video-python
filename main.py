import os
import sys
import urllib3
import xml.etree.ElementTree as ET
http = urllib3.PoolManager()

if len(sys.argv) > 1:
	# TODO: check if begins with http etc
	url_parts = sys.argv[1].split('/')
	base_url = '/'.join(url_parts[0:3])
	bbb_id = url_parts[len(url_parts) - 1]

	shapes_url = base_url + "/presentation/" + bbb_id + "/shapes.svg"
	r = http.request('GET', shapes_url)
	shapes = r.data.decode('utf-8')
	shapes_xml_root = ET.fromstring(shapes)
	print("wget " + base_url + "/presentation/" + bbb_id + "/video/webcams.webm")
	print("ffmpeg -i webcams.webm -vn -c:a copy audio.ogg")  # read webcams write no video use same audio codec
	with open(os.getcwd() + '/parts.txt', 'w') as f:
		for child in shapes_xml_root:
			start_str = child.attrib["in"].split(".")[0]
			end_str = child.attrib["out"].split(".")[0]
			print("wget " + base_url + "/presentation/" + bbb_id + "/" + child.attrib['{http://www.w3.org/1999/xlink}href'] + " -O " + child.attrib["id"] + ".png")
			print("ffmpeg -loop 1 -i " + child.attrib["id"] + ".png -c:v libx264 -t " + str(int(end_str) - int(start_str)) + " -pix_fmt yuv420p -r 15.000150 " + child.attrib[
				"id"] + ".mp4")  # read image write using H264 use duration from shapes file, use frame rate from webcam file
			f.writelines(["file '" + child.attrib["id"] + ".mp4'\n"])

	print("ffmpeg -f concat -safe 0 -i " + os.getcwd() + "/parts.txt -c copy slides.mp4")  # read list from file, use same codecs
	print("ffmpeg -i slides.mp4 -i audio.ogg -c copy final.mp4") # read video-only and audio-only, output using same codec
else:
	print("No argument supplied, call with BBB URL")
