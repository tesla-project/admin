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
 * Locale: EL (Greek; ελληνικά)
 */
$.extend( $.validator.messages, {
	required: "Αυτό το πεδίο είναι υποχρεωτικό.",
	remote: "Παρακαλώ διορθώστε αυτό το πεδίο.",
	email: "Παρακαλώ εισάγετε μια έγκυρη διεύθυνση email.",
	url: "Παρακαλώ εισάγετε ένα έγκυρο URL.",
	date: "Παρακαλώ εισάγετε μια έγκυρη ημερομηνία.",
	dateISO: "Παρακαλώ εισάγετε μια έγκυρη ημερομηνία (ISO).",
	number: "Παρακαλώ εισάγετε έναν έγκυρο αριθμό.",
	digits: "Παρακαλώ εισάγετε μόνο αριθμητικά ψηφία.",
	creditcard: "Παρακαλώ εισάγετε έναν έγκυρο αριθμό πιστωτικής κάρτας.",
	equalTo: "Παρακαλώ εισάγετε την ίδια τιμή ξανά.",
	extension: "Παρακαλώ εισάγετε μια τιμή με έγκυρη επέκταση αρχείου.",
	maxlength: $.validator.format( "Παρακαλώ εισάγετε μέχρι και {0} χαρακτήρες." ),
	minlength: $.validator.format( "Παρακαλώ εισάγετε τουλάχιστον {0} χαρακτήρες." ),
	rangelength: $.validator.format( "Παρακαλώ εισάγετε μια τιμή με μήκος μεταξύ {0} και {1} χαρακτήρων." ),
	range: $.validator.format( "Παρακαλώ εισάγετε μια τιμή μεταξύ {0} και {1}." ),
	max: $.validator.format( "Παρακαλώ εισάγετε μια τιμή μικρότερη ή ίση του {0}." ),
	min: $.validator.format( "Παρακαλώ εισάγετε μια τιμή μεγαλύτερη ή ίση του {0}." )
} );
return $;
}));