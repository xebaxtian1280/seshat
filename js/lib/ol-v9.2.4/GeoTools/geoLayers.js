function GeoLayers(){

}

GeoLayers.prototype.ObtenerLayersBase = function(){
    var listaLayers =[];

    var mapasBase = new ol.layer.Group({
        title:'Mapa Base',
        layers:[
          new ol.layer.Tile({
            title: "Hybrid",
            type: 'base',
            source: new ol.source.XYZ({
              url: "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            }),
          }),
          new ol.layer.Tile({
            // A layer must have a title to appear in the layerswitcher
            title: 'OSM',
            // Again set this layer as a base layer
            type: 'base',
            visible: true,
            source: new ol.source.OSM()
          })
        ]
      })

      listaLayers.push(mapasBase)

      return listaLayers

}
    

