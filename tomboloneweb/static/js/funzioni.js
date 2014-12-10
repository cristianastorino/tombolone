$(".numero").click(function(){

  $.getJSON('/aggiungi_rimuovi_estratto', {
        num: $(this).html()
      }, function(data) {}
  );

  if ($(this).hasClass('nonuscito')) {
   $(this).removeClass('nonuscito');
   $(this).addClass('uscito');
  }
  else {
   $(this).removeClass('uscito');
   $(this).addClass('nonuscito');
  }
});

$(function() {
  $.getJSON('/get_estratti', {}, 
    function(data) {
      jQuery.each(data.numeri, function() {
        $("#div" + this).removeClass('nonuscito');
        $("#div" + this).addClass('uscito');
      });
  });

$('a#ambo').bind('click', function() {
  $.getJSON('/vittoria', {
    tipo: "Ambo!"
  }, function(data) {});
  return false;
});

$('a#terno').bind('click', function() {
  $.getJSON('/vittoria', {
    tipo: "Terno!"
  }, function(data) {});
  return false;
});

$('a#quaterna').bind('click', function() {
  $.getJSON('/vittoria', {
    tipo: "Quaterna!"
  }, function(data) {});
  return false;
});

$('a#cinquina').bind('click', function() {
  $.getJSON('/vittoria', {
    tipo: "Cinquina!"
  }, function(data) {});
  return false;
});

$('a#tombola').bind('click', function() {
  $.getJSON('/vittoria', {
    tipo: "Tombola!"
  }, function(data) {});
  return false;
});

});

$body = $("body");

$(document).on({
    ajaxStart: function() { 
        $body.addClass("loading"); 
    },
    ajaxStop: function() { 
        $body.removeClass("loading"); 
    }    
});
