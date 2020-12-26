var BABEL_POLYFILL_MODULES={}
function __babelPolyfillDefine(t,e,n){var r={},o=e.map((function(t){return"exports"===t?r:BABEL_POLYFILL_MODULES[t]}))
n.apply(null,o)
BABEL_POLYFILL_MODULES[t]=r}__babelPolyfillDefine("shared.js",["exports"],(function(t){"use strict"
function e(t,e){return t(e={exports:{}},e.exports),e.exports}var n=e((function(t){var e=t.exports="undefined"!=typeof window&&window.Math==Math?window:"undefined"!=typeof self&&self.Math==Math?self:Function("return this")()
"number"==typeof __g&&(__g=e)})),r=e((function(t){var e=t.exports={version:"2.6.11"}
"number"==typeof __e&&(__e=e)})),o=(r.version,function(t){return"object"==typeof t?null!==t:"function"==typeof t}),i=function(t){if(!o(t))throw TypeError(t+" is not an object!")
return t},u=function(t){try{return!!t()}catch(e){return!0}},a=!u((function(){return 7!=Object.defineProperty({},"a",{get:function(){return 7}}).a})),c=n.document,f=o(c)&&o(c.createElement),l=function(t){return f?c.createElement(t):{}},s=!a&&!u((function(){return 7!=Object.defineProperty(l("div"),"a",{get:function(){return 7}}).a})),p=function(t,e){if(!o(t))return t
var n,r
if(e&&"function"==typeof(n=t.toString)&&!o(r=n.call(t)))return r
if("function"==typeof(n=t.valueOf)&&!o(r=n.call(t)))return r
if(!e&&"function"==typeof(n=t.toString)&&!o(r=n.call(t)))return r
throw TypeError("Can't convert object to primitive value")},d=Object.defineProperty,y={f:a?Object.defineProperty:function(t,e,n){i(t)
e=p(e,!0)
i(n)
if(s)try{return d(t,e,n)}catch(r){}if("get"in n||"set"in n)throw TypeError("Accessors not supported!")
"value"in n&&(t[e]=n.value)
return t}},h=function(t,e){return{enumerable:!(1&t),configurable:!(2&t),writable:!(4&t),value:e}},v=a?function(t,e,n){return y.f(t,e,h(1,n))}:function(t,e,n){t[e]=n
return t},m={}.hasOwnProperty,g=function(t,e){return m.call(t,e)},L=0,S=Math.random(),_=function(t){return"Symbol(".concat(void 0===t?"":t,")_",(++L+S).toString(36))},O=e((function(t){var e=n["__core-js_shared__"]||(n["__core-js_shared__"]={});(t.exports=function(t,n){return e[t]||(e[t]=void 0!==n?n:{})})("versions",[]).push({version:r.version,mode:"global",copyright:"© 2019 Denis Pushkarev (zloirock.ru)"})})),b=O("native-function-to-string",Function.toString),$=e((function(t){var e=_("src"),o=(""+b).split("toString")
r.inspectSource=function(t){return b.call(t)};(t.exports=function(t,r,i,u){var a="function"==typeof i
a&&(g(i,"name")||v(i,"name",r))
if(t[r]!==i){a&&(g(i,e)||v(i,e,t[r]?""+t[r]:o.join(String(r))))
if(t===n)t[r]=i
else if(u)t[r]?t[r]=i:v(t,r,i)
else{delete t[r]
v(t,r,i)}}})(Function.prototype,"toString",(function(){return"function"==typeof this&&this[e]||b.call(this)}))})),M=function(t){if("function"!=typeof t)throw TypeError(t+" is not a function!")
return t},w=function(t,e,n){M(t)
if(void 0===e)return t
switch(n){case 1:return function(n){return t.call(e,n)}
case 2:return function(n,r){return t.call(e,n,r)}
case 3:return function(n,r,o){return t.call(e,n,r,o)}}return function(){return t.apply(e,arguments)}},P=function(t,e,o){var i,u,a,c,f=t&P.F,l=t&P.G,s=t&P.S,p=t&P.P,d=t&P.B,y=l?n:s?n[e]||(n[e]={}):(n[e]||{}).prototype,h=l?r:r[e]||(r[e]={}),m=h.prototype||(h.prototype={})
l&&(o=e)
for(i in o){a=((u=!f&&y&&void 0!==y[i])?y:o)[i]
c=d&&u?w(a,n):p&&"function"==typeof a?w(Function.call,a):a
y&&$(y,i,a,t&P.U)
h[i]!=a&&v(h,i,c)
p&&m[i]!=a&&(m[i]=a)}}
n.core=r
P.F=1
P.G=2
P.S=4
P.P=8
P.B=16
P.W=32
P.U=64
P.R=128
var T=P,j={}.toString,E=function(t){return j.call(t).slice(8,-1)},k=Math.ceil,I=Math.floor,x=function(t){return isNaN(t=+t)?0:(t>0?I:k)(t)},F=Math.min,A=function(t){return t>0?F(x(t),9007199254740991):0},C=e((function(t){var e=O("wks"),r=n.Symbol,o="function"==typeof r;(t.exports=function(t){return e[t]||(e[t]=o&&r[t]||(o?r:_)("Symbol."+t))}).store=e})),D=function(t){if(null==t)throw TypeError("Can't call method on  "+t)
return t},B=function(t){return Object(D(t))},G=C("unscopables"),R=Array.prototype
null==R[G]&&v(R,G,{})
var V,N=function(t){R[G][t]=!0},U=Object("z").propertyIsEnumerable(0)?Object:function(t){return"String"==E(t)?t.split(""):Object(t)},H=function(t){return U(D(t))},Y=Math.max,z=Math.min,W=O("keys"),q=function(t){return W[t]||(W[t]=_(t))},J=(V=!1,function(t,e,n){var r,o=H(t),i=A(o.length),u=(function(t,e){return(t=x(t))<0?Y(t+e,0):z(t,e)})(n,i)
if(V&&e!=e){for(;i>u;)if((r=o[u++])!=r)return!0}else for(;i>u;u++)if((V||u in o)&&o[u]===e)return V||u||0
return!V&&-1}),K=q("IE_PROTO"),Q=function(t,e){var n,r=H(t),o=0,i=[]
for(n in r)n!=K&&g(r,n)&&i.push(n)
for(;e.length>o;)g(r,n=e[o++])&&(~J(i,n)||i.push(n))
return i},X="constructor,hasOwnProperty,isPrototypeOf,propertyIsEnumerable,toLocaleString,toString,valueOf".split(","),Z=Object.keys||function(t){return Q(t,X)},tt=q("IE_PROTO"),et=Object.prototype,nt=Object.getPrototypeOf||function(t){t=B(t)
return g(t,tt)?t[tt]:"function"==typeof t.constructor&&t instanceof t.constructor?t.constructor.prototype:t instanceof Object?et:null},rt=y.f,ot=C("toStringTag"),it=function(t,e,n){t&&!g(t=n?t:t.prototype,ot)&&rt(t,ot,{configurable:!0,value:e})},ut=a?Object.defineProperties:function(t,e){i(t)
for(var n,r=Z(e),o=r.length,u=0;o>u;)y.f(t,n=r[u++],e[n])
return t},at=n.document,ct=at&&at.documentElement,ft=q("IE_PROTO"),lt=function(){},st=function(){var t,e=l("iframe"),n=X.length
e.style.display="none"
ct.appendChild(e)
e.src="javascript:";(t=e.contentWindow.document).open()
t.write("<script>document.F=Object<\/script>")
t.close()
st=t.F
for(;n--;)delete st.prototype[X[n]]
return st()},pt=Object.create||function(t,e){var n
if(null!==t){lt.prototype=i(t)
n=new lt
lt.prototype=null
n[ft]=t}else n=st()
return void 0===e?n:ut(n,e)},dt=n.navigator,yt=dt&&dt.userAgent||"",ht=[].slice,vt=/MSIE .\./.test(yt),mt=function(t){return function(e,n){var r=arguments.length>2,o=!!r&&ht.call(arguments,2)
return t(r?function(){("function"==typeof e?e:Function(e)).apply(this,o)}:e,n)}}
T(T.G+T.B+T.F*vt,{setTimeout:mt(n.setTimeout),setInterval:mt(n.setInterval)})
var gt,Lt,St,_t=n.process,Ot=n.setImmediate,bt=n.clearImmediate,$t=n.MessageChannel,Mt=n.Dispatch,wt=0,Pt={},Tt=function(){var t=+this
if(Pt.hasOwnProperty(t)){var e=Pt[t]
delete Pt[t]
e()}},jt=function(t){Tt.call(t.data)}
if(!Ot||!bt){Ot=function(t){for(var e=[],n=1;arguments.length>n;)e.push(arguments[n++])
Pt[++wt]=function(){((function(t,e,n){var r=void 0===n
switch(e.length){case 0:return r?t():t.call(n)
case 1:return r?t(e[0]):t.call(n,e[0])
case 2:return r?t(e[0],e[1]):t.call(n,e[0],e[1])
case 3:return r?t(e[0],e[1],e[2]):t.call(n,e[0],e[1],e[2])
case 4:return r?t(e[0],e[1],e[2],e[3]):t.call(n,e[0],e[1],e[2],e[3])}t.apply(n,e)}))("function"==typeof t?t:Function(t),e)}
gt(wt)
return wt}
bt=function(t){delete Pt[t]}
if("process"==E(_t))gt=function(t){_t.nextTick(w(Tt,t,1))}
else if(Mt&&Mt.now)gt=function(t){Mt.now(w(Tt,t,1))}
else if($t){St=(Lt=new $t).port2
Lt.port1.onmessage=jt
gt=w(St.postMessage,St,1)}else if(n.addEventListener&&"function"==typeof postMessage&&!n.importScripts){gt=function(t){n.postMessage(t+"","*")}
n.addEventListener("message",jt,!1)}else gt="onreadystatechange"in l("script")?function(t){ct.appendChild(l("script")).onreadystatechange=function(){ct.removeChild(this)
Tt.call(t)}}:function(t){setTimeout(w(Tt,t,1),0)}}var Et={set:Ot,clear:bt}
T(T.G+T.B,{setImmediate:Et.set,clearImmediate:Et.clear})
var kt=function(t,e){return{value:e,done:!!t}},It={},xt={}
v(xt,C("iterator"),(function(){return this}))
var Ft=function(t,e,n){t.prototype=pt(xt,{next:h(1,n)})
it(t,e+" Iterator")},At=C("iterator"),Ct=!([].keys&&"next"in[].keys()),Dt=function(){return this},Bt=(function(t,e,n,r,o,i,u){Ft(n,e,r)
var a,c,f,l=function(t){if(!Ct&&t in y)return y[t]
switch(t){case"keys":case"values":return function(){return new n(this,t)}}return function(){return new n(this,t)}},s=e+" Iterator",p="values"==o,d=!1,y=t.prototype,h=y[At]||y["@@iterator"]||o&&y[o],m=h||l(o),g=o?p?l("entries"):m:void 0,L="Array"==e&&y.entries||h
if(L&&(f=nt(L.call(new t)))!==Object.prototype&&f.next){it(f,s,!0)
"function"!=typeof f[At]&&v(f,At,Dt)}if(p&&h&&"values"!==h.name){d=!0
m=function(){return h.call(this)}}(Ct||d||!y[At])&&v(y,At,m)
It[e]=m
It[s]=Dt
if(o){a={values:p?m:l("values"),keys:i?m:l("keys"),entries:g}
if(u)for(c in a)c in y||$(y,c,a[c])
else T(T.P+T.F*(Ct||d),e,a)}return a})(Array,"Array",(function(t,e){this._t=H(t)
this._i=0
this._k=e}),(function(){var t=this._t,e=this._k,n=this._i++
if(!t||n>=t.length){this._t=void 0
return kt(1)}return kt(0,"keys"==e?n:"values"==e?t[n]:[n,t[n]])}),"values")
It.Arguments=It.Array
N("keys")
N("values")
N("entries")
for(var Gt=C("iterator"),Rt=C("toStringTag"),Vt=It.Array,Nt={CSSRuleList:!0,CSSStyleDeclaration:!1,CSSValueList:!1,ClientRectList:!1,DOMRectList:!1,DOMStringList:!1,DOMTokenList:!0,DataTransferItemList:!1,FileList:!1,HTMLAllCollection:!1,HTMLCollection:!1,HTMLFormElement:!1,HTMLSelectElement:!1,MediaList:!0,MimeTypeArray:!1,NamedNodeMap:!1,NodeList:!0,PaintRequestList:!1,Plugin:!1,PluginArray:!1,SVGLengthList:!1,SVGNumberList:!1,SVGPathSegList:!1,SVGPointList:!1,SVGStringList:!1,SVGTransformList:!1,SourceBufferList:!1,StyleSheetList:!0,TextTrackCueList:!1,TextTrackList:!1,TouchList:!1},Ut=Z(Nt),Ht=0;Ht<Ut.length;Ht++){var Yt,zt=Ut[Ht],Wt=Nt[zt],qt=n[zt],Jt=qt&&qt.prototype
if(Jt){Jt[Gt]||v(Jt,Gt,Vt)
Jt[Rt]||v(Jt,Rt,zt)
It[zt]=Vt
if(Wt)for(Yt in Bt)Jt[Yt]||$(Jt,Yt,Bt[Yt],!0)}}t.default=E
t.default$1=o
t.default$2=A
t.default$3=w
t.default$4=C
t.default$5=T
t.default$6=B
t.default$7=M
t.default$8=N
t.default$9=u
t.default$10=!1
t.default$11=n
t.default$12=y
t.default$13=a
t.default$14=Z
t.default$15=H
t.default$16=Q
t.default$17=X
t.default$18=i
t.default$19=h
t.default$20=p
t.default$21=g
t.default$22=s
t.default$23=nt
t.default$24=$
t.default$25=r
t.default$26=x
t.default$27=D
t.default$28=v
t.createCommonjsModule=e
t.default$29=_
t.default$30=O
t.default$31=it
t.default$32=pt
t.default$33=yt}))

//# sourceMappingURL=polyfill-shared.map