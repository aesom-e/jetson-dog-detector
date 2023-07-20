# Dog detector

Point a camera, run the program, and be alerted when a dog has been detected

This runs easily on the Jetson Nano board

## How it works

This program uses imagenet with googlenet to scan what's coming in from the camera each frame

If the detection is more than 50% confident it has catagorized the image, it checks if any pre-programmed words associated with dog are in the catagorization

Once a dog is detected, it runs the code specefied in the ondog() function inside settings.py then sends a text or email if told to do so

### How the detection works

```py
inpt = videoSource(args.input, argv=sys.argv)

# Later in the program
img = inpt.Capture()
```
This gets the webcam's stream and captures it as a cudaImage which is easy for the neural network to process

Next, the program uses googlenet to classify the image and test it against the list of words the network might think a dog would be

```py
net = imageNet("googlenet", sys.argv)

# After img is set to inpt.Capture()

classID, confidence = net.Classify(img)
confidence *= 100
# Turns the decimal (ex 0.6) to a percentage (60%)

if confidence > 50:
    label = net.GetClassLabel(classID).lower()
    # Turn the ID into words
    for item in dogs:
        if item in label:
            run(img)
            # Send it off to the processer function
```

### How the emailing works

For text messages, it's easy!

Most carriers have an email that will forward the message recieved to a phone number

For example, with bell, emailing [phone number]@txt.bell.ca sends a message directly to the phone connected to that number

smtplib provides an easy way for python programs to send emails

Here's how it would look with a phone number of 1234567890 and using bell as a carrier
```py
server = smtplib.SMTP_SSL("smtp.gmail.com")
server.login(settings.eml, settings.passwd)
# Logs into gmail

to = settings.phoneNumber + settings.carriers[settings.carrier]
# Resolves as: to = "1234567890@txt.bell.ca"

server.sendmail(settings.eml, to, settings.message)
# Sends your message to the phone number through bell
server.quit()
print("Text sent")
```

Sending an email to another email is essentially the same code, but adding the image captured requires a complete rewrite

```py
server = smtplib.SMTP_SSL("smtp.gmail.com")
server.login(settings.eml, settings.passwd)
# Logs into gmail

msg = MIMEMultipart()
# Create a multipart message with the email.mime.multipart library
msg.attach(MIMEText(settings.message))
# Attach the text to the message

imgmsg = MIMEText("<br><br><img src='cid:image1'>", "html")
msg.attach(imgmsg)
# Attach html code with a pointer to an image to the root message

imsave("img.png", cudaToNumpy(img))
# Because img is a cudaImage, the program uses imsave and cudaToNumpy to save the image to a file

f = open("img.png", "rb")
msgImage = MIMEImage(f.read())
f.close()
# Store the image into msgImage

msgImage.add_header('Content-ID', '<image1>')
# Sets <img src='cid:image1'> from imgmsg to the image

msg.attach(msgImage)
os.remove("img.png")
# Attach the image to the root message and delete the lingering img.png file

msg['From'] = settings.eml
msg['To'] = to
# Set the destination and source

server.sendmail(settings.eml, to, msg.as_string())
# Send the email

server.quit()
print("Email sent")

```

## Prerequisites

On your board, run these commands:

```sh 
cd ~
sudo apt-get update
sudo apt-get install git cmake
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference
git submodule update --init
sudo apt-get install libpython3-dev python3-numpy
mkdir build
cd build
cmake ../
```

Select the default options then once the window has closed run these commands

```sh
make
sudo make install
sudo ldconfig
```

Then install required libraries

```sh
sudo apt-get install python-scipy
pip3 install scipy
```

Then in the directory of the main.py and settings.py run:

```sh
sudo chmod 700 main.py
```

## Running the program

Inside the directory both main.py and settings.py are in, run this command:

```sh
./main.py /dev/video0
```
This runs the program on the first camera plugged in to your board

## Settings

The settings for the program are stored inside settings.py

If you have a carrier which isn't inside the list, add it like this:

Inside the dictionary carriers, add a comma then "[your carrier name]" : "[their email to sms address starting with @]" next to "" : ""

To do anything with messaging though, you first have to setup your email to work with the program

### Setting up an email for use with the program

1. [Go to your gmail of choice's account page](https://myaccount.google.com/)

2. Enable 2 step verification under Security then How you sign in to Google

3. Use the search bar in the top left corner of the page to search for "App passwords"

4. In the app passwords menu, select mail as the app you want to use and set the device to other

5. Pick the name you want to use (This doesn't affect anything within the code) and click generate

6. Copy the password and DON'T LOSE IT

7. Set the variable passwd in settings.py to your app password

8. Set the variable eml in settings.py to the email connected to your app password

[If this doesn't work for you, check this page](https://support.google.com/mail/answer/185833?hl=en)
