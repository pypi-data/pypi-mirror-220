import os.path

import matplotlib.pyplot as plt
import librosa.display
import numpy as np
from pathlib import Path

import sklearn
from matplotlib import cm
from scipy import signal

from .. import core

__all__ = [
    'visualizer',
    'WaveVisualizer',
]


class visualizer:
    def __init__(self):
        self.plt = plt
        self.fig = self.plt.figure(figsize=(7, 5))
        self.plt.subplots_adjust(wspace=0.3, hspace=0.3)

    def loss_plot(self, loss, val_loss):
        """
        Plot loss curve.

        loss : list [ float ]
            training loss time series.
        val_loss : list [ float ]
            validation loss time series.

        return   : None
        """
        ax = self.fig.add_subplot(1, 1, 1)
        ax.cla()
        ax.plot(loss)
        ax.plot(val_loss)
        ax.set_title("Model loss")
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Loss")
        ax.legend(["Train", "Validation"], loc="upper right")

    def show_figure(self):
        self.fig.show()

    def save_figure(self, name):
        self.plt.savefig(name)


class WaveVisualizer(visualizer):
    def __init__(self, figsize=(7, 5), dpi=200, subplots: int = None):
        super().__init__()
        self.plt = plt
        if subplots:
            self.row_len = subplots
            self.fig, self.ax = plt.subplots(self.row_len, 2, figsize=(11, 8))
        else:
            self.fig = self.plt.figure(figsize=figsize, dpi=dpi)
        self.plt.subplots_adjust(wspace=0.3, hspace=0.3)

    @classmethod
    def multi_plot(cls, size=None, figsize=None):
        if size:
            if not figsize:
                if size == 5:
                    figsize = (11, 8)
            return cls(figsize, subplots=size)
        else:
            return cls(figsize)

    def plot(self, wave_list, title=None):
        self.wave_length = len(wave_list)
        print(f'[kudio] plot {self.wave_length} wave(s)')
        if not len(title) == self.wave_length:
            title = [Path(w).stem for w in wave_list]

        for ind, (w, t) in enumerate(zip(wave_list, title)):
            self.ax[ind][0].set_title(str(t))
            y, sr = core.file_load(w)
            librosa.display.waveplot(y,
                                     sr=sr,
                                     ax=self.ax[ind][0])

            self.ax[ind][1].set_title(str(t))
            DA = librosa.amplitude_to_db(
                np.abs(librosa.stft(
                    y, n_fft=512, hop_length=256, win_length=512, window='hamming')), ref=np.max)
            librosa.display.specshow(DA,
                                     sr=sr,
                                     hop_length=256,
                                     x_axis='time',
                                     y_axis='linear',
                                     cmap=cm.get_cmap('jet'),
                                     ax=self.ax[ind][1])
        self.multi_hide_xlabel()
        self.fig.tight_layout()

    def multi_hide_xlabel(self):
        id = 0
        while id < self.wave_length - 1:
            self.ax[id, 0].set_xlabel("")
            self.ax[id, 1].set_xlabel("")
            id += 1

    def save_figure(self, path):
        path = Path(path)
        if path.exists():
            print('[kudio] 檔案或路徑已存在')
            return
        self.plt.savefig(path)

    def copy_wave(self, path, wave_list):
        core.copy_waves(path, wave_list)


def basic_analyze(file, show: bool = False, save_dir=None):
    # 畫 波形圖, STFT, ZCR
    x, sr = core.file_load(file)

    plt.figure(figsize=(10, 8), dpi=200)
    plt.subplot(311)
    plt.title(Path(file).stem)
    librosa.display.waveplot(x, sr=sr)

    # display Spectrogram
    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.subplot(312)
    plt.title('STFT')
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz', cmap=cm.get_cmap('jet'))
    # librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log')
    # plt.colorbar()

    # Zero-crossing-rate
    plt.subplot(313)
    plt.title('ZCR')
    zcrs = librosa.feature.zero_crossing_rate(x + 0.0001)
    time2 = np.linspace(0, int((len(x) / sr)), len(zcrs[0]))
    plt.plot(time2, zcrs[0])
    plt.axis([0, int(len(x) / sr), 0, max(zcrs[0])])

    plt.tight_layout()

    if save_dir is not None:
        # save_dir = Path(save_dir)
        plt.savefig(str(save_dir))
    if show:
        plt.show()
    plt.close()



def plot_4_features(file, show: bool = False, save_dir=None, dpi=200):
    """
    Plot Waveform / Spectral Centroid / Spectral Rolloff / ZCR /Power Spectral Density
    """
    x, sr = core.file_load(file)

    ### Normalising the spectral centroid for visualisation

    fig, ax = plt.subplots(2, 1, figsize=(10, 10), dpi=dpi)

    # Plotting the Spectral Centroid along the waveform
    librosa.display.waveplot(x, sr=sr, alpha=0.4, ax=ax[0], label='waveform')
    plot_spectral_centroid(ax[0], x, sr, color='r', label='spectral_centroid')

    # Spectral Rolloff
    # librosa.display.waveplot(x, sr=sr, alpha=0.4, ax=ax[1])
    plot_spectral_rolloff(ax[0], x, sr, color='b', label='spectral_rolloff')

    plot_zcr(ax[0], x, sr, color='g', label='zcr')

    plot_power_spectral_density(ax[1], x, sr)

    ax[0].set_xlim(0, int(len(x)/sr))
    ax[0].grid(which='major', axis='both')
    ax[0].set_title('spectral centroid & spectral rolloff & zcr')
    # ax[0].set_aspect('auto')
    # ax[0].minorticks_on()

    plt.tight_layout()
    if save_dir is not None:
        plt.savefig(save_dir)
    if show is not None:
        plt.show()
    plt.close()


def plot_3_features(file, show: bool = False, save_dir=None, dpi=200):
    """
    Plot Waveform / Spectral Centroid / Spectral Rolloff / ZCR
    """
    x, sr = core.file_load(file)

    ### Normalising the spectral centroid for visualisation

    fig, ax = plt.subplots(figsize=(7, 5), dpi=dpi)

    # Plotting the Spectral Centroid along the waveform
    librosa.display.waveplot(x, sr=sr, alpha=0.4, ax=ax, label='waveform')
    plot_spectral_centroid(ax, x, sr, color='r', label='spectral_centroid')

    # Spectral Rolloff
    # librosa.display.waveplot(x, sr=sr, alpha=0.4, ax=ax[1])
    plot_spectral_rolloff(ax, x, sr, color='b', label='spectral_rolloff')

    plot_zcr(ax, x, sr, color='g', label='zcr')

    # plot_power_spectral_density(ax[1], x, sr)

    ax.set_xlim(0, int(len(x)/sr))
    ax.grid(which='major', axis='both')
    ax.set_title('spectral centroid & spectral rolloff & zcr')

    plt.tight_layout()
    if save_dir is not None:
        plt.savefig(save_dir)
    if show is not None:
        plt.show()
    plt.close()

def plot_PSD(file, show: bool = False, save_dir=None, dpi=200):
    """
    Plot Power Spectral Density
    """
    x, sr = core.file_load(file)

    fig, ax = plt.subplots(figsize=(7, 5), dpi=dpi)

    plot_power_spectral_density(ax, x, sr)

    plt.tight_layout()
    if save_dir is not None:
        plt.savefig(save_dir)
    if show is not None:
        plt.show()
    plt.close()

def normalize(x, axis=0):
    return sklearn.preprocessing.minmax_scale(x, axis=axis)
    # try:
    #     import sklearn
    #     return sklearn.preprocessing.minmax_scale(x, axis=axis)
    # except Exception as e:
    #     print(e)
    #     _mean = np.mean(spectral_centroids)
    #     _std = np.std(spectral_centroids) + 1e-12
    #     return (spectral_centroids - _mean) / _std


def plot_spectral_centroid(ax, y, sr, color='r', label=None):
    ### spectral centroid -- centre of mass -- weighted mean of the frequencies present in the sound
    spectral_centroids = librosa.feature.spectral_centroid(y, sr=sr)[0]

    ### Computing the time variable for visualization
    # frames = range(len(spectral_centroids))
    # t = librosa.frames_to_time(frames, sr=sr)
    t = np.linspace(0, int((len(y) / sr)), len(spectral_centroids))

    ax.plot(t, normalize(spectral_centroids), color=color, label=label)
    ax.set_title('Spectral Centroid')
    # ax.axis([0, int(len(y) / sr), 0, max(spectral_centroids)])
    if label is not None: ax.legend()


def plot_spectral_rolloff(ax, y, sr, color='r', label=None):
    # Spectral Rolloff
    spectral_rolloff = librosa.feature.spectral_rolloff(y, sr=sr)[0]

    # frames = range(len(spectral_rolloff))
    # t = librosa.frames_to_time(frames, sr=sr)
    t = np.linspace(0, int((len(y) / sr)), len(spectral_rolloff))

    ax.plot(t, normalize(spectral_rolloff), color=color, label=label)
    # ax.axis([0, int(len(y) / sr), 0, max(spectral_rolloff)])
    ax.set_title('Spectral Rolloff')
    if label is not None: ax.legend()


def plot_power_spectral_density(ax, y, sr, color='b', label=None):
    # Compute and plot the power spectral density.
    freqs, psd = signal.welch(y, sr, nfft=1024)
    ax.semilogx(freqs, psd, color=color, label=label)
    ax.set_title('Power Spectral Density')
    ax.set_xlabel('Frequency[Hz]')
    ax.set_ylabel('PSD [V**2/Hz]')
    ax.grid(which='major', axis='both')
    if label is not None: ax.legend()

def plot_zcr(ax, y, sr, color='r', label=None):
    ax.set_title('ZCR')
    zcrs = librosa.feature.zero_crossing_rate(y + 0.0001)
    time2 = np.linspace(0, int((len(y) / sr)), len(zcrs[0]))
    ax.plot(time2, zcrs[0], color=color, label=label)
    # ax.axis([0, int(len(y) / sr), 0, max(zcrs[0])])
    if label is not None: ax.legend()
