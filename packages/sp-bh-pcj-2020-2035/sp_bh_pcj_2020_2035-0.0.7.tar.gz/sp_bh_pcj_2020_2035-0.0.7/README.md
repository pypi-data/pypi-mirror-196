# Plano de Bacias PCJ 2020-2035

- [PyPi](https://pypi.org/project/sp-bh-pcj-2020-2035/)
- [GitHub](https://github.com/open-geodata/sp_bh_pcj-2020-2035)

<br>

A Agência das Bacias PCJ mantem um [ArcGIS Server](https://mapas.agenciapcj.org.br/arcgis/rest/services) possibilitando o consumo de dados espaciais.

Visando baixar todos os dados disponíveis, referente ao [Plano de Bacias 2020-2035](https://plano.agencia.baciaspcj.org.br/), em 20.05.2022 acessei todos os dados usando o repositório [ArcGIS REST API](https://github.com/open-geodata/arcgis_rest_api).

![ArcGIS Server](https://i.imgur.com/ZAKT1bE.png)

O enderenço com os parâmetros, que utilizei, esta apresentado abaixo:

- https://mapas.agenciapcj.org.br/arcgis/rest/services/Planos/PlanoBacias_CRF/FeatureServer/49/query?where=1%3D1&objectIds=1&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&gdbVersion=&historicMoment=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&multipatchOption=xyFootprint&resultOffset=&resultRecordCount=&returnTrueCurves=false&returnExceededLimitFeatures=false&quantizationParameters=&returnCentroid=false&sqlFormat=none&resultType=&featureEncoding=esriDefault&datumTransformation=&f=geojson

<br>

Notei também que a Agência PCJ mantem uma [API Swagger](https://ssd.baciaspcj.org.br/api/index.html) com disponibilização de dados.

<br>

---

### Como Usar?

O repositório faz parte do projeto [**_OpenGeodata_**](https://pypi.org/project/open-geodata), que tem por objetivo compartilhar dados espaciais por meio de _packages_ do python.

```bash
# Install
pip3 install open-geodata --upgrade
pip3 install sp-bh-pcj-2020-2035 --upgrade
```

<br>

Uma vez instalado os pacotes, é possível listar e carregar os _datasets_ disponíveis, com os comandos abaixo.

```python
# List Datasets from package (dataframes and geodataframes)
geo.get_dataset_from_package('sp_bh_pcj_2020_2035')

# Load Dataset from package
geo.load_dataset_from_package('sp_bh_pcj_2020_2035', dataset_name)
```

<br>

---

### Observação

Existem três _layers_ que não inseri no repositório, visto apresentarem mais de 25mb (limite do GitHub). a saber:

- inventario florestal 2020 - bacia pcj - poligonos.7z
- uso da terra - poligonos.7z
- área de preservação permanente - poligonos.7z

<br>

---

### _TODO_

1. Definir _layers_
