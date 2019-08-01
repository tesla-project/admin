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
 * Locale: FI (Finnish; suomi, suomen kieli)
 */
$.extend( $.validator.messages, {
	required: "T&auml;m&auml; kentt&auml; on pakollinen.",
	email: "Sy&ouml;t&auml; oikea s&auml;hk&ouml;postiosoite.",
	url: "Sy&ouml;t&auml; oikea URL-osoite.",
	date: "Sy&ouml;t&auml; oikea p&auml;iv&auml;m&auml;&auml;r&auml;.",
	dateISO: "Sy&ouml;t&auml; oikea p&auml;iv&auml;m&auml;&auml;r&auml; muodossa VVVV-KK-PP.",
	number: "Sy&ouml;t&auml; luku.",
	creditcard: "Sy&ouml;t&auml; voimassa oleva luottokorttinumero.",
	digits: "Sy&ouml;t&auml; pelk&auml;st&auml;&auml;n numeroita.",
	equalTo: "Sy&ouml;t&auml; sama arvo uudestaan.",
	maxlength: $.validator.format( "Voit sy&ouml;tt&auml;&auml; enint&auml;&auml;n {0} merkki&auml;." ),
	minlength: $.validator.format( "V&auml;hint&auml;&auml;n {0} merkki&auml;." ),
	rangelength: $.validator.format( "Sy&ouml;t&auml; v&auml;hint&auml;&auml;n {0} ja enint&auml;&auml;n {1} merkki&auml;." ),
	range: $.validator.format( "Sy&ouml;t&auml; arvo v&auml;lilt&auml; {0}&ndash;{1}." ),
	max: $.validator.format( "Sy&ouml;t&auml; arvo, joka on enint&auml;&auml;n {0}." ),
	min: $.validator.format( "Sy&ouml;t&auml; arvo, joka on v&auml;hint&auml;&auml;n {0}." )
} );
return $;
}));