"use strict";(self.webpackChunk=self.webpackChunk||[]).push([[8840],{96929:function(i,t,e){var s=e(41564),r=e(87240),a=e(28e3),n=e(73465),o=e(70026),h=e(36634);class u extends n.Ay{constructor(i){super({attributions:(i=i||{}).attributions,interpolate:i.interpolate,projection:i.projection,resolutions:i.resolutions}),this.crossOrigin_=void 0!==i.crossOrigin?i.crossOrigin:null,this.hidpi_=void 0===i.hidpi||i.hidpi,this.url_=i.url,this.imageLoadFunction_=void 0!==i.imageLoadFunction?i.imageLoadFunction:n.VV,this.params_=Object.assign({},i.params),this.imageSize_=[0,0],this.renderedRevision_=0,this.ratio_=void 0!==i.ratio?i.ratio:1.5,this.loaderProjection_=null}getParams(){return this.params_}getImageInternal(i,t,e,s){return void 0===this.url_?null:(this.loader&&this.loaderProjection_===s||(this.loaderProjection_=s,this.loader=(0,o.E)({crossOrigin:this.crossOrigin_,params:this.params_,projection:s,hidpi:this.hidpi_,url:this.url_,ratio:this.ratio_,load:(i,t)=>(this.image.setImage(i),this.imageLoadFunction_(this.image,t),(0,h.D4)(i))})),super.getImageInternal(i,t,e,s))}getImageLoadFunction(){return this.imageLoadFunction_}getUrl(){return this.url_}setImageLoadFunction(i){this.imageLoadFunction_=i,this.changed()}setUrl(i){i!=this.url_&&(this.url_=i,this.loader=null,this.changed())}updateParams(i){Object.assign(this.params_,i),this.changed()}changed(){this.image=null,super.changed()}}var c=u,l=e(12185),d=e(47085);const g=[new l.A({source:new a.A}),new d.A({source:new c({ratio:1,params:{},url:"https://sampleserver6.arcgisonline.com/ArcGIS/rest/services/USA/MapServer"})})];new s.A({layers:g,target:"map",view:new r.Ay({center:[-10997148,4569099],zoom:4})})}},function(i){var t;t=96929,i(i.s=t)}]);
//# sourceMappingURL=arcgis-image.js.map