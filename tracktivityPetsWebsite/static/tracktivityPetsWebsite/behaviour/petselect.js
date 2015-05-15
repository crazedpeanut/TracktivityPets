$(document).ready(function(){
	  		updateCharacterSelectScreen();
		});
		
		function updateCharacterSelectScreen()
		{
			//hide all images
	$("#pet_selector .pet_image, #pet_selector .pet_silohuette").hide();
	var insert_into = $("#visible_pets");
	
	var active = $("#pet_selector").find(".active");

	var image_alt = active.find("img").attr("alt");
	$("#pet_content").children().hide();
	$("[id='"+image_alt+"_content']").show();
	
	next_silohuette = active.next('span').next('span').next('span');
	if(next_silohuette.val() === undefined){next_silohuette = $("#pet_selector .pet_silohuette:first");}
	
	prev_silohuette = active.prev('span');
	if(prev_silohuette.val() === undefined){prev_silohuette = $("#pet_selector .pet_silohuette:last");}
	

	insert_into.show();
	insert_into.empty();
	insert_into.append(prev_silohuette.html());
	insert_into.append(active.html());
	insert_into.append(next_silohuette.html());
}

var pet_number =  1;
var pets_available_count = {{ pets_available_count }}	    

$(function () {      
    
    $('#selectLeft').click(function() {
    	pet_number--;
    	if(pet_number < 1) { pet_number = pets_available_count; }
	  	$('#viewing_pet_number').html(pet_number);
		
		var active = $("#pet_selector").find(".active");
		active.toggleClass('active'); //remove the active class
		next = active.prev('span').prev('span');
		if(next.val() === undefined){next = $("#pet_selector .pet_image:last");}
		next.toggleClass('active');
		
		updateCharacterSelectScreen();

	});
	
	$('#selectRight').click(function() {
		pet_number++;
    	if(pet_number > pets_available_count) { pet_number = 1; }
		$('#viewing_pet_number').html(pet_number);
		
		var active = $("#pet_selector").find(".active");
		active.toggleClass('active'); //remove the active class
		next = active.next('span').next('span');
		if(next.val() === undefined){next = $("#pet_selector .pet_image:first");}
		next.toggleClass('active');
		
		updateCharacterSelectScreen();
	});
});

function getPet()
{
	var image_alt = $("#pet_selector").find(".active").find("img").attr("alt");
	$("#petSubmitForm").find("#pet").val(image_alt);
}