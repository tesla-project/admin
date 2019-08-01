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

$(function () {
    var stats = {};
    var opts = {
        angle: 0, // The span of the gauge arc
        lineWidth: 0.44, // The line thickness
        radiusScale: 1, // Relative radius
        pointer: {
            length: 0.6, // // Relative to gauge radius
            strokeWidth: 0.035, // The thickness
            color: '#000000' // Fill color
        },
        colorStart: '#6FADCF',   // Colors
        colorStop: '#8FC0DA',    // just experiment with them
        strokeColor: '#E0E0E0',  // to see which ones work best for you
        generateGradient: true,
        highDpiSupport: true     // High resolution support
    };

    var opts_pending = $.extend({}, opts);
    opts_pending['staticZones'] = [
           {strokeStyle: "#30B32D", min: 0, max: 500}, // Green
           {strokeStyle: "#FFDD00", min: 501, max: 1000}, // Yellow
           {strokeStyle: "#F03E3E", min: 1001, max: 2000}  // Red
        ];

    var opts_d = $.extend({}, opts);
    opts_d['staticZones'] = [
           {strokeStyle: "#30B32D", min: -500, max: 0}, // Green
           {strokeStyle: "#FFDD00", min: 1, max: 20}, // Yellow
           {strokeStyle: "#F03E3E", min: 20, max: 500}  // Red
        ];

    function createInstrumentStats(acronym) {
        if (! document.getElementById(acronym.toLowerCase() + '-pending-canvas')) {
            return
        }
        var gauge_pending = new Gauge(document.getElementById(acronym.toLowerCase() + '-pending-canvas')).setOptions(opts_pending);
        gauge_pending.setTextField(document.getElementById(acronym.toLowerCase() + '-pending-value'));
        gauge_pending.maxValue = 2000; // set max gauge value
        gauge_pending.setMinValue(0); // set min value

        var gauge_d1 = new Gauge(document.getElementById(acronym.toLowerCase() + '-d1-canvas')).setOptions(opts_d);
        gauge_d1.setTextField(document.getElementById(acronym.toLowerCase() + '-d1-value'));
        gauge_d1.maxValue = 500; // set max gauge value
        gauge_d1.setMinValue(-500); // set min value

        var gauge_d2 = new Gauge(document.getElementById(acronym.toLowerCase() + '-d2-canvas')).setOptions(opts_d);
        gauge_d2.setTextField(document.getElementById(acronym.toLowerCase() + '-d2-value'));
        gauge_d2.maxValue = 500; // set max gauge value
        gauge_d2.setMinValue(-500); // set min value

        stats[acronym.toLowerCase()] = {'pending': gauge_pending, 'd1': gauge_d1, 'd2':gauge_d2};
    }


    function setInstrumentStats(acronym, pending, velocity, acceleration, workers, status, service, database, updated) {

        acronym = acronym.toLowerCase();
        var current_stats = stats[acronym];

        if (! current_stats) {
            return;
        }

        $('#' + acronym + '-status').removeClass();
        $('#' + acronym + '-status-update').text(moment(updated).fromNow());
        if (status > 0) {
            $('#' + acronym + '-status').addClass('led-green');
            $(".instrument-stats[data-acronym='" + acronym + "'] > .chart").show();
            $('#' + acronym + '-msg-disabled').hide();
            $('#' + acronym + '-msg-missing').hide();
            if (service) {
                $('.' + acronym + '-workers').hide();
            } else {
                $('.' + acronym + '-service').hide();
            }
        } else {
            $(".instrument-stats[data-acronym='" + acronym + "'] > .chart").hide();
            if(status == 0) {
                $('#' + acronym + '-status').addClass('led-off');
                $('#' + acronym + '-msg-disabled').show();
                $('#' + acronym + '-msg-missing').hide();
            } else {
                $('#' + acronym + '-status').addClass('led-red');
                $('#' + acronym + '-msg-disabled').hide();
                $('#' + acronym + '-msg-missing').show();
            }
        }

        current_stats['pending'].set(pending);
        current_stats['d1'].set(velocity);
        current_stats['d2'].set(acceleration);

        $('#' + acronym + '-workers').text(workers);
        $('#' + acronym + '-service').text(service);
        $('#' + acronym + '-db').text(database);
        $('#' + acronym + '-satus').removeClass();


    }

    $.each($('.instrument-stats'), function() {
        var inst = this.dataset['acronym'].toLowerCase();
        createInstrumentStats(inst);
        setInstrumentStats(inst, 0, 0, 0, 0, 0);
    });

    (function worker() {
        $.ajax({
            url: Flask.url_for("system.instrument_status"),
        success: function(data) {
                if(parseInt(data['status_code']) == 0) {
                    $.each(data['status'], function() {
                        var service = 0;
                        var database = 0;
                        if(this['service']!=null) {
                            if(this['service']) {
                                service = 1;
                            }
                        }
                        if(this['service_info']!=null){
                            database = this['service_info']['db_connection']
                        }
                        var status = 0;
                        if(this['active']) {
                            if(this['workers']>0 || (service==1 && database==1)) {
                                status = 1;
                            } else {
                                status = -1;
                            }
                        }
                        setInstrumentStats(this['acronym'].toLowerCase(), this['pending'], this['d1'], this['d2'], this['workers'], status, service, database, this['updated']);
                    });
                }
        },
        complete: function() {
            // Schedule the next request when the current one's complete
            setTimeout(worker, 5000);
        }
        });
    })();
});