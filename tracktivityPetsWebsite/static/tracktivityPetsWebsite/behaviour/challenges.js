function get_available_challenges()
{
    $.get("get_available_challenges/", function( data )
     {

     var size = 0;

    parent = document.getElementById("avail_challenges");

     for(d in data)
     {
        size++;

        chal = document.createElement("div");
        chal.setAttribute("id", data[d]['pk']);
        chal.setAttribute("class", "list-group-item");
        chal.innerHTML = data[d]['fields']['name'];
        parent.appendChild(chal);

        chal.addEventListener("click", get_challenge_details);

     }

      if(size <= 0)
      {
         $( "#avail_challenges" ).append("<div class='list-group-item'> No available challenges!</div>");
      }
        setSetUpClickListeners();
     });
}

function get_challenge_details()
{
    var challenge = this.getAttribute("id");
    $.ajax({
        url:"get_challenge_details/" + challenge,
        type:"GET",
        success: function( data )
        {
            $(".challenge_detail_description").html(data[0]['fields']['overview']);
            $(".challenge_detail_header").html(data[0]['fields']['name']);
        }
    });
}

function setSetUpClickListeners()
{
    var modalScreenWidth = 768;

    $("#avail_challenges > div").click(function(event)
    {
        if (screen.width <= modalScreenWidth)
        {
            $("#challenges_detail_modal").find("#challenge_accept_btn").show();
            $("#challenges_detail_modal").find("#available_challenge_rewards").show();
            $("#challenges_detail_modal").find("#completed_challenge_reward").hide();
            $('#challenges_detail_modal').modal('show');
        }
    });

    $("#current_challenges > div").click(function(event)
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

    $("#completed_challenges > div").click(function(event)
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