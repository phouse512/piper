function loadPage(){
	$("#submitAttendance").on("click", function(){
		submitClick();
	});

	$(".list-group").updateList({onFinish: displayHelpText}).updateList('template', 
			'<li class="suggested list-group-item"><span class="firstname">{firstname}</span> <span class="lastname">{lastname}</span>' + 
			'<input class="dorm" type="hidden" name="dorm" value="{dorm}"><span class="pull-right year">{year}' + 
			'</span><input type="hidden" name="email" value="{email}"></li>')
			.updateList('listener', autoSuggestClickListener);

	updateSuggestionsListener();
}

function displayConfirmation(){
	$("#input-form").fadeOut("slow", function(){
		$("#confirmation").fadeIn("slow");
	});
	setTimeout(function() {
		$("#confirmation").fadeOut("slow", function() {
			$("#input-form").fadeIn();
		});
	}, 2000);
}

// Large group tracking - Reset display
function resetScreen(){
	$("input").val("");
	$("select").val("");
	// still need to add the clearing of suggestions
	$("#suggestionsList ul > li").remove();
	$("#help").fadeOut('slow', function() { $("#help").remove(); });
}

// Large group tracking - Submit button click
function submitClick(){
    var group_hash = $.trim($("#group_hash").html().toLowerCase());
    var event_id = $.trim($("#event_id").html().toLowerCase());
	$.getJSON($SCRIPT_ROOT + '/arkaios/' + group_hash + '/track/' + event_id + '/save/', {
		firstName: $('#firstName').val().toLowerCase(),
        lastName: $('#lastName').val().toLowerCase(),
        email: $('#email').val().toLowerCase(),
        year: $('select').val(),
        listserv: $('#checkBox').prop('checked')
	}, function(data) {
		parseTrackingStatus(data);
	});
}

// Large group tracking - Parse jsonified data
function parseTrackingStatus(data){
	if(data.status=="error"){
		console.log("error");

		//add error handling
	} else if(data.status=="success") {
		resetScreen();
		displayConfirmation();
	}	
}

function searchUsers(){
    var group_hash = $.trim($("#group_hash").html().toLowerCase());
	$.getJSON($SCRIPT_ROOT + '/arkaios/' + group_hash + '/_search/', {
		first_name: $.trim($('#firstName').val().toLowerCase()),
		last_name: $.trim($('#lastName').val().toLowerCase()),
		email: $.trim($("#email").val().toLowerCase()),
		//dorm: $.trim($("#dorm").val()),
		year: $('select').val()
	}, function(data) {
		updateSuggestions(data);
	});
}

function updateSuggestions(data){
	for(var i=0; i<data.results.length; i++){
		data.results[i] = data.results[i];
	}
	$(".list-group").updateList('update', data.results);
}

// listens to any input fields changing
function updateSuggestionsListener(){
	$("input").change(function() {
		searchUsers();
	});
	$("select").change(function() {
		searchUsers();
	});
}

// listens to a user clicking on a suggested user
function autoSuggestClickListener(object){
	$(object).on('click', function(){
		//$("#dorm").val($(this).children('input[name="dorm"]').val());
		$("#email").val($(this).children('input[name="email"]').val());
		$("#firstName").val(firstName = $(this).children('.firstname').html());
		$("#lastName").val($(this).children('.lastname').html());
		$("select").val($(this).children('.year').html());
	});
}

// called when the updateList plugin finishes running!
function displayHelpText(){
	setTimeout(function() {
		if($("li").length > 0 && $('#help').length == 0){
			help = $.parseHTML(helpText);
			$(help).css('display', 'none');
			$("#helpContainer").html($(help));
			$(help).fadeIn('slow');
		} else if($("li").length < 1) {
			$("#help").fadeOut('slow', function() { $("#help").remove(); });
		}
	}, 1000);
}