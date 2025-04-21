# gauge_widget.py

import math
import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import QPen, QFont, QColor, QPainterPath, QBrush
from PyQt5.QtCore import QRectF, Qt, QPointF, QTimer
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsPathItem

class GaugeWidget(QWidget):
    def __init__(self, parent=None, label=""):
        super(GaugeWidget, self).__init__(parent)
        
        self.view = QGraphicsView(self)
        self.view.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)
        
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        
        self.radius = 100
        self.center_x = self.radius + 10
        self.center_y = self.radius + 10
        
        self.label_text = label
        
        # Create timer for random updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_random)
        self.timer.start(500)  # Update every 1000ms (1 second)
        
        self.draw_gauge()
        
    def set_label(self, label):
        """Set or update the gauge label"""
        self.label_text = label
        self.draw_gauge()
        
    def draw_gauge(self):
        self.scene.clear()
        
        # Draw background arc (gray)
        background_path = QPainterPath()
        background_path.arcMoveTo(self.center_x - self.radius, self.center_y - self.radius, 
                                2 * self.radius, 2 * self.radius, 180)
        background_path.arcTo(self.center_x - self.radius, self.center_y - self.radius,
                            2 * self.radius, 2 * self.radius, 180, -180)  # Note the negative angle
        background_arc = QGraphicsPathItem(background_path)
        background_arc.setPen(QPen(QColor(50, 50, 50), 20, Qt.SolidLine, Qt.RoundCap))
        self.scene.addItem(background_arc)
        
        # Create progress arc (will be updated by set_speed)
        self.progress_path = QPainterPath()
        self.progress_arc = QGraphicsPathItem()
        self.progress_arc.setPen(QPen(QColor(255, 20, 147), 20, Qt.SolidLine, Qt.RoundCap))
        self.scene.addItem(self.progress_arc)
        
        # Add gauge label at the top
        if self.label_text:
            label = QGraphicsTextItem(self.label_text)
            label.setFont(QFont('Arial', 23, QFont.Bold))
            label.setDefaultTextColor(QColor('white'))
            text_width = label.boundingRect().width()
            # Position the label above the gauge
            label.setPos(self.center_x - text_width/2, self.center_y - self.radius +150)
            self.scene.addItem(label)
        
        # Add percentage text in center
        self.percentage_text = QGraphicsTextItem("0%")
        self.percentage_text.setFont(QFont('Arial',26, QFont.Bold))
        self.percentage_text.setDefaultTextColor(QColor('white'))
        text_width = self.percentage_text.boundingRect().width()
        text_height = self.percentage_text.boundingRect().height()
        # Center the text both horizontally and vertically
        self.percentage_text.setPos(self.center_x - text_width/2, self.center_y - text_height/2)
        self.scene.addItem(self.percentage_text)
        
        self.set_speed(0)
    
    def update_random(self):
        """Update gauge with random value"""
        random_value = random.randint(0, 100)
        self.set_speed(random_value)
    
    def set_speed(self, percentage):
        # Ensure percentage is between 0 and 100
        percentage = max(0, min(100, percentage))
        
        # Update progress arc
        self.progress_path = QPainterPath()
        self.progress_path.arcMoveTo(self.center_x - self.radius, self.center_y - self.radius,
                                   2 * self.radius, 2 * self.radius, 180)
        span_angle = -percentage * 180 / 100  # Negative angle to go clockwise
        self.progress_path.arcTo(self.center_x - self.radius, self.center_y - self.radius,
                               2 * self.radius, 2 * self.radius, 180, span_angle)
        self.progress_arc.setPath(self.progress_path)
        
        # Update percentage text
        self.percentage_text.setPlainText(f"{int(percentage)}%")
        text_width = self.percentage_text.boundingRect().width()
        text_height = self.percentage_text.boundingRect().height()
        # Keep text centered
        self.percentage_text.setPos(self.center_x - text_width/2, self.center_y - text_height/2)

# For testing the widget directly
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create widget with dark background for better visibility
    window = QWidget()
    window.setStyleSheet("background-color: #1a1a1a;")
    layout = QVBoxLayout(window)
    
    # Create and add gauge
    gauge = GaugeWidget()
    layout.addWidget(gauge)
    
    # Set window properties
    window.setGeometry(100, 100, 300, 200)
    window.show()
    
    sys.exit(app.exec_())