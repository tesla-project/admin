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

function get_histogram_data_prob(data, bean, polarity) {
    var lower_results = Array(10);
    var higher_results = Array(10);
    var current_value = Array(10);

    for(i=0;i<10;i++){
        if (i < bean - 1) {
            lower_results[i] = data[i];
            current_value[i] = 0;
            higher_results[i] = 0;
        } else if (i < bean) {
            lower_results[i] = data[i];
            current_value[i] = data[i] * 0.5;
            higher_results[i] = 0;
        } else if (i == bean) {
            lower_results[i] = 0;
            current_value[i] = data[i];
            higher_results[i] = 0;
        } else if (i== bean + 1) {
            lower_results[i] = 0;
            current_value[i] = data[i] * 0.5;
            higher_results[i] = data[i];
        } else {
            lower_results[i] = 0;
            current_value[i] = 0;
            higher_results[i] = data[i];
        }
    }

    var h_values = null;
    if (polarity > 0) {
        h_values = higher_results;
    } else {
        h_values = lower_results;
    }

    return { 'h_values': h_values, 'current': current_value};
}

(function() {
    try {
        var d3 = Plotly.d3;
        var WIDTH_IN_PERCENT_OF_PARENT = 100,
            HEIGHT_IN_PERCENT_OF_PARENT = 15;

        var gd3 = d3.selectAll(".responsive-plot")
            .style({
                width: WIDTH_IN_PERCENT_OF_PARENT + '%',
                //'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',
                'margin-left': '2px',

                height: HEIGHT_IN_PERCENT_OF_PARENT + 'vh',
                //'margin-top': (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + 'vh'
                'margin-top': '2px'
            });

        var nodes_to_resize = gd3[0]; //not sure why but the goods are within a nested array
        window.onresize = function () {
            try {
                for (var i = 0; i < nodes_to_resize.length; i++) {
                    if (nodes_to_resize[i].childNodes.length > 0) {
                        Plotly.Plots.resize(nodes_to_resize[i]);
                    }
                }
            } catch(error) {

            }
        };
    } catch(error) {

    }
})();

function norm_hist(hist) {
    var hist_sum = 0;
    var norm_hist = Array(10);

    for( i=0; i<hist.length; i++) {
        hist_sum = hist_sum + hist[i];
        norm_hist[i] = hist[i];
    }
    if(hist_sum > 0) {
        for( i=0; i<hist.length; i++) {
            norm_hist[i] = Math.round((norm_hist[i]/hist_sum) * 1000)/10;
        }
    }
    return norm_hist;
}

function get_hist_data(histogram, result_bean, polarity) {
    var hist_data = [];
    var n_hist = norm_hist(histogram);

    // Add learner histogram
    hist_data.push({
        type: 'bar',
        name: 'Results',
        x: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        y: n_hist,
        marker: {
            color: '#C8A2C8',
            line: {
                width: 2.5
            }
        }
    });

    if (result_bean != null) {
        var data = get_histogram_data_prob(n_hist, result_bean, polarity);

        // Add better values overlay
        hist_data.push({
            type: 'bar',
            name: 'Better Results',
            x: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            y: data.h_values,
            marker: {
                color: '#ea1320',
                opacity: 0.5,
                line: {
                    width: 2.5
                }
            }
        });

        // Add current value overlay
        hist_data.push({
            type: 'bar',
            name: 'Current Result',
            x: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            y: data.current,
            marker: {
                color: '#1cc81c',
                opacity: 0.5,
                line: {
                    width: 2.5
                }
            }
        });
    }

    return hist_data;
}
$(function () {
    $( ".learner-histogram" ).each(function( index ) {
        var instrument_id = this.dataset.id;
        var hist_data = get_hist_data(instrument_data[instrument_id].learner_histogram, instrument_data[instrument_id].result_bean, instrument_data[instrument_id].polarity);

        Plotly.plot(this.id, hist_data, {
            title: 'Learner histogram',
            xaxis: {
                range: [-1, 10],
                showticklabels : false
                //tickmode: 'array',
                //ticktext: ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
            },
            yaxis: {
                range: [0, 100],
                showticklabels : false
            },
            showlegend: false,
            margin: {l: 10, t:30, b:10, r:10},
            barmode: "overlay"
        }, {
            displayModeBar: false
        });
    });
    $( ".context-histogram" ).each(function( index ) {
        var instrument_id = this.dataset.id;

        var hist_data = get_hist_data(instrument_data[instrument_id].context_histogram, instrument_data[instrument_id].result_bean, instrument_data[instrument_id].polarity);

        Plotly.plot(this.id, hist_data, {
            title: 'Context histogram',
            xaxis: {
                range: [-1, 10],
                showticklabels : false
                //tickmode: 'array',
                //ticktext: ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
            },
            yaxis: {
                range: [0, 100],
                showticklabels : false
            },
            showlegend: false,
            margin: {l: 10, t:30, b:10, r:10},
            barmode: "overlay"
        }, {
            displayModeBar: false
        });
    });


    var plot_data = [];
    Object.keys(instrument_data).forEach(function(key) {
        plot_data.push({
            name: instrument_data[key].acronym,
            type: "scatter",
            mode: "lines+markers",
            x: instrument_data[key].temporal.date,
            y: instrument_data[key].temporal.value
        });
    });
    plot_data.push({
        name: 'Errors',
        type: "scatter",
        mode: "markers+text",
        text: failed_requests.error,
        textposition: 'top center',
        x: failed_requests.date,
        y: failed_requests.value,
        marker: {
            color: 'rgb(255, 0, 0)',
            symbol: 'triangle-up'
        }
    });
    var layout = {
        title: 'Temporal Results',
        xaxis: {
            type: 'date'
        },
        yaxis: {
            autorange: true,
            range: [0, 1],
            type: 'linear'
        },
        rangeslider:{
            visible: true
        },
        connectgaps: false
    };

    Plotly.newPlot('temporal_results', plot_data, layout, {
            displayModeBar: false
        });

});