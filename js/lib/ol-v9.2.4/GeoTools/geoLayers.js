function GeoLayers(){
  this.vectorGeoJson = null
}

GeoLayers.prototype.ObtenerLayersBase = function(){
    var listaLayers =[];

      var hybrid = new ol.layer.Tile({
        title: "Hybrid",
        baseLayer:true,
        visible:false,
        source: new ol.source.XYZ({
          url: "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        }),
      })

      listaLayers.push(hybrid)

      var oms = new ol.layer.Tile({
        // A layer must have a title to appear in the layerswitcher
        title: 'OSM',
        // Again set this layer as a base layer
        baseLayer:true,
        visible: true,
        source: new ol.source.OSM()
      })


      listaLayers.push(oms)

      return listaLayers
}

/*
http://localhost:8080/geoserver/Avaluos/wms
&layers=Avaluos%3AAvaluosISA&bbox=-75.2917251586914%2C2.892789840698242%2C-72.91071319580078%2C6.246711254119873&width=545&height=768&srs=EPSG%3A4326&styles=&format=application/openlayers

*/

GeoLayers.prototype.CargarLayersTematicos = function(){
  var listaTematicos = []

  var lyrAvaluo = new ol.layer.Tile({
    title:'Avaluo',
    visible: true,
    source: new ol.source.TileWMS({
      url: 'http://localhost:8080/geoserver/Avaluos/wms',
          params: {'FORMAT': 'image/png',
                   'VERSION': '1.1.0',  
                "STYLES": '',
                "LAYERS": 'Avaluos:AvaluosISA',
          }
    })
  })

  listaTematicos.push(lyrAvaluo)

  return listaTematicos
  /*return new ol.layer.Group({
    title: 'Tematicos',
    layers: listaTematicos
  })*/

}

GeoLayers.prototype.CargarGeoJson = function(){
  var lista = []

  this.vectorGeoJson = new ol.source.Vector({
    url: '/Recursos/punto.json',
    format: new ol.format.GeoJSON()
  })

  var lyrGeoJson = new ol.layer.Vector({
    title: 'Avaluos',
    style: new ol.style.Style({
      image: new ol.style.Icon({
        src:'/Recursos/Iconos/Casas/house.png'
      })
    }),
    source: this.vectorGeoJson
  })

  lista.push(lyrGeoJson)

  return lista
}


    

