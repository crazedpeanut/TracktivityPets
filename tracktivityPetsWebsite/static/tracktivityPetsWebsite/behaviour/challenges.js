function get_available_challenges()
{
    $("#avail_challenges").html("");
    $("#avail_challenges").prepend("<img class='loadimg' src='../static/tracktivityPetsWebsite/images/petpenny.gif'/>");

    $.get("get_available_challenges/", function( data )
     {

     var size = 0;

        $("#avail_challenges").html("");

        parent = document.getElementById("avail_challenges");

     for(d in data)
     {
        size++;

        chal = document.createElement("a");
        chal.setAttribute("id", data[d]['pk']);
        chal.setAttribute("class", "list-group-item");
        chal.innerHTML = data[d]['fields']['name'];
        parent.appendChild(chal);

        chal.addEventListener("click", avail_challenges_click_handler);

     }

      if(size <= 0)
      {
         $( "#avail_challenges" ).append("<a class='list-group-item'>No available challenges!</a>");
         $( "#available" ).find("#challenge_detail_container").html("No available challenges!");
      }
      else
      {
        get_available_challenge_details(data[0]['pk']);
      }
        setSetUpClickListeners();
     });
}

function avail_challenges_click_handler()
{
    var challenge = this.getAttribute("id");

    get_available_challenge_details(challenge);
}

function active_challenge_click_handler()
{
    var challenge = this.getAttribute("id");

    get_active_challenge_details(challenge);
}

function get_available_challenge_details(challenge)
{
    $("#available .challenge_detail_description").html("<img class='loadimg' src='../static/tracktivityPetsWebsite/images/petpenny.gif'/>");

    $.ajax({
        url:"get_challenge_details/" + challenge,
        type:"GET",
        success: function( data )
        {
            $("#available").find(".challenge_detail_description").html(data['challenge']['overview']);
            $("#available").find(".challenge_detail_header").html(data['challenge']['name']);

            $("#available_challenge_rewards_table").html("");
            for(var d in data['goals'])
            {
                $("#available_challenge_rewards_table").append("<tr><td>" + data['goals'][d]['medal'] +
                "</td><td>"+ data['goals'][d]['description'] +"</td><td>"+ data['goals'][d]['pet_pennies'] +"</td></tr>");
            }
        }
    });


    $(".accept-chal-button").click(function(event)
    {

            $.ajax({
               url:"accept_challenge/" + challenge,
               type:"GET",
               success: function( data )
               {
                   get_active_challenges();
               }
           });
       });


}

function get_active_challenge_details(challenge)
{
    $("#current").find(".challenge_detail_description").html("<img class='loadimg' src='../static/tracktivityPetsWebsite/images/petpenny.gif'/>");

    $.ajax({
        url:"get_active_challenge_details/" + challenge,
        type:"GET",
        success: function( data )
        {
            $("#current").find(".challenge_detail_description").html(data['challenge']['overview']);
            $("#current").find(".challenge_detail_header").html(data['challenge']['name']);
            $("#current").find(".active_chal_end_date").html(data['challenge']['date_end']);

            $("#current_challenge_rewards_table").html("");
            for(var d in data['goals'])
            {
                $("#current_challenge_rewards_table").append("<tr><td>" + data['goals'][d]['medal'] +
                "</td><td>"+ data['goals'][d]['description'] +"</td><td>"+ data['goals'][d]['pet_pennies'] +"</td></tr>");
            }
        }
    });
}

function complete_challenge_click_handler(challenge)
{
    var challenge = this.getAttribute("id");

    get_active_challenge_details(challenge);
}

function get_completed_challenge_details(challenge)
{
    $("#completed").find(".challenge_detail_description").html("<img class='loadimg' src='../static/tracktivityPetsWebsite/images/petpenny.gif'/>");

    $.ajax({
        url:"get_complete_challenge_details/" + challenge,
        type:"GET",
        success: function( data )
        {
            $("#completed").find(".challenge_detail_description").html(data['challenge']['overview']);
            $("#completed").find(".challenge_detail_header").html(data['challenge']['name']);


            for(var d in data['goals'])
            {
             /**   $("#current_challenge_rewards_table").append("<tr><td>" + data['goals'][d]['medal'] +
                "</td><td>"+ data['goals'][d]['description'] +"</td><td>"+ data['goals'][d]['pet_pennies'] +"</td></tr>");**/
            }
        }
    });
}

function get_active_challenges()
{
    $("#current_challenges").html("");
    $("#current_challenges").prepend("<img class='loadimg' src='../static/tracktivityPetsWebsite/images/petpenny.gif'/>");

    $.get("get_active_challenges/", function( data )
     {

     var size = 0;

        $("#current_challenges").html("");

        parent = document.getElementById("current_challenges");

     for(d in data)
     {
        size++;

        chal = document.createElement("a");
        chal.setAttribute("id", data[d]['pk']);
        chal.setAttribute("class", "list-group-item");
        chal.innerHTML = data[d]['name'];
        parent.appendChild(chal);

        chal.addEventListener("click", active_challenge_click_handler);

     }

      if(size <= 0)
      {
         $( "#current_challenges" ).append("<a class='list-group-item'> No active challenges!</a>");
         $( "#current" ).find("#challenge_detail_container").html("No current challenges!");
      }
      else
      {
        get_active_challenge_details(data[0]['pk']);
      }
        setSetUpClickListeners();
     });
}

function get_completed_challenges()
{
    $("#completed_challenges").html("");
    $("#completed_challenges").prepend("<img class='loadimg' src='../static/tracktivityPetsWebsite/images/petpenny.gif'/>");

    $.get("get_complete_challenges/", function( data )
     {

     var size = 0;

        $("#completed_challenges").html("");

        parent = document.getElementById("completed_challenges");

     for(d in data)
     {
        size++;

        chal = document.createElement("a");
        chal.setAttribute("id", data[d]['pk']);
        chal.setAttribute("class", "list-group-item");
        chal.innerHTML = data[d]['name'];
        parent.appendChild(chal);

        chal.addEventListener("click", complete_challenge_click_handler);

     }

      if(size <= 0)
      {
         $( "#completed_challenges" ).append("<a class='list-group-item'> No completed challenges!</a>");
         $( "#completed" ).find("#challenge_detail_container").html("No completed challenges!");
      }
        setSetUpClickListeners();
     });
}


function setSetUpClickListeners()
{
    var modalScreenWidth = 768;

    $("#avail_challenges > a").click(function(event)
    {
        if (screen.width <= modalScreenWidth)
        {
            $("#challenges_detail_modal").find("#challenge_accept_btn").show();
            $("#challenges_detail_modal").find("#available_challenge_rewards").show();
            $("#challenges_detail_modal").find("#completed_challenge_reward").hide();
            $('#challenges_detail_modal').modal('show');
        }
    });

    $("#current_challenges > a").click(function(event)
    {
        if (screen.width <= modalScreenWidth)
        {
            $("#challenges_detail_modal").find(".modal-title").html("This is a current challenge");
            $("#challenges_detail_modal").find("#challenge_accept_btn").hide();
            $("#challenges_detail_modal").find("#available_challenge_rewards").show();
            $("#challenges_detail_modal").find("#completed_challenge_reward").hide();
            $('#challenges_detail_modal').modal('show');
        }
    });

    $("#completed_challenges > a").click(function(event)
    {
        if (screen.width <= modalScreenWidth)
        {
            $("#challenges_detail_modal").find("#challenge_accept_btn").hide();
            $("#challenges_detail_modal").find(".modal-title").html("This is a completed challenge");
            $("#challenges_detail_modal").find("#completed_challenge_reward").show();
            $("#challenges_detail_modal").find("#available_challenge_rewards").hide();
            $('#challenges_detail_modal').modal('show');
        }
    });
}