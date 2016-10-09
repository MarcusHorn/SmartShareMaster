// Your code goes here
function GPSpush(){
gm.info.getCurrentPosition (processPosition, true)

function processPosition(position){
	var lat = position.coords.latitude;
 	var lng = position.coords.longitude;
 	var rental_id = 1
 	var newtext = {'latitude':lat, 'longitude':lng, 'rental_id':1}
 	 	$.ajax({
		type: "POST",
		url: "http://45.56.110.227:8080/updatelocation/",
		dataType: 'text',
		data: newtext,
			success: function(msg) 
			    {
			    alert(msg);
			    },
			error: function(jqXHR, textStatus) 
			    {
			    alert(textStatus);
			    }
});
}
}
