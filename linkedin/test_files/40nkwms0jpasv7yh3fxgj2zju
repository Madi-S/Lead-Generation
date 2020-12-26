!(function(e){"function"==typeof define&&define.amd?define(e):e()})((function(){"use strict"
function e(t){return(e="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(t)}function t(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function r(e,t){for(var r=0;r<t.length;r++){var n=t[r]
n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function n(e,t,n){return t&&r(e.prototype,t),n&&r(e,n),e}function s(e){return(s=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function o(e,t){return(o=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function i(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called")
return e}function a(e,t,r){return(a="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=(function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=s(e)););return e})(e,t)
if(n){var o=Object.getOwnPropertyDescriptor(n,t)
return o.get?o.get.call(r):o.value}})(e,t,r||e)}function u(e,t,r,n){this.type=e,this.bubbles=t,this.cancelable=r,this.target=n}u.prototype={stopPropagation:function(){},preventDefault:function(){this.defaultPrevented=!0}}
var l={100:"Continue",101:"Switching Protocols",200:"OK",201:"Created",202:"Accepted",203:"Non-Authoritative Information",204:"No Content",205:"Reset Content",206:"Partial Content",300:"Multiple Choice",301:"Moved Permanently",302:"Found",303:"See Other",304:"Not Modified",305:"Use Proxy",307:"Temporary Redirect",400:"Bad Request",401:"Unauthorized",402:"Payment Required",403:"Forbidden",404:"Not Found",405:"Method Not Allowed",406:"Not Acceptable",407:"Proxy Authentication Required",408:"Request Timeout",409:"Conflict",410:"Gone",411:"Length Required",412:"Precondition Failed",413:"Request Entity Too Large",414:"Request-URI Too Long",415:"Unsupported Media Type",416:"Requested Range Not Satisfiable",417:"Expectation Failed",422:"Unprocessable Entity",500:"Internal Server Error",501:"Not Implemented",502:"Bad Gateway",503:"Service Unavailable",504:"Gateway Timeout",505:"HTTP Version Not Supported"},p={"Accept-Charset":!0,"Accept-Encoding":!0,Connection:!0,"Content-Length":!0,Cookie:!0,Cookie2:!0,"Content-Transfer-Encoding":!0,Date:!0,Expect:!0,Host:!0,"Keep-Alive":!0,Referer:!0,TE:!0,Trailer:!0,"Transfer-Encoding":!0,Upgrade:!0,"User-Agent":!0,Via:!0}
function h(e,t){t.addEventListener(e,(function(r){var n=t["on"+e]
n&&"function"==typeof n&&n.call(r.target,r)}))}function d(){this._eventListeners={}
for(var e=["loadstart","progress","load","abort","loadend"],t=e.length-1;0<=t;t--)h(e[t],this)}function c(){d.call(this),this.readyState=c.UNSENT,this.requestHeaders={},this.requestBody=null,this.status=0,this.statusText="",this.upload=new d}d.prototype={addEventListener:function(e,t){this._eventListeners[e]=this._eventListeners[e]||[],this._eventListeners[e].push(t)},removeEventListener:function(e,t){for(var r=this._eventListeners[e]||[],n=0,s=r.length;n<s;++n)if(r[n]==t)return r.splice(n,1)},dispatchEvent:function(e){for(var t=e.type,r=this._eventListeners[t]||[],n=0;n<r.length;n++)"function"==typeof r[n]?r[n].call(this,e):r[n].handleEvent(e)
return!!e.defaultPrevented},_progress:function(e,t,r){var n=new u("progress")
n.target=this,n.lengthComputable=e,n.loaded=t,n.total=r,this.dispatchEvent(n)}},c.prototype=new d
var f={UNSENT:c.UNSENT=0,OPENED:c.OPENED=1,HEADERS_RECEIVED:c.HEADERS_RECEIVED=2,LOADING:c.LOADING=3,DONE:c.DONE=4,async:!0,withCredentials:!1,open:function(e,t,r,n,s){this.method=e,this.url=t,this.async="boolean"!=typeof r||r,this.username=n,this.password=s,this.responseText=null,this.response=this.responseText,this.responseXML=null,this.responseURL=t,this.requestHeaders={},this.sendFlag=!1,this._readyStateChange(c.OPENED)},setRequestHeader:function(e,t){if(v(this),p[e]||/^(Sec-|Proxy-)/.test(e))throw new Error('Refused to set unsafe header "'+e+'"')
this.requestHeaders[e]?this.requestHeaders[e]+=","+t:this.requestHeaders[e]=t},send:function(e){if(v(this),!/^(get|head)$/i.test(this.method)){var t=!1
Object.keys(this.requestHeaders).forEach((function(e){"content-type"===e.toLowerCase()&&(t=!0)})),t||(e||"").toString().match("FormData")||(this.requestHeaders["Content-Type"]="text/plain;charset=UTF-8"),this.requestBody=e}this.errorFlag=!1,this.sendFlag=this.async,this._readyStateChange(c.OPENED),"function"==typeof this.onSend&&this.onSend(this),this.dispatchEvent(new u("loadstart",!1,!1,this))},abort:function(){this.aborted=!0,this.responseText=null,this.response=this.responseText,this.errorFlag=!0,this.requestHeaders={},this.dispatchEvent(new u("abort",!1,!1,this)),this.readyState>c.UNSENT&&this.sendFlag&&(this._readyStateChange(c.UNSENT),this.sendFlag=!1),"function"==typeof this.onerror&&this.onerror()},getResponseHeader:function(e){if(this.readyState<c.HEADERS_RECEIVED)return null
if(/^Set-Cookie2?$/i.test(e))return null
for(var t in e=e.toLowerCase(),this.responseHeaders)if(t.toLowerCase()==e)return this.responseHeaders[t]
return null},getAllResponseHeaders:function(){if(this.readyState<c.HEADERS_RECEIVED)return""
var e=""
for(var t in this.responseHeaders)this.responseHeaders.hasOwnProperty(t)&&!/^Set-Cookie2?$/i.test(t)&&(e+=t+": "+this.responseHeaders[t]+"\r\n")
return e},overrideMimeType:function(e){"string"==typeof e&&(this.forceMimeType=e.toLowerCase())},_readyStateChange:function(e){this.readyState=e,"function"==typeof this.onreadystatechange&&this.onreadystatechange(new u("readystatechange")),this.dispatchEvent(new u("readystatechange")),this.readyState==c.DONE&&this.dispatchEvent(new u("load",!1,!1,this)),this.readyState!=c.UNSENT&&this.readyState!=c.DONE||this.dispatchEvent(new u("loadend",!1,!1,this))},_setResponseHeaders:function(e){for(var t in this.responseHeaders={},e)e.hasOwnProperty(t)&&(this.responseHeaders[t]=e[t])
this.forceMimeType&&(this.responseHeaders["Content-Type"]=this.forceMimeType),this.async?this._readyStateChange(c.HEADERS_RECEIVED):this.readyState=c.HEADERS_RECEIVED},_setResponseBody:function(e){!(function(e){if(e.readyState==c.DONE)throw new Error("Request done")})(this),(function(e){if(e.async&&e.readyState!=c.HEADERS_RECEIVED)throw new Error("No headers received")})(this),(function(e){if("string"!=typeof e){var t=new Error("Attempted to respond to fake XMLHttpRequest with "+e+", which is not a string.")
throw t.name="InvalidBodyException",t}})(e)
var t=this.chunkSize||10,r=0
for(this.responseText="",this.response=this.responseText;this.async&&this._readyStateChange(c.LOADING),this.responseText+=e.substring(r,r+t),this.response=this.responseText,(r+=t)<e.length;);var n,s,o=this.getResponseHeader("Content-Type")
if(this.responseText&&(!o||/(text\/xml)|(application\/xml)|(\+xml)/.test(o)))try{this.responseXML=(n=this.responseText,"undefined"!=typeof DOMParser?s=(new DOMParser).parseFromString(n,"text/xml"):((s=new ActiveXObject("Microsoft.XMLDOM")).async="false",s.loadXML(n)),s)}catch(e){}this.async?this._readyStateChange(c.DONE):this.readyState=c.DONE},respond:function(e,t,r){this._setResponseHeaders(t||{}),this.status="number"==typeof e?e:200,this.statusText=l[this.status],this._setResponseBody(r||"")}}
for(var y in f)c.prototype[y]=f[y]
function v(e){if(e.readyState!==c.OPENED)throw new Error("INVALID_STATE_ERR")
if(e.sendFlag)throw new Error("INVALID_STATE_ERR")}function m(){return window&&window.performance&&window.performance.mark&&window.performance.measure&&window.performance.getEntriesByName}var q=Number.MAX_VALUE,g=(function(){!(function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function")
e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&o(e,t)})(r,c)
var e=(function(e){var t=(function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1
if(Reflect.construct.sham)return!1
if("function"==typeof Proxy)return!0
try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(n){return!1}})()
return function(){var r,n,o=s(e)
if(t){var a=s(this).constructor
r=Reflect.construct(o,arguments,a)}else r=o.apply(this,arguments)
return!(n=r)||"object"!=typeof n&&"function"!=typeof n?i(this):n}})(r)
function r(){var n
return t(this,r),(n=e.call(this)).chunkSize=q,c.call(i(n)),n}return n(r,[{key:"open",value:function(){a(s(r.prototype),"open",this).apply(this,arguments),this.method=this.method&&this.method.toUpperCase()}},{key:"_createMarkerName",value:function(e){return"mark_bigpipe_".concat(e)}},{key:"fulfillPendingRequest",value:function(e){var t=_bpr.requestSupervisor.responseTable[e],r=t.responseData,n=t.status
if(m()){var s=this._createMarkerName(e),o="".concat(s,"_phase"),i="".concat(s,"_start"),a="".concat(s,"_end")
0<window.performance.getEntriesByName(i).length?(window.performance.mark(a),window.performance.measure(o,i,a)):window.jet&&window.jet.error(new Error("start marker not found: ".concat(i)),["bpr","perf_measure"],!1)}this.respond(n,{"Content-Type":"application/json"},r)}},{key:"send",value:function(e){var t=this.url,n=this.method,o=this.requestHeaders,i=t,u=_bpr.isQueryTunneledRequest(n,o)
if(m()){var l=this._createMarkerName(t)
window.performance.mark("".concat(l,"_start"))}if(u&&(t=_bpr.generatUrlForPostRequest(t,e)),_bpr.isPresentInTable("response",t))this.fulfillPendingRequest(t),_bpr.deleteJqueryRequest(t)
else{var p=this.method,h=this.upload,d=this.responseType,c=this.username,f=void 0===c?"":c,y=this.password,v=void 0===y?"":y,q={url:i,method:p,async:this.async,username:f,password:v,timeout:this.timeout,requestHeaders:this.requestHeaders,withCredentials:this.withCredentials,xhr:this,isJqueryRequest:!1,postData:"POST"===p||"PUT"===p?e:null,events:{onreadystatechange:this.onreadystatechange,onload:this.onload,onerror:this.onerror,onprogress:this.onprogress,onloadstart:this.onloadstart,onabort:this.onabort,onloadend:this.onloadend,ontimeout:this.ontimeout},uploadEvents:{onload:h.onload,onerror:h.onerror,onprogress:h.onprogress,onloadstart:h.onloadstart,onabort:h.onabort,onloadend:h.onloadend,ontimeout:h.ontimeout}}
d&&(q.responseType=d)
var g=_bpr.isPresentInTable("jQuery",t)
if(g&&(q.isJqueryRequest=!0,q.jqueryOptions=g.slice(-1)[0]),_bpr.requestSupervisor.terminatorCalled||_bpr.isPassThroughRequest(p,u)||_bpr.isBlacklistedUrl(t))return _bpr.refireRequest(q),void _bpr.deleteJqueryRequest(t)
_bpr.isPresentInTable("request",t)||(_bpr.requestSupervisor.requestTable[t]=[]),_bpr.requestSupervisor.requestTable[t].push(q),a(s(r.prototype),"send",this).call(this,e)}}}]),r})()
function R(e,t){var r=document.querySelector('meta[name="'.concat(e,'"]'))
return r&&r.getAttribute("content")||t}var E=null,w=R("bigpipeResponseTimeout",12e3),S=R("bigpipeBlacklistUrls",""),b=R("isQueryTunnelRequestSupported",!1),_="POST",T="mark_data_streaming",P=(function(){function r(){if(t(this,r),E)throw new Error("There can be only one instance of RequestManager.")
var e=setTimeout(this._handleResponseTimeout.bind(this),w),n=[]
return""!==S&&(n=JSON.parse(S).map((function(e){return new RegExp(e)}))),this.requestSupervisor={requestTable:{},responseTable:{},jqueryRequests:{},originalXHR:null,originalJqueryAjax:null,terminatorCalled:!1,pageRendered:!1,isInitialPageLoaded:!1,responseTimer:e,refiredRequestUrls:[],blacklistUrlsRegex:n,isQueryTunnelRequestSupported:b,VERSION:1},this._injectFakeXHR(),(E=this).isFirstDataletSeen=!1,this._setupRequestSupervisorEventListener(),E}return n(r,[{key:"_measureStreamingStart",value:function(){this.isFirstDataletSeen||(this.isFirstDataletSeen=!0,m()&&window.performance.mark("".concat(T,"_start")))}},{key:"_measureStreamingEnd",value:function(){if(m()){var e="".concat(T,"_start"),t="".concat(T,"_end"),r="".concat(T,"_phase")
0<window.performance.getEntriesByName(e).length&&(window.performance.mark(t),window.performance.measure(r,e,t))}}},{key:"_setupRequestSupervisorEventListener",value:function(){var e="datalet-bpr-guid",t=e.length,r=this
document.addEventListener("load",(function n(s){var o=s.target
if("IMG"===o.tagName){var i=o.getAttribute("class")
if(1===(i=i?i.split(" "):[]).length&&i[0].substring(0,t)===e){r._measureStreamingStart()
var a=i[0]
r.response(a)}1===i.length&&"terminatorlet"===i[0]&&(r._measureStreamingEnd(),r.done(),document.removeEventListener("load",n,!0))}}),!0)}},{key:"isBlacklistedUrl",value:function(e){return this.requestSupervisor.blacklistUrlsRegex.some((function(t){return t.test(e)}),this)}},{key:"isPresentInTable",value:function(e,t){var r=null
if("request"===e)r=this.requestSupervisor.requestTable
else if("response"===e)r=this.requestSupervisor.responseTable
else{if("jQuery"!==e)throw new Error("Invalid table name.")
r=this.requestSupervisor.jqueryRequests}return r[t]}},{key:"deleteJqueryRequest",value:function(e){this.isPresentInTable("jQuery",e)&&delete this.requestSupervisor.jqueryRequests[e]}},{key:"_deleteRequest",value:function(e){delete this.requestSupervisor.requestTable[e],this.deleteJqueryRequest(e)}},{key:"_handleResponseTimeout",value:function(){console.info("Terminator datalet is not seen within ".concat(w," ms."))}},{key:"_injectFakeXHR",value:function(){this.requestSupervisor.originalXHR=window.XMLHttpRequest,window.XMLHttpRequest=g}},{key:"response",value:function(t){var r=t
"object"!==e(t)&&(r=JSON.parse(this._getResponseData(t)))
var n=r.request,s=r.status,o=this._getResponseData(r.body)
r.method&&r.method===_&&(n=this.generatUrlForPostRequest(n,r.encodedRequestBody))
var i={url:n,status:s,responseData:o}
this.requestSupervisor.responseTable[n]=i
var a=this.requestSupervisor.requestTable[n]
a&&(a.forEach((function(e){e.xhr.fulfillPendingRequest(n)})),this._deleteRequest(n))}},{key:"_getResponseData",value:function(e){var t=document.getElementById(e),r={}
return t&&(t.normalize(),r=t.firstChild.nodeValue),r}},{key:"done",value:function(){if(this.requestSupervisor.terminatorCalled)throw new Error("Terminator cannot be called multiple times.")
this.requestSupervisor.terminatorCalled=!0,this._clearResponseTimer(),this._fullFillPendingRequests(),this._refirePendingRequests(),this.requestSupervisor.pageRendered&&this._reset()}},{key:"_fullFillPendingRequests",value:function(){var e=this,t=this.requestSupervisor.requestTable
Object.keys(t).forEach((function(t){if(e.isPresentInTable("response",t)){var r=e.requestSupervisor.requestTable[t]
r&&(r.forEach((function(e){e.xhr.fulfillPendingRequest(t)})),e._deleteRequest(t))}}))}},{key:"_refirePendingRequests",value:function(){var e=this
Object.keys(this.requestSupervisor.requestTable).forEach((function(t){e.requestSupervisor.requestTable[t].forEach((function(t){e.refireRequest(t)}),e)}),this)}},{key:"_copyXhrData",value:function(e,t){var r=t.responseType
e.status=t.status,e.headers=t.headers,e.getAllResponseHeaders=function(){return t.getAllResponseHeaders()},e.response=t.response,e.responseURL=t.responseURL,"document"===r?e.responseXML=t.responseXML:""!==r&&"text"!==r||(e.responseText=t.responseText)}},{key:"refireRequest",value:function(e){var t=e.xhr,r=e.url,n=e.jqueryOptions,s=e.requestHeaders,o=e.timeout,i=e.events,a=e.responseType,u=e.withCredentials,l=window.XMLHttpRequest
if(window.XMLHttpRequest=this.requestSupervisor.originalXHR,e.isJqueryRequest){var p=n.originalPromise
this.requestSupervisor.originalJqueryAjax(n).then((function(e,t,r){p.resolve(e,t,r)}),(function(e,t,r){p.reject(e,t,r)}))}else{var h=new XMLHttpRequest,d=t,c=this
for(var f in h.open(e.method,r,e.async,e.username,e.password),s)h.setRequestHeader(f,s[f])
o&&(h.timeout=o),a&&(h.responseType=a),void 0!==u&&(h.withCredentials=u),Object.keys(i).forEach((function(e){"function"==typeof i[e]&&(h[e]=function(){!d||"onreadystatechange"!==e&&"onload"!==e||c._copyXhrData(d,h),i[e].call(h)})}))
var y=e.uploadEvents
Object.keys(y).forEach((function(e){"function"==typeof y[e]&&(h.upload[e]=function(){d&&"onload"===e&&c._copyXhrData(d,h),y[e].call(h)})})),e.postData?h.send(e.postData):h.send()}window.XMLHttpRequest=l}},{key:"_resetRequestSupervisor",value:function(){this.requestSupervisor.responseTable={},this.requestSupervisor.requestTable={},this.requestSupervisor.jqueryRequests={}}},{key:"rendered",value:function(){if(this.requestSupervisor.pageRendered)throw new Error("Initial page render cannot be called multiple times.")
this.requestSupervisor.pageRendered=!0,this.requestSupervisor.terminatorCalled&&this._reset()}},{key:"_reset",value:function(){if(this.requestSupervisor.isInitialPageLoaded)throw new Error("Request manager cannot be reset multiple times.")
this._resetRequestSupervisor(),this.requestSupervisor.isInitialPageLoaded=!0,window.XMLHttpRequest=this.requestSupervisor.originalXHR,"undefined"!=typeof jQuery&&(jQuery.ajax=this.requestSupervisor.originalJqueryAjax)}},{key:"_clearResponseTimer",value:function(){var e=this.requestSupervisor.responseTimer
e&&(clearTimeout(e),this.requestSupervisor.responseTimer=null)}},{key:"isQueryTunneledRequest",value:function(e,t){var r=1<arguments.length&&void 0!==t?t:{}
return"true"===this.requestSupervisor.isQueryTunnelRequestSupported&&e===_&&"GET"===r["x-http-method-override"]}},{key:"generatUrlForPostRequest",value:function(e,t){return t?e+";"+t:e}},{key:"isPassThroughRequest",value:function(e,t){return"GET"!==e&&!t}}]),r})()
window._bpr=new P,window._getRenderMode=function(){if(!window||"node"!==window.appEnvironment){var e=document.getElementsByName("renderingMode")
if(1!==e.length)return
return e[0].getAttribute("data-mode")}},window._isBigPipeMode=function(){var e=window._getRenderMode()
return-1<["BIGPIPE","SSRPIPE"].indexOf(e)}}))

//# sourceMappingURL=bigpipe.min.map