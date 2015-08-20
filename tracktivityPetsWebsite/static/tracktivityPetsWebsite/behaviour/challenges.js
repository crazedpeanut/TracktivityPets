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
        chal.setAttribute("id", data[d]['fields']['name']);
        chal.setAttribute("class", "list-group-item");
        chal.innerHTML = data[d]['fields']['name'];
        parent.appendChild(chal);

        chal.addEventListener("click", get_challenge_details);

     }

      if(size <= 0)
      {
         $( "#avail_challenges" ).append("<div class='list-group-item'> No available challenges!</div>");
      }
     });
}

function get_challenge_details()
{
    var challenge = this.innerHTML;
    alert(challenge);
    $.ajax({
        url:"get_challenge_details/",
        data:{
            "challenge_name":challenge
        },
        type:"GET",
        success: function( data )
        {
            $("#challenge_detail_description").html(data[0]['fields']['description']);
        }
    });
}