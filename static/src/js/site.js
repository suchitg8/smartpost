/* global window */
window.jQuery = window.$ = require('jquery');

const $ = window.$;

require('bootstrap');
require('fullcalendar');
require('./jquery-1.12.4');
require('./jquery-ui.min');
require('./jquery.steps');
require('./jquery.validate.min');
require('./source');

var toggle=true;

$(() => {
  const popoverContent = event => {
    let buttons = '';
    console.log(event);
    console.log("popover");

    if (event.approved === null) {
      buttons = `<button type='button' class='btn btn-primary pull-left btn-sm js-approve-content'>Approve</button><button type='button' class='btn btn-danger pull-right btn-sm js-reject-content'>Reject</button>`;
    }
  
    console.log(event.fb_groups);
    console.log(event.fb_pages);
    var fb_groups = "", fb_pages="";
    for(var i=0; i<event.fb_groups.length; i++)
      fb_groups += event.fb_groups[i].id + ":" + event.fb_groups[i].name + "|";
    for(var i=0; i<event.fb_pages.length; i++)
      fb_pages += event.fb_pages[i].id + ":" + event.fb_pages[i].name + "|";

    return `<div class='date'>${event.start.format('MMMM Do YYYY, h:mm:ss a')}</div>
     <div class='description col-md-6'>${event.content.slice(0,100)}</div>
     <div class='pull-right col-md-4'> <img width='100%' height="100px" src='${event.image}' alt=''/> </div>
     <div style="display:none;" class="fb-groups"> ${fb_groups} </div>
     <div style="display:none;" class="fb-pages"> ${fb_pages} </div>
     <div class="clearfix"> </div> <br/>`;
  };

  $('#calendar').fullCalendar({
    viewRender: view => {
      $('.fc-left h2').html(`<small>Manage your social media publications for ${view.title}</small>`);
    },
    events: '/publications/get_all',

    eventRender: function(event, element){
        element.popover({
          title: event.title,
          animation: true,
          delay: 300,
          html: true,
          placement: 'top',
          template: `<div class="popover calendar-popover col-md-6" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content" data-id="${event.id}"></div></div>`,
          content: popoverContent(event),
          trigger: 'hover'
        });
    },
    eventClick(event) {
      var portal=$("#publish-portal");
      var content = $(`<div>`+popoverContent(event)+`</div>`);
      var social_ct = $("#user_social_info");
      var fb_groups = $(content).find(".fb-groups").first().text(), fb_parsed = "", tp;
      var fb_pages = $(content).find(".fb-pages").first().text();
      console.log(fb_groups);
      console.log(fb_pages);
      fb_parsed = `<div class="social_info"><h4> <b>Post to Facebook and Pinterest?</b></h4>`;
      for(var i=0; i<fb_groups.split("|").length-1;i++) {
        tp = fb_groups.split("|")[i].split(":");
        fb_parsed += `<label><input type="checkbox" name="groups[`+tp[0]+']" value="'+tp[1]+'" /> '+tp[1]+'</label>';
      }
      for(var i=0; i<fb_pages.split("|").length-1;i++) {
        tp = fb_pages.split("|")[i].split(":");
        fb_parsed += `<label><input type="checkbox" name="pages[`+tp[0]+']" value="'+tp[1]+'" /> '+tp[1]+'</label>';
      }
      fb_parsed+='</div>'
      content.append(fb_parsed);
      console.log(content);
      portal.find(".title").first().text(event.title);
      portal.find(".content").first().html(content.html());
      portal.modal();
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
