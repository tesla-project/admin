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

/**
 * Bootstrap Table French (France) translation
 * Author: Dennis Hernández (http://djhvscf.github.io/Blog/)
 * Modification: Tidalf (https://github.com/TidalfFR)
 */
(function ($) {
    'use strict';

    $.fn.bootstrapTable.locales['fr-FR'] = {
        formatLoadingMessage: function () {
            return 'Chargement en cours, patientez, s´il vous plaît ...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' lignes par page';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Affichage des lignes ' + pageFrom + ' à ' + pageTo + ' sur ' + totalRows + ' lignes au total';
        },
        formatSearch: function () {
            return 'Rechercher';
        },
        formatNoMatches: function () {
            return 'Aucun résultat trouvé';
        },
        formatPaginationSwitch: function () {
            return 'Montrer/Masquer pagination';
        },
        formatRefresh: function () {
            return 'Rafraîchir';
        },
        formatToggle: function () {
            return 'Alterner';
        },
        formatColumns: function () {
            return 'Colonnes';
        },
        formatAllRows: function () {
            return 'Tous';
        },
        formatExport: function () {
            return 'Exporter les données';
        },
        formatClearFilters: function () {
            return 'Vider les filtres';
        },
        formatMultipleSort: function() {
            return 'Tri avancé';
        },
        formatAddLevel: function() {
            return 'Ajouter un niveau';
        },
        formatDeleteLevel: function() {
            return 'Supprimer un niveau';
        },
        formatColumn: function() {
            return 'Colonne';
        },
        formatOrder: function() {
            return 'Ordre';
        },
        formatSortBy: function() {
            return 'Trier par';
        },
        formatThenBy: function() {
            return 'Puis par';
        },
        formatSort: function() {
            return 'Trier';
        },
        formatCancel: function() {
            return 'Annuler';
        },
        formatDuplicateAlertTitle: function() {
            return 'Doublon(s) détecté(s)!';
        },
        formatDuplicateAlertDescription: function() {
            return 'Supprimez ou changez les colonnes dupliquées.';
        },
        formatSortOrders: function() {
            return {
                asc: 'Croissant',
                desc: 'Décroissant'
            };
        },
        formatAdvancedSearch: function() {
            return 'Recherche avancée';
        },
        formatAdvancedCloseButton: function() {
            return "Fermer";
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['fr-FR']);

})(jQuery);
