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
 * Locale: ET (Estonian; eesti, eesti keel)
 */
$.extend( $.validator.messages, {
	required: "See väli peab olema täidetud.",
	maxlength: $.validator.format( "Palun sisestage vähem kui {0} tähemärki." ),
	minlength: $.validator.format( "Palun sisestage vähemalt {0} tähemärki." ),
	rangelength: $.validator.format( "Palun sisestage väärtus vahemikus {0} kuni {1} tähemärki." ),
	email: "Palun sisestage korrektne e-maili aadress.",
	url: "Palun sisestage korrektne URL.",
	date: "Palun sisestage korrektne kuupäev.",
	dateISO: "Palun sisestage korrektne kuupäev (YYYY-MM-DD).",
	number: "Palun sisestage korrektne number.",
	digits: "Palun sisestage ainult numbreid.",
	equalTo: "Palun sisestage sama väärtus uuesti.",
	range: $.validator.format( "Palun sisestage väärtus vahemikus {0} kuni {1}." ),
	max: $.validator.format( "Palun sisestage väärtus, mis on väiksem või võrdne arvuga {0}." ),
	min: $.validator.format( "Palun sisestage väärtus, mis on suurem või võrdne arvuga {0}." ),
	creditcard: "Palun sisestage korrektne krediitkaardi number."
} );
return $;
}));