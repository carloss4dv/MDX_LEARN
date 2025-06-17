/*!
* Copyright 2010 - 2021 Hitachi Vantara.  All rights reserved.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
*/

define(["dojo/_base/declare","dojo/_base/lang","dijit/form/_FormWidget","dojox/widget/ColorPicker","dojo/text!pentaho/common/CustomColorPicker/CustomColorPicker.html","dojo/dom-class","dojo/dom-style","dojo/dom-geometry","dojo/dom-style","dojo/fx","dijit/focus","dojo/dnd/move","dojo/fx","dojox/color","dojo/i18n","dijit/ColorPalette"],function(o,i,t,e,s,n,r,h,a,u,c){return o("pentaho.common.CustomColorPicker",[e],{showPreview:!0,templateString:s,postCreate:function(){this.inherited(arguments),this.showPreview||(this.previewNode.style.visibility="hidden"),this.showHsv||r.set(this.hsvRow,"display","none"),this.showPreview||this.webSafe||this.showPreview||a.set(this.previewNodes,"display","none")},_setTimer:function(o){(n.contains(o.node,"dojoxHuePickerPoint")||n.contains(o.node,"dojoxColorPickerPoint"))&&this.inherited(arguments)},_clearTimer:function(o){(n.contains(o.node,"dojoxHuePickerPoint")||n.contains(o.node,"dojoxColorPickerPoint"))&&this.inherited(arguments)},_setPoint:function(o){var i=this.PICKER_SAT_SELECTOR_H/2,t=this.PICKER_SAT_SELECTOR_W/2,e=h.position(this.colorUnderlay,!0),s=o.pageY-e.y-i,n=o.pageX-e.x-t;o&&c.focus(o.target),this.animatePoint?fx.slideTo({node:this.cursorNode,duration:this.slideDuration,top:s,left:n,onEnd:d.hitch(this,function(){this._updateColor(!0),c.focus(this.cursorNode)})}).play():(a.set(this.cursorNode,{left:n+"px",top:s+"px"}),this._updateColor(!0))},_setHuePoint:function(o){var t=this.PICKER_HUE_SELECTOR_H/2,e=h.position(this.colorUnderlay,!0),s=o.pageY-e.y-t;this.animatePoint?u.slideTo({node:this.hueCursorNode,duration:this.slideDuration,top:s,left:0,onEnd:i.hitch(this,function(){this._updateColor(!0),c.focus(this.hueCursorNode)})}).play():(a.set(this.hueCursorNode,"top",s+"px"),this._updateColor(!0))},_onMouseDown:function(o){this.isDragging=!0},_onMouseMove:function(o){this.isDragging&&this._updateColor(!1)},_onMouseUp:function(o){this.isDragging=!1,this._updateColor(!0)}})});