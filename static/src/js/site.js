/* global window */
window.jQuery = window.$ = require('jquery');

const $ = window.$;

require('bootstrap');

$(() => {
  $('[data-toggle="popover"]').popover();

  $('body').on('click', '.js-approve-content', e => {
    console.log('approve');
    console.log($(e.target).parents('p').data('id'));

    const triggerElement = $(e.target).parents('p').children('a');
    triggerElement.popover('hide');

    const td = triggerElement.parents('td');
    td.addClass('approved');
  });

  $('body').on('click', '.js-reject-content', e => {
    console.log('reject');
    console.log($(e.target).parents('p').data('id'));

    const triggerElement = $(e.target).parents('p').children('a');
    triggerElement.popover('hide');

    const td = triggerElement.parents('td');
    td.addClass('rejected');
  });
});
