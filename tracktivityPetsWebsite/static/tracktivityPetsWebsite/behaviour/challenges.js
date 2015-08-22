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

        chal.addEventListener("click", get_challenge_details);

     }

      if(size <= 0)
      {
         $( "#avail_challenges" ).append("<a class='list-group-item'> No available challenges!</a>");
      }
        setSetUpClickListeners();
     });
}

function get_challenge_details()
{
    var challenge = this.getAttribute("id");

    $(".challenge_detail_description").html("<img class='loadimg' src='../static/tracktivityPetsWebsite/images/petpenny.gif'/>");

    $.ajax({
        url:"get_challenge_details/" + challenge,
        type:"GET",
        success: function( data )
        {
            $(".challenge_detail_description").html(data[0]['fields']['overview']);
            $(".challenge_detail_header").html(data[0]['fields']['name']);
            $(".challenge_detail_header").html(data[0]['fields']['name']);
        }
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