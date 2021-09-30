import streamlink
import cv2
import imutils

RESOLUTIONS = ('360p', '480p', '720p', '720p60', '1080p60', 'best')

def _create_capture(url):
	streams = streamlink.streams(url)
	for res in RESOLUTIONS:
		if res in streams:
			break
	else:
		return None
	url = streams[res].url
	pipeline = f'souphttpsrc location={url} ! decodebin ! videoconvert ! appsink max-buffers=1 drop=true'
	cap = cv2.VideoCapture(pipeline)
	return cap

class StreamCapture:
	def __init__(self, url, width=640):
		self._width = width
		self._url = url
		self._capture = _create_capture(url)

	def read(self):
		if self._capture is None:
			return None
		ret, frame = self._capture.read()
		if not ret:
			return None
		
		frame = imutils.resize(frame, width=self._width)
		return frame
