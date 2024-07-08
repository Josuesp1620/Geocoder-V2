# API

Para depuración, puedes ejecutar el servidor simple de Uvicorn:

## Endpoints

### /search/

Realiza una búsqueda de texto completo.

#### Parámetros

- **query** *(requerido)*: cadena de texto a buscar
- **limit**: limita el número de resultados (por defecto: 5)
- **autocomplete**: activa o desactiva la autocompletación (por defecto: 1)
- **filters**: cada filtro que se haya declarado en la [configuración](config.md) está disponible como parámetro

#### Formato de respuesta

```json
{
    "attribution": "Geosolution S.A.C.",
    "features": [
        {
            "geometry": {
                "coordinates": [
                    -12.04633641994232,
                    -77.0602306736944
                ],
                "type": "Point"
            },
            "properties": {
                "cod_departament": "15",
                "cod_district": "01",
                "cod_province": "01",
                "context": "LIMA - LIMA - LIMA",
                "distance": 8,
                "id": "MZ_LT-150101-11a5359a-03d3-4bce-8506-bcdb80150e85",
                "id_urb": "URB-150101-0d132a59-806a-4848-8838-ecfe379edba9",
                "label": "PJV SAN VICENTE DE PAUL Mz. R - Lt. 22",
                "lote": "22",
                "manzana": "R",
                "manzana_lote": "Mz. R - Lt. 22",
                "name": "Mz. R - Lt. 22",
                "name_manzana": "Mz. R",
                "nombre_urbanizacion": "PJV SAN VICENTE DE PAUL",
                "postcode": 150101,
                "score": 0.9999999694735917,
                "type": "manzana_lote"
            },
            "type": "Feature"
        }
    ],
    "limit": 1,
    "type": "FeatureCollection",
    "version": "draft"
}
```

### /reverse/

Realiza una geocodificación inversa.

Parámetros:

- **lat**/**lon** *(requerido)*: centro para la geocodificación inversa (**lng** también se acepta en lugar de **lon**)
- cada filtro que se haya declarado en la [configuración](config.md) está disponible como parámetro

El mismo formato de respuesta que el endpoint `/search/`.