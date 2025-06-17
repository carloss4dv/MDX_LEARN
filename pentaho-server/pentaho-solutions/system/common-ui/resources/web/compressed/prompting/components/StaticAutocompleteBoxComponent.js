/*!
 * Copyright 2010 - 2020 Hitachi Vantara.  All rights reserved.
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

define(["common-ui/util/util","cdf/components/BaseComponent","amd!cdf/lib/jquery.ui"],function(e,t,a){return t.extend({needsUpdateOnNextRefresh:!1,_searchResponseCallback:null,update:function(){var e=a("#"+this.htmlObject);this.labelValueMap={},a.each(this.valuesArray,function(e,t){this.labelValueMap[t.label]=t.value}.bind(this));var t;this.parameter&&a.each(this.param.values,function(e,a){a.selected&&(t=this.formatter?this.formatter.format(this.transportFormatter.parse(a.label)):a.label)}.bind(this));var i=a("input",e);0===i.length?this._createAndInitializeInputAutocompleteElement(e,t):t!==this.prevSelValue&&void 0!==t&&i.val(t),this.needsUpdateOnNextRefresh&&(this.needsUpdateOnNextRefresh=!1,this._finalizeSource(this.prevSelValue,this._searchResponseCallback),this._searchResponseCallback=null)},getValue:function(){var e=a("#"+this.htmlObject+"-input").val();return this.param.list?this.labelValueMap[e]||e:this.formatter?this.transportFormatter.format(this.formatter.parse(e)):e},_createAndInitializeInputAutocompleteElement:function(e,t){var i='<input type="text" id="'+this.htmlObject+'-input"';void 0!==t&&(i+=' value="'+t+'"'),i+="></input>",e.html(i);var s=a("input",e);s.autocomplete({delay:200,create:function(){a(s).data("ui-autocomplete")._renderItem=function(e,t){return a("<li></li>").append(this._createLabelTag(t.label)).appendTo(e)}.bind(this);var e=0;void 0!==this.getValue()&&(e=2*this.getValue().length),!0===this.autoFocus&&s[0].setSelectionRange(e,e)}.bind(this),source:function(e,t){this.prevSelValue!==e.term?(this.prevSelValue=e.term,this._searchResponseCallback=t,this.needsUpdateOnNextRefresh=!0,this.dashboard.processChange(this.name)):this._finalizeSource(e.term,t)}.bind(this),select:function(e,t){a("#"+this.htmlObject+"-input").val(t.item.value),this.dashboard.processChange(this.name)}.bind(this)}),s.keypress(function(e){13===e.which&&this.dashboard.processChange(this.name)}.bind(this)),s.focus(function(){this.prevSelValue=this.getValue()}.bind(this)),s.focusout(function(){if(this.prevSelValue!==this.getValue()){try{var e=a("#ui-active-menuitem").text();e&&a("#"+this.htmlObject+"-input").val(e)}catch(e){}this.dashboard.processChange(this.name)}}.bind(this)),this._doAutoFocus()},_createLabelTag:function(e){return a("<a></a>").html(e)},_finalizeSource:function(e,t){var i=e.toUpperCase();t(a.map(this.valuesArray,function(e){if(this._createLabelTag(e.label).text().toUpperCase().indexOf(i)>=0)return e}.bind(this)))}})});