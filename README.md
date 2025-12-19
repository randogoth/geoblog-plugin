Repository moved to [codeberg.org/randogoth/geoblog-plugin.git](https://codeberg.org/randogoth/geoblog-plugin.git)

# GeoBlog Pelican Plugin

This plugin scans for `Location: <latitude>, <longitude>` metadata in articles and displays them on a map using the included `archives.html` template. It also writes `articles.gpx` and `articles.kml` files with the same information for offline GPS devices and Apps.

## Installation

Copy the `geoblog` folder to your local Pelican plug-ins folder and activate the plug-in in your `pelicanconf.py` file:

```
PLUGINS = ['geoblog']
```

Copy the `archives.html` file to your Pelican theme's `templates` folder.

If you want to use it for `categories` or other `index.html` derived template files, make sure to adjust the loop accordingly:

```
{% for article in articles %}
```

## Use

Add location coordinates as decimal latitude and longitude values to your article metadata header. The map will display markers that show a pop up with the clickable title of the article when clicked.

```
Location: 12.009621864420991, 79.81141615530888
```

## Notes

The generated map is based on [leaflet.js](https://leafletjs.com) and is highly customizable