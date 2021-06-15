import os
import subprocess
import sys
import urllib3
import xml.etree.ElementTree as ET
http = urllib3.PoolManager()

if len(sys.argv) > 1:
	# TODO: check if begins with http etc
	url_parts = sys.argv[1].split('/')
	base_url = '/'.join(url_parts[0:3])
	# print("base_url " + base_url)
	last = url_parts[len(url_parts) - 1].split('=')
	bbb_id = last[len(last)-1]
	# print("bbb_id " + bbb_id)

	shapes_url = base_url + "/presentation/" + bbb_id + "/shapes.svg"
	# print("shapes_url " + shapes_url)
	r = http.request('GET', shapes_url)
	shapes = r.data.decode('utf-8')
	shapes_xml_root = ET.fromstring(shapes)
	print("wget " + base_url + "/presentation/" + bbb_id + "/video/webcams.webm")
	print("ffmpeg -i webcams.webm -vn -c:a copy audio.ogg")  # read webcams write no video use same audio codec
	print("wget " + base_url + "/presentation/" + bbb_id + "/deskshare/deskshare.webm")
	print("ffmpeg -i deskshare.webm  -c:v libx264 -pix_fmt yuv420p -r 15.000150 deskshare.mp4")
	print("W=`ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=nw=1:nk=1 deskshare.mp4`")
	print("H=`ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=nw=1:nk=1 deskshare.mp4`")
	with open(os.getcwd() + '/parts.txt', 'w') as f:
		for child in shapes_xml_root:
			if 'in' in child.attrib:
				start_str = child.attrib["in"].split(".")[0]
				end_str = child.attrib["out"].split(".")[0]
				href = child.attrib['{http://www.w3.org/1999/xlink}href']
				if "deskshare.png" in href:
					print("ffmpeg -i deskshare.mp4 -c copy -ss " + start_str + " -to " + end_str + " " + child.attrib[
						"id"] + ".mp4")  # read image write using H264 use duration from shapes file, use frame rate from webcam file
					f.writelines(["file '" + child.attrib["id"] + ".mp4'\n"])
				else:
					print("wget " + base_url + "/presentation/" + bbb_id + "/" + href + " -O " + child.attrib["id"] + ".png")
					print("ffmpeg -loop 1 -i " + child.attrib["id"] + ".png -c:v libx264 -t " + str(max(0.01,int(end_str) - int(start_str))) + " -pix_fmt yuv420p -r 15.000150 -vf scale=\"w=$W:h=$H:force_original_aspect_ratio=1,pad=$W:$H:(ow-iw)/2:(oh-ih)/2\" " + child.attrib[
						"id"] + ".mp4")  # read image write using H264 use duration from shapes file, use frame rate from webcam file
					f.writelines(["file '" + child.attrib["id"] + ".mp4'\n"])
	print("ffmpeg -f concat -safe 0 -i " + os.getcwd() + "/parts.txt -c:v libx264 -vf scale=$W:$H -aspect $W:$H slides.mp4")  # read list from file, use same codecs
	print("ffmpeg -i slides.mp4 -i audio.ogg -c copy -strict -2 final.mp4") # read video-only and audio-only, output using same codec
else:
	print("No argument supplied, call with BBB URL")
