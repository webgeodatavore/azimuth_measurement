# coding: utf-8
from PyQt4.QtCore import Qt, SIGNAL, pyqtSignal
from qgis.core import QGis, QgsGeometry, QgsPoint
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand


class DrawMonoLineMapTool(QgsMapToolEmitPoint):

    azimuth_calcul = pyqtSignal(QgsPoint, QgsPoint)

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Line)
        self.rubberBandDraw = QgsRubberBand(self.canvas, QGis.Line)
        self.rubberBandDraw.setColor(Qt.blue)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        self.points = []
        self.reset()

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QGis.Line)
        self.rubberBandDraw.reset(QGis.Line)

    def canvasPressEvent(self, e):
        self.isEmittingPoint = False

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = True
        self.startPoint = self.toMapCoordinates(e.pos())
        if len(self.points) < 2:
            self.rubberBandDraw.reset(QGis.Line)
            self.rubberBand.reset(QGis.Line)
            self.points.append(self.startPoint)
        if len(self.points) == 2:
            self.rubberBandDraw.setToGeometry(
                QgsGeometry.fromPolyline([
                    self.points[0],
                    self.points[1]
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
                    self.startPoint,
                    self.endPoint
                ]),
                None
            )
            if (self.startPoint is not None and self.endPoint is not None and self.startPoint != self.endPoint):
                self.azimuth_calcul.emit(self.startPoint, self.endPoint)
            # self.result = self.calculate_azimuth()
            # if (self.result is not None and 'distance' in self.result and
            #     'reverse_azimuth' in self.result and 'azimuth' in self.result):
            #     self.azimuth_calcul.emit(
            #         self.result['distance'],
            #         self.result['reverse_azimuth'],
            #         self.result['azimuth']
            #     )

    def activate(self):
        self.reset()
        super(DrawMonoLineMapTool, self).activate()
        self.emit(SIGNAL("activated()"))

    def deactivate(self):
        self.reset()
        super(DrawMonoLineMapTool, self).deactivate()
        self.emit(SIGNAL("deactivated()"))
