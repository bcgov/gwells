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
	
	//var touchenabled = !!('ontouchstart' in window) || !!('ontouchstart' in document.documentElement) || !!window.ontouchstart || !!window.Touch || !!window.onmsgesturechange || (window.DocumentTouch && window.document instanceof window.DocumentTouch);
	var touchenabled = (('ontouchstart' in window) || (navigator.MaxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0));
	
	$('#footerToggle > a').click(function(event) {
        event.preventDefault();
        toggleFooter(event);
    });

    //open/close menu when a user clicks, tabs over the govMainMenu
    $('.menu-button').on("focus mousedown",function(e) {
       	toggleHeaderElements(e);
       	addScrollableBurgerMenu();
        e.preventDefault();
	});
 
    // Handler for when the user clicks on the search button (mobile and collapsed header views only)
    $('.search-button').on("focus mousedown", function(e) {
    	toggleHeaderElements(e);
        e.preventDefault();
	});    

    // When the search field is toggled, move focus to the input field (mobile and collapsed header views only)
	$('#header-main-row1').on("shown.bs.collapse", function() {
		$("input#global-search").focus();
	});      
    
	$('#header-main-row2').on("shown.bs.collapse", function() {
		if($("#header").hasClass("collapsed-header")) {
			addScrollableBurgerMenu();
		}	
	});    
    
    $("#govNavMenu li a").on("focus", function(e) {
        var list = $(this).closest("li").addClass("focus")
    }).on("blur", function(e) {
        var list = $(this).closest("li").removeClass("focus")
    });
    
    govNav.init({
    	menuid: 'govMainMenu'	
    })
    //navigate menu with keyboard 
    $(document).keydown(function(e) {
    	if($("#govNavMenu").is(":visible") && !$("#govNavMenu input").is(":focus")) {
    		var currentItem= $("#govNavMenu :focus").closest("li");
    	    switch(e.which) {
    	    	case 9: //tab - close menu
	    			setTimeout(function(){
	    				$('.menu-button').focus();
	 	           }, 100);
        	        break;
    	        case 37: // left - select parent list item
    	        	var prevItem=currentItem.closest("ul").closest("li");
    	        	prevItem.find("> a").focus();
					//if top level close menu
    	        	if(!prevItem.length>0){
    	        		$("#govNavMenu").each(function(){
    	        			$(this).addClass("hidden").removeAttr("style");
    	        			$(this).removeClass("expanded");
    	        		});
    	        	}else if(prevItem.hasClass("hassub")){
    					govNav.showhide(prevItem, 'show',govNav.setting);
    					if(currentItem.hasClass("hassub")){
        					govNav.showhide(currentItem, 'hide',govNav.setting);
    					}
    	        	}
    	        break;
    	
    	        case 38: // up - open previous item in the current list
    	        	var prevItem=currentItem.closest("li").prev("li");
    	        	if(prevItem.length){
    	        		prevItem.find("> a").focus();
    	    		}		
    	        	if(prevItem.hasClass("hassub")){
    					govNav.showhide(prevItem, 'show',govNav.setting);
    					if(currentItem.hasClass("hassub")){
        					govNav.showhide(currentItem, 'hide',govNav.setting);
    					}
    	        	}
    	        break;
    	
    	        case 39: // right - select first item in the next sub list
    	        	var nextItem=currentItem.closest("li").find("ul li:first");
    	        	if(nextItem.length){
    	        		nextItem.find("> a").focus();
    	        	}
    	        	if(nextItem.hasClass("hassub")){
    	        		govNav.showhide(nextItem, 'show',govNav.setting);
    					if(currentItem.hasClass("hassub")){
    	        			govNav.showhide(currentItem, 'hide',govNav.setting);
    	        		}
    	        	}
    	        break;
    	
    	        case 40: // down - open next item in the current list
    	        	
    	        	var nextItem=currentItem.closest("li").next("li");
    	        	if(currentItem.closest("#govNavMenu").length<1){
    	        		nextItem=$("#govNavMenu ul.firstLevel li:first");
    	        	}
    	        	
    	        	if(nextItem.length){
    	        		nextItem.find("> a").focus();
    	        	}
    	        	if(nextItem.hasClass("hassub")){
    	        		govNav.showhide(nextItem, 'show',govNav.setting);
    					if(currentItem.hasClass("hassub")){
    	        			govNav.showhide(currentItem, 'hide',govNav.setting);
    	        		}
    	        	}
    	        break;
    	
    	        default: return; // exit this handler for other keys
    	    }
    	    e.preventDefault(); // prevent the default action (scroll / move caret)
    	}else if($(".explore ul:visible").length>0){
    		var currentItem= $(":focus");
    	    switch(e.which) {
    	
    	        case 38: // up - open previous item in the current list
    	        	var prevItem=currentItem.closest("li").prev("li");
    	        	if(prevItem.length){
    	        		prevItem.find("> a").focus();
    	    		}		
    	        break;
    	
    	        case 40: // down - open next item in the current list
    	        	if(currentItem.hasClass("explore")){
    	    			//select first 
    	        		currentItem.find("ul li:first > a").focus();
    	    		}else{
        	        	var nextItem=currentItem.closest("li").next("li");
        	        	if(nextItem.length){
        	        		nextItem.find("> a").focus();
        	        	}
    	    		}
    	        break;
    	
    	        default: return; // exit this handler for other keys
    	    }
    	    e.preventDefault(); // prevent the default action (scroll / move caret)
    	}
	});
    
    // Expand "Explore Within" menu when it has focus (clicked or tabbed into)
	$(".explore").on("focusin", function(e) {		
	    var list = $(this).find("ul");
		if(!list.is(':visible')){
		    list.slideDown(200, 'linear', function () { });	
		}
	});
    // When the last item of an "Explore Within" menu is tabbed past, close the menu	
	$(".explore ul li:last-child a").on("focusout", function(e) {
		$(this).closest("ul").slideUp(200, 'linear', function () { });
	});
	
	// Submit the search query when the search icon is clicked
	// Applies to the global search and burger menu theme search
    $(".search-trigger").on("click", function(e) {
    	var currentForm = $(e.currentTarget).closest("form");
    	if(currentForm.find(".searchbox").val() == ''){
    		alert("Please enter one or more search terms");
    		return false;
    	} else {
    		$(currentForm).submit();
    	}
    })
 
    $(".tile-sort-button").on("click", function(e) {
    	if($(this).hasClass("sortedByOrderWeight")) {
    		sortTiles("div.homepage-theme-tiles", "alphabetical");  		  		
    		$(this).removeClass("sortedByOrderWeight").addClass("sortedByAlphabetical");
    		$(this).attr("src", "/StaticWebResources/static/gov3/images/az-sort-button-on.png");
    		$(this).attr("alt", "Sort by popularity");
    		$(this).attr("title", "Sort by popularity");      		    	    		
    	}
    	else if($(this).hasClass("sortedByAlphabetical")) {
    		sortTiles("div.homepage-theme-tiles", "orderWeight");     		
    		$(this).removeClass("sortedByAlphabetical").addClass("sortedByOrderWeight");
    		$(this).attr("src", "/StaticWebResources/static/gov3/images/az-sort-button-off.png");    
    		$(this).attr("alt", "Sort alphabetically");
    		$(this).attr("title", "Sort alphabetically");     		
    	}
		// Reset the first/last classes so the arrow styling is updated
		$(".homepage-theme-tiles .homepage-tile").removeClass("first last");
		$(".homepage-theme-tiles .homepage-tile").first().addClass("first");
		$(".homepage-theme-tiles .homepage-tile").last().addClass("last");  
    });
    
    
    // cleanup for Facebook RSS feed entries
    cleanFacebookFeedEntries();  
    
	// reset the top padding on the content	
	var headerHeight = $("#header-main").height();
	var topOffset = headerHeight + 5;
	$("#themeTemplate, #subthemeTemplate, #topicTemplate").css("padding-top", topOffset).css("background-position", "right " + topOffset + "px");	
   
	//Fix z-index youtube video embedding
	//youtube fix is moved to '/shared/scripts.misc.js'
	
	//mental health search detail page, iframe map
    var div = $('.mhDetailIframeMap');
    var width = div.width();
    
    div.css('height', width);
	
	// Clear out menu searchbox query suggestions when the user hovers away from the current theme
	$("#govMainMenu > ul > li").hover(function() {
		$("#govMainMenu > ul > li").find(".menu-searchbox").val("").addClass("placeholder");
		$("#govMainMenu > ul > li").find(".ss-gac-m").children().remove();		
		$("#govMainMenu > ul > li input").blur();		
	});	
	
	// Clear cached query suggestions when focus goes into a search field
	$("input.searchbox, input.tile-searchbox, input.menu-searchbox").focus(function() {
		console.log("clearing query suggestions");
		ss_cached = [];
		ss_qshown = null;		
	});	
	
	// [RA-368] CS - when focus goes into a burger menu search field, force a scroll to top of page (fix for iPad landscape view)
	$("input.menu-searchbox").focus(function() {
		$("body").scrollTop(0);
	});		
	
	// [CLD-1454] RL - js for accordion expand/collapse
	//Initialize Arrows
	initAccordionArrows();

    //OPEN / CLOSE All
    $(".show-btn").click(function(){
    	$('img[usemap]').rwdImageMaps();
		$(this).parent().siblings().children().children('.panel-collapse:not(".in")').collapse('show');
  		$(this).parent().siblings().children().children(".panel-heading").children(".collapseArrow").addClass("open");
  		return false;
    });

   $(".hide-btn").click(function(){
 		$(this).parent().siblings().children().children('.panel-collapse.in').collapse('hide');
 		$(this).parent().siblings().children().children(".panel-heading").children(".collapseArrow").removeClass("open");
 		return false;
    });
 

   //HANDEL Panel Heading Click functions
   $(".panel-heading").click(function(){

		//IF - This Panel is already open
	   if( $(this).children().hasClass("collapseArrow")){
	   
			if( $(this).children(".collapseArrow").hasClass("open") ){
				//Open Close handled by Bootstrap Collapse, we handle arrow here
				$(this).children(".collapseArrow").removeClass("open");
			} else{
				$('img[usemap]').rwdImageMaps();
				//Enforce accordion on other panes
				$(this).parent().siblings().children(".panel-collapse.in").collapse('hide');
				//Handle arrows for this element
				$(this).children(".collapseArrow").addClass("open");
	
				//Enforce accordion behaviour for other arrows
				$(this).parent().siblings().children(".panel-collapse").each( function(){
					if( !($(this).hasClass("in")) ){
						$(this).siblings().children(".collapseArrow").removeClass("open");
					}
				});
			}
	   }
		
   });
   // END [CLD-1454]
   // RA-389: Anchor Links not working properly

   // RA-551: Javascript console error on Theme/Subtheme pages
   // selector is changed for more specific...
   $("#themeTemplate a, #subthemeTemplate a, #topicTemplate a, area a").on("mouseup", function(){
	   if($(this).attr('href').charAt(0) == "#") {
			var href = $(this).attr('href');
			var anchorTimer;
			// fix the position if needed
			if(anchorTimer) {
				clearTimeout(anchorTimer);
			}
			// adjust the anchor position because of the header
			anchorTimer = setTimeout(function() { 			
			   // fix the position if needed
			   scroll_if_anchor(href)
			}, 300);
	   }
   });
   
   //RA-492 - Link Share Button Expand/Collapse action
   $(document).on('click', function(event) {
           //click outside the sharebubble will collapse it
           if ($(event.target).closest('#shareBubble').length <=0 && $("#shareBubble").hasClass("open")) {
        	   $("#shareBubble").toggle("slide", { direction: "right" }, 250);
               $("#shareBubble").removeClass("open");
               return false;
           }
           //click share button when share bubble is open will close it
           else if ($(event.target).closest('#shareButton').length >0 && $("#shareBubble").hasClass("open")) {
        	   $("#shareBubble").toggle("slide", { direction: "right" }, 250);
               $("#shareBubble").removeClass("open");
               return false;
           }
           //click 'cancel' button when share bubble is open will close it
           else if ($(event.target).closest('#closeShare').length >0 && $("#shareBubble").hasClass("open")) {
        	   $("#shareBubble").toggle("slide", { direction: "right" }, 250);
               $("#shareBubble").removeClass("open");
               return false;
           }
           //else open
           else if ($(event.target).closest('#shareButton').length >0 && !($("#shareBubble").hasClass("open"))){
        	   $("#shareBubble").toggle("slide", { direction: "right" }, 250);
               $("#shareBubble").addClass("open");
               return false;
           }
  
   });
   
   
});


$(document).mouseup(function(e) {
	var touchenabled = !!('ontouchstart' in window) || !!('ontouchstart' in document.documentElement) || !!window.ontouchstart || !!window.Touch || !!window.onmsgesturechange || (window.DocumentTouch && window.document instanceof window.DocumentTouch);
	var target = $(e.target);

	// Close the navigation menu when there is a click on the page somewhere other than the menu button or within the menu
	if(!target.hasClass("menu-button") && !target.parent().hasClass("menu-button") && target.closest("#govNavMenu").length == 0) {
		$("#govNavMenu").removeClass("expanded").addClass("hidden");			
		$("#header-main-row2").removeClass("in");
	}
	// Close the search box when there is a click on the page somewhere other than the search box or within the search box
	if(!target.hasClass("search-button") && !target.parent().hasClass("search-button") && target.closest(".header-search").length == 0) {
		$(".header-search").removeClass("in");
	}		
	
	// Close any navigation tile menus
    $(".explore ul").not(target.closest(".explore").find("ul")).slideUp(200, 'linear', function () { });

    
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

//		console.log("$('#footer').offset().top: " + $("#footer").offset().top);
//		console.log("$('#footer').height(): " + $("#footer").height());
//		console.log("$(window).scrollTop(): " + $(window).scrollTop());
//		console.log("$(window).height(): " + $(window).height());
//		console.log("$(window).scrollTop() + $(window).height(): " + ($(window).scrollTop() + $(window).height()));
		
		if($(window).scrollTop() > 0) {
			$(".back-to-top").show();
			$("#shareContainer").css("bottom","70px");
		} else {
			$(".back-to-top").hide();
			$("#shareContainer").css("bottom","10px");
		}
		
		// Check if the footer is within the viewport and switch the position of the button accordingly
		var windowBottomCoordinate = $(window).scrollTop() + $(window).height();	
		if(windowBottomCoordinate > $("#footer").offset().top) {
			$(".back-to-top").addClass("footer-overlap");
			$("#shareContainer").addClass("footer-overlap");
		} else {
			$(".back-to-top").removeClass("footer-overlap");
			$("#shareContainer").removeClass("footer-overlap");
		}
		
		/* 
		 * When the page is scrolled in desktop mode, collapse the header
		*/				
	/* var scrollPosition = $(window).scrollTop();
		if(scrollPosition > 50 && $(window).width() >= 768) {
			if(!$("#header").hasClass("collapsed-header")) {
				$("#header-main > .container").hide();
				$("#header").addClass("collapsed-header");
                $("#header-main > .container").fadeIn("300"); 
			}	
		} else {
			if($("#header").hasClass("collapsed-header")) {
				$("#header-main > .container").hide();
				$("#header").removeClass("collapsed-header");
				$("#header-main > .container").fadeIn("300", function()  {
					// After the full header is fully loaded, readjust the top padding on content
					adjustContentPadding();	
				})
			}		
		} */
		addScrollableBurgerMenu();

	}, 100); // Timeout in msec
});

// When page is resized
$(window).on("resize", function() {
	adjustContentPadding();
	addScrollableBurgerMenu();
});

// When page is loaded or window is resized 
$(window).on("load resize", function() {
		
	// workaround for left nav collapsing on page load
	// Bootstrap known issue - https://github.com/twbs/bootstrap/issues/14282
	$('#leftNav').collapse({'toggle': false})
	
	//hide mobile topic menu
	 if ($(this).width() < 767) {
			$("#leftNav").removeClass('in')
	 }else{
			$("#leftNav").addClass('in').attr('style','')
	 }

	$('#leftNav').collapse({'toggle': true})
  
	// When our page loads, check to see if it contains and anchor
	scroll_if_anchor(window.location.hash);

	// Intercept all anchor clicks in the accessibility section and page content
	//$("#access").on("click", "a", scroll_if_anchor);		
	//$("#main-content").on("click", "a", scroll_if_anchor);	
	
});


function toggleHeaderElements(event) {

	// Mobile only?
	if(event.type=="focus"&&$(event.currentTarget).hasClass("navbar-toggle")){		
		if(  $("#header-main-row2.collapse").hasClass('in')){	
			  $("#header-main-row2.collapse").removeClass('in');
		}else{
			  $("#header-main-row2.collapse").addClass('in').attr('style','')	
		}
	}
	
	// Non-mobile?
	else {	
		// Toggle the main menu
		$("#govNavMenu").each(function(){
			if($(this).is(":visible")){	
				$(this).addClass("hidden").removeAttr("style");
				$(this).removeClass("expanded");
	
			}else{					
				$(this).addClass("expanded");
				$(this).removeClass("hidden");
	
			};
		});		
		
	/*	// Collapsed header-specific behaviours
		if($("#header").hasClass("collapsed-header")) {
			if($(event.currentTarget).hasClass("search-button")) {
				// Close header-links section if it's open
				if($("#header-main-row2").hasClass("in")){	
					$("#header-main-row2").removeClass("in");
				}
			}
			else if($(event.currentTarget).hasClass("menu-button")) {
				// Close search if it's open
				if($(".header-search").hasClass("in")) {
					$(".header-search").removeClass("in");
				}
			}
		}		*/
	}
}


function ieVersion() {
    var ua = window.navigator.userAgent;
    if (ua.indexOf("Trident/7.0") > 0)
        return 11;
    else if (ua.indexOf("Trident/6.0") > 0)
        return 10;
    else if (ua.indexOf("Trident/5.0") > 0)
        return 9;
    else
        return 0;  // not IE9, 10 or 11
}

var animate = 1;

function toggleFooter(event) {

	var ua = window.navigator.userAgent;
    var msie = ua.indexOf("MSIE ");
    if(msie < 0){
    	//check for IE 11
    	msie = ieVersion();
    }
	
	$("#footerCollapsible").css("height", $("#footerCollapsible").height());

	if (msie > 0) {
		$("#footerCollapsible").slideToggle(0, function() {			
			// expand
			if($(this).is(":visible")) {
				$("#footer").addClass("expanded");
				$("#footerToggle a.footerExpand").hide();
				$("#footerToggle a.footerCollapse").show();
			} 
			// collapse
			else {
				$("#footer").removeClass("expanded");				
				$("#footerToggle a.footerExpand").show();
				$("#footerToggle a.footerCollapse").hide();
			}
			
			$('html, body').animate({
				scrollTop: $(document).height()
			}, 'slow');
		});
	}
	else{
		$("#footerCollapsible").slideToggle('slow', function() {			
			// expand
			if($(this).is(":visible")) {
				$("#footer").addClass("expanded");								
				$("#footerToggle a.footerExpand").hide();
				$("#footerToggle a.footerCollapse").show();
				animate = 0;								
			} 
			// collapse
			else {
				$("#footer").removeClass("expanded");				
				$("#footerToggle a.footerExpand").show();
				$("#footerToggle a.footerCollapse").hide();
				animate = 1;				
			}
		});
		
		if (animate == 1){
			$('html, body').animate({
				scrollTop: $(document).height()
			}, 'slow');		
			var temp = animate;		//get animate var
		}
	}
}

function sortTiles(selector, sortType) {
    $(selector).children("div.homepage-tile").sort(function(a, b) {
        // Sort based on the Tile title
    	if(sortType == "alphabetical") {    	
        	var stringA = $(a).find(".tile-text > .title > a").text().toUpperCase();
            var stringB = $(b).find(".tile-text > .title > a").text().toUpperCase();
            return (stringA < stringB) ? -1 : (stringA > stringB) ? 1 : 0;
        }
    	// Sort based on the Tile order weight
        else if(sortType == "orderWeight") {
        	var intA = parseInt($(a).attr("data-order"));
            var intB = parseInt($(b).attr("data-order"));
            return (intA < intB) ? -1 : (intA > intB) ? 1 : 0;
        }
    }).appendTo(selector);
}

/**
 * Check an href for an anchor. If exists, and in document, scroll to it.
 * If href argument omitted, assumes context (this) is HTML Element,
 * which will be the case when invoked by jQuery after an event
 */
function scroll_if_anchor(href) {
   href = typeof(href) == "string" ? href : $(this).attr("href");

   // If href missing, ignore
   if(!href) return;
  
   // Do not trigger on mobile view
   if($(window).width() < 768) {
	   return;
   } else {
	   var fromTop = $("#header-main").height() + 20;	   
	   
	   // Case #1 - href points to a valid anchor on the same page in the format "#foo"
	   if(href.charAt(0) == "#") {
		   
		   var $target = $(href);

		   // If no element with the specified id is found, check for name instead (some of the GOV2 content is like this)
		   if(!$target.length)  {
			   $target = $("a[name='" + href.substring(1) + "']");
		   }
	      
		   // Older browsers without pushState might flicker here, as they momentarily jump to the wrong position (IE < 10)
	       if($target.length) {
	           $('html, body').animate({ scrollTop: $target.offset().top - fromTop });
	       }
	   } 
	   // Case #2 - href points to a valid anchor on the same page in the format "/gov/current/page#foo"
	   else if(href.indexOf("#") > -1) {

		   var targetHrefPath = href.split("#")[0];
		   var targetHrefHash = href.split("#")[1];
		   		   
		   if(href.indexOf(location.pathname) > -1) {
			   var $target = $("#" + targetHrefHash);

			   if(!$target.length)  {
				   $target = $("a[name='" + targetHrefHash + "']");
			   }

		       if($target.length) {
		           $('html, body').animate({ scrollTop: $target.offset().top - fromTop });
		       }			   
		   }
	   }
   }
}  

/**
 * Clean up links and image references coming from the Facebook Graph JSON feed.
 */
function cleanFacebookFeedEntries() {
	
	try { 
		
	    // Process all feed entries and perform all cleanup required for Facebook feed items
	    $(".feedEntry").each(function() {
	    	var feedEntry = $(this);
	    	var feedEntryWidth = feedEntry.width();
	    	var videoId;
	    	var fbUrl = feedEntry.find("a:first").attr("href");
	    	
	    	// [RA-570] CS - If the feed entry isn't part of a Facebook feed, skip processing it and continue to the next entry
	    	// TODO: in the JSP, add a class that identifies the feed as being sourced from Facebook
	    	var feedLink = feedEntry.parent().find("a.arrow-link");
	    	if(feedLink !== "undefined" && feedLink.attr("href").indexOf("www.facebook.com") < 0) {
	    		return;
	    	}
	    	
    		/* If the feed's a Facebook video? Thumbnail need to be processed differently
    		 * for videos
    		 */
    		if (fbUrl.indexOf("videos") > -1) {
    			// video ID is needed to get more infor about the video from Facebook
    			var urlRegex = /\/videos\/(?:t\.\d+\/)?(\d+)/;
    			videoId = fbUrl.match(urlRegex)[1];
    			// console.log("Video ID: " + videoId);
    		}
    		
	    	// Change image references so that a larger image is retrieved
		    feedEntry.find("img").each(function() {
		    	var imgTag = $(this);
		    	if (videoId !== null && typeof videoId !== "undefined") {
		    		var cleanImgSrc;
		    		
		    		// URL used to get more infor about the video
		    		var videoInfoUrl = "https://graph.facebook.com/" + videoId;
		    		$.getJSON( videoInfoUrl, {format: "json"})
		    		.done(function( data ) {
		    			$.each( data.format, function(i, item) {
		    				// find the format that is the right size
		    				if (item.width > feedEntryWidth) {
		    					// use the image source
		    					cleanImgSrc = item.picture;
		    					return false;
		    				}
		    			});

		    			// set the image source to the new image source
			    		if (cleanImgSrc !== null && typeof cleanImgSrc !== "undefined") {
			    			imgTag.attr("src", cleanImgSrc);
			    		}
		    		}).fail(function() { console.log('JSon call to Facebook failed'); });
		    		
		    	} else {
			    	// https://fbexternal-a.akamaihd.net/safe_image.php?d=AQBJxwDdy74cYCcs&w=158&h=158&url=http%3A%2F%2Froyalbcmuseum.bc.ca%2Fassets%2Faboriginal-festival-770-360.jpg    	
			    	if($(this).attr("src").indexOf("https://fbexternal-a.akamaihd.net/safe_image.php") > -1) {
			    		// Images hosted on facebook
			    		if($(this).attr("src").indexOf("graph.facebook.com") > -1) {
				    		// if w=XXX and h=XXX parameters are specified, remove them so a large image is retrieved
				    		var cleanImgSrc = $(this).attr("src").replace(/w=[0-9]{3}&h=[0-9]{3}/gi, "");	    		
				    		$(this).attr("src", cleanImgSrc); 		    		    			
			    		}
			    		// Images hosted externally
			    		else {	    		
			    			var cleanImgSrc = $(this).attr("src").split("&url=")[1];
			    			
			    			// remove any additional parameters
			    			cleanImgSrc = cleanImgSrc.split("&")[0];    			
				    		cleanImgSrc = unescape(cleanImgSrc);
				    		$(this).attr("src", cleanImgSrc);	 
			    		}
			    	}
			    	
			    	// https://scontent.xx.fbcdn.net/hphotos-xtf1/v/t1.0-9/s130x130/11412352_1006579099360382_2608795475977532679_n.jpg?oh=9d08e3210a82714ba13a2de37d803c59&oe=56329FB4    	
			    	if($(this).attr("src").indexOf("https://scontent.xx.fbcdn.net") > -1) {
			    		//bigger_image="https://graph.facebook.com/" + picture_url_from_facebook.match(/_\d+/)[0].slice(1) + "/picture?type=normal";
			    		var imageId = $(this).attr("src").split("_")[1];
			    		cleanImgSrc = "https://graph.facebook.com/" + imageId + "/picture?type=normal";
			    		$(this).attr("src", cleanImgSrc);
			    	}
		    	}
		    });	    	
	    	
		    // Replace plain text URLs with a hyperlink
	    	feedEntry.find("p").each(function() {
		    	var inputText = $(this).text();
		        var replacedText = "";
		    	
		    	// Replace Links beginning with http://, https://, or www.
		    	var replacePattern1 = /(\b(https?:\/\/|www\.)[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
		        replacedText = inputText.replace(replacePattern1, '<a href="$1">$1</a>');      
		        
		        // Add the protocol to any links that omit it 
		        replacedText = replacedText.replace("<a href=\"www.", "<a href=\"http://www.");	  
		        
		        // Facebook hashtag links
		        var replacePattern2 = /(^|\s)#([a-z\d-]+)/gi;
		        replacedText = replacedText.replace(replacePattern2, "$1<a href='http://www.facebook.com/hashtag/$2'>#$2</a>");
		        
		    	$(this).html(replacedText);	
		    });	 	    		    	
	    	
	    	// Link up any message_tags found in the facebook post message
	    	feedEntry.find("span.messageTag").each(function() {
	    		var messageTag = $(this);
		    	//console.log(messageTag.text());
		    	var tag = messageTag.text();
		    	var tagName = tag.split("::")[0];	    	
		    	var tagId = tag.split("::")[1];
		    	
		    	//console.log("Tag Name: " + tagName);
		    	//console.log("Tag ID: " + tagId);
		    	
		    	// Replace each tag found in the message body with a link
		    	feedEntry.find("p").each(function() {
		    		var pElement = $(this);
		    		var html = pElement.html();
		    		html = html.replace(tagName, "<a href='http://www.facebook.com/" + tagId + "'>" + tagName + "</a>");
		    		$(this).html(html);	
		    		//console.log("New HTML: " + html);
		    	})  	
		    });	
	    	
			// Open all feed entry links in a new window
		    feedEntry.find("a").each(function() {
		        $(this).attr("target", "_blank");
		    });	
		    
	    });    
	}
	
	catch(err) {
		console.log("Error when attempting to clean Facebook RSS feed data");
		return;
	}
}

/**
 * If the burger menu overflows beyond the window height, make it scrollable so that all nav links can be accessed.
 */
function addScrollableBurgerMenu() {
	
	var $menu = $("#govNavMenu");	
	
	// Reset the burger menu styles to normal
	$menu.css("height", "auto");
	$menu.css("width", "");		
	$menu.css("overflow-y", "initial");
	$menu.removeClass("scrollable");	
	
	// Position of the burger menu from the top of the page (px)
	var menuTopOffset = $("#header-main > .container").height();
	
	// If the QA banner is on the page, need to add its height to menuTopOffset
	if($(".qa-banner").length) {
		menuTopOffset = menuTopOffset + $(".qa-banner").height();
	}

	// If the header is in collapsed mode, need to add height of "header-links" to menuTopOffset
	if($("#header").hasClass("collapsed-header")) {
		menuTopOffset = menuTopOffset + $("#header-links").height();
	}
	
	//var overflow = $menu.offset().top + $menu.height() - $(window).height();		
	var overflow = menuTopOffset + $menu.height() - $(window).height();			
	//console.log("overflow:" + overflow);
	
	// If overflow is positive, burger menu is too long for the current window height, and some of the links may not be visible to the user
	// To fix this, set the burger menu height so that it goes to the bottom of the window, add a vertical scrollbar, and adjust other values as necessary	
	if($(window).width() >= 750 && overflow > 0) {	
		var newMenuHeight = $menu.height() - overflow;
		$menu.height(newMenuHeight);
		$menu.css("width", "auto");				
		$menu.css("overflow-y", "scroll");
		$menu.addClass("scrollable");
	}  
}

/**
 * Search box typing event. Configure the query suggestion variables based on which search box is active
 */

var timeoutId = 0;
function searchBoxKeypress(event, numDelay, searchBoxIndex) {
	// Remove placeholder text when the user starts typing in the search field					
	var $textInputField = $(event.target);
    if($textInputField.val() == '') {
    	$textInputField.addClass('placeholder');
	} else {
		$textInputField.removeClass('placeholder');			
	}   
    
    // Burger menu search boxes
    if($textInputField.hasClass("menu-searchbox")) {
		window.ss_form_element = 'menu_suggestion_form_' + searchBoxIndex; // search form
		window.ss_popup_element = 'menu_search_suggest_' + searchBoxIndex; // search suggestion drop-down			   	
    }
    // Tile flyout search boxes
    else if($textInputField.hasClass("tile-searchbox")) {
    	window.ss_form_element = 'tile_suggestion_form_' + searchBoxIndex; // search form
    	window.ss_popup_element = 'tile_search_suggest_' + searchBoxIndex; // search suggestion drop-down	    	
    }
    // Mobile menu search boxes
    else if($textInputField.hasClass("mobile-menu-searchbox")) {
    	window.ss_form_element = 'mobile_menu_search_form_' + searchBoxIndex; // search form
    	window.ss_popup_element = 'mobile_menu_search_suggest_' + searchBoxIndex; // search suggestion drop-down	    	
    } 
    else {
    	window.ss_form_element = 'suggestion_form'; // search form
    	window.ss_popup_element = 'search_suggest'; // search suggestion drop-down	    	
    }
    
	// Clear the cache of suggested queries
//	ss_cached = [];
//	ss_clear();
//	console.log(window.ss_form_element);
//	console.log(window.ss_popup_element);   
	
	// If the keypress is an arrow (up/down/left/right), call the ss_handleKey function without using a timeout.
	// Otherwise, the user is typing the search query. Use the timeout so the search app is not flooded with requests.
    if(event.which == 37 || event.which == 38 || event.which == 39 || event.which == 40) {
    	ss_handleKey(event);
    } else {
    	clearTimeout(timeoutId); 
    	timeoutId = setTimeout(function () {
    		ss_handleKey(event);
    	}, numDelay);   	
    }
	
}

/**
 * Reset the top padding on the content (to compensate for the fixed header)
 */	
function adjustContentPadding() {
	var headerHeight = $("#header-main").height();
	var topOffset = headerHeight + 5;
	$("#themeTemplate, #subthemeTemplate, #topicTemplate").css("padding-top", topOffset).css("background-position", "right " + topOffset + "px");	
}

/**
 * [CLD-1454] RL - js for accordion expand/collapse
 * 	Initialize expand collapse. Class .in defaults to open (currently unsupported
 */
function initAccordionArrows(){

	$(".panel-collapse").each(function(){
		if( $(this).hasClass("in")){
			$(this).siblings().children(".collapseArrow").addClass("open");
		} else{
			$(this).siblings().children(".collapseArrow").removeClass("open");
		}
	});
}
