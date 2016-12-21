eye-contact-opencv

Made to detect blinking and play piano sounds on blink. Uses the Python bindings for OpenCV and FluidSynth.

This was hacked together very quickly for an art project. See http://ideate.xsead.cmu.edu/gallery/projects/eye-contact for more.

Usage

Made for Python 3

`git clone https://github.com/moorejs/eye-contact-opencv.git`

`cd eye-contact-opencv`

`pip install -r requirements.txt`

`python webcam.py`

You're going to need to have installed OpenCV (3 is used here) and FluidSynth. You can use brew to install these.
You'll also need a SoundFont. I use 'Nice-Keys-Giga-JNv1.7.sf2'. Expect to need to modify `webcam.py`.
