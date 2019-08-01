/*
 * TeSLA Admin
 * Copyright (C) 2019 Universitat Oberta de Catalunya
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

(function( factory ) {
	if ( typeof define === "function" && define.amd ) {
		define( ["jquery", "../jquery.validate"], factory );
	} else if (typeof module === "object" && module.exports) {
		module.exports = factory( require( "jquery" ) );
	} else {
		factory( jQuery );
	}
}(function( $ ) {

/*
 * Translated default messages for the jQuery validation plugin.
 * Locale: HY_AM (Armenian; հայերեն լեզու)
 */
$.extend( $.validator.messages, {
	required: "Պարտադիր լրացման դաշտ",
	remote: "Ներմուծեք ճիշտ արժեքը",
	email: "Ներմուծեք վավեր էլեկտրոնային փոստի հասցե",
	url: "Ներմուծեք վավեր URL",
	date: "Ներմուծեք վավեր ամսաթիվ",
	dateISO: "Ներմուծեք ISO ֆորմատով վավեր ամսաթիվ։",
	number: "Ներմուծեք թիվ",
	digits: "Ներմուծեք միայն թվեր",
	creditcard: "Ներմուծեք ճիշտ բանկային քարտի համար",
	equalTo: "Ներմուծեք միևնուն արժեքը ևս մեկ անգամ",
	extension: "Ընտրեք ճիշտ ընդլանումով ֆայլ",
	maxlength: $.validator.format( "Ներմուծեք ոչ ավել քան {0} նիշ" ),
	minlength: $.validator.format( "Ներմուծեք ոչ պակաս քան {0} նիշ" ),
	rangelength: $.validator.format( "Ներմուծեք {0}֊ից {1} երկարությամբ արժեք" ),
	range: $.validator.format( "Ներմուծեք թիվ {0}֊ից {1} միջակայքում" ),
	max: $.validator.format( "Ներմուծեք թիվ, որը փոքր կամ հավասար է {0}֊ին" ),
	min: $.validator.format( "Ներմուծեք թիվ, որը մեծ կամ հավասար է {0}֊ին" )
} );
return $;
}));