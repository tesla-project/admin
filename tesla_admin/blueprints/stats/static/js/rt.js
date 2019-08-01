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

var legendState = true;
    if ($(window).outerWidth() < 576) {
        legendState = false;
    }

var num_learners_chart_opts = {
    type: 'line',
    options: {
        scales: {
            xAxes: [{
                type: 'time',
                display: true,
                gridLines: {
                    display: false
                }
            }],
            yAxes: [{
                display: true,
                gridLines: {
                    display: false
                }
            }]
        },
        legend: {
            display: legendState
        }
    },
    data: {
        labels: [],
        datasets: [
            {
                label: "Total",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: '#535353',
                pointBorderColor: '#000000',
                pointHoverBackgroundColor: '#000000',
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 0,
                data: [],
                spanGaps: false
            },
            {
                label: "Valid IC",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: "#54e69d",
                pointHoverBackgroundColor: "#44c384",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBorderColor: "#44c384",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
                spanGaps: false
            },
            {
                label: "Outdated IC",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: "#f9b02f",
                pointHoverBackgroundColor: "#e69d2f",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBorderColor: "#e69d2f",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
                spanGaps: false
            },
            {
                label: "Rejected IC",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: '#f15765',
                pointBorderColor: '#da4c59',
                pointHoverBackgroundColor: '#da4c59',
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 0,
                data: [],
                spanGaps: false
            },
            {
                label: "No IC",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: '#2d91f1',
                pointBorderColor: '#1a1fda',
                pointHoverBackgroundColor: '#1a1fda',
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 0,
                data: [],
                spanGaps: false
            }
            ]
        }
    };
var num_requests_chart_opts = {
    type: 'line',
    options: {
        scales: {
            xAxes: [{
                type: 'time',
                display: true,
                gridLines: {
                    display: false
                }
            }],
            yAxes: [{
                display: true,
                gridLines: {
                    display: false
                }
            }]
        },
        legend: {
            display: legendState
        }
    },
    data: {
        labels: [],
        datasets: [
            {
                label: "Enrolment (Pending)",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: '#535353',
                pointBorderColor: '#000000',
                pointHoverBackgroundColor: '#000000',
                borderCapStyle: 'butt',
                borderDash: [5, 15],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 0,
                data: [],
                spanGaps: false
            },
            {
                label: "Enrolment (Processed)",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: "#54e69d",
                pointBorderColor: "#44c384",
                pointHoverBackgroundColor: "#44c384",
                borderCapStyle: 'butt',
                borderDash: [5, 15],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
                spanGaps: false
            },
            {
                label: "Enrolment (Failed)",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: '#f15765',
                pointBorderColor: '#da4c59',
                pointHoverBackgroundColor: '#da4c59',
                borderCapStyle: 'butt',
                borderDash: [5, 15],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 0,
                data: [],
                spanGaps: false
            },
            {
                label: "Verification (Pending)",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: '#535353',
                pointBorderColor: '#000000',
                pointHoverBackgroundColor: '#000000',
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 0,
                data: [],
                spanGaps: false
            },
            {
                label: "Verification (Processed)",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: "#54e69d",
                pointBorderColor: "#44c384",
                pointHoverBackgroundColor: "#44c384",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: [],
                spanGaps: false
            },
            {
                label: "Verification (Failed)",
                fill: true,
                lineTension: 0,
                backgroundColor: "transparent",
                borderColor: '#f15765',
                pointBorderColor: '#da4c59',
                pointHoverBackgroundColor: '#da4c59',
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                borderWidth: 1,
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBorderColor: "#fff",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 0,
                data: [],
                spanGaps: false
            }
            ]
        }
    };

var num_learners_chart = null;
var num_requests_chart = null;

function update_plots(data) {
    if (num_learners_chart) {
        num_learners_chart.data.labels.push(data['timestamp']);
        num_learners_chart.data.datasets[0].data.push(data['stats']['learners']['total']);
        num_learners_chart.data.datasets[1].data.push(data['stats']['learners']['ic_ok']);
        num_learners_chart.data.datasets[2].data.push(data['stats']['learners']['ic_outdated']);
        num_learners_chart.data.datasets[3].data.push(data['stats']['learners']['ic_rejected']);
        num_learners_chart.data.datasets[4].data.push(data['stats']['learners']['no_ic']);
        num_learners_chart.update()
    }
    if (num_requests_chart) {
        num_requests_chart.data.labels.push(data['timestamp']);
        num_requests_chart.data.datasets[0].data.push(data['stats']['requests']['enrolment']['pending']);
        num_requests_chart.data.datasets[1].data.push(data['stats']['requests']['enrolment']['processed']);
        num_requests_chart.data.datasets[2].data.push(data['stats']['requests']['enrolment']['failed']);
        num_requests_chart.data.datasets[3].data.push(data['stats']['requests']['verification']['pending']);
        num_requests_chart.data.datasets[4].data.push(data['stats']['requests']['verification']['processed']);
        num_requests_chart.data.datasets[5].data.push(data['stats']['requests']['verification']['failed']);
        num_requests_chart.update()
    }
}

$(function () {
    num_learners_chart = new Chart("chart_num_learners", num_learners_chart_opts);
    num_requests_chart = new Chart("chart_num_requests", num_requests_chart_opts);
    (function worker() {
        $.ajax({
            url: Flask.url_for("stats.rt_stats"),
        success: function(data) {
                if(parseInt(data['status_code']) == 0) {
                    $("#current_total").text(data['stats']['learners']['total']);
                    $("#current_ic_ok").text(data['stats']['learners']['ic_ok']);
                    $("#current_ic_outdated").text(data['stats']['learners']['ic_outdated']);
                    $("#current_ic_rejected").text(data['stats']['learners']['ic_rejected']);
                    $("#current_no_ic").text(data['stats']['learners']['no_ic']);

                    $("#current_req_en_total").text(data['stats']['requests']['enrolment']['pending'] + data['stats']['requests']['enrolment']['processed'] + data['stats']['requests']['enrolment']['failed']);
                    $("#current_req_en_pending").text(data['stats']['requests']['enrolment']['pending']);
                    $("#current_req_en_processed").text(data['stats']['requests']['enrolment']['processed']);
                    $("#current_req_en_failed").text(data['stats']['requests']['enrolment']['failed']);
                    $("#current_req_ver_total").text(data['stats']['requests']['verification']['pending'] + data['stats']['requests']['verification']['processed'] + data['stats']['requests']['verification']['failed']);
                    $("#current_req_ver_pending").text(data['stats']['requests']['verification']['pending']);
                    $("#current_req_ver_processed").text(data['stats']['requests']['verification']['processed']);
                    $("#current_req_ver_failed").text(data['stats']['requests']['verification']['failed']);

                    update_plots(data);
                }
        },
        complete: function() {
            // Schedule the next request when the current one's complete
            setTimeout(worker, 5000);
        }
        });
    })();
});

