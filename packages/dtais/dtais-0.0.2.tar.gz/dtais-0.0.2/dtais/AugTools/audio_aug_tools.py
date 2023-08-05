import matplotlib.pyplot as plt
import librosa
import os
import soundfile as sf
import numpy as np


def aug_pitch_shift(input_path, output_path, step):
    y, sr = librosa.load(input_path, sr=44100)
    y_shift = librosa.effects.pitch_shift(y, sr, n_steps=step)  # 使用PS生成新数据
    sf.write(output_path, y_shift, sr)


def aug_time_stretch(input_path, output_path, rate):
    y, sr = librosa.load(input_path, sr=44100)
    y_shift = librosa.effects.time_stretch(y, rate=rate)  # 使用TS生成新数据
    sf.write(output_path, y_shift, sr)


# 噪声因子
def add_noise1(input_path, output_path, w):
    y, sr = librosa.load(input_path, sr=44100)
    y_shift = y + w * np.random.normal(loc=0, scale=1, size=len(y))
    sf.write(output_path, y_shift, sr)


def add_noise2(input_path, output_path, snr):
    # snr：生成的语音信噪比
    y, sr = librosa.load(input_path, sr=44100)
    P_signal = np.sum(abs(y) ** 2) / len(y)  # 信号功率
    P_noise = P_signal / 10 ** (snr / 10.0)  # 噪声功率
    y_shift = y + np.random.randn(len(y)) * np.sqrt(P_noise)
    sf.write(output_path, y_shift, sr)


# 高斯分布加噪
def add_noise3(input_path, output_path, id):
    y, sr = librosa.load(input_path, sr=44100)
    wn = np.random.normal(0, 1, len(y))  # 从高斯分布（正态分布）提取样本
    y_shift = np.where(y != 0.0, y.astype('float64') + 0.02 * wn, 0.0).astype(np.float32)
    sf.write(output_path, y_shift, sr)


# 波形位移
def time_shift(input_path, output_path, shift):
    # shift：移动的长度
    y, sr = librosa.load(input_path, sr=44100)
    y_shift = np.roll(y, int(shift))
    sf.write(output_path, y_shift, sr)


def demo_plot(audio):
    y, sr = librosa.load(audio, sr=44100)
    y_ps = librosa.effects.pitch_shift(y, sr, n_steps=6)  # n_steps控制音调变化尺度
    y_ts = librosa.effects.time_stretch(y, rate=1.2)  # rate控制时间维度的变换尺度
    plt.subplot(311)
    plt.plot(y)
    plt.title('Original waveform')
    plt.axis([0, 200000, -0.4, 0.4])
    # plt.axis([88000, 94000, -0.4, 0.4])
    plt.subplot(312)
    plt.plot(y_ts)
    plt.title('Time Stretch transformed waveform')
    plt.axis([0, 200000, -0.4, 0.4])
    plt.subplot(313)
    plt.plot(y_ps)
    plt.title('Pitch Shift transformed waveform')
    plt.axis([0, 200000, -0.4, 0.4])
    # plt.axis([88000, 94000, -0.4, 0.4])
    plt.tight_layout()
    plt.show()

# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     audio = './audio/Dog/1-30226-A.ogg'
#     # demo_plot(audio)
#     aug_pitch_shift(audio)
