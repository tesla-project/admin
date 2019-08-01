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

// Prevent Dropzone from auto discovering this element:
Dropzone.options.demoUpload = false;
// This is useful when you want to create the
// Dropzone programmatically later
// I use it here just to avoid auto-init for the demo element, you don't have to use this approach in your app

$(function () {
    var dropzone = new Dropzone('#demo-upload', {
        
        parallelUploads: 2,
        thumbnailHeight: 120,
        thumbnailWidth: 120,
        maxFilesize: 3,
        filesizeBase: 1000,
        thumbnail: function(file, dataUrl) {
          if (file.previewElement) {
            file.previewElement.classList.remove("dz-file-preview");
            var images = file.previewElement.querySelectorAll("[data-dz-thumbnail]");
            for (var i = 0; i < images.length; i++) {
              var thumbnailElement = images[i];
              thumbnailElement.alt = file.name;
              thumbnailElement.src = dataUrl;
            }
            setTimeout(function() { file.previewElement.classList.add("dz-image-preview"); }, 1);
          }
        }
    
      });
    
    
      // Now fake the file upload for demo purposes, delete this function on production and create a backend script
      // and returns a 404
    
      var minSteps = 6,
          maxSteps = 60,
          timeBetweenSteps = 100,
          bytesPerStep = 100000;
    
      dropzone.uploadFiles = function(files) {
        var self = this;
    
        for (var i = 0; i < files.length; i++) {
    
          var file = files[i];
              totalSteps = Math.round(Math.min(maxSteps, Math.max(minSteps, file.size / bytesPerStep)));
    
          for (var step = 0; step < totalSteps; step++) {
            var duration = timeBetweenSteps * (step + 1);
            setTimeout(function(file, totalSteps, step) {
              return function() {
                file.upload = {
                  progress: 100 * (step + 1) / totalSteps,
                  total: file.size,
                  bytesSent: (step + 1) * file.size / totalSteps
                };
    
                self.emit('uploadprogress', file, file.upload.progress, file.upload.bytesSent);
                if (file.upload.progress == 100) {
                  file.status = Dropzone.SUCCESS;
                  self.emit("success", file, 'success', null);
                  self.emit("complete", file);
                  self.processQueue();
                }
              };
            }(file, totalSteps, step), duration);
          }
        }
      }
});

