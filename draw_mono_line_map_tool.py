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
                    QgsPoint(self.points[0].x(), self.points[0].y()),
                    QgsPoint(self.points[1].x(), self.points[1].y())
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
            start = QgsPoint(self.startPoint.x(), self.startPoint.y())
            end = QgsPoint(self.endPoint.x(), self.endPoint.y())
            geom = QgsGeometry.fromPolyline([start, end])
            self.rubberBand.setToGeometry(geom, None)
            if ((self.startPoint is not None and
                 self.endPoint is not None and
                 self.startPoint != self.endPoint)):
                self.azimuth_calcul.emit(start, end)

    def activate(self):
        self.reset()
        super(DrawMonoLineMapTool, self).activate()
        self.activated.emit()

    def deactivate(self):
        self.reset()
        super(DrawMonoLineMapTool, self).deactivate()
        self.deactivated.emit()
