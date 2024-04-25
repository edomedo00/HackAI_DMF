from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QPushButton, QLabel,  QFrame
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt, QSize, QPoint
from PySide6.QtGui import QIcon, QPixmap, QPalette, QBrush

class AnimationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('IAnimator')
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.backgroundPixmap = QPixmap('images/Fondo.jpg')
        self.set_background(self.backgroundPixmap)
        self.oldPos = None

        # Crear layouts principales
        self.main_layout = QVBoxLayout()
        self.upper_section_layout = QHBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.lower_section_layout = QHBoxLayout()

        self.create_custom_titlebar()
        self.create_action_bar()

        # Sección superior
        self.create_video_section()
        self.create_bones_section()
        self.create_sprite_section()

        # Sección de botones
        self.create_buttons()

        # Sección inferior (Timeline)
        self.create_timeline_placeholder()

        # Añadir layouts a la ventana principal
        self.main_layout.addLayout(self.upper_section_layout)
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addLayout(self.lower_section_layout)

        # Establecer el layout principal en un widget central
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Media Player
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.showMaximized()


    def set_background(self, image_path):
        # Configura el fondo para que se ajuste siempre al tamaño de la ventana
        self.backgroundPixmap = QPixmap(image_path)
        self.update_background()

    def resizeEvent(self, event):
        # Actualiza el fondo cuando cambia el tamaño de la ventana
        self.update_background()

    def update_background(self):
        # Escala y ajusta el fondo
        scaledPixmap = self.backgroundPixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        brush = QBrush(scaledPixmap)
        palette = QPalette()
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)
    
    def open_video_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir Video", "", "Archivos de Video (*.mp4 *.avi *.mov)")
        if filename:
            self.mediaPlayer.setSource(QUrl.fromLocalFile(filename))
            self.mediaPlayer.play()

    def open_sprite_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir Sprite", "", "Archivos de Imagen (*.png *.jpg *.bmp)")
        if filename:
            pixmap = QPixmap(filename)
            self.spriteDisplay.setPixmap(pixmap.scaled(self.spriteDisplay.size(), Qt.KeepAspectRatio))
    
    def setButtonIcon(self, button, imagePath):
        pixmap = QPixmap(imagePath)
        icon = QIcon(pixmap)
        button.setIcon(icon)
        button.setIconSize(button.size())


    def create_custom_titlebar(self):
        # Contenedor para la barra de título
        self.titleBar = QFrame()
        self.titleBar.setFixedHeight(40)
        self.titleBar.setStyleSheet("background-color: Transparent;")
        self.titleBar.setMouseTracking(True)
        self.titleBar.mousePressEvent = self.mousePressEvent
        self.titleBar.mouseMoveEvent = self.mouseMoveEvent
        self.titleBar.mouseReleaseEvent = self.mouseReleaseEvent

        # Layout para los botones de la barra de título y el logo
        titleBarLayout = QHBoxLayout()
        titleBarLayout.setContentsMargins(0, 0, 0, 0)

        # Logo de la aplicación
        self.logoLabel = QLabel()
        self.logoPixmap = QPixmap('images/Logo.png')
        self.logoLabel.setPixmap(self.logoPixmap.scaled(300, 30, Qt.KeepAspectRatio))
        self.logoLabel.setFixedSize(300, 30)
        titleBarLayout.addWidget(self.logoLabel)  # Añadir el logo al layout

        titleBarLayout.addStretch(1)  # Añade un stretch para empujar todo a la derecha

        # Botón Minimizar
        self.minimizeButton = QPushButton()
        self.minimizeButton.setIcon(QIcon('images/Iconosarriba1.png'))
        self.minimizeButton.clicked.connect(self.showMinimized)
        self.minimizeButton.setIconSize(QSize(30, 30))
        self.minimizeButton.setFixedSize(QSize(30, 30))
        self.minimizeButton.setCursor(Qt.PointingHandCursor)
        self.minimizeButton.pressed.connect(lambda: self.setButtonIcon(self.minimizeButton, 'images/Iconosarriba2.png'))
        self.minimizeButton.released.connect(lambda: self.setButtonIcon(self.minimizeButton, 'images/Iconosarriba1.png'))
        self.minimizeButton.setStyleSheet("background: transparent; border: none;")

        # Botón Maximizar/Restaurar
        self.maximizeButton = QPushButton()
        self.maximizeButton.setIcon(QIcon('images/Iconosarriba4.png'))
        self.maximizeButton.clicked.connect(self.toggle_maximize_restore)
        self.maximizeButton.setIconSize(QSize(30, 30))
        self.maximizeButton.setFixedSize(QSize(30, 30))
        self.maximizeButton.setCursor(Qt.PointingHandCursor)
        self.maximizeButton.pressed.connect(lambda: self.setButtonIcon(self.maximizeButton, 'images/Iconosarriba5.png'))
        self.maximizeButton.released.connect(lambda: self.setButtonIcon(self.maximizeButton, 'images/Iconosarriba4.png'))
        self.maximizeButton.setStyleSheet("background: transparent; border: none;")

        # Botón Cerrar
        self.closeButton = QPushButton()
        self.closeButton.setIcon(QIcon('images/Iconosarriba7.png'))
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setIconSize(QSize(30, 30))
        self.closeButton.setFixedSize(QSize(30, 30))
        self.closeButton.setCursor(Qt.PointingHandCursor)
        self.closeButton.pressed.connect(lambda: self.setButtonIcon(self.closeButton, 'images/Iconosarriba8.png'))
        self.closeButton.released.connect(lambda: self.setButtonIcon(self.closeButton, 'images/Iconosarriba7.png'))
        self.closeButton.setStyleSheet("background: transparent; border: none;")

        # Añadir botones al layout
        titleBarLayout.addWidget(self.minimizeButton)
        titleBarLayout.addWidget(self.maximizeButton)
        titleBarLayout.addWidget(self.closeButton)

        self.titleBar.setLayout(titleBarLayout)

        # Añadir la barra de título al layout principal
        self.main_layout.insertWidget(0, self.titleBar)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def create_action_bar(self):
        # Contenedor para la barra de acciones
        self.actionBar = QFrame()
        self.actionBar.setFixedHeight(22)
        self.actionBar.setStyleSheet("background-color: Transparent;")  # Un color diferente para distinguir

        # Layout para los botones de la barra de acciones
        actionBarLayout = QHBoxLayout()
        actionBarLayout.setContentsMargins(0, 0, 0, 0)
        actionBarLayout.addStretch(1)  # Alinear los botones a la derecha

        # Ejemplo de un botón de acción
        self.actionButton1 = QPushButton(QIcon('images/action_icon1.png'), "")  # Sin texto, solo ícono
        self.actionButton1.setFixedSize(30, 30)
        self.actionButton1.setStyleSheet("background: transparent; border: none;")

        # Añadir más botones según sea necesario
        actionBarLayout.addWidget(self.actionButton1)
        
        self.actionBar.setLayout(actionBarLayout)

        # Añadir la barra de acciones al layout principal debajo de la barra de título
        self.main_layout.insertWidget(1, self.actionBar)

    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def load_and_scale_image(self, image_path, width, height):
        pixmap = QPixmap(image_path)
        return pixmap.scaled(width, height, Qt.KeepAspectRatio)

    def create_video_section(self):
        self.videoWidget = QVideoWidget()
        self.videoWidget.setFixedSize(480, 340)
        self.videoFrame = QLabel(self.videoWidget)
        video_frame_pixmap = self.load_and_scale_image('images/BordeVideo.png', 480, 350)
        self.videoFrame.setPixmap(video_frame_pixmap)
        self.videoFrame.setStyleSheet("background: transparent;")
        self.videoFrame.setGeometry(0, 0, 480, 350)
        self.upper_section_layout.addWidget(self.videoWidget)

    def create_bones_section(self):
        self.bonesDisplay = QLabel()
        self.bonesDisplay.setFixedSize(210, 340)
        self.bonesDisplay.setAlignment(Qt.AlignCenter)
        self.bonesDisplay.setStyleSheet("QLabel { background: transparent; }")
        self.bonesFrame = QLabel(self.bonesDisplay)
        bones_frame_pixmap = self.load_and_scale_image('images/BordeBones.png', 210, 350)
        self.bonesFrame.setPixmap(bones_frame_pixmap)
        self.bonesFrame.setStyleSheet("background: transparent;")
        self.bonesFrame.setGeometry(0, 0, 210, 340)
        self.upper_section_layout.addWidget(self.bonesDisplay)

    def create_sprite_section(self):
        self.spriteDisplay = QLabel()
        self.spriteDisplay.setFixedSize(480, 340)
        self.spriteDisplay.setAlignment(Qt.AlignCenter)
        self.spriteDisplay.setStyleSheet("QLabel { background: transparent; }")
        self.spriteFrame = QLabel(self.spriteDisplay)
        sprite_frame_pixmap = self.load_and_scale_image('images/BordeSprite.png', 480, 350)
        self.spriteFrame.setPixmap(sprite_frame_pixmap)
        self.spriteFrame.setStyleSheet("background: transparent;")
        self.spriteFrame.setGeometry(0, 0, 480, 340)
        self.upper_section_layout.addWidget(self.spriteDisplay)

    def create_buttons(self):
        self.loadVideoButton = QPushButton()
        self.loadVideoButton.clicked.connect(self.open_video_file)
        self.loadVideoButton.setIcon(QIcon('images/Boton-Video.png'))
        self.loadVideoButton.setIconSize(QSize(150, 40))
        self.loadVideoButton.setFixedSize(QSize(150, 40))
        self.loadVideoButton.setCursor(Qt.PointingHandCursor)
        self.loadVideoButton.pressed.connect(lambda: self.setButtonIcon(self.loadVideoButton, 'images/Boton-Video.png'))
        self.loadVideoButton.released.connect(lambda: self.setButtonIcon(self.loadVideoButton, 'images/Boton-Video.png'))

        
        self.loadSpriteButton = QPushButton()
        self.loadSpriteButton.clicked.connect(self.open_sprite_file)
        self.loadSpriteButton.setIcon(QIcon('images/Boton-Sprite.png'))
        self.loadSpriteButton.setIconSize(QSize(150, 40))
        self.loadSpriteButton.setFixedSize(QSize(150, 40))
        self.loadSpriteButton.setCursor(Qt.PointingHandCursor)
        
        self.reboneButton = QPushButton()
        self.reboneButton.setIcon(QIcon('images/Boton-Rebone.png'))
        self.reboneButton.setIconSize(QSize(150, 40))
        self.reboneButton.setFixedSize(QSize(150, 40))
        self.reboneButton.setCursor(Qt.PointingHandCursor)
        
        # Configurar el layout de botones
        self.buttons_layout.setContentsMargins(83, 0, 0, 0)
        self.buttons_layout.addWidget(self.loadVideoButton)
        self.buttons_layout.addWidget(self.reboneButton)
        self.buttons_layout.addWidget(self.loadSpriteButton)
        self.buttons_layout.addStretch(1)

    def create_timeline_placeholder(self):
        self.timeline_placeholder = QLabel()
        self.timeline_placeholder.setFixedSize(1350, 300)

        # Cargar la imagen de fondo
        pixmap = QPixmap('images/Linea.png')
        self.timeline_placeholder.setPixmap(pixmap.scaled(self.timeline_placeholder.size(), Qt.KeepAspectRatio))
        self.timeline_placeholder.setAlignment(Qt.AlignCenter)
        self.lower_section_layout.addWidget(self.timeline_placeholder)

# Código para ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication([])
    main_window = AnimationApp()
    main_window.show()
    app.exec()