// function showSlotDiv(id) {
//     $('#'+"slotTTS_67AM").hide();
//     $('#'+"slotTTS_78AM").hide();
//     $('#'+"slotTTS_89AM").hide();
//     $('#'+"slotTTS_56PM").hide();
//     $('#'+"slotTTS_67PM").hide();
//     $('#'+"slotTTS_78PM").hide();
//     $('#'+"slotWFS_67AM").hide();
//     $('#'+"slotWFS_78AM").hide();
//     $('#'+"slotWFS_89AM").hide();
//     $('#'+"slotWFS_56PM").hide();
//     $('#'+"slotWFS_67PM").hide();
//     $('#'+"slotWFS_78PM").hide();

//     $('#'+id).show();
// }

$("#userType").change(function() {


    if ($(this).val() == "studenttype") {

   
        $('#entnoDiv').show();
        // $('#entnoDiv').attr('required','');
        // $('#entnoDiv').attr('data-error', 'This field is required.');
		$('#hostelDiv').show();
        // $('#hostelDiv').attr('required','');
        // $('#hostelDiv').attr('data-error', 'This field is required.');
        $('#relativeDiv').hide();
        // $('#relativeDiv').removeAttr('required');
        // $('#relativeDiv').removeAttr('data-error');
    } else if($(this).val() == "nonstudenttype"){
        
        $('#entnoDiv').hide();
        // $('#entnoDiv').removeAttr('required');
        // $('#entnoDiv').removeAttr('data-error');
		$('#hostelDiv').hide();
        // $('#hostelDiv').removeAttr('required');
        // $('#hostelDiv').removeAttr('data-error');
        $('#relativeDiv').hide();
        // $('#relativeDiv').removeAttr('required');
        // $('#relativeDiv').removeAttr('data-error');	
    } else
    {
        $('#entnoDiv').hide();
        // $('#entnoDiv').removeAttr('required');
        // $('#entnoDiv').removeAttr('data-error');
		$('#hostelDiv').hide();
        // $('#hostelDiv').removeAttr('required');
        // $('#hostelDiv').removeAttr('data-error');
        $('#relativeDiv').show();
        // $('#relativeDiv').attr('required','');
        // $('#relativeDiv').attr('data-error', 'This field is required.');
    }
});


// $("#Gender").trigger("change");

// $("#femaleSlot").change(function() {

//     var changed_value = $(this).val();
//     $('#'+"slots-left-div").hide();
// 	showSlotDiv(changed_value);

// });

$("#maleSlot").change(function() {


    var myClasses = document.querySelectorAll('.slots-div'),
    i = 0,
    l = myClasses.length;

    for (i; i < l; i++) {
        myClasses[i].style.display = 'none';
    }

    var myClasses = document.querySelectorAll('.slots-div1'),
    i = 0,
    l = myClasses.length;

    for (i; i < l; i++) {
        myClasses[i].style.display = 'none';
    }


    var changed_value = $(this).val();
    
    var v = "a" + changed_value.substring(0, 2) + changed_value.substring(3, 5) + changed_value.substring(6, 15) 
    
    console.log(v);

    // document.getElementById(v).style.display = "none";

    $('#'+v).show();

});



// $("#Gender").change(function() {
//     if ($(this).val() == "Male") {
//         $('#maleSlotDiv').show();
//         $('#maleSlot').attr('required','');
//         $('#maleSlot').attr('data-error', 'This field is required.');
//     } else {
//         $('#maleSlotDiv').hide();
//         $('#maleSlot').removeAttr('required');
//         $('#maleSlot').removeAttr('data-error');				
//     }
// });
// $("#Gender").trigger("change");


// $("#Gender").change(function() {
//     if ($(this).val() == "Female") {
//         $('#femaleSlotDiv').show();
//         $('#femaleSlot').attr('required','');
//         $('#femaleSlot').attr('data-error', 'This field is required.');
//     } else {
//         $('#femaleSlotDiv').hide();
//         $('#femaleSlot').removeAttr('required');
//         $('#femaleSlot').removeAttr('data-error');				
//     }
// });
// $("#Gender").trigger("change");	





function ValidateSize2(file){
    var filePath = file.value;
        var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.pdf)$/i; 
        
        
        if (!allowedExtensions.exec(filePath)){
            alert('Please upload an image of type .jpg , .jpeg , .png or a .pdf file');
			$(file).val('');
        }


    var FileSize = file.files[0].size / 1024; // in kB
    if (FileSize > 40) {
        alert('File size exceeds 40 KB');
        $(file).val('');
       // $(file).val(''); //for clearing with Jquery
    } else {

    }
}


function ValidateSize(file) {
        var filePath = file.value;
        var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i; 
        
        
        if (!allowedExtensions.exec(filePath)){
            alert('Please upload an image of type .jpg , .jpeg or .png');
			$(file).val('');
        }
        
        var FileSize = file.files[0].size / 1024; // in kB
        if (FileSize > 40) {
            alert('File size exceeds 40 KB');
			$(file).val('');
           // $(file).val(''); //for clearing with Jquery
        } else {

        }
    }

