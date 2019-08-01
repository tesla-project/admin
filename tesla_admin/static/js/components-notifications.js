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

    Messenger.options = {
        extraClasses: 'messenger-fixed messenger-on-top  messenger-on-right',
        theme: 'flat',
        messageDefaults: {
            showCloseButton: true
        }
    }

    $('#demoMessage').on('click', function () {
        Messenger().post({
            message: 'How are you?',
            type: 'success'
        });
    });

    $('#demoMessage2').on('click', function () {
        Messenger().post({
            message: 'There was an explosion while processing your request.',
            type: 'error',
            showCloseButton: true
        });
    });

    $('#demoMessage3').on('click', function () {
        Messenger().post({
            message: 'No unusual activity around. Carry on.',
            type: 'info',
            showCloseButton: true
        });
    });


    $('#demoMessage4').on('click', function () {
        i = 0;

        Messenger().run({
            errorMessage: 'Error destroying alien planet',
            successMessage: 'Alien planet destroyed!',
            action: function (opts) {
                if (++i < 2) {
                    return opts.error({
                        status: 500,
                        readyState: 0,
                        responseText: 0
                    });
                } else {
                    return opts.success();
                }
            }
        });
    });

    $('#demoMessage5').on('click', function () {
        msg = Messenger().post({
            message: "I'm sorry Hal, I just can't do that.",
            actions: {
                retry: {
                    label: 'retry now',
                    phrase: 'Retrying TIME',
                    auto: true,
                    delay: 10,
                    action: function () {}
                },
                cancel: {
                    action: function () {
                        return msg.cancel();
                    }
                }
            }
        });
    });
});