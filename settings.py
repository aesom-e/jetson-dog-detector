#!/usr/bin/env python

# Send a message outside the program
sendmessage = True

#Email to send the messages from (Must be gmail)
eml = "example@gmail.com"

# With google an account needs an application specific password or it will raise an error
passwd = ""

# If True the program will send a text to your phone number, if False it will send an email to the adress specified in the variable "to"
usetext = True

# If usetext is False then send to this email
to = "example@gmail.com"

# If usetext is True then send to this number
phoneNumber = ""

# Carriers supported: bell, rogers, at&t, t-mobile, sprint, verizon, virgin
carrier = ""

# List of known carriers 
carriers = {"bell" : "@txt.bell.ca", "rogers" : "@pcs.rogers.com", "at&t" : "@txt.att.net", "t-mobile" : "tmomail.net", "sprint" : "@messaging.sprintpcs.com", \
			"verizon" : "@vtext.com", "virgin" : "@vmobl.com", "" : ""}

# Time to wait before the program can send another text (seconds)
timeoutSeconds = 20

# Message to send
message = "Dog's waiting"

# Include the image of the dog (Only works if usetext is False)
includeimage = True

# Customizable code to run when a dog has been detected
def ondog():
	pass
