from PyQt5.QtWidgets import QApplication,QHBoxLayout,QFrame,QLabel,QPushButton,QSlider,QSizePolicy
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QUrl,QSize,Qt
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer,QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget

class Player(QFrame):
    def __init__(self, parent=None):
        """头部区域，包括图标/搜索/设置/登陆/最大/小化/关闭。"""
        super().__init__()

        self.setObjectName('Header')
        self.parent = parent

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.mainLayout = QHBoxLayout(self)
        #self.mainLayout.setSpacing(0)

        self.preButton = QPushButton()
        #self.preButton.setIcon(QIcon("../icons/music_pre.png"))
        self.preButton.setStyleSheet("QPushButton{border-image: url(icons/music_pre.png)}")
        #self.preButton.setMaximumSize(48,48)
        self.preButton.setMinimumSize(36, 36)
        self.preButton.setObjectName("preButton")
        self.mainLayout.addWidget(self.preButton)

        self.playButton = QPushButton()
        self.playButton.setStyleSheet("QPushButton{border-image: url(icons/music_on.png)}")
        #self.playButton.setMaximumSize(48, 48)
        self.playButton.setMinimumSize(36, 36)
        self.playButton.setObjectName("playButton")
        self.mainLayout.addWidget(self.playButton)

        self.nextButton = QPushButton()
        self.nextButton.setStyleSheet("QPushButton{border-image: url(icons/music_next.png)}")
        #self.nextButton.setMaximumSize(48, 48)
        self.nextButton.setMinimumSize(36, 36)
        self.nextButton.setObjectName("nextButton")
        self.mainLayout.addWidget(self.nextButton)

        self.currentTimeLabel = QLabel("00:00")
        self.currentTimeLabel.setMinimumSize(QSize(60, 0))
        self.currentTimeLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.currentTimeLabel.setObjectName("currentTimeLabel")
        self.mainLayout.addWidget(self.currentTimeLabel)

        self.timeSlider = QSlider()
        self.timeSlider.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.timeSlider.setOrientation(Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")
        self.mainLayout.addWidget(self.timeSlider)

        self.totalTimeLabel = QLabel("00:00")
        self.totalTimeLabel.setMinimumSize(QSize(60, 0))
        self.totalTimeLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.totalTimeLabel.setObjectName("totalTimeLabel")
        self.mainLayout.addWidget(self.totalTimeLabel)

        self.volumeButton = QPushButton()
        self.volumeButton.setObjectName("volumeButton")
        self.mainLayout.addWidget(self.volumeButton)

        self.volumeSlider = QSlider()
        self.volumeSlider.setMinimumWidth(100)
        self.volumeSlider.setMaximumWidth(150)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setProperty("value", 5)
        self.volumeSlider.setOrientation(Qt.Horizontal)
        self.volumeSlider.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.volumeSlider.setObjectName("volumeSlider")
        self.player.setVolume(self.volumeSlider.value())
        self.mainLayout.addWidget(self.volumeSlider)

        self.musicCycleButton = QPushButton()
        self.musicCycleButton.setObjectName("musicCycle")
        self.musicCycleButton.setToolTip("音乐循环")
        self.mainLayout.addWidget(self.musicCycleButton)

        self.musicCycleButton = QPushButton("词")
        self.musicCycleButton.setObjectName("musicCycle")
        self.musicCycleButton.setToolTip("歌词")
        self.mainLayout.addWidget(self.musicCycleButton)

        self.playlistButton = QPushButton("列")
        self.playlistButton.setObjectName("playlistButton")
        self.mainLayout.addWidget(self.playlistButton)

        #self.mainLayout.addStretch(1)

        self.registerSignalConnect()

    def registerSignalConnect(self):
        self.player.error.connect(self.erroralert)

        self.preButton.pressed.connect(self.playlist.previous)
        self.playButton.pressed.connect(self.playButtonClicked)
        self.nextButton.pressed.connect(self.playlist.next)

        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)
        #self.timeSlider.valueChanged.connect(self.player.setPosition)
        #self.timeSlider.sliderMoved.connect(self.player.setPosition)
        self.timeSlider.sliderReleased.connect(self.timeSliderReleased)
        self.timeSlider.sliderPressed.connect(self.timeSliderPressed)
        self.timeSlider.sliderMoved.connect(self.timeSliderMoved)

    def playMusic(self,url):
        print(url)
        content = QMediaContent(QUrl.fromLocalFile(url))
        self.playlist.addMedia(content)
        self.playlist.setCurrentIndex(self.playlist.mediaCount()-1)
        if self.player.state() != QMediaPlayer.PlayingState:
            self.player.play()
        #self.player.setMedia(content)
        #self.player.play()

    def playButtonClicked(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def timeSliderPressed(self):
        """按下准备拖动时。"""
        # 将进度条自动更新取消。
        self.player.durationChanged.disconnect()
        self.player.positionChanged.disconnect()
        # 添加进度条移动事件。
        #self.slider.sliderMoved.connect(self.sliderMovedEvent)

    def timeSliderReleased(self):
        """拖动进度条的事件，用于快进快退。"""
        value = self.timeSlider.value()
        self.player.setPosition(value)

        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)

    def timeSliderMoved(self):
        self.currentTimeLabel.setText(hhmmss(self.timeSlider.value()))

    def update_duration(self, mc):
        self.timeSlider.setMaximum(self.player.duration())
        duration = self.player.duration()

        if duration >= 0:
            self.totalTimeLabel.setText(hhmmss(duration))

    def update_position(self, *args):
        position = self.player.position()
        if position >= 0:
            self.currentTimeLabel.setText(hhmmss(position))

        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        #self.timeSlider.blockSignals(True)
        self.timeSlider.setValue(position)
        #self.timeSlider.blockSignals(False)



    def erroralert(self, *args):
        print(args)

def hhmmss(ms):
    # s = 1000
    # m = 60000
    # h = 360000
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d:%02d" % (h,m,s)) if h else ("%d:%02d" % (m,s))
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = Player()
    Form.resize(900, 40)
    Form.show()
    sys.exit(app.exec_())