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
 * Locale: MK (Macedonian; македонски јазик)
 */
$.extend( $.validator.messages, {
	required: "Полето е задолжително.",
	remote: "Поправете го ова поле",
	email: "Внесете правилна e-mail адреса",
	url: "Внесете правилен URL.",
	date: "Внесете правилен датум",
	dateISO: "Внесете правилен датум (ISO).",
	number: "Внесете правилен број.",
	digits: "Внесете само бројки.",
	creditcard: "Внесете правилен број на кредитната картичка.",
	equalTo: "Внесете ја истата вредност повторно.",
	extension: "Внесете вредност со соодветна екстензија.",
	maxlength: $.validator.format( "Внесете максимално {0} знаци." ),
	minlength: $.validator.format( "Внесете барем {0} знаци." ),
	rangelength: $.validator.format( "Внесете вредност со должина помеѓу {0} и {1} знаци." ),
	range: $.validator.format( "Внесете вредност помеѓу {0} и {1}." ),
	max: $.validator.format( "Внесете вредност помала или еднаква на {0}." ),
	min: $.validator.format( "Внесете вредност поголема или еднаква на {0}" )
} );
return $;
}));