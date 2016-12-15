import Queue

import numpy as np
import cv2

from mingus.containers import Note, NoteContainer
from mingus.midi import fluidsynth

SF2 = 'Nice-Keys-Giga-JNv1.7.sf2'  # https://sites.google.com/site/soundfonts4u/

if not fluidsynth.init(SF2):
    import sys
    print('Failed to load {}'.format(SF2))
    sys.exit(1)

print('FluidSynth initialized')

TARGET_WIDTH = 1280
TARGET_HEIGHT = 720

x_offset = int(0.4 * TARGET_WIDTH)
y_offset = int(0.3 * TARGET_HEIGHT)
height = TARGET_HEIGHT - 2 * y_offset - 60  # remove torso
width = TARGET_WIDTH - 2 * x_offset

cam = cv2.VideoCapture(0)

detect_timer = 0
DETECT_WAIT = 9

has_user = False
has_user_counter = 0
has_user_timeout = 0
HAS_USER_WAIT = 50

BASE_OCTAVE = 5
base_note = int(Note('C', BASE_OCTAVE))
notes = NoteContainer()

NOTE_COUNT = 6
NOTE_SPACING = 3
for offset in range(0, NOTE_SPACING * NOTE_COUNT, NOTE_SPACING):
    note = Note().from_int(base_note + offset)
    note.next_octave = offset >= 12
    notes += note

eyes = cv2.CascadeClassifier('haarcascade_eye.xml')

if cam.isOpened():
    while True:
        ret, frame = cam.read()
        frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))
        frame = frame[y_offset:y_offset + height, x_offset:x_offset + width]
        if ret:
            print("Has user: ", has_user, has_user_counter,
                  "timeout timer", has_user_timeout)

            detect_timer += 1

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            detected = eyes.detectMultiScale(frame, 1.3, 5)  # 1.3, 5

            if not len(detected):
                has_user_counter = 0
                has_user_timeout += 1

                if has_user_timeout > HAS_USER_WAIT:
                    has_user = False
                elif has_user and detect_timer > DETECT_WAIT:
                    detect_timer = 0

                    print('========= BLINK =========')

                    fluidsynth.play_NoteContainer(notes)

                    for note in notes:
                        print(note, int(note), note.next_octave,
                              (BASE_OCTAVE + note.next_octave) * 12)
                        new_note = (int(note) + 1) % 12
                        if new_note == 0:
                            note.next_octave = not note.next_octave
                        note = note.from_int(
                            (BASE_OCTAVE + note.next_octave) * 12 + new_note)

            else:
                has_user_counter += 1
                has_user_timeout = 0
                if not has_user and has_user_counter > HAS_USER_WAIT:
                    has_user = True
                    octave = 0

            cv2.namedWindow('Cam View', cv2.WINDOW_NORMAL)
            cv2.imshow('Cam View', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cam.release()

cv2.destroyAllWindows()
