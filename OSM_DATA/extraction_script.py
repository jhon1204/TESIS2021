import overpy
api = overpy.Overpass()
result= api.query("[out:xml];(node(-12.0765,-77.0847,-12.0317,-76.9880);<;);out meta;")
print(result)
