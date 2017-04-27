$( document ).ready(function() {
	$('#search_form').on('submit', function(event){
	    event.preventDefault();
	    search();
	});
	
	function search() {
		$.ajax({
	        url : "search", // the endpoint
	        type : "POST", // http method
	        data : { video_date_year : $('#video_date_year').val(), 
	        	video_date_month : $('#video_date_month').val(),
	        	video_date_day : $('#video_date_day').val(),
	        	location : $('#location').val()}, 

	        // handle a successful response
	        success : function(data) {
	        	$('#videos').empty();
	        	for (var i = 0; i < data.videos.length; i++) {
	        		var video = data.videos[i];
		        	$('#videos').append("<div class=\"col-md-2 text-center\">" +
		        			"<div class=\"row\"><a href=\"view_video\\" + video.id + "\">" +
		        			"<img class= \"img-thumbnail\" width=\"100\" height=\"100\" alt=\"PoliceVideo\" src=\"gif\\" + video.id + "\">" +
		        			"</a></div><div class=\"row\">" +
		        			"<a href=\"view_video\\" + video.id + "\">Date:" + video.video_date + " Location:" + video.location + "</a>" +
		        			"</div></div>");
	        	}
	        }
	    });
	};
	
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	  }

	  var csrftoken = getCookie('csrftoken');

	  function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	  }

	  $.ajaxSetup({
	      beforeSend: function(xhr, settings) {
	          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	              xhr.setRequestHeader("X-CSRFToken", csrftoken);
	          }
	      }
	  });
});