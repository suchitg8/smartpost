/* global window */
window.jQuery = window.$ = require('jquery');

const $ = window.$;

require('bootstrap');
<<<<<<< HEAD
require('./jquery-1.12.4');
require('./jquery-ui.min');
require('./jquery.steps');
require('./jquery.validate.min');
require('./source');
=======
require('fullcalendar');
>>>>>>> 4d59c9886edec9be62651346c98ca5bfa53c47a9

$(() => {
  const popoverContent = event => {
    let buttons = '';
    console.log(event);

    if (event.approved === null) {
      buttons = `<button type='button' class='btn btn-primary pull-left btn-sm js-approve-content'>Approve</button><button type='button' class='btn btn-danger pull-right btn-sm js-reject-content'>Reject</button>`;
    }
  
    return `<div class='date'>${event.start.format('MMMM Do YYYY, h:mm:ss a')}</div>
     <div class='description'>${event.content}</div>
     <div class='buttons'>${buttons}</div>
     <div style="margin-top:10px"><a href="" class="js-publish pull-right"><small>Publish now</small></a></div>`;
  };

  $('#calendar').fullCalendar({
    viewRender: view => {
      $('.fc-left h2').html(`<small>Manage your social media publications for ${view.title}</small>`);
    },
    events: '/publications/get_all',
    eventClick(event) {
      const options = {
        title: event.title,
        content: popoverContent(event),
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

  $('body').on('click', '.js-publish', e => {
    e.preventDefault();

    updateEvent(e, 'publish', () => {
      $('#calendar').fullCalendar('refetchEvents');
    });
  });

  $('body').on('click', '.js-reject-content', e => {
    updateEvent(e, 'reject', data => {
      $('#calendar').fullCalendar('refetchEvents');

      if (!data.length) {
        $('#support-modal').modal();
      }
    });
  });

  $('.js-get-posts').on('click', () => {
    $.ajax({
      url: '/publications/get_new/',
      method: 'POST',
      success: () => {
        $('#calendar').fullCalendar('refetchEvents');
      }
    });
  });
});
