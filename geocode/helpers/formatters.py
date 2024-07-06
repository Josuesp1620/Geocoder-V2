def geojson(result):
    
    properties = {
        "label": str(result),
    }
    
    if result._scores:
        properties["score"] = result.score
    for key in result.keys:
        val = getattr(result, key, None)
        if val and key not in ["lat", "lon", "_id", "bbox"]:
            properties[key] = val
    
    housenumber = getattr(result, "housenumber", None)
    if housenumber:
        properties["name"] = "{} {}".format(properties.get("name"), housenumber)
        properties["label"] = properties["name"]

    type_ = result._doc.get("type")

    if type_ and type_ not in properties:
        properties[type_] = properties.get("name")

        if type_ == "manzana_lote" or type_ == "manzana":
            properties["label"] = properties["nombre_urbanizacion"] + ' ' + properties["name"]

    if result.postcode:
        if len(str(result.postcode)) == 5:
            properties["postcode"] = '0'+str(result.postcode)
        if len(str(result.postcode)) == 1:
            properties["postcode"] = '0'+str(result.postcode)
        if len(str(result.postcode)) == 3:
            properties["postcode"] = '0'+str(result.postcode)




    if result.cod_departament:
        if len(str(result.cod_departament)) == 1:
            properties["cod_departament"] = '0'+str(result.cod_departament)
        else:
            properties["cod_departament"] = str(result.cod_departament)

    if result.cod_province:
        if len(str(result.cod_province)) == 1:
            properties["cod_province"] = '0'+str(result.cod_province)
        else:
            properties["cod_province"] = str(result.cod_province)


    if result.cod_district:
        if len(str(result.cod_district)) == 1:
            properties["cod_district"] = '0'+str(result.cod_district)
        else:
            properties["cod_district"] = str(result.cod_district)


    if result.bbox:
        properties["bbox"] = eval(result.bbox)
    try:
        properties["distance"] = int(result.distance)
    except ValueError:
        pass
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(result.lat), float(result.lon)],
        },
        
        "properties": properties,
    }
