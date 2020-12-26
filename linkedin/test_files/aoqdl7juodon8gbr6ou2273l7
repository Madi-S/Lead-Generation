define("@glimmer/component/-private/base-component-manager",["exports","@babel/runtime/helpers/esm/defineProperty","@glimmer/component/-private/component"],function(e,t,n){"use strict"
Object.defineProperty(e,"__esModule",{value:!0})
e.default=function(e,n,r){return class{static create(e){let t=n(e)
return new this(t)}constructor(n){(0,t.default)(this,"capabilities",r)
e(this,n)}createComponent(e,t){0
return new e(n(this),t.named)}getContext(e){return e}}}})
define("@glimmer/component/-private/component",["exports","@babel/runtime/helpers/esm/defineProperty","@glimmer/component/-private/owner"],function(e,t,n){"use strict"
Object.defineProperty(e,"__esModule",{value:!0})
e.setDestroying=function(e){r.set(e,!0)}
e.setDestroyed=function(e){o.set(e,!0)}
e.default=e.ARGS_SET=void 0
const r=new WeakMap,o=new WeakMap
let s
e.ARGS_SET=s
0
e.default=class{constructor(e,s){(0,t.default)(this,"args",void 0)
this.args=s;(0,n.setOwner)(this,e)
r.set(this,!1)
o.set(this,!1)}get isDestroying(){return r.get(this)}get isDestroyed(){return o.get(this)}willDestroy(){}}})
define("@glimmer/component/-private/ember-component-manager",["exports","@glimmer/component/-private/base-component-manager","@glimmer/component/-private/component"],function(e,t,n){"use strict"
Object.defineProperty(e,"__esModule",{value:!0})
e.default=void 0
const r=Ember._componentManagerCapabilities("3.13",{destructor:!0,asyncLifecycleCallbacks:!1,updateHook:!1})
class o extends((0,t.default)(Ember.setOwner,Ember.getOwner,r)){destroyComponent(e){if(e.isDestroying)return
let t=Ember.meta(e)
t.setSourceDestroying();(0,n.setDestroying)(e)
Ember.run.schedule("actions",e,e.willDestroy)
Ember.run.schedule("destroy",this,s,e,t)}}function s(e,t){if(!e.isDestroyed){Ember.destroy(e)
t.setSourceDestroyed();(0,n.setDestroyed)(e)}}0
var i=o
e.default=i})
define("@glimmer/component/-private/owner",["exports"],function(e){"use strict"
Object.defineProperty(e,"__esModule",{value:!0})
e.setOwner=void 0
var t=Ember.setOwner
e.setOwner=t})
define("@glimmer/component/index",["exports","@glimmer/component/-private/ember-component-manager","@glimmer/component/-private/component"],function(e,t,n){"use strict"
Object.defineProperty(e,"__esModule",{value:!0})
e.default=void 0
let r=n.default
0
Ember._setComponentManager(e=>new t.default(e),r)
var o=r
e.default=o})

//# sourceMappingURL=engine-vendor.map