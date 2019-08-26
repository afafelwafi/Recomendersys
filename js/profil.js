/*function previewFile(){
   var preview = document.querySelector("#profile-image1"); //selects the query named img
   var file    = document.querySelector('input[type=file]').files[0]; //sames as here
   var reader  = new FileReader();

   reader.onloadend = function () {
	   preview.src = reader.result;
   }

   if (file) {
	   reader.readAsDataURL(file); //reads the data as a URL
   } else {
	   preview.src = "https://x1.xingassets.com/assets/frontend_minified/img/users/nobody_m.original.jpg";
   }
}*/
 //calls the function named previewFile()
$("#profile-image").click(function(e) {
    $("#profile-image-upload").click();
});

function fasterPreview( uploader ) {
    if ( uploader.files && uploader.files[0] ){
          $('#profile-image').attr('src', 
             window.URL.createObjectURL(uploader.files[0]) );
			$('#profile-image').attr('alt',window.URL.createEventObject(uploader.files[1]));
    }
}

$("#profile-image-upload").change(function(){
    fasterPreview( this );
});