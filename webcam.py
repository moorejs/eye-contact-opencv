import numpy as np
import cv2

from mingus.containers import Note, NoteContainer
from mingus.midi import fluidsynth

SF2 = 'Nice-Keys-Giga-JNv1.7.sf2'  # https://sites.google.com/site/soundfonts4u/

if not fluidsynth.init(SF2):
    import sys
    print('Failed to load {}'.format(SF2))
    sys.exit(1)
else:
    print('found')

x_offset = 480
y_offset = 30
height = 720 - 2 * y_offset - 100
width = 1280 - 2 * x_offset

cam = cv2.VideoCapture(0)

detect_timer = 0
DETECT_WAIT = 10

has_user = True  # debug
has_user_counter = 0
has_user_timeout = 0
HAS_USER_WAIT = 50

NOTE_NAMES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
NOTE_COUNT = 7
notes = NoteContainer([Note("A", 4), Note("D", 4), Note("G", 4)])

if cam.isOpened():
    while True:
        ret, frame = cam.read()
        frame = frame[y_offset:y_offset + height, x_offset:x_offset + width]
        if ret:
            print("Has user: ", has_user, has_user_counter,
                  "timeout timer", has_user_timeout)

            detect_timer += 1

            # frame = cv2.cvtColor(cv2.resize(
            #    frame, size), cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = cv2.CascadeClassifier('haarcascade_eye.xml')
            detected = faces.detectMultiScale(frame, 1.3, 5)

            if not len(detected):
                has_user_counter = 0
                has_user_timeout += 1

                if has_user_timeout > HAS_USER_WAIT:
                    has_user = False
                elif has_user and detect_timer > DETECT_WAIT:
                    detect_timer = 0

                    print('========= BLINK =========')

                    fluidsynth.play_NoteContainer(notes)

                    new_notes = NoteContainer()
                    for note in notes:
                        # note.set_note
                        new_note = note.from_int((int(note) + 1) % 12)
                        new_notes.add_note(new_note)
                       # notes.add_note(new_note)
                       # notes.remove_note(note)
                        # note.octave_up()
                    #    # note.set_note()
                    #    note.octave_up()
                    print(new_notes)
                    notes = new_notes
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
