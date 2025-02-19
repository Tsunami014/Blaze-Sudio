import pygame
import numpy as np
pygame.mixer.init()

def beep(frequency: int = 500, duration: int = 100):
    """
    Play a beep/tone.

    Args:
        frequency (int): Frequency of the beep in Hertz. Frequencies below 100 are treated as 100.
        duration (int): Duration of the beep in milliseconds. If the duration is less than 0, then the method returns immediately, and the frequency play continues to play indefinitely.
    """
    # Thanks https://stackoverflow.com/questions/7816294/simple-pygame-audio-at-a-frequency for the idea and https://stackoverflow.com/questions/48043004/how-do-i-generate-a-sine-wave-using-python
    # Set some vars
    volume = 1
    forever = duration < 0

    sample_rate = 44100
    n_samples = lambda time: int(round(time*sample_rate))
    duration = n_samples(duration / 1000)
    
    fade_in = n_samples(0.01)
    fade_out = n_samples(0.02)
    
    #kernel = 0.5**np.arange(5)

    samples = np.arange(duration) / sample_rate
    left_signal = np.sin(2 * np.pi * (frequency-50) * samples)
    left_signal *= 32767
    #left_signal[-fade_out:] = np.convolve(left_signal[-fade_out:], kernel, mode='full')[:len(left_signal[-fade_out:])]
    
    right_signal = np.sin(2 * np.pi * (frequency+50) * samples)
    right_signal *= 32767
    
    buf = np.array(tuple(zip(left_signal, right_signal)))
    buf = np.int16(buf)
    if not forever:
        buf[:fade_in] = [buf[i]*(i / fade_in) for i in range(len(buf[:fade_in]))]
        buf[-fade_out:] = [buf[fade_out+i]*((duration-i) / duration) for i in range(len(buf[-fade_out:]))]

        sound = pygame.sndarray.make_sound(buf)
        sound.set_volume(volume)
        chan = sound.play()
        # self.busy = True
        while chan.get_busy():
            pass
        # self.busy = False
    else:
        sound1 = pygame.sndarray.make_sound(buf)
        sound1.set_volume(volume)
        buf[:fade_in] = [buf[i]*(i / fade_in) for i in range(len(buf[:fade_in]))]
        sound2 = pygame.sndarray.make_sound(buf)
        sound2.set_volume(volume)
        chan = sound2.play()
        # self.busy = True
        while chan.get_busy():
            pass
        # self.busy = False
        sound1.play(-1)
