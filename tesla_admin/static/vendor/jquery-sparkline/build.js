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

var shell = require('shelljs');

var package = require('./package');

var files = ['header.js', 'defaults.js', 'utils.js', 'simpledraw.js', 'rangemap.js', 'interact.js', 'base.js', 'chart-line.js', 'chart-bar.js', 'chart-tristate.js', 'chart-discrete.js', 'chart-bullet.js', 'chart-pie.js', 'chart-box.js', 'vcanvas-base.js', 'vcanvas-canvas.js', 'vcanvas-vml.js', 'footer.js'];

shell.cd('src');

var src = shell.cat(files).replace(/@VERSION@/mg, package.version);

shell.cd('..');

src.to('jquery.sparkline.js');
