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
 * Locale: SV (Swedish; Svenska)
 */
$.extend( $.validator.messages, {
	required: "Detta f&auml;lt &auml;r obligatoriskt.",
	maxlength: $.validator.format( "Du f&aring;r ange h&ouml;gst {0} tecken." ),
	minlength: $.validator.format( "Du m&aring;ste ange minst {0} tecken." ),
	rangelength: $.validator.format( "Ange minst {0} och max {1} tecken." ),
	email: "Ange en korrekt e-postadress.",
	url: "Ange en korrekt URL.",
	date: "Ange ett korrekt datum.",
	dateISO: "Ange ett korrekt datum (&Aring;&Aring;&Aring;&Aring;-MM-DD).",
	number: "Ange ett korrekt nummer.",
	digits: "Ange endast siffror.",
	equalTo: "Ange samma v&auml;rde igen.",
	range: $.validator.format( "Ange ett v&auml;rde mellan {0} och {1}." ),
	max: $.validator.format( "Ange ett v&auml;rde som &auml;r mindre eller lika med {0}." ),
	min: $.validator.format( "Ange ett v&auml;rde som &auml;r st&ouml;rre eller lika med {0}." ),
	creditcard: "Ange ett korrekt kreditkortsnummer."
} );
return $;
}));