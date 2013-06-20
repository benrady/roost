function triggerEvent(name, data) {
  $('#content-main>*').trigger(appName + '.' + name, data);
}

function showView(name) {
  triggerEvent('viewClose', name);
  $('.nav li').removeClass('active');
  $('a[href=#' + name +']').closest('li').addClass('active');
  $('#content-main').
    empty().
    append(routes[name]());
}

function currentView() {
  return window.location.hash.split('#')[1] || 'home';
}

function routerOnReady() {
  $(document).ready(function() {
    window.onhashchange = function() {
      showView(currentView());
      return true;
    };
    showView(currentView());
  });
}
