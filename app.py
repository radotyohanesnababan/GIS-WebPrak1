from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from shapely import wkb
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class PointData (db.Model):
    __tablename__ = 'point_data'
    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column(db.String())
    name = db.Column(db.String())
class LineData (db.Model):
    __tablename__ = 'line_data'
    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column(db.String())
    name = db.Column(db.String())
class PolygonData (db.Model):
    __tablename__ = 'polygon_data'
    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column(db.String())
    name = db.Column(db.String())
    

@app.route('/')
@app.route('/')
def index():
    geo_points = PointData.query.all()
    geo_lines = LineData.query.all()
    geo_polygons = PolygonData.query.all()
    
    geojson_features_points = []
    geojson_features_lines = []
    geojson_features_polygons = []
    
    for point in geo_points:
        if point.geom:
            geom = wkb.loads(bytes.fromhex(point.geom))
            lon, lat = geom.x, geom.y  # Mengambil koordinat
            geojson_features_points.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [lat, lon]  
                },
                'properties': {
                    'name': point.name
                }
            })
        
    for line in geo_lines:
        if line.geom:
            geom = wkb.loads(bytes.fromhex(line.geom))
            coords = list(geom.coords)
            geojson_features_lines.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [[lon, lat] for lat, lon in coords]  # Ubah urutan menjadi [lat, lon]
                },
                'properties': {
                    'name': line.name
                }
            })

        
    for polygon in geo_polygons:
        if polygon.geom:
            geom = wkb.loads(bytes.fromhex(polygon.geom))
            coords = list(geom.exterior.coords)
            geojson_features_polygons.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [[list(reversed(coord)) for coord in coords]]  # Ubah urutan menjadi [lon, lat]
                },
                'properties': {
                    'name': polygon.name
                }
            })


        
    return render_template('home.html', geojson_points=geojson_features_points, geojson_lines=geojson_features_lines, geojson_polygons=geojson_features_polygons)

if __name__ == '__main__':
    app.run(debug=True)
            