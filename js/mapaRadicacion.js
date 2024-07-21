//import OSM from '/ol/source/OSM.js';
//import TileLayer from '/ol/layer/Tile.js';
//import {Map, View} from '/ol'; 
//import {fromLonLat} from '/ol/proj';

// var lyrGoogleSatelite = new ol.layer.Tile({
//   title:'Satelite',
//   source: new ol.source.XYZ({
//   url: "http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"
// })})

var map = new ol.Map({
  target: 'mapa-localizacion-radicacion',
  layers: [
    //lyrGoogleSatelite,          
        
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
        
      
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([-74.10230906706656,4.637177535872905]),
    zoom: 11
  }),
});

var layerSwitcher = new ol.control.LayerSwitcher({
  
  tipLabel: 'Leyenda',
  // groupSelectStyle: 'children',
  // UserActivationMode:'click',
  // collapseTipLabel:'Hide layer list',
  // groupSelectStyle: 'group'
});
map.addControl(layerSwitcher)



    /*new ol.layer.Group({
      title: "Mapa Base",
      /*type: "Base",
      combine: true,
      visible: false,
      layers: [
        new TileLayer({
          title: "OMS",
          source: new OSM(),
        }),
        new ol.layer.Tile({
          title: "Hybrid",
          source: new ol.source.XYZ({
            url: "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
          }),
        }),
      ],
    }),*/
    /*new ol.layer.Tile({
      title: "Hybrid",
      source: new ol.source.XYZ({
        url: "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
      })
    })*/

/*var layerSwitcher = new ol.control.LayerSwitcher({
  activationMode: 'click',
  tipLabel: 'Show layer list', // Optional label for button
  collapseTipLabel: 'Hide layer list', // Optional label for button
  groupSelectStyle: 'children' // Can be 'children' [default], 'group' or 'none'
});
map.addControl(layerSwitcher);*/
