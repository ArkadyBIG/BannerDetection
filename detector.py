import cv2
import imutils
from utils import nms

def _load_banner(path, width):
	banner = cv2.imread(path)
	banner_gray = cv2.cvtColor(banner, cv2.COLOR_BGR2GRAY)
	banner_gray = imutils.resize(banner_gray, width=width)
	return banner_gray

def _create_hough_detector(template, thresh=60):
	ght = cv2.createGeneralizedHoughBallard()
	ght.setTemplate(template)
	ght.setLevels(360)
	ght.setDp(2)
	ght.setVotesThreshold(thresh)
	return ght

class BannerDetector:
	def __init__(self, baner_path='./banner.jpg', banner_width=70):
		self.banner_template = _load_banner(banner_path, banner_width)
		self._detector = _create_hough_detector(self.banner_template)

	def detect(image, scale_from=0.8, scale_to=1.2, intervals=20)
		boxes = []
		scores = []
		scales = []

		tH, tW = self.banner_template.shape
		iH, iW = image.shape

		_range = np.linspace(scale_from, scale_to, intervals)
		for scale in (_range):
			resized = imutils.resize(frame, width=int(frame.shape[1] * scale))
			# _start = time()
			positions = self._detector.detect(resized)
			# print('Houg:', time() - _start)
			if positions[0] is not None:
				votes = positions[1].reshape(-1, 3)[:, 0]
				scores.extend(votes)
				scales.append(scale)
				center_x = positions[0].reshape(-1, 4)[:, 0]
				center_y = positions[0].reshape(-1, 4)[:, 1]
				
				curboxes = np.array(
					[
						(center_x - tW / 2) / iW, 
						(center_y - tH / 2) / iH,  
						(center_x + tW / 2) / iW, 
						(center_y + tH / 2) / iH
					]
				)
				curboxes = curboxes.transpose((1, 0)) / scale
				boxes.extend(curboxes)

		boxes, scores = nms(boxes, scores)
		return boxes, scores, scales
	



