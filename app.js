'use strict';
(async()=>{
  const $=id=>document.getElementById(id);
  const load=async path=>{const response=await fetch(path);if(!response.ok)throw new Error(`No se pudo cargar ${path}`);return response.json();};
  try{
    const [upz,localities,points,legend]=await Promise.all(['data/upz_priorizacion.geojson','data/localidades_contexto.geojson','data/manzanas_existentes.geojson','data/leyenda.json'].map(load));
    const colors=new Map(legend.map(l=>[l.id,l.color]));
    let selected='',category='';
    const map=L.map('map',{scrollWheelZoom:false});
    const base=L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);
    const context=L.geoJSON(localities,{interactive:false,style:{color:'#73828e',weight:1,fillColor:'#e5e9ec',fillOpacity:.35}}).addTo(map);
    const style=f=>({color:f.properties.upz_codigo===selected?'#12283e':'#687b86',weight:f.properties.upz_codigo===selected?3:.7,fillColor:colors.get(f.properties.prioridad_id),fillOpacity:(!category||category===f.properties.prioridad_id)?0.82:0.12});
    // Build text nodes instead of interpreting data fields as HTML.
    function info(f){const p=f.properties,box=document.createElement('div'),title=document.createElement('strong'),body=document.createElement('p');title.textContent=`UPZ ${p.upz_codigo} · ${p.upz_nombre}`;body.textContent=`Prioridad: ${p.prioridad}. ${p.puntaje_publicado===null?'Sin puntaje publicado en la Tabla 3.':`Puntaje publicado: ${p.puntaje_publicado} (posición ${p.posicion_publicada}).`}`;box.append(title,body);return box;}
    const byCode=new Map();
    const layer=L.geoJSON(upz,{style,onEachFeature(f,l){byCode.set(f.properties.upz_codigo,l);l.bindPopup(info(f));l.on('click',()=>select(f.properties.upz_codigo,false));l.on('add',()=>{const el=l.getElement();if(el){el.setAttribute('tabindex','0');el.setAttribute('role','button');el.setAttribute('aria-label',`UPZ ${f.properties.upz_codigo}, ${f.properties.upz_nombre}, prioridad ${f.properties.prioridad}`);el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(f.properties.upz_codigo);}});}});}}).addTo(map);
    const anchors=L.geoJSON(points,{interactive:false,pointToLayer:(_f,latlng)=>L.circleMarker(latlng,{radius:4,color:'#fff',weight:1.5,fillColor:'#12283e',fillOpacity:1,interactive:false})}).addTo(map);
    L.control.layers({'Calles OpenStreetMap':base,'Sin mapa base':L.layerGroup()},{'Prioridad por UPZ':layer,'Localidades (contexto)':context,'Manzanas existentes (27)':anchors},{collapsed:false}).addTo(map);
    map.attributionControl.addAttribution('Polígonos: SDP / IDECA · Categorías: SDMujer (2025), recuperadas de la figura');
    map.fitBounds(layer.getBounds(),{padding:[15,15]});
    function select(code,zoom=true){selected=code;$('upz').value=code;layer.setStyle(style);const l=byCode.get(code);if(l){$('detail').replaceChildren(info(l.feature));if(zoom){if(!map.hasLayer(layer))layer.addTo(map);map.fitBounds(l.getBounds(),{padding:[30,30],maxZoom:14});l.openPopup();}}else{map.closePopup();$('detail').textContent='Seleccione una UPZ para consultar su categoría y, cuando esté publicado, su puntaje.';}}
    for(const f of [...upz.features].sort((a,b)=>a.properties.upz_nombre.localeCompare(b.properties.upz_nombre,'es'))){const p=f.properties;const o=document.createElement('option');o.value=p.upz_codigo;o.textContent=`${p.upz_codigo} · ${p.upz_nombre}`;$('upz').append(o);}
    for(const item of legend.filter(l=>l.upz)){const o=document.createElement('option');o.value=item.id;o.textContent=item.etiqueta;$('category').append(o);const row=document.createElement('span'),chip=document.createElement('i');chip.style.background=item.color;row.append(chip,document.createTextNode(`${item.etiqueta} (${item.upz})`));$('legend').append(row);}
    $('upz').addEventListener('change',e=>{select(e.target.value);if(!e.target.value)map.fitBounds(layer.getBounds());});
    $('category').addEventListener('change',e=>{category=e.target.value;layer.setStyle(style);});
    $('fit-upz').addEventListener('click',()=>map.fitBounds(layer.getBounds(),{padding:[15,15]}));
    $('fit-district').addEventListener('click',()=>map.fitBounds(context.getBounds(),{padding:[15,15]}));
    $('fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('map-shell').requestFullscreen();}catch{$('detail').textContent='La pantalla completa no está disponible en este navegador.';}});
    document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Salir de pantalla completa':'Pantalla completa';map.invalidateSize();});
  }catch(error){$('detail').textContent=`${error.message}. Abra esta carpeta con un servidor HTTP local; consulte README.md.`;}
})();
