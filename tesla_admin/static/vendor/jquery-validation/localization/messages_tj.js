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
 * Locale: TJ (Tajikistan; Забони тоҷикӣ)
 */
$.extend( $.validator.messages, {
	required: "Ворид кардани ин филд маҷбури аст.",
	remote: "Илтимос, маълумоти саҳеҳ ворид кунед.",
	email: "Илтимос, почтаи электронии саҳеҳ ворид кунед.",
	url: "Илтимос, URL адреси саҳеҳ ворид кунед.",
	date: "Илтимос, таърихи саҳеҳ ворид кунед.",
	dateISO: "Илтимос, таърихи саҳеҳи (ISO)ӣ ворид кунед.",
	number: "Илтимос, рақамҳои саҳеҳ ворид кунед.",
	digits: "Илтимос, танҳо рақам ворид кунед.",
	creditcard: "Илтимос, кредит карди саҳеҳ ворид кунед.",
	equalTo: "Илтимос, миқдори баробар ворид кунед.",
	extension: "Илтимос, қофияи файлро дуруст интихоб кунед",
	maxlength: $.validator.format( "Илтимос, бештар аз {0} рамз ворид накунед." ),
	minlength: $.validator.format( "Илтимос, камтар аз {0} рамз ворид накунед." ),
	rangelength: $.validator.format( "Илтимос, камтар аз {0} ва зиёда аз {1} рамз ворид кунед." ),
	range: $.validator.format( "Илтимос, аз {0} то {1} рақам зиёд ворид кунед." ),
	max: $.validator.format( "Илтимос, бештар аз {0} рақам ворид накунед." ),
	min: $.validator.format( "Илтимос, камтар аз {0} рақам ворид накунед." )
} );
return $;
}));