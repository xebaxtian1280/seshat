"use strict";(self.webpackChunk=self.webpackChunk||[]).push([[887],{16058:function(e,t,n){var o=n(41564),r=n(93595),c=n(12185),i=n(87240),p=n(55238),a=n(28487),s=n(61341);const u=document.getElementById("popup"),l=document.getElementById("popup-content"),m=document.getElementById("popup-closer"),w=new r.A({element:u,autoPan:{animation:{duration:250}}});m.onclick=function(){return w.setPosition(void 0),m.blur(),!1};new o.A({layers:[new c.A({source:new p.A({attributions:'<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',url:"https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=get_your_own_D6rA4zTHduk6KOKTXzGB",tileSize:512})})],overlays:[w],target:"map",view:new i.Ay({center:[0,0],zoom:2})}).on("singleclick",(function(e){const t=e.coordinate,n=(0,s.xi)((0,a.WP)(t));l.innerHTML="<p>You clicked here:</p><code>"+n+"</code>",w.setPosition(t)}))}},function(e){var t;t=16058,e(e.s=t)}]);
//# sourceMappingURL=popup.js.map