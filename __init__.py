# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AzimuthMeasurement
                                 A QGIS plugin
 Just measure Azimuth when you draw a line
                             -------------------
        begin                : 2015-12-18
        copyright            : (C) 2015 by WebGeoDataVore
        email                : contact@webgeodatavore.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AzimuthMeasurement class from file AzimuthMeasurement.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .azimuth_measurement import AzimuthMeasurement
    return AzimuthMeasurement(iface)
