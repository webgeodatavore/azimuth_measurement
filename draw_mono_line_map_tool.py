# coding: utf-8
from PyQt4.QtCore import Qt, SIGNAL, pyqtSignal
from qgis.core import (QGis, QgsGeometry,
                       QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform)
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
from gc_geo import *


class DrawMonoLineMapTool(QgsMapToolEmitPoint):

    azimuth_calcul = pyqtSignal(float, float, float)

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
            self.result = self.calculate_azimuth()
            if (self.result is not None and 'distance' in self.result and
                'reverse_azimuth' in self.result and 'azimuth' in self.result):
                self.azimuth_calcul.emit(
                    self.result['distance'],
                    self.result['reverse_azimuth'],
                    self.result['azimuth']
                )

    def calculate_azimuth(self):
        if (self.startPoint is not None and self.endPoint is not None and self.startPoint != self.endPoint):
            sp = self.transform_to_epsg_4326(self.startPoint)
            ep = self.transform_to_epsg_4326(self.endPoint)
            calculus = great_distance(
                start_longitude=sp.x(),
                start_latitude=sp.y(),
                end_longitude=ep.x(),
                end_latitude=ep.y()
            )
            return calculus

    def activate(self):
        self.reset()
        super(DrawMonoLineMapTool, self).activate()
        self.emit(SIGNAL("activated()"))

    def deactivate(self):
        self.reset()
        super(DrawMonoLineMapTool, self).deactivate()
        self.emit(SIGNAL("deactivated()"))

    def transform_to_epsg_4326(self, point):
        if self.canvas.mapRenderer().destinationCrs().authid() != 'EPSG:4326':
            crs_src = self.canvas.mapRenderer().destinationCrs()
            crs_dest = QgsCoordinateReferenceSystem(4326)
            xform = QgsCoordinateTransform(crs_src, crs_dest)
            return QgsGeometry.fromPoint(xform.transform(point)).asPoint()
        else:
            return point
