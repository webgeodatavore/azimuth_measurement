# coding: utf-8
from qgis.PyQt.QtCore import pyqtSignal, QSettings
from qgis.PyQt.QtGui import QColor
from qgis.core import Qgis, QgsGeometry, QgsPoint, QgsWkbTypes
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand


class DrawMonoLineMapTool(QgsMapToolEmitPoint):

    azimuth_calcul = pyqtSignal(QgsPoint, QgsPoint)

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('qgis')
        color = QColor(
            int(s.value('default_measure_color_red', 222)),
            int(s.value('default_measure_color_green', 17)),
            int(s.value('default_measure_color_blue', 28))
        )
        s.endGroup()
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rubberBandDraw = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points = []
        self.reset()

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QgsWkbTypes.LineGeometry)
        self.rubberBandDraw.reset(QgsWkbTypes.LineGeometry)

    def canvasPressEvent(self, e):
        self.isEmittingPoint = False

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = True
        self.startPoint = self.toMapCoordinates(e.pos())
        if len(self.points) < 2:
            self.rubberBandDraw.reset(QgsWkbTypes.LineGeometry)
            self.rubberBand.reset(QgsWkbTypes.LineGeometry)
            self.points.append(self.startPoint)
        if len(self.points) == 2:
            self.rubberBandDraw.setToGeometry(
                QgsGeometry.fromPolyline([
                    QgsPoint(self.points[0]),
                    QgsPoint(self.points[1])
                ]),
                None
            )
            self.points = []
            self.isEmittingPoint = False

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(e.pos())
        if len(self.points) > 0:
            self.rubberBand.setToGeometry(
                QgsGeometry.fromPolyline([
                    QgsPoint(self.startPoint),
                    QgsPoint(self.endPoint)
                ]),
                None
            )
            if ((self.startPoint is not None and
                 self.endPoint is not None and
                 self.startPoint != self.endPoint)):
                self.azimuth_calcul.emit(QgsPoint(self.startPoint), QgsPoint(self.endPoint))

    def activate(self):
        self.reset()
        super(DrawMonoLineMapTool, self).activate()
        self.activated.emit()

    def deactivate(self):
        self.reset()
        super(DrawMonoLineMapTool, self).deactivate()
        self.deactivated.emit()
