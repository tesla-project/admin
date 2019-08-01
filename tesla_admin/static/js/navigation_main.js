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

$('#messageModal').on('show.bs.modal', function (event) {
    var msg_link = $(event.relatedTarget);
    var message_id = msg_link.data('message-id');
    var modal = $(this);
    $.ajax(Flask.url_for("api_learner.get_user_message", {"message_id": message_id}), {
            method: 'GET'
    }).done(function(msg) {
        //"messageModal-title"
        //"messageModal-subject"
        //"messageModal-date"
        //"messageModal-content"
        modal.find('#messageModal-title').text('');
        modal.find('#messageModal-subject').text(msg['subject']);
        modal.find('#messageModal-date').text(moment(msg['created']).fromNow());
        modal.find('#messageModal-content').text(msg['content']);

        $.ajax(Flask.url_for("api_learner.read_user_message", {"message_id": message_id}), {
            method: 'GET'
        });
    }).fail(function() {

    });
});

$(function () {

});