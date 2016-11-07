var firstYear = 0
var firstMonth = 0
var lastYear = 0
var lastMonth = 0
var reqYear = 0
var reqMonth = 0;

function updateFirst() {
  var elem = $("table[year]:first");
  firstYear = elem.attr("year");
  firstMonth = elem.attr("month");
}

function updateLast() {
  var elem = $("table[year]:last");
  lastYear = elem.attr("year");
  lastMonth = elem.attr("month");
}

function scrollToToday() {
  var body = $('html, body');
  var today = $('#id-today');
  if( today.length == 0 )
  {
    initPosition();
    return;
  }

  body.animate({
    scrollTop: today.offset().top - $(window).height() / 2
  }, 500, "swing", initPosition );
}

function initPosition()
{
  $(document).scroll(function() {
    var docHeight = $(document).height();
    var scrollTop = $(window).scrollTop();
    var currentScroll = $(window).scrollTop() + $(window).height();

    msg = "docHeight:" + docHeight + " ";
    msg += "winScrollTop:" + $(window).scrollTop() + " ";
    msg += "winHeight:" + $(window).height();

    $("#id-navmsg").text(msg);

    if(scrollTop < 100)
    {
      Prepend();
    }
    else if(docHeight <= currentScroll+100 )
    {
      Append();
    }
  })
}

$(document).ready(function() {
  updateFirst();
  updateLast();

  scrollToToday();
})

function Append()
{
  if( lastYear == 9999 && lastMonth == 12 )
    return;

  if( lastYear == reqYear && lastMonth == reqMonth )
    return;

  reqYear = lastYear
  reqMonth = lastMonth
  $.ajax({method: 'GET',
          url: '/cal/flood/next_year/' + reqYear + '/' + reqMonth + '/' })
  .done( function(response, textStatus) {
    var mainDiv = $("#id-maindiv");
    mainDiv.append(response);
    updateLast();
  })
}

function Prepend()
{
  if( firstYear == 2 && firstMonth == 1 )
    return;

  if( firstYear == reqYear && firstMonth == reqMonth )
    return;

  reqYear = firstYear
  reqMonth = firstMonth
  $.ajax({method: 'GET',
          url: '/cal/flood/prev_year/' + reqYear + '/' + reqMonth + '/' })
  .done( function(response, textStatus) {
    var mainDiv = $("#id-maindiv");
    var heightBefore = mainDiv.height();
    mainDiv.prepend(response);
    var heightAfter = mainDiv.height();

    if( heightBefore != heightAfter )
      $(window).scrollTop($(window).scrollTop() + heightAfter - heightBefore);

    updateFirst();
  })
}
