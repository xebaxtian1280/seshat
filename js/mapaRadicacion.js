import OSM from '/ol/source/OSM.js';
import TileLayer from '/ol/layer/Tile.js';
import {Map, View} from '/ol';git 
import {fromLonLat} from '/ol/proj';

new Map({
  target: 'map-container-radication',
  layers: [
    new TileLayer({
      source: new OSM(),
    }),
  ],
  view: new View({
    center: fromLonLat([0, 0]),
    zoom: 2,
  }),
});