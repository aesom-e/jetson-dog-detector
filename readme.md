# Dog detector

Point a camera, run the program, and be alerted when a dog has been detected

This runs easily on the Jetson Nano board

## How it works

This program uses imagenet with googlenet to scan what's coming in from the camera each frame

If the detection is more than 50% confident it has catagorized the image, it checks if any pre-programmed words associated with dog are in the catagorization

Once a dog is detected it runs the code specefied in the onrun() function inside settings.py then sends a text or email if told to do so


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

The settings inside should be self explanitory

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
