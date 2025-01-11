/**
 * Bundled by jsDelivr using Rollup v2.79.1 and Terser v5.19.2.
 * Original file: /npm/react-dom@19.0.0/index.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
import e from"../react@19.0.0/6ae65287.js";var t={exports:{}},r={},i=e;function n(e){var t="https://react.dev/errors/"+e;if(1<arguments.length){t+="?args[]="+encodeURIComponent(arguments[1]);for(var r=2;r<arguments.length;r++)t+="&args[]="+encodeURIComponent(arguments[r])}return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function o(){}var s={d:{f:o,r:function(){throw Error(n(522))},D:o,C:o,L:o,m:o,X:o,S:o,M:o},p:0,findDOMNode:null},f=Symbol.for("react.portal");var c=i.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;function p(e,t){return"font"===e?"":"string"==typeof t?"use-credentials"===t?t:"":void 0}r.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=s,r.createPortal=function(e,t){var r=2<arguments.length&&void 0!==arguments[2]?arguments[2]:null;if(!t||1!==t.nodeType&&9!==t.nodeType&&11!==t.nodeType)throw Error(n(299));return function(e,t,r){var i=3<arguments.length&&void 0!==arguments[3]?arguments[3]:null;return{$$typeof:f,key:null==i?null:""+i,children:e,containerInfo:t,implementation:r}}(e,t,null,r)},r.flushSync=function(e){var t=c.T,r=s.p;try{if(c.T=null,s.p=2,e)return e()}finally{c.T=t,s.p=r,s.d.f()}},r.preconnect=function(e,t){"string"==typeof e&&(t?t="string"==typeof(t=t.crossOrigin)?"use-credentials"===t?t:"":void 0:t=null,s.d.C(e,t))},r.prefetchDNS=function(e){"string"==typeof e&&s.d.D(e)},r.preinit=function(e,t){if("string"==typeof e&&t&&"string"==typeof t.as){var r=t.as,i=p(r,t.crossOrigin),n="string"==typeof t.integrity?t.integrity:void 0,o="string"==typeof t.fetchPriority?t.fetchPriority:void 0;"style"===r?s.d.S(e,"string"==typeof t.precedence?t.precedence:void 0,{crossOrigin:i,integrity:n,fetchPriority:o}):"script"===r&&s.d.X(e,{crossOrigin:i,integrity:n,fetchPriority:o,nonce:"string"==typeof t.nonce?t.nonce:void 0})}},r.preinitModule=function(e,t){if("string"==typeof e)if("object"==typeof t&&null!==t){if(null==t.as||"script"===t.as){var r=p(t.as,t.crossOrigin);s.d.M(e,{crossOrigin:r,integrity:"string"==typeof t.integrity?t.integrity:void 0,nonce:"string"==typeof t.nonce?t.nonce:void 0})}}else null==t&&s.d.M(e)},r.preload=function(e,t){if("string"==typeof e&&"object"==typeof t&&null!==t&&"string"==typeof t.as){var r=t.as,i=p(r,t.crossOrigin);s.d.L(e,r,{crossOrigin:i,integrity:"string"==typeof t.integrity?t.integrity:void 0,nonce:"string"==typeof t.nonce?t.nonce:void 0,type:"string"==typeof t.type?t.type:void 0,fetchPriority:"string"==typeof t.fetchPriority?t.fetchPriority:void 0,referrerPolicy:"string"==typeof t.referrerPolicy?t.referrerPolicy:void 0,imageSrcSet:"string"==typeof t.imageSrcSet?t.imageSrcSet:void 0,imageSizes:"string"==typeof t.imageSizes?t.imageSizes:void 0,media:"string"==typeof t.media?t.media:void 0})}},r.preloadModule=function(e,t){if("string"==typeof e)if(t){var r=p(t.as,t.crossOrigin);s.d.m(e,{as:"string"==typeof t.as&&"script"!==t.as?t.as:void 0,crossOrigin:r,integrity:"string"==typeof t.integrity?t.integrity:void 0})}else s.d.m(e)},r.requestFormReset=function(e){s.d.r(e)},r.unstable_batchedUpdates=function(e,t){return e(t)},r.useFormState=function(e,t,r){return c.H.useFormState(e,t,r)},r.useFormStatus=function(){return c.H.useHostTransitionStatus()},r.version="19.0.0",function e(){if("undefined"!=typeof __REACT_DEVTOOLS_GLOBAL_HOOK__&&"function"==typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE)try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(e)}catch(e){console.error(e)}}(),t.exports=r;var a=t.exports,d=t.exports.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,y=t.exports.createPortal,u=t.exports.flushSync,l=t.exports.preconnect,g=t.exports.prefetchDNS,_=t.exports.preinit,O=t.exports.preinitModule,v=t.exports.preload,S=t.exports.preloadModule,m=t.exports.requestFormReset,h=t.exports.unstable_batchedUpdates,E=t.exports.useFormState,T=t.exports.useFormStatus,R=t.exports.version;export{d as __DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,y as createPortal,a as default,u as flushSync,l as preconnect,g as prefetchDNS,_ as preinit,O as preinitModule,v as preload,S as preloadModule,m as requestFormReset,h as unstable_batchedUpdates,E as useFormState,T as useFormStatus,R as version};
