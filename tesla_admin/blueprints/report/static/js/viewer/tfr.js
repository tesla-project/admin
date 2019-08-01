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

var frame_index = [];
var color = Chart.helpers.color;
    window.chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };
var video_data = {
  labels: [],
  datasets: {
      no_face: [],
      no_recog: [],
      multiple_face: []
  }
};

function is_video(audit_data) {
  if(audit_data.results.total_frames > 1) {
    return true;
  }
  return false;
}

function build_enrollment(enrollment_user_faces) {
  // Build the HTML code
  var html = [];
  html.push('<div class="card border-dark mb-3">');
  html.push('    <div class="card-header">' + gettext('FR_TITLE_ENROLLMENT_CARD') + '</div>');
  html.push('        <div class="owl-carousel owl-theme enrollment card-body">');
  for(var i=0; i< enrollment_user_faces.length; i++) {
      html.push('            <div class="item">');
      html.push('                <img height="270px" src="' + enrollment_user_faces[i] + '" class="rounded"></a>');
      html.push('            </div>');
  }
  html.push('        </div>');
  html.push('    </div>');
  html.push('</div>');

  return html.join('\n');
}

function build_chart(audit_data) {
  // Build the HTML code
  var html = [];
  html.push('<div class="card-body" style="margin-top: 1rem;">');
  html.push('    <canvas id="video_summary_canvas"></canvas>');
  html.push('</div>');

  // Create the datasets
  for(var i=0; i<audit_data.results.frame_codes.length; i++) {
      video_data.labels.push(i + 1);
      var code = audit_data.results.frame_codes[i];
      if (code > 0) {
          frame_index.push(i);
          if (code == 1) {
              video_data.datasets.no_face.push(1);
              video_data.datasets.no_recog.push(0);
              video_data.datasets.multiple_face.push(0);
          } else if (code == 2) {
              video_data.datasets.no_face.push(0);
              video_data.datasets.no_recog.push(0);
              video_data.datasets.multiple_face.push(1);
          } else {
              video_data.datasets.no_face.push(0);
              video_data.datasets.no_recog.push(1);
              video_data.datasets.multiple_face.push(0);
          }
      } else {
          video_data.datasets.no_face.push(0);
          video_data.datasets.no_recog.push(0);
          video_data.datasets.multiple_face.push(0);
      }
  }

  return html.join('\n');
}

function build_scene_card_body(audit_data) {
    var html = [];
    for(var i = 0; i < audit_data.results.frame_details.length; i++) {
        var code = audit_data.results.frame_codes[i];
        if (code > 0 ) {
            var item_header = '        <div class="item ';
            if(code == 1) {
                item_header += 'no_face';
            } else if(code == 2){
                item_header += 'multiple_faces';
            } else {
                item_header += 'not_recognized';
            }
            item_header += ' card" style="max-width: 40rem;">';
            html.push(item_header);
            html.push('            <img width="160px" src="' + audit_data.results.frame_details[i].scene_image + '" class="rounded card-img-top"></a>');
            html.push('            <div class="card-body">');
            if(code == 1) {
                html.push('                <h5 class="card-title">' + gettext('FR_TITLE_NO_FACE') + '</h5>');
                html.push('                <p class="card-text">' + gettext('FR_DESC_NO_FACE') + '</p>');
            } else if(code == 2){
                html.push('                <h5 class="card-title">' + gettext('FR_TITLE_MULT_FACE') + '</h5>');
                html.push('                <p class="card-text">' + gettext('FR_DESC_MULT_FACE') + '</p>');
            } else {
                html.push('                <h5 class="card-title">' + gettext('FR_TITLE_NO_RECON') + '</h5>');
                html.push('                <p class="card-text">' + gettext('FR_DESC_NO_RECON') + '</p>');
            }
            html.push('                <div class="card-group">');
            for(var f =0; f<audit_data.results.frame_details[i].face_distances.length; f++) {
                html.push('                    <div class="card mb3" style="max-width: 18rem;">');
                html.push('                        <img src="' + audit_data.results.frame_details[i].detected_faces[f] + '" class="rounded card-img-top"></a>');
                html.push('                        <div class="card-body"></div>');
                var score = 100.0 * Math.min(1.0, 1.0 - audit_data.results.frame_details[i].face_distances[f]);
                score = Math.round(score * 100) / 100.0;
                html.push('                        <div class="card-footer"><b>Score:</b> ' + score + '&#37;</div>');
                html.push('                    </div>');
            }
            html.push('                </div>');
            html.push('            </div>');
            html.push('        </div>');
        }
    }
    return html.join('\n');
}

function build_audit_body(audit_data) {
    var html = [];
    html.push('<div class="card border-dark mb-3">');
    html.push('    <div class="card-header">' + gettext('FR_TITLE_DETAILS_CARD') + '</div>');
    if(is_video(audit_data)) {
        html.push(build_chart(audit_data));
    }
    html.push('    <div class="row card-body">');
    if(is_video(audit_data)) {
        html.push('        <div class="owl-carousel owl-theme scene card-body card-desk col">');
    } else {
        html.push('        <div class="scene card-body card-desk col">');
    }
    html.push(build_scene_card_body(audit_data));
    html.push('        </div>');
    html.push('    </div>');
    html.push('</div>');
    return html.join('\n');
}

function show_summary_chart() {
    var barChartData = {
        labels: video_data.labels,
        datasets: [{
            label: gettext('FR_CHART_TITLE_NO_FACE'),
            backgroundColor: color(window.chartColors.grey).alpha(0.5).rgbString(),
            borderColor: window.chartColors.grey,
            borderWidth: 1,
            data: video_data.datasets.no_face
        }, {
            label: gettext('FR_CHART_TITLE_NO_RECOG'),
            backgroundColor: color(window.chartColors.orange).alpha(0.5).rgbString(),
            borderColor: window.chartColors.orange,
            borderWidth: 1,
            data: video_data.datasets.no_recog
        }, {
            label: gettext('FR_CHART_TITLE_MULT_FACES'),
            backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
            borderColor: window.chartColors.red,
            borderWidth: 1,
            data: video_data.datasets.multiple_face
        }]
    };
    var ctx = document.getElementById("video_summary_canvas").getContext("2d");
    window.myBar = new Chart(ctx, {
        type: 'bar',
        data: barChartData,
        options: {
            title:{
                display:true,
                text: gettext('FR_CHART_TITLE')
            },
            tooltips: {
                enabled: false
            },
            responsive: true,
            maintainAspectRatio: false,
            events: ['click'],
            onClick: function(e, active) {
                if (active.length > 0) {
                    var frame_idx = active[0]._index;
                    var num_frame = frame_index.indexOf(frame_idx);
                    var owl = $('.owl-carousel.scene');
                    owl.trigger('to.owl.carousel', [num_frame, 300]);
                }
            },
            scales: {
                xAxes: [{
                    stacked: true,
                    scaleLabel: {
                        display: true,
                        labelString: gettext('FR_CHART_X_LEGEND')
                    }
                }],
                yAxes: [{
                    stacked: true,
                    display: false,
                    ticks: {
                        max: 1,
                        min: 0,
                        stepSize: 1
                    }

                }]
            }
        }
    });
}

function show_details_carrousel() {
    $('.owl-carousel.scene').owlCarousel({
        loop:false,
        margin:10,
        nav:true,
        autoplay:false,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:1
            },
            1000:{
                items:1
            }
        }
    });
}

function buildInterface(json) {

    // Create the enrollment faces carousel
    var div = $('#enrolment');
    div.append(build_enrollment(json.audit_data.enrollment_user_faces));

    // Create the audit visualization block
    div = $('#request');
    div.append(build_audit_body(json.audit_data));

    // Activate the enrollment carousel
    $('.owl-carousel.enrollment').owlCarousel({
          loop: true,
          margin: 10,
          nav: true,
          autoplay: true,
          autoplayTimeout: 500,
          autoplayHoverPause: true,
          responsive: {
              0: {
                  items: 1
              },
              600: {
                  items: 3
              },
              1000: {
                  items: 6
              }
          }
    });
    if(is_video(json.audit_data)) {
        show_summary_chart();
        show_details_carrousel();
    }
}

$(document).ready(function() {
    /*var json = document.getElementById('audit_data').value;
    json = JSON.parse(json);
    json.audit_data = JSON.parse(json.audit_data.audit_data)
    buildInterface(json);*/
});