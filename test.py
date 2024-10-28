from shapely import wkb

def check_hex_polygon_validity(hex_data):
    try:
        # Mengonversi heksadesimal ke WKB
        wkb_data = bytes.fromhex(hex_data)

        # Memuat data WKB menjadi geometri menggunakan Shapely
        geometry = wkb.loads(wkb_data)

        # Memeriksa apakah geometri merupakan Poligon dan valid
        if geometry.geom_type == 'Polygon' and geometry.is_valid:
            print("Poligon valid.")
            return True
        else:
            print("Poligon tidak valid atau bukan poligon.")
            return False
            
    except Exception as e:
        print("Terjadi kesalahan:", e)
        return False

# Contoh heksadesimal dari poligon
hex_polygon = "0103000020E6100000010000000500000014AE47E17A140240AE47E17A14BE5840A4703D0AD7A30240AE47E17A14BE5840A4703D0AD7A3024014AE47E17AC4584014AE47E17A14024014AE47E17AC4584014AE47E17A140240AE47E17A14BE5840"

# Memeriksa validitas poligon
is_valid = check_hex_polygon_validity(hex_polygon)
print("Hasil Validitas:", is_valid)
