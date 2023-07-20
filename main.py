#!/usr/bin/env python

import sys
import argparse
from jetson_inference import imageNet
from jetson_utils import videoSource, cudaToNumpy
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from scipy.misc import imsave
import settings

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

net = imageNet("googlenet", sys.argv)

inpt = videoSource(args.input, argv=sys.argv)

dogs = ["retriever", "cocker" "weimaraner", "terrier", "dog", "basset", "hound", "griffon", "beagle"]

waitto = 0

def saveimage(cudaimage, filename):
	array = cudaToNumpy(cudaimage)
	imsave(filename, array)

def run(img):
	settings.ondog()
	global waitto
	print("Detected dog")
	timestamp = int(round(time.time()))
	if timestamp > waitto:
		waitto = timestamp + settings.timeoutSeconds
		server = smtplib.SMTP_SSL("smtp.gmail.com")
		server.login(settings.eml, settings.passwd)
		if settings.usetext:
			to = settings.phoneNumber + settings.carriers[settings.carrier]
		else:
			to = settings.to
		try:
			if not settings.usetext:
				msg = MIMEMultipart()
				msg.attach(MIMEText(settings.message))
				if settings.includeimage:
					imgmsg = MIMEText("<br><br><img src='cid:image1'>", "html")
					msg.attach(imgmsg)
					saveimage(img, "img.png")
					f = open("img.png", "rb")
					msgImage = MIMEImage(f.read())
					f.close()
					msgImage.add_header('Content-ID', '<image1>')
					msg.attach(msgImage)
					os.remove("img.png")
				msg['From'] = settings.eml
				msg['To'] = to
				server.sendmail(settings.eml, to, msg.as_string())
				server.quit()
				print("Email sent")
			else:
				server.sendmail(settings.eml, to, settings.message)
				server.quit()
				print("Text sent")
		except Exception as error:
			print("ERROR: {}".format(error))

while True:
	img = inpt.Capture()
	if img is None:
		continue
	classID, confidence = net.Classify(img)
	confidence *= 100
	if confidence > 50:
		label = net.GetClassLabel(classID).lower()
		for item in dogs:
			if item in label:
				run(img)
	if not inpt.IsStreaming():
		break
