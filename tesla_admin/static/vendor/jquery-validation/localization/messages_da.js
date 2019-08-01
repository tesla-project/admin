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
 * Locale: DA (Danish; dansk)
 */
$.extend( $.validator.messages, {
	required: "Dette felt er påkrævet.",
	maxlength: $.validator.format( "Indtast højst {0} tegn." ),
	minlength: $.validator.format( "Indtast mindst {0} tegn." ),
	rangelength: $.validator.format( "Indtast mindst {0} og højst {1} tegn." ),
	email: "Indtast en gyldig email-adresse.",
	url: "Indtast en gyldig URL.",
	date: "Indtast en gyldig dato.",
	number: "Indtast et tal.",
	digits: "Indtast kun cifre.",
	equalTo: "Indtast den samme værdi igen.",
	range: $.validator.format( "Angiv en værdi mellem {0} og {1}." ),
	max: $.validator.format( "Angiv en værdi der højst er {0}." ),
	min: $.validator.format( "Angiv en værdi der mindst er {0}." ),
	creditcard: "Indtast et gyldigt kreditkortnummer."
} );
return $;
}));