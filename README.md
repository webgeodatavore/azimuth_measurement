QGIS Azimuth Measurement documentation
======================================

Purpose
-------

This plugin was created to mimic the behaviour from Google Earth© as
illustrated below. We only choose to display information in a widget
instead of a dialog.

![Azimuth in Google Earth]

We just want to draw a temporary start point, draw a end point and then
display the resulting distance and azimuth. At the moment, we don’t give
the option to save the line drawing.

Installation
------------

You just need to install it through the menu Plugins &gt;
Manage and Install Plugins... and choose Azimuth Measurement.

> **warning**
>
> You need to tick Show also Experimental plugins in Settings lateral
> tab or you will not see the plugin.

Usage
-----

You just have to follow below demonstration to understand how to use the
plugin.

![Azimuth in QGIS]

Credits
-------

The logo copyright is from the icon created by Denis Moskowitz from the
Noun Project under [Licence CC BY 3.0 US].

For the azimuth calculation, we choose to reuse [pygc], a MIT licensed
Python azimuth calculation library (so we can sublicence it in the GPL
plugin code). We removed the dependency to Numpy Python package from it.

Alternatives
------------

Depending of your requirements, you may prefer using other plugins, more
complex and for other use cases:

-   [Azimuth and Distance Plugin]
-   [Azimuth and Distance Calculator]

Contact us
----------

You can open an issue on [the repository] or drop us an email at
contact(at)webgeodatavore.com

We also do QGIS support for users and Python development in France. You
can see more at [our official website].

  [Azimuth in Google Earth]: help/source/_static/images/google-earth-azimuth.gif
  [Azimuth in QGIS]: help/source/_static/images/qgis-azimuth-measurement.gif
  [Licence CC BY 3.0 US]: http://creativecommons.org/licenses/by/3.0/us/
  [pygc]: https://github.com/axiom-data-science/pygc
  [Azimuth and Distance Plugin]: http://planet.qgis.org/plugins/qgsAzimuth/
  [Azimuth and Distance Calculator]: http://planet.qgis.org/plugins/AzimuthDistanceCalculator/
  [the repository]: https://github.com/webgeodatavore/azimuth_measurement/issues
  [our official website]: http://webgeodatavore.com/en/