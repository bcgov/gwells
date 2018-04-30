/********************************
* Collapse Menu 
********************************/


$(document).ready(function(event) {
	$(".back-to-top").on("focus mousedown", function(e) {
		e.preventDefault();
	    $('html,body').animate({ scrollTop: 0 }, 'slow', function(){
	    	$("#shareContainer").css("bottom","10px");
	    });
	});
});


var scrollTimer;
$(window).on("scroll", function() {
	
	// Clear timeout if one is pending
	if(scrollTimer) {
		clearTimeout(scrollTimer);
	}
	// Set timeout
	scrollTimer = setTimeout(function() { 			
		/* 
		 * Re-position the "Back to top" button if it is touching the footer
		*/				
		
		if($(window).scrollTop() > 0) {
			$(".back-to-top").show();
			$("#shareContainer").css("bottom","70px");
		} else {
			$(".back-to-top").hide();
			$("#shareContainer").css("bottom","10px");
		}
		
		// Check if the footer is within the viewport and switch the position of the button accordingly
		var windowBottomCoordinate = $(window).scrollTop() + $(window).height();	
		if(windowBottomCoordinate > $("footer").offset().top) {
			$(".back-to-top").addClass("footer-overlap");
			$("#shareContainer").addClass("footer-overlap");
		} else {
			$(".back-to-top").removeClass("footer-overlap");
			$("#shareContainer").removeClass("footer-overlap");
		}

	}, 100); // Timeout in msec
});