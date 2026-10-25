(function () {
  'use strict';
  var config = window.blogCommunity || {};
  var username = String(config.buttondownUsername || '').trim();
  var websiteId = String(config.hyvorWebsiteId || '').trim();

  document.querySelectorAll('[data-newsletter]').forEach(function (section) {
    if (!/^[a-zA-Z0-9_-]+$/.test(username)) return;
    var form = section.querySelector('form');
    form.action = 'https://buttondown.com/api/emails/embed-subscribe/' + encodeURIComponent(username);
    section.hidden = false;
    form.querySelector('button').disabled = false;
  });

  var comments = document.querySelector('[data-comments]');
  if (!comments || !/^[1-9][0-9]*$/.test(websiteId)) return;
  comments.hidden = false;
  // Loading is explicit: reading an article alone does not contact Hyvor.
  var button = comments.querySelector('button');
  button.addEventListener('click', function () {
    button.disabled = true;
    var status = comments.querySelector('[role="status"]');
    status.textContent = 'Loading comments…';
    var embed = document.createElement('hyvor-talk-comments');
    embed.setAttribute('website-id', websiteId);
    // A fixed post slug keeps the thread stable across .html/clean URLs.
    embed.setAttribute('page-id', comments.dataset.pageId);
    comments.appendChild(embed);
    var script = document.createElement('script');
    script.src = 'https://talk.hyvor.com/embed/embed.js';
    script.type = 'module';
    script.async = true;
    script.onload = function () {
      button.hidden = true;
      status.textContent = 'If comments do not appear, check your content blocker and reload to try again.';
    };
    script.onerror = function () {
      embed.remove();
      script.remove();
      button.disabled = false;
      status.textContent = 'Comments could not load. Please try again.';
    };
    document.head.appendChild(script);
  });
})();
