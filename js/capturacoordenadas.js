const btnGuardar = document.querySelector(".btnSaveCoordinates");
const btnCancelar = document.querySelector(".btnCancelCoordinates");
const longitudInmuebleSolicitud = document.getElementById("form-activo-radicacion-longitud")
const latitudInmuebleSolicitud = document.getElementById("form-activo-radicacion-latitud")

let coordenadasInmueble

var layers = new GeoLayers();

window.onload = init();

function init() {
  const map = new ol.Map({
    target: "mapLocRadication",
    view: new ol.View({
      center: [-74.1, 4.65],
      zoom: 11,
      projection: "EPSG:4326",
    }),
    layers: [//layers.ObtenerLayersBase()
      
       new ol.layer.Group({
          title: 'Mapa base',
          layers: layers.ObtenerLayersBase()
          
       }),
       new ol.layer.Group({
        title: 'Tematicos',
        layers: 
          layers.CargarGeoJson()      
        
     })

    ]

  });

  var vector = new ol.layer.Vector({ 
    title:'Capa de Dibujo',
    source: new ol.source.Vector()})
  map.addLayer(vector)

  var controlModificar = new ol.interaction.Modify({source:vector.getSource()})
  map.addInteraction(controlModificar)
    
  var layerSwitcher = new ol.control.LayerSwitcher({
    tiplabel: 'Leyenda',
    groupSelecStyle: 'children'
  })

  map.addControl(layerSwitcher)

  var mainBar = new ol.control.Bar()
  map.addControl(mainBar)

  mainBar.addControl(new ol.control.FullScreen())
  mainBar.addControl(new ol.control.Rotate())
  mainBar.setPosition('top-left')

  var drawBar = new ol.control.Bar({
    Group: true,
    toggleOne:true
  })

  mainBar.addControl(drawBar)  

  var controlDraw = new ol.control.Toggle({
    title:'Ubicar Avaluo',
    html: '<i class="fas fa-map-marker-alt"></i>',
    active: true,
    interaction: new ol.interaction.Draw({
      type:'Point',
      source: vector.getSource()
    }),
    onToggle: function(active){
      console.log(active);
    },
    // condition: function(){
    //   if (vector.getLength>0){
    //     alert('Ya existe una localizacion')
    //     return true
    //   }else{
    //     return false
    //   }
    // }

  })

  drawBar.addControl(controlDraw)

  var controlSelect = new ol.control.Toggle({
    title:'Seleccionar puto',
    html: '<i class="fa-solid fa-hand-point-up"></i>',
    interaction: new ol.interaction.Select(),
    bar: new ol.control.Bar({
      controls:[
        new ol.control.TextButton({
          title:'Eliminar',
          html:'Eliminar',
          handleClick: function(){
            
            var features = controlSelect.getInteraction().getFeatures()
            console.log(features.getLength());
            if(features.getLength()==0){
              alert('Selecionar un punto')
            }

            for(var i=0, f;f=features.item(i);i++){

              vector.getSource().removeFeature(f)

            }

            controlSelect.getInteraction().getFeatures().clear()

          }
        })
      ]
    })
  })

  drawBar.addControl(controlSelect)

  var controlBusqueda = new ol.control.SearchFeature({
    source: layers.vectorGeoJson,
    property: 'id_android_store'
  })

  map.addControl(controlBusqueda)

  var select = new ol.interaction.Select({})
  map.addControl(select)

  controlBusqueda.on('select', function(e){
    select.getFeatures().clear()
    select.getFeatures().push(e.search)

    var p = e.search.getGeometry().getFirstCoordinate()
    map.getView().animate({
      center:p,
      zoom:19
    })

  })

  const divUbicacionInmueble = document.getElementById("titleCoorSelected");
  const contUbicacioninm = document.querySelector(".seleccionLocalizacion");

  const inmuebleCoordenada = new ol.Overlay({
    element: contUbicacioninm,
    positioning: "left",
  });

  // const dibujarPunto  = new ol.interaction.Draw({
  //   type:'Point',
  //   source: vector.getSource()
  // })

  // map.addInteraction(dibujarPunto)

  btnGuardar.onclick = function(){

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

  // map.on("click", function (e) {

  
  //     coordenadasInmueble = e;
  //   inmuebleCoordenada.setPosition(coordenadasInmueble.coordinate);
  //   divUbicacionInmueble.innerHTML = coordenadasInmueble.coordinate;
    
    
  // });
}