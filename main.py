import json
import os
from collections import deque
from datetime import datetime, timedelta
from time import sleep
import argparse

from detector import BannerDetector
from stream_capture import StreamCapture

banner_detector = BannerDetector()


class Stream:
	def __init__(self, url):
		self._url = url
		self._nickname = url.rsplit('/')[-1]
		self._stream_capture = StreamCapture(url)
		self.key_frames = []
		self._missing_frames_count = 0

	def _update_stream_capture(self):
		self._missing_frames_count += 1
		if self._missing_frames_count > 1000:
			self._stream_capture = StreamCapture(self._url)
			self._missing_frames_count = 0

	@property
	def is_online(self):
		if not self.key_frames:
			frame = self._stream_capture.read()
			return frame is not None
		return bool(self.key_frames[-1][1])

	def check_last_frame(self):
		frame = self._stream_capture.read()
		capture_date = datetime.now()
		if frame is None:
			self._update_stream_capture()
			data = {}
		else:
			detections, scores, _ = banner_detector.detect(frame)
			data = {
				'detections': detections,
				'scores': scores
			}
			frame_info = [capture_date, data]
			self.key_frames.append(frame_info)

	def capture_timedelta(self):
		if not self.key_frames:
			return timedelta()
		
		return self.key_frames[-1][0] - self.key_frames[0][0]

	def clear_key_frames(self):
		self.key_frames.clear()

	def jsonify_key_frames(self):
		if not self.key_frames:
			return False

		_from, to = self.key_frames[0][0], self.key_frames[-1][0]
		total_seconds = (to - _from).total_seconds()

		detected_count = sum(bool(k[1].get('detections')) for k in self.key_frames)
		total_detections_count = sum(bool(k[1]) for k in self.key_frames)
		meta = {
			'total_detection_seconds': total_seconds,
			'total_detection_count': total_detections_count,
			'banner_displayed_count': detected_count,
			'banner_displayed': detected_count / (total_detections_count or 1),
			'fps': len(self.key_frames) / total_seconds
		}
		key_frames_json = [[str(k[0]), k[1]] for k in self.key_frames if k[1]]
		result = {
			'meta': meta,
			'key_frames': key_frames_json
		}
		return result

	def dump_key_frames(self, file=None):
		if (not self.key_frames) or (not any(k[1] for k in self.key_frames)):
			return False

		if file is None:
			_from, to = self.key_frames[0][0], self.key_frames[-1][0]
			day = to.strftime('%d-%m-%Y')
			folder = f'./results/{self._nickname}/{day}/'
			os.makedirs(folder, exist_ok=True)
			_time = to.strftime('%H:%M:%S')
			file = folder + f'{_time}.json'
		
		key_frames_info = self.jsonify_key_frames()
		with open(file, 'w') as f:
			json.dump(key_frames_info, f, indent=4)
	
def get_streams():
	with open('streams.txt', 'r') as f:
		streams = f.readlines()
		streams = [s.strip().strip('\n') for s in streams]
	return streams

def update_streams(stream_captures, streams_to_track):
	streams_to_track = set(streams_to_track)
	for s in set(stream_captures.keys()) - streams_to_track:
		del stream_captures[s]
	
	for s in streams_to_track - set(stream_captures.keys()):
		stream_captures[s] = Stream(s)

if __name__ == '__main__':
	streams = {}
	parse = argparse.ArgumentParser()
	parse.add_argument('-p', '--dump-every', default=1, type=int, help='Period of saving results. Measured in minutes')
	args = parse.parse_args()
	watch_period = timedelta(minutes=args.dump_every)
	while True:
		streams_to_track = get_streams()
		update_streams(streams, streams_to_track)

		for stream in streams.values():
			stream.check_last_frame()
			if stream.capture_timedelta() > watch_period:
				stream.dump_key_frames()
				stream.clear_key_frames()
			
		if not any(s.is_online for s in streams.values()):
			sleep(5)


