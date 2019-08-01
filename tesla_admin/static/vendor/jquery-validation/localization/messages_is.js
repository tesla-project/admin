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
 * Locale: IS (Icelandic; íslenska)
 */
$.extend( $.validator.messages, {
	required: "Þessi reitur er nauðsynlegur.",
	remote: "Lagaðu þennan reit.",
	maxlength: $.validator.format( "Sláðu inn mest {0} stafi." ),
	minlength: $.validator.format( "Sláðu inn minnst {0} stafi." ),
	rangelength: $.validator.format( "Sláðu inn minnst {0} og mest {1} stafi." ),
	email: "Sláðu inn gilt netfang.",
	url: "Sláðu inn gilda vefslóð.",
	date: "Sláðu inn gilda dagsetningu.",
	number: "Sláðu inn tölu.",
	digits: "Sláðu inn tölustafi eingöngu.",
	equalTo: "Sláðu sama gildi inn aftur.",
	range: $.validator.format( "Sláðu inn gildi milli {0} og {1}." ),
	max: $.validator.format( "Sláðu inn gildi sem er minna en eða jafnt og {0}." ),
	min: $.validator.format( "Sláðu inn gildi sem er stærra en eða jafnt og {0}." ),
	creditcard: "Sláðu inn gilt greiðslukortanúmer."
} );
return $;
}));