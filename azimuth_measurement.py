# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AzimuthMeasurement
                                 A QGIS plugin
 Just measure Azimuth when you draw a line
                              -------------------
        begin                : 2015-12-18
        git sha              : $Format:%H$
        copyright            : (C) 2015 by WebGeoDataVore
        email                : contact@webgeodatavore.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import (QSettings, Qt, QTranslator, qVersion,
                          QCoreApplication)

from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources

from draw_mono_line_map_tool import DrawMonoLineMapTool

# Import the code for the widget
from azimuth_measurement_widget import AzimuthMeasurementWidget
import os.path


class AzimuthMeasurement:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AzimuthMeasurement_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dock = AzimuthMeasurementWidget()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.dock.hide()

        # Declare instance attributes
        self.actions = []

        if not hasattr(self, 'draw_mono_line'):
            self.draw_mono_line = DrawMonoLineMapTool(self.canvas)
            self.draw_mono_line.deactivated.connect(self.desactivateTool)
            self.draw_mono_line.azimuth_calcul.connect(self.populate_dock_widget)

        self.dock.clear_button.clicked.connect(self.clear_all)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AzimuthMeasurement', message)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/AzimuthMeasurement/icon.png'

        icon = QIcon(icon_path)
        action = QAction(
            icon, self.tr(u'Azimut Measurement'),
            self.iface.mainWindow()
        )
        action.triggered.connect(self.run)
        self.iface.attributesToolBar().actions()[8].defaultWidget().addAction(
            action
        )
        self.actions.append(action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.clear_canvas()
        widget_measurement = self.iface.attributesToolBar().actions()[8]
        widget_measurement.defaultWidget().removeAction(self.actions[0])

    def run(self):
        """Run method that performs all the real work"""
        # show the widget
        self.dock.show()
        self.canvas.setMapTool(self.draw_mono_line)

    def desactivateTool(self):
        """Slot called when desactivate the tool.
        Reset values in the dock and hide the dock"""
        self.clear_widget_content()
        self.dock.hide()

    def populate_dock_widget(self, distance, azimuth, reverse_azimuth):
        """Fill the fields in the dock"""
        self.dock.geographic_distance.setText(str(distance))
        self.dock.azimuth.setText(str(azimuth))
        self.dock.reverse_azimuth.setText(str(reverse_azimuth))

    def clear_widget_content(self):
        self.dock.geographic_distance.setText("")
        self.dock.azimuth.setText("")
        self.dock.reverse_azimuth.setText("")

    def clear_canvas(self):
        self.draw_mono_line.reset()

    def clear_all(self):
        self.clear_canvas()
        self.clear_widget_content()
