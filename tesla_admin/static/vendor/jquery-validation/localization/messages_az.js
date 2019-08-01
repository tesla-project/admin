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
 * Locale: Az (Azeri; azərbaycan dili)
 */
$.extend( $.validator.messages, {
	required: "Bu xana mütləq doldurulmalıdır.",
	remote: "Zəhmət olmasa, düzgün məna daxil edin.",
	email: "Zəhmət olmasa, düzgün elektron poçt daxil edin.",
	url: "Zəhmət olmasa, düzgün URL daxil edin.",
	date: "Zəhmət olmasa, düzgün tarix daxil edin.",
	dateISO: "Zəhmət olmasa, düzgün ISO formatlı tarix daxil edin.",
	number: "Zəhmət olmasa, düzgün rəqəm daxil edin.",
	digits: "Zəhmət olmasa, yalnız rəqəm daxil edin.",
	creditcard: "Zəhmət olmasa, düzgün kredit kart nömrəsini daxil edin.",
	equalTo: "Zəhmət olmasa, eyni mənanı bir daha daxil edin.",
	extension: "Zəhmət olmasa, düzgün genişlənməyə malik faylı seçin.",
	maxlength: $.validator.format( "Zəhmət olmasa, {0} simvoldan çox olmayaraq daxil edin." ),
	minlength: $.validator.format( "Zəhmət olmasa, {0} simvoldan az olmayaraq daxil edin." ),
	rangelength: $.validator.format( "Zəhmət olmasa, {0} - {1} aralığında uzunluğa malik simvol daxil edin." ),
	range: $.validator.format( "Zəhmət olmasa, {0} - {1} aralığında rəqəm daxil edin." ),
	max: $.validator.format( "Zəhmət olmasa, {0} və ondan kiçik rəqəm daxil edin." ),
	min: $.validator.format( "Zəhmət olmasa, {0} və ondan böyük rəqəm daxil edin" )
} );
return $;
}));