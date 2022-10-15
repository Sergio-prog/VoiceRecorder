import pyaudio
import wave
import time
import datetime
import tkinter as tk
import threading

# filename =
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 2
sample_rate = 44100
record_seconds = 100

count = 0
stopped = False

root = tk.Tk()
root.title("Recorder")


def start_pyaduio():
    global p, stream, count, frames
    p = pyaudio.PyAudio()

    data = ''
    frames = []
    count = 0

    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)


def rec():
    global stream, p, frames, count

    start_pyaduio()

    print("Recorder Started")

    label1.config(text="00:00")
    count_plus()

    print("recording")
    for i in range(int(sample_rate / chunk * record_seconds)):
        if stopped == False:
            data = stream.read(chunk)
            frames.append(data)


def Stop():
    global stopped, frames, stream, count
    print("Recorder Stopped")

    stopped = True
    count_stop()

    stream.stop_stream()
    stream.close()

    p.terminate()

    wf = wave.open((datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S") + ".wav"), "wb")

    wf.setnchannels(channels)

    wf.setsampwidth(p.get_sample_size(FORMAT))

    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()


def start():
    global stopped
    stopped = False
    t1 = threading.Thread(target=rec)
    t1.start()


def count_plus():
    global label1, count
    if count != -1:
        root.after(1000, count_plus)

        cou = datetime.time(second=int(count)).strftime("%M:%S")

        print(count, cou)
        label1.config(text=str(cou))
        count += 1


def count_stop():
    global count
    count = -1


label = tk.Label(root, text="Python Voice Recorder").place(relx=0.5, rely=0.1, anchor=tk.CENTER)

button = tk.Button(root, text="Start", command=start, width=10, height=2, bg="LimeGreen").place(relx=0.5, rely=0.4,
                                                                                                anchor=tk.CENTER)

label1 = tk.Label(root, text="00:00")
label1.place(relx=0.5, rely=0.553, anchor=tk.CENTER)

button2 = tk.Button(root, text="Stop", command=Stop, width=10, height=2, bg="FireBrick").place(relx=0.5, rely=0.7,
                                                                                               anchor=tk.CENTER)

root.mainloop()
