(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[6780],{2850:function(e,n,t){"use strict";t.d(n,{M:function(){return a},W:function(){return c}});var r=t(9518),i=t(23831),l=t(3055),c=34*t(49125).iI,a=r.default.div.withConfig({displayName:"indexstyle__BeforeStyle",componentId:"sc-12ee2ib-0"})(["min-height:calc(100vh - ","px);",""],l.Mz,(function(e){return"\n    border-left: 1px solid ".concat((e.theme.borders||i.Z.borders).medium,";\n  ")}))},56681:function(e,n,t){"use strict";t.d(n,{G:function(){return g},Z:function(){return Z}});var r=t(75582),i=t(82394),l=t(26304),c=t(32316),a=t(22673),s=t(86532),o=t(86673),u=t(19711),d=t(87815),p=t(49125),f=t(19395),b=t(28598),v=["height","heightOffset","pipeline","selectedRun","selectedTab","setSelectedTab"];function h(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function m(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?h(Object(t),!0).forEach((function(n){(0,i.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):h(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var j={uuid:"Run details"},x={uuid:"Dependency tree"},g=[x,j];function Z(e){var n=e.height,t=e.heightOffset,i=e.pipeline,h=e.selectedRun,Z=e.selectedTab,y=e.setSelectedTab,O=m({},(0,l.Z)(e,v));h?O.blockStatus=(0,f.IJ)(null===h||void 0===h?void 0:h.block_runs):O.noStatus=!0;var P=(null===h||void 0===h?void 0:h.variables)||{};null!==h&&void 0!==h&&h.event_variables&&(P.event=h.event_variables);var _=[];P&&JSON.stringify(P,null,2).split("\n").forEach((function(e){_.push("    ".concat(e))}));var k=h&&[["Run ID",null===h||void 0===h?void 0:h.id],["Variables",(0,b.jsx)(a.Z,{language:"json",small:!0,source:_.join("\n")})]],I=h&&(0,b.jsx)(o.Z,{pb:p.cd,px:p.cd,children:(0,b.jsx)(d.Z,{alignTop:!0,columnFlex:[null,1],columnMaxWidth:function(e){return 1===e?"100px":null},rows:k.map((function(e){var n=(0,r.Z)(e,2),t=n[0],i=n[1];return[(0,b.jsx)(u.ZP,{monospace:!0,muted:!0,children:t}),(0,b.jsx)(u.ZP,{monospace:!0,textOverflow:!0,children:i})]})),uuid:"LogDetail"})}),w=Z&&y;return(0,b.jsxs)(b.Fragment,{children:[w&&(0,b.jsx)(o.Z,{py:p.cd,children:(0,b.jsx)(c.Z,{onClickTab:y,selectedTabUUID:null===Z||void 0===Z?void 0:Z.uuid,tabs:g})}),(!w||x.uuid===(null===Z||void 0===Z?void 0:Z.uuid))&&(0,b.jsx)(s.Z,m(m({},O),{},{height:n,heightOffset:(t||0)+(w?76:0),pipeline:i})),j.uuid===(null===Z||void 0===Z?void 0:Z.uuid)&&I]})}},58122:function(e,n,t){"use strict";t.d(n,{CL:function(){return f},FS:function(){return b},JZ:function(){return h},e7:function(){return m},v0:function(){return p},wx:function(){return v}});var r=t(75582),i=t(82394),l=t(43313),c=t(93348),a=t(1286),s=t(90211),o=t(84779);function u(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function d(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?u(Object(t),!0).forEach((function(n){(0,i.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):u(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function p(e){var n=e.statistics,t=Object.keys(n),r=Array(l.Dy.length).fill(0);return 0===t.length?null:(t.forEach((function(e){if(l.Dy.includes(e)){var t=l.CC[e],i=n[e],c=i,a=!1,s=[2,3],u=l.Ub[e],d=l.oH[e],p=l.OD[e];if(l.y_.includes(e))a=!0,s=[2,1,2];else if(e in l.Sq){i=(0,o.Jw)(i,0);var f=l.Sq[e];c=n[f]}var b={columnFlexNumbers:s,name:t,progress:a,rate:c,successDirection:d,warning:p};l.y_.includes(e)||(b.value=i),r[u]=b}})),r)}function f(e){var n=e.columnTypes,t=void 0===n?{}:n,r=e.statistics,i=Object.keys(r);if(0===i.length)return null;var c=Object.values(t),o=c.length,u=[];u.push({name:"Column count",successDirection:l.oH.column_count,value:(0,s.x6)(o)}),i.forEach((function(e){if(l.Zu.includes(e)){var n=l.CC[e],t=r[e],i=l.OD[e];u.push({name:n,successDirection:l.oH[e],value:(0,s.x6)(t),warning:i})}}));var d=(0,a.QO)(c),p=d.countCategory,f=d.countDatetime,b=d.countNumerical;return u.push({name:"Categorical Features",rate:p/o,value:(0,s.x6)(p)},{name:"Numerical Features",rate:b/o,value:(0,s.x6)(b)},{name:"Datetime Features",rate:f/o,value:(0,s.x6)(f)}),u}function b(e){return"string"===typeof e?e:JSON.stringify(e)}function v(e,n){var t,r;return null===e||void 0===e||null===(t=e.find((function(e){var t=e.block;return n(t)})))||void 0===t||null===(r=t.variables)||void 0===r?void 0:r.map((function(e){var n=e.value;return d(d({},e),{},{value:b(n)})}))}function h(e,n){return n===c.Xm.TIME?e.push({uuid:"execution_date",value:"<run datetime>"}):n===c.Xm.EVENT&&e.push({uuid:"event",value:"<trigger event>"}),e}function m(e){return e?Object.entries(e).reduce((function(e,n){var t=(0,r.Z)(n,2),l=t[0],c=t[1],a=c;try{a=JSON.parse(c)}catch(s){}return d(d({},e),{},(0,i.Z)({},l,a))}),{}):e}},18025:function(e,n,t){"use strict";t.d(n,{J:function(){return s},U:function(){return a}});var r=t(9518),i=t(23831),l=t(73942),c=t(49125),a=r.default.div.withConfig({displayName:"indexstyle__CardStyle",componentId:"sc-m7tlau-0"})(["border-radius:","px;border-style:solid;border-width:2px;height:","px;margin-right:","px;padding:","px;width:","px;"," ",""],l.TR,14*c.iI,c.cd*c.iI,c.cd*c.iI,40*c.iI,(function(e){return!e.selected&&"\n    border-color: ".concat((e.theme.borders||i.Z.borders).light,";\n  ")}),(function(e){return e.selected&&"\n    border-color: ".concat((e.theme.interactive||i.Z.interactive).linkPrimary,";\n  ")})),s=r.default.div.withConfig({displayName:"indexstyle__DateSelectionContainer",componentId:"sc-m7tlau-1"})(["border-radius:","px;padding:","px;"," "," ",""],l.n_,c.tr,(function(e){return"\n    background-color: ".concat((e.theme.interactive||i.Z.interactive).defaultBackground,";\n  ")}),(function(e){return e.absolute&&"\n    position: absolute;\n    z-index: 2;\n    right: 0;\n    top: ".concat(2.5*c.iI,"px;\n  ")}),(function(e){return e.topPosition&&"\n    top: -".concat(42*c.iI,"px;\n  ")}))},43526:function(e,n,t){"use strict";t.d(n,{I7:function(){return r},IB:function(){return s},VV:function(){return l},_7:function(){return c},rn:function(){return a}});var r,i=t(66050),l="datetime",c="code",a=i.V;!function(e){e.SECOND="second",e.MINUTE="minute",e.HOUR="hour",e.DAY="day",e.WEEK="week",e.MONTH="month",e.YEAR="year",e.CUSTOM="custom"}(r||(r={}));var s=[r.SECOND,r.MINUTE,r.HOUR,r.DAY,r.WEEK,r.MONTH,r.YEAR,r.CUSTOM]},2713:function(e,n,t){"use strict";var r=t(82394),i=t(44495),l=t(67971),c=t(55378),a=t(86673),s=t(19711),o=t(18025),u=t(49125),d=t(24224),p=t(28598);function f(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function b(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?f(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):f(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}n.Z=function(e){var n=e.selectedDate,t=e.selectedTime,r=e.setSelectedDate,f=e.setSelectedTime,v=e.topPosition;return(0,p.jsxs)(o.J,{absolute:!0,topPosition:v,children:[(0,p.jsx)(i.ZP,{onChange:r,value:n}),(0,p.jsx)(a.Z,{mb:2}),(0,p.jsxs)(l.Z,{alignItems:"center",children:[(0,p.jsx)(s.ZP,{default:!0,large:!0,children:"Time (UTC):"}),(0,p.jsx)(a.Z,{pr:2}),(0,p.jsx)(c.Z,{compact:!0,monospace:!0,onChange:function(e){e.preventDefault(),f((function(n){return b(b({},n),{},{hour:e.target.value})}))},paddingRight:5*u.iI,placeholder:"HH",value:null===t||void 0===t?void 0:t.hour,children:(0,d.m5)(24,0).map((function(e){return String(e).padStart(2,"0")})).map((function(e){return(0,p.jsx)("option",{value:e,children:e},"hour_".concat(e))}))}),(0,p.jsx)(a.Z,{px:1,children:(0,p.jsx)(s.ZP,{bold:!0,large:!0,children:":"})}),(0,p.jsx)(c.Z,{compact:!0,monospace:!0,onChange:function(e){e.preventDefault(),f((function(n){return b(b({},n),{},{minute:e.target.value})}))},paddingRight:5*u.iI,placeholder:"MM",value:null===t||void 0===t?void 0:t.minute,children:(0,d.m5)(60,0).map((function(e){return String(e).padStart(2,"0")})).map((function(e){return(0,p.jsx)("option",{value:e,children:e},"minute_".concat(e))}))})]})]})}},22673:function(e,n,t){"use strict";var r=t(82684),i=t(73199),l=t.n(i),c=t(71593),a=t(9518),s=t(65292),o=t(23831),u=t(2005),d=t(49125),p=t(28598);n.Z=function(e){var n=e.language,t=e.maxWidth,i=e.showLineNumbers,f=e.small,b=e.source,v=e.wrapLines,h=(0,r.useContext)(a.ThemeContext);return(0,p.jsx)(l(),{source:b,renderers:{code:function(e){var r=e.value;return(0,p.jsx)(c.Z,{customStyle:{backgroundColor:(h.background||o.Z.background).popup,border:"none",borderRadius:"none",boxShadow:"none",fontFamily:u.Vp,fontSize:f?12:14,marginBottom:0,marginTop:0,paddingBottom:2*d.iI,paddingTop:2*d.iI,maxWidth:t},lineNumberStyle:{color:(h.content||o.Z.content).muted},language:n,showLineNumbers:i,style:s._4,useInlineStyles:!0,wrapLines:v,children:r})}}})}},32316:function(e,n,t){"use strict";t.d(n,{Z:function(){return v}});var r=t(82684),i=t(60328),l=t(67971),c=t(882),a=t(86673),s=t(99994),o=t(9518),u=t(49125),d=t(37391),p=o.default.div.withConfig({displayName:"indexstyle__TabsContainerStyle",componentId:"sc-segf7l-0"})(["padding-left:","px;padding-right:","px;"," "," ",""],u.cd*u.iI,u.cd*u.iI,(function(e){return e.noPadding&&"\n    padding: 0;\n  "}),(function(e){return e.allowScroll&&"\n    overflow: auto;\n  "}),d.w5),f=t(66653),b=t(28598);var v=function(e){var n=e.allowScroll,t=e.contained,o=e.noPadding,d=e.onClickTab,v=e.selectedTabUUID,h=e.small,m=e.tabs,j=(0,r.useMemo)((function(){var e=m.length,n=[];return m.forEach((function(t,r){var o=t.Icon,p=t.IconSelected,m=t.label,j=t.uuid,x=j===v,g=x&&p||o,Z=m?m():j,y=(0,b.jsxs)(l.Z,{alignItems:"center",children:[g&&(0,b.jsxs)(b.Fragment,{children:[(0,b.jsx)(g,{default:!x,size:2*u.iI}),(0,b.jsx)(a.Z,{mr:1})]}),Z]});r>=1&&e>=2&&n.push((0,b.jsx)("div",{style:{marginLeft:1.5*u.iI}},"spacing-".concat(j))),x?n.push((0,b.jsx)(c.Z,{backgroundGradient:s.yr,backgroundPanel:!0,borderLess:!0,borderWidth:2,compact:h,onClick:function(e){(0,f.j)(e),d(t)},paddingUnitsHorizontal:2,paddingUnitsVertical:1.25,small:h,children:y},j)):n.push((0,b.jsx)("div",{style:{padding:4},children:(0,b.jsx)(i.Z,{borderLess:!0,compact:h,default:!0,onClick:function(e){(0,f.j)(e),d(t)},outline:!0,small:h,children:y},"button-tab-".concat(j))}))})),n}),[d,v,m]),x=(0,b.jsx)(l.Z,{alignItems:"center",children:j});return t?x:(0,b.jsx)(p,{allowScroll:n,noPadding:o,children:x})}},82944:function(e,n,t){"use strict";var r=t(82394),i=t(91835),l=t(82684),c=t(9518),a=t(69898),s=t(28598);function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function u(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var d=c.default.input.withConfig({displayName:"TextInput__TextInputStyle",componentId:"sc-1ii4qtc-0"})(["",""],a.p),p=function(e,n){var t=(0,i.Z)({},e);return(0,s.jsx)(a.Z,u(u({},t),{},{input:(0,s.jsx)(d,u({},t)),ref:n}))};n.Z=l.forwardRef(p)},12625:function(e,n,t){"use strict";t.r(n),t.d(n,{default:function(){return te}});var r=t(75582),i=t(77837),l=t(82394),c=t(38860),a=t.n(c),s=t(82684),o=t(83455),u=t(34376),d=t(43526),p=t(60328),f=t(34744),b=t(67971),v=t(87372),h=t(51099),m=t(2626),j=t(97496),x=t(47409),g=t(55378),Z=t(86673),y=t(87815),O=t(19711),P=t(82531),_=t(56681),k=t(10503),I=t(2850),w=t(49125),S=t(59920),D=t(90211),C=t(58122),E=t(33766),N=t(7715),T=t(9736),M=t(96510),L=t(66653),F=t(59e3),U=t(28598);function A(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function R(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?A(Object(t),!0).forEach((function(n){(0,l.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):A(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var H=function(e){var n=e.backfill,t=e.fetchBackfill,i=e.pipeline,l=e.variables,c=(0,T.Ct)(),a=(0,u.useRouter)(),A=n||{},H=A.block_uuid,B=A.end_datetime,V=A.id,z=A.interval_type,Y=A.interval_units,J=A.name,W=A.pipeline_run_dates,q=A.start_datetime,G=A.status,K=A.total_run_count,X=A.variables,Q=void 0===X?{}:X,$=i.uuid,ee=(0,F.iV)(),ne=(0,s.useState)(null),te=ne[0],re=ne[1],ie={_limit:40,_offset:40*(null!==ee&&void 0!==ee&&ee.page?ee.page:0)};null!==ee&&void 0!==ee&&ee.status&&(ie.status=ee.status);var le=P.ZP.pipeline_runs.list(R(R({},ie),{},{backfill_id:V,order_by:["id DESC"]}),{refreshInterval:3e3,revalidateOnFocus:!0},{pauseFetch:!V}),ce=le.data,ae=le.mutate,se=!(q&&B&&z&&Y),oe=!G,ue=(0,s.useMemo)((function(){return(oe?W:null===ce||void 0===ce?void 0:ce.pipeline_runs)||[]}),[ce,W,oe]),de=(0,s.useMemo)((function(){var e;return(null===ce||void 0===ce||null===(e=ce.metadata)||void 0===e?void 0:e.count)||[]}),[ce]),pe=(0,s.useState)(null),fe=pe[0],be=pe[1],ve=(0,s.useMemo)((function(){var e=null!==ee&&void 0!==ee&&ee.page?ee.page:0;return(0,U.jsxs)(U.Fragment,{children:[(0,U.jsx)(j.Z,{disableRowSelect:oe,emptyMessage:null!==ee&&void 0!==ee&&ee.status?"No runs available":'No runs available. Please complete backfill configuration by clicking "Edit backfill" above.',fetchPipelineRuns:ae,onClickRow:function(e){return be((function(n){var t=ue[e];return(null===n||void 0===n?void 0:n.id)!==t.id?t:null}))},pipelineRuns:ue,selectedRun:fe}),(0,U.jsx)(Z.Z,{p:2,children:(0,U.jsx)(h.Z,{page:Number(e),maxPages:9,onUpdate:function(e){var n=Number(e),t=R(R({},ee),{},{page:n>=0?n:0});a.push("/pipelines/[pipeline]/triggers/[...slug]","/pipelines/".concat($,"/triggers/").concat(V,"?").concat((0,F.uM)(t)))},totalPages:Math.ceil(de/40)})})]})}),[ae,i,ue,fe]),he=(0,s.useState)(_.G[0]),me=he[0],je=he[1],xe=(0,o.Db)(P.ZP.backfills.useUpdate(V),{onSuccess:function(e){return(0,M.wD)(e,{callback:function(){t(),ae()},onErrorCallback:function(e,n){return re({errors:n,response:e})}})}}),ge=(0,r.Z)(xe,2),Ze=ge[0],ye=ge[1].isLoading,Oe=(0,s.useMemo)((function(){return!!G&&(d.rn.CANCELLED!==G&&d.rn.FAILED!==G)}),[G]),Pe=(0,s.useMemo)((function(){return G&&d.rn.CANCELLED!==G&&d.rn.FAILED!==G&&d.rn.INITIAL!==G&&d.rn.RUNNING!==G}),[G]),_e=(0,s.useMemo)((function(){var e={default:!0,size:1.5*w.iI},n=[[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.VW,R({},e)),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"Backfill type"})]},"backfill_type_label"),(0,U.jsx)(O.ZP,{monospace:!0,children:H?d._7:d.VV},"backfill_type")],[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.rs,R({},e)),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"Status"})]},"backfill_status_label"),(0,U.jsx)(O.ZP,{danger:d.rn.CANCELLED===G||d.rn.FAILED==G,default:d.rn.INITIAL===G,monospace:!0,muted:!G,success:d.rn.RUNNING===G||d.rn.COMPLETED===G,children:G||"inactive"},"backfill_status")]];return H||n.push.apply(n,[[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.aw,R({},e)),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"Start date and time"})]},"backfill_start_date_label"),(0,U.jsx)(O.ZP,{monospace:!0,children:q},"backfill_start_date")],[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.aw,R({},e)),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"End date and time"})]},"backfill_end_date_label"),(0,U.jsx)(O.ZP,{monospace:!0,children:B},"backfill_end_date")],[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.Pf,R({},e)),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"Interval type"})]},"interval_type_label"),(0,U.jsx)(O.ZP,{monospace:!0,children:z&&(0,D.kC)(z)},"interval_type")],[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.Pf,R({},e)),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"Interval units"})]},"interval_units_label"),(0,U.jsx)(O.ZP,{monospace:!0,children:Y},"interval_units")],[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.qZ,R({},e)),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"Total runs"})]},"total_runs_label"),(0,U.jsx)(O.ZP,{monospace:!0,children:K},"total_runs")]]),(0,U.jsx)(y.Z,{columnFlex:[null,1],rows:n})}),[H,B,z,Y,Oe,q,G]),ke=(0,s.useMemo)((function(){return Q||{}}),[Q]),Ie=(0,s.useMemo)((function(){var e,n=[];return(0,N.Qr)(ke)?n=(0,C.wx)(l,(function(e){return"global"===e.uuid})):Object.entries(ke).forEach((function(e){var t=(0,r.Z)(e,2),i=t[0],l=t[1];n.push({uuid:i,value:(0,C.FS)(l)})})),"undefined"!==typeof n&&null!==(e=n)&&void 0!==e&&e.length?(0,U.jsx)(y.Z,{columnFlex:[null,1],rows:n.map((function(e){var n=e.uuid,t=e.value;return[(0,U.jsx)(O.ZP,{default:!0,monospace:!0,small:!0,children:n},"settings_variable_label_".concat(n)),(0,U.jsx)(O.ZP,{monospace:!0,small:!0,children:t},"settings_variable_".concat(n))]}))}):null}),[ke,l]);return(0,U.jsx)(U.Fragment,{children:(0,U.jsxs)(m.Z,{afterHidden:!fe,before:(0,U.jsxs)(I.M,{children:[(0,U.jsxs)(Z.Z,{mb:w.HN,pt:w.cd,px:w.cd,children:[(0,U.jsx)(Z.Z,{mb:w.cd,children:(0,U.jsx)(k.yg,{size:5*w.iI})}),(0,U.jsx)(v.Z,{children:J})]}),(0,U.jsx)(Z.Z,{px:w.cd,children:(0,U.jsx)(v.Z,{level:5,children:"Settings"})}),(0,U.jsx)(f.Z,{light:!0,mt:1,short:!0}),_e,Ie&&(0,U.jsxs)(Z.Z,{my:w.HN,children:[(0,U.jsx)(Z.Z,{px:w.cd,children:(0,U.jsx)(v.Z,{level:5,children:"Runtime variables"})}),(0,U.jsx)(f.Z,{light:!0,mt:1,short:!0}),Ie]})]}),beforeWidth:34*w.iI,breadcrumbs:[{label:function(){return"Backfills"},linkProps:{as:"/pipelines/".concat($,"/backfills"),href:"/pipelines/[pipeline]/backfills"}},{label:function(){return J},linkProps:{as:"/pipelines/".concat($,"/backfills/").concat(V),href:"/pipelines/[pipeline]/backfills/[...slug]"}}],buildSidekick:function(e){return(0,_.Z)(R(R({},e),{},{selectedRun:fe,selectedTab:me,setSelectedTab:je}))},errors:te,pageName:S.M.BACKFILLS,pipeline:i,setErrors:re,subheader:(0,U.jsxs)(b.Z,{alignItems:"center",children:[!Pe&&(0,U.jsxs)(U.Fragment,{children:[(0,U.jsx)(p.Z,{beforeIcon:Oe?(0,U.jsx)(k.dz,{size:2*w.iI}):(0,U.jsx)(k.Py,{inverted:!(d.rn.CANCELLED===G||d.rn.FAILED===G),size:2*w.iI}),danger:Oe,disabled:se,loading:ye,onClick:function(e){(0,L.j)(e),Ze({backfill:{status:Oe?d.rn.CANCELLED:d.rn.INITIAL}})},outline:!0,success:!Oe&&!(d.rn.CANCELLED===G||d.rn.FAILED===G)&&!se,children:Oe?"Cancel backfill":d.rn.CANCELLED===G||d.rn.FAILED===G?"Retry backfill":"Start backfill"}),(0,U.jsx)(Z.Z,{mr:w.cd})]}),!c&&(0,U.jsxs)(U.Fragment,{children:[G===x.V.COMPLETED?(0,U.jsx)(O.ZP,{bold:!0,default:!0,large:!0,children:"Filter runs by status:"}):(0,U.jsx)(p.Z,{linkProps:{as:"/pipelines/".concat($,"/backfills/").concat(V,"/edit"),href:"/pipelines/[pipeline]/backfills/[...slug]"},noHoverUnderline:!0,outline:!0,sameColorAsText:!0,children:"Edit backfill"}),(0,U.jsx)(Z.Z,{mr:w.cd})]}),!oe&&(0,U.jsxs)(g.Z,{compact:!0,defaultColor:!0,onChange:function(e){e.preventDefault(),"all"===e.target.value?a.push("/pipelines/[pipeline]/backfills/[...slug]","/pipelines/".concat($,"/backfills/").concat(V)):(0,E.u)({page:0,status:e.target.value})},paddingRight:4*w.iI,placeholder:"Select run status",value:(null===ee||void 0===ee?void 0:ee.status)||"all",children:[(0,U.jsx)("option",{value:"all",children:"All statuses"},"all_statuses"),Object.values(x.V).map((function(e){return(0,U.jsx)("option",{value:e,children:x.D[e]},e)}))]})]}),title:function(){return J},uuid:"backfill/detail",children:[(0,U.jsx)(Z.Z,{mt:w.cd,px:w.cd,children:(0,U.jsx)(v.Z,{level:5,children:"Runs for this backfill"})}),(0,U.jsx)(f.Z,{light:!0,mt:w.cd,short:!0}),ve]})})},B=t(2713),V=t(47999),z=t(93461),Y=t(82944),J=[{label:function(){return"Date and time window"},description:function(){return"Backfill between a date and time range."},uuid:d.VV}],W=t(18025),q=t(19395);function G(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function K(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?G(Object(t),!0).forEach((function(n){(0,l.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):G(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var X=function(e){var n=e.backfill,t=e.fetchBackfill,i=e.pipeline,l=(e.variables,(0,u.useRouter)()),c=(0,s.useState)(),a=c[0],h=c[1],j=a||{},x=j.block_uuid,_=j.id,I=j.interval_type,E=j.interval_units,T=(j.end_datetime,j.start_datetime,j.name),L=i.uuid,F=(0,s.useState)(null),A=F[0],R=F[1],H=(0,s.useState)({}),G=H[0],X=(H[1],(0,s.useState)(x?d._7:d.VV)),Q=X[0],$=X[1],ee=(0,s.useState)(!1),ne=ee[0],te=ee[1],re=(0,s.useState)(!1),ie=re[0],le=re[1],ce=(0,s.useState)(null),ae=ce[0],se=ce[1],oe=(0,s.useState)(null),ue=oe[0],de=oe[1],pe=(0,s.useState)({hour:"00",minute:"00"}),fe=pe[0],be=pe[1],ve=(0,s.useState)({hour:"00",minute:"00"}),he=ve[0],me=ve[1];(0,s.useEffect)((function(){if(n){h(n);var e=n.start_datetime;if(e){var t=e.split(" ")[1];de((0,q.eI)(e)),me({hour:t.substring(0,2),minute:t.substring(3,5)})}var r=n.end_datetime;if(r){var i=r.split(" ")[1];se((0,q.eI)(r)),be({hour:i.substring(0,2),minute:i.substring(3,5)})}}}),[n]);var je=(0,s.useMemo)((function(){var e=[[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.KJ,{default:!0,size:1.5*w.iI}),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"Backfill name"})]},"model_name_detail"),(0,U.jsx)(Y.Z,{monospace:!0,onChange:function(e){e.preventDefault(),h((function(n){return K(K({},n),{},{name:e.target.value})}))},placeholder:"Name this backfill",value:T},"model_name_input_detail")]];return d.VV===Q&&e.push.apply(e,[[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.aw,{default:!0,size:1.5*w.iI}),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"Start date and time"})]},"start_time"),(0,U.jsxs)("div",{style:{minHeight:"".concat(5.75*w.iI,"px")},children:[!ne&&(0,U.jsx)(Y.Z,{monospace:!0,onClick:function(){return te((function(e){return!e}))},onFocus:function(){return te(!0)},placeholder:"YYYY-MM-DD HH:MM",value:ue?"".concat(ue.toISOString().split("T")[0]," ").concat(null===he||void 0===he?void 0:he.hour,":").concat(null===he||void 0===he?void 0:he.minute):""}),(0,U.jsx)("div",{style:{width:"400px"},children:(0,U.jsx)(V.Z,{disableEscape:!0,onClickOutside:function(){return te(!1)},open:ne,style:{position:"relative"},children:(0,U.jsx)(B.Z,{selectedDate:ue,selectedTime:he,setSelectedDate:de,setSelectedTime:me,topPosition:!0})})})]},"start_time_input")],[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.aw,{default:!0,size:1.5*w.iI}),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"End date and time"})]},"end_time"),(0,U.jsxs)("div",{style:{minHeight:"".concat(5.75*w.iI,"px")},children:[!ie&&(0,U.jsx)(Y.Z,{monospace:!0,onClick:function(){return le((function(e){return!e}))},onFocus:function(){return le(!0)},placeholder:"YYYY-MM-DD HH:MM",value:ae?"".concat(ae.toISOString().split("T")[0]," ").concat(null===fe||void 0===fe?void 0:fe.hour,":").concat(null===fe||void 0===fe?void 0:fe.minute):""}),(0,U.jsx)("div",{style:{width:"400px"},children:(0,U.jsx)(V.Z,{disableEscape:!0,onClickOutside:function(){return le(!1)},open:ie,style:{position:"relative"},children:(0,U.jsx)(B.Z,{selectedDate:ae,selectedTime:fe,setSelectedDate:se,setSelectedTime:be,topPosition:!0})})})]},"end_time_input")],[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.Pf,{default:!0,size:1.5*w.iI}),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"Interval type"})]},"interval_type"),(0,U.jsxs)(g.Z,{monospace:!0,onChange:function(e){e.preventDefault(),h((function(n){return K(K({},n),{},{interval_type:e.target.value})}))},placeholder:"Time spacing between each backfill",value:I,children:[!I&&(0,U.jsx)("option",{value:""}),d.IB.map((function(e){return(0,U.jsx)("option",{value:e,children:(0,D.kC)(e)},e)}))]},"interval_type_input")],[(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(k.Pf,{default:!0,size:1.5*w.iI}),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(O.ZP,{default:!0,children:"Interval units"})]},"interval_units"),(0,U.jsx)(Y.Z,{disabled:!I,monospace:!0,onChange:function(e){e.preventDefault(),h((function(n){return K(K({},n),{},{interval_units:e.target.value})}))},placeholder:I?"Number of ".concat(I).concat(I!==d.I7.CUSTOM?"s":""," between each backfill"):"Interval type is required",type:"number",value:E},"interval_unit_input")]]),(0,U.jsxs)(U.Fragment,{children:[(0,U.jsx)(Z.Z,{mb:2,px:w.cd,children:(0,U.jsx)(v.Z,{children:"Settings"})}),(0,U.jsx)(f.Z,{light:!0,short:!0}),(0,U.jsx)(y.Z,{columnFlex:[null,1],rows:e})]})}),[ae,ue,I,E,T,Q,ne,ie,fe,he]),xe=(0,o.Db)(P.ZP.backfills.useUpdate(_),{onSuccess:function(e){return(0,M.wD)(e,{callback:function(){t(),l.push("/pipelines/[pipeline]/backfills/[...slug]","/pipelines/".concat(L,"/backfills/").concat(_))},onErrorCallback:function(e,n){return R({errors:n,response:e})}})}}),ge=(0,r.Z)(xe,2),Ze=ge[0],ye=ge[1].isLoading,Oe=(0,s.useCallback)((function(){var e=K(K({},(0,N.GL)(a,["name"])),{},{end_datetime:null,interval_type:null,interval_units:null,start_datetime:null,variables:(0,C.e7)(G)});return d._7===Q||(e.interval_type=I,e.interval_units=E,e.end_datetime=ae&&null!==fe&&void 0!==fe&&fe.hour&&null!==fe&&void 0!==fe&&fe.minute?"".concat(ae.toISOString().split("T")[0]," ").concat(null===fe||void 0===fe?void 0:fe.hour,":").concat(null===fe||void 0===fe?void 0:fe.minute,":00"):null,e.start_datetime=ue&&null!==he&&void 0!==he&&he.hour&&null!==he&&void 0!==he&&he.minute?"".concat(ue.toISOString().split("T")[0]," ").concat(null===he||void 0===he?void 0:he.hour,":").concat(null===he||void 0===he?void 0:he.minute,":00"):null),Ze({backfill:e})}),[ae,ue,I,E,a,G,Q,fe,he]),Pe=(0,s.useMemo)((function(){return d._7===Q?!x:!(ae&&ue&&I&&E)}),[x,ae,ue,I,E,Q,fe,he]);return(0,U.jsxs)(m.Z,{breadcrumbs:[{label:function(){return"Backfills"},linkProps:{as:"/pipelines/".concat(L,"/backfills"),href:"/pipelines/[pipeline]/backfills"}},{label:function(){return null===a||void 0===a?void 0:a.name},linkProps:{as:"/pipelines/".concat(L,"/backfills/").concat(_),href:"/pipelines/[pipeline]/backfills/[...slug]"}}],errors:A,pageName:S.M.BACKFILLS,pipeline:i,setErrors:R,subheader:(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(p.Z,{disabled:Pe,loading:ye,onClick:Oe,outline:!0,primary:!0,children:"Save changes"}),(0,U.jsx)(Z.Z,{mr:1}),(0,U.jsx)(p.Z,{linkProps:{href:"/pipelines/[pipeline]/backfills/[...slug]",as:"/pipelines/".concat(L,"/backfills/").concat(_)},noHoverUnderline:!0,outline:!0,sameColorAsText:!0,children:"Cancel"})]}),title:function(){return"Edit ".concat(null===a||void 0===a?void 0:a.name)},uuid:"backfill/edit",children:[(0,U.jsxs)(Z.Z,{p:w.cd,children:[(0,U.jsxs)(Z.Z,{mb:2,children:[(0,U.jsx)(v.Z,{children:"Backfill type"}),(0,U.jsx)(O.ZP,{muted:!0,children:"How would you like this pipeline to be backfilled?"})]}),(0,U.jsx)(b.Z,{children:J.map((function(e){var n=e.label,t=e.description,r=e.uuid,i=Q===r,l=Q&&!i;return(0,U.jsx)(p.Z,{noBackground:!0,noBorder:!0,noPadding:!0,onClick:function(){$(r)},children:(0,U.jsx)(W.U,{selected:i,children:(0,U.jsxs)(b.Z,{alignItems:"center",children:[(0,U.jsx)(z.Z,{children:(0,U.jsx)("input",{checked:i,type:"radio"})}),(0,U.jsx)(Z.Z,{mr:w.cd}),(0,U.jsxs)(z.Z,{alignItems:"flex-start",flexDirection:"column",children:[(0,U.jsx)(v.Z,{bold:!0,default:!i&&!l,level:5,muted:!i&&l,children:n()}),(0,U.jsx)(O.ZP,{default:!i&&!l,leftAligned:!0,muted:l,children:t()})]})]})})},r)}))})]}),(0,U.jsx)(Z.Z,{mt:5,children:je})]})},Q=t(41788);function $(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function ee(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?$(Object(t),!0).forEach((function(n){(0,l.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):$(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function ne(e){var n=e.backfillId,t=e.pipelineUUID,r=e.subpath,i=P.ZP.variables.pipelines.list(t).data,l=(0,s.useMemo)((function(){return null===i||void 0===i?void 0:i.variables}),[i]),c=P.ZP.pipelines.detail(t,{includes_content:!1,includes_outputs:!1},{revalidateOnFocus:!1}).data,a=(0,s.useMemo)((function(){return ee(ee({},null===c||void 0===c?void 0:c.pipeline),{},{uuid:t})}),[c,t]),o=P.ZP.backfills.detail(n,{include_preview_runs:!0}),u=o.data,d=o.mutate,p=(0,s.useMemo)((function(){return null===u||void 0===u?void 0:u.backfill}),[u]);return"edit"===r?(0,U.jsx)(X,{backfill:p,fetchBackfill:d,pipeline:a,variables:l}):(0,U.jsx)(H,{backfill:p,fetchBackfill:d,pipeline:a,variables:l})}ne.getInitialProps=function(){var e=(0,i.Z)(a().mark((function e(n){var t,i,l,c,s,o;return a().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(t=n.query,i=t.pipeline,l=t.slug,!Array.isArray(l)){e.next=4;break}return c=(0,r.Z)(l,2),s=c[0],o=c[1],e.abrupt("return",{backfillId:s,pipelineUUID:i,subpath:o});case 4:return e.abrupt("return",{pipelineUUID:i});case 5:case"end":return e.stop()}}),e)})));return function(n){return e.apply(this,arguments)}}();var te=(0,Q.Z)(ne)},53664:function(e,n,t){(window.__NEXT_P=window.__NEXT_P||[]).push(["/pipelines/[pipeline]/backfills/[...slug]",function(){return t(12625)}])}},function(e){e.O(0,[3850,2083,5896,4804,1774,5872,2524,4495,9767,3573,434,9898,1830,2626,4463,6532,1286,4846,9774,2888,179],(function(){return n=53664,e(e.s=n);var n}));var n=e.O();_N_E=n}]);