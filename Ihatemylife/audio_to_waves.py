import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# wav_obj = wave.open('sample-3s.wav', 'rb')


def audio_to_waves(wav_obj, is_l_channel):
    sample_freq = wav_obj.getframerate()
    n_samples = wav_obj.getnframes()
    t_audio = n_samples/sample_freq
    n_channels = wav_obj.getnchannels()
    signal_wave = wav_obj.readframes(n_samples)

    signal_array = np.frombuffer(signal_wave, dtype=np.int16)
    times = np.linspace(0, n_samples/sample_freq, num=n_samples)[:(n_samples)//5]

    if is_l_channel:
        channel = signal_array[0::2][:n_samples//5] #выбираем только одну пятую от всего аудиофайла
        title = 'Left Channel'
    else:
        channel = signal_array[1::2][:(n_samples)//5]
        title = 'Right Channel'

    fig, ax = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(15)
    line2 = ax.plot(times, channel)[0]
    ax.set(xlabel='Время [s]', ylabel='Значение сигнала', title=title)

    def update(frame):
        x = times[:100*frame] #для скорости воспроизведения ставим :100*frame
        y = channel[:100*frame]
        line2.set_xdata(x)
        line2.set_ydata(y)
        return line2
    ani = animation.FuncAnimation(fig=fig, func=update, interval=0.005)
    plt.show()

if __name__ == '__main__':
    for i in range(1, 4):
        wav_obj = wave.open(f'sample-{3*i}s.wav', 'rb')
        audio_to_waves(wav_obj, False)