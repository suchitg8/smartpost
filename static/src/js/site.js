/* global window */
window.jQuery = window.$ = require('jquery');

const $ = window.$;

require('bootstrap');
require('fullcalendar');

$(() => {
  $('#calendar').fullCalendar({
    header: {
      left: ''
    },
    events: '/publications/get_all',
    eventClick(event) {
      const options = {
        title: event.title,
        content: `<div class='date'>${event.start.format('MMMM Do YYYY, h:mm:ss a')}</div><div class='description'>${event.content}</div><div class='buttons'><button type='button' class='btn btn-primary pull-left btn-sm js-approve-content'>Approve</button><button type='button' class='btn btn-danger pull-right btn-sm js-reject-content'>Reject</button></div>`,
        html: true,
        placement: 'top',
        template: `<div class="popover calendar-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content" data-id="${event.id}"></div></div>`,
        trigger: 'manual'
      };

      $(this).popover(options);
      $(this).popover('toggle');
    }
  });

  const updateEvent = (e, action, callback) => {
    const id = $(e.target).parents('.popover-content').data('id');

    $.ajax({
      method: 'POST',
      url: `/publications/${id}/${action}/`,
      success: data => {
        callback(data);
      }
    });
  };

  $('body').on('click', '.js-approve-content', e => {
    updateEvent(e, 'approve', () => {
      $('#calendar').fullCalendar('refetchEvents');
    });
  });

  $('body').on('click', '.js-reject-content', e => {
    updateEvent(e, 'reject', data => {
      $('#calendar').fullCalendar('refetchEvents');
      console.log(data);
    });
  });
});
