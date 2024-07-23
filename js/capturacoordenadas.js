const btnGuardar = document.querySelector(".btnSaveCoordinates");
const btnCancelar = document.querySelector(".btnCancelCoordinates");
const longitudInmuebleSolicitud = document.getElementById("form-activo-radicacion-longitud")
const latitudInmuebleSolicitud = document.getElementById("form-activo-radicacion-latitud")

let coordenadasInmueble

var layers = new GeoLayers();

window.onload = init();


function init() {
  const map = new ol.Map({
    view: new ol.View({
      center: [-74.1, 4.65],
      zoom: 11,
      projection: "EPSG:4326",
    }),
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM(),
      }),
    ],
    target: "mapLocRadication",
  });
  const divUbicacionInmueble = document.getElementById("titleCoorSelected");
  const contUbicacioninm = document.querySelector(".seleccionLocalizacion");

  const inmuebleCoordenada = new ol.Overlay({
    element: contUbicacioninm,
    positioning: "left",
  });

  const dibujarPunto  = new ol.interaction.Draw({
    type:'Point'
  })

  map.addInteraction(dibujarPunto)

  btnGuardar.onclick = function(){
    console.log(coordenadasInmueble.coordinate[0].toString());
    longitudInmuebleSolicitud.value = coordenadasInmueble.coordinate[0].toString()
    latitudInmuebleSolicitud.value = coordenadasInmueble.coordinate[1].toString()

   
    inmuebleCoordenada.setPosition(undefined)
    
    return false
  }

  btnCancelar.onclick = function(){
    inmuebleCoordenada.setPosition(undefined)
    close.blur()
    return false
  }

  map.addOverlay(inmuebleCoordenada);

  map.on("click", function (e) {
    coordenadasInmueble = e;
    inmuebleCoordenada.setPosition(coordenadasInmueble.coordinate);

    divUbicacionInmueble.innerHTML = coordenadasInmueble.coordinate;
    
  });
}