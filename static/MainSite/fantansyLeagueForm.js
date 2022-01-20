// $("#batsman1").on("change",function(){

//     $("#submitButton").attr('disabled','disabled');

// });

function checkValidSubmition() {

    var x = false;
    // $("#submitButton").attr('disabled','disabled');
    if ($("#batsman1").val() == $("#batsman2").val() ||
    $("#batsman1").val() == $("#batsman3").val() ||
    $("#batsman1").val() == $("#batsman4").val() ||
    $("#batsman2").val() == $("#batsman3").val() ||
    $("#batsman2").val() == $("#batsman4").val() ||
    $("#batsman3").val() == $("#batsman4").val() ){
        x = true
        $('#batsmenErrorDiv').show();
    }
    else{
        
        $('#batsmenErrorDiv').hide();
    }

    if
    ($("#bowler1").val() == $("#bowler2").val() ||
    $("#bowler1").val() == $("#bowler3").val() ||
    $("#bowler1").val() == $("#bowler4").val() ||
    $("#bowler2").val() == $("#bowler3").val() ||
    $("#bowler2").val() == $("#bowler4").val() ||
    $("#bowler3").val() == $("#bowler4").val() ){
        x = true
        $('#bowlersErrorDiv').show();
    }
    else{
        
        $('#bowlersErrorDiv').hide();
    }

    if($("#allRounder1").val() == $("#allRounder2").val() ||
    $("#allRounder1").val() == $("#allRounder3").val() ||
    $("#allRounder2").val() == $("#allRounder3").val() ){
        x = true
        $('#allRoundersErrorDiv').show();
    }
    else{
        
        $('#allRoundersErrorDiv').hide();
    }

    if(
    $("#captain").val() != $("#batsman1").val() &&
    $("#captain").val() != $("#batsman2").val() &&
    $("#captain").val() != $("#batsman3").val() &&
    $("#captain").val() != $("#batsman4").val() &&
    $("#captain").val() != $("#bowler1").val() &&
    $("#captain").val() != $("#bowler2").val() &&
    $("#captain").val() != $("#bowler3").val() &&
    $("#captain").val() != $("#bowler4").val() &&
    $("#captain").val() != $("#allRounder1").val() &&
    $("#captain").val() != $("#allRounder2").val() &&
    $("#captain").val() != $("#allRounder3").val() 
    ) {
        x = true
        $('#captainErrorDiv').show();
    }
    else{
        
        $('#captainErrorDiv').hide();
    }

    if(
    $("#vice_captain").val() != $("#batsman1").val() &&
    $("#vice_captain").val() != $("#batsman2").val() &&
    $("#vice_captain").val() != $("#batsman3").val() &&
    $("#vice_captain").val() != $("#batsman4").val() &&
    $("#vice_captain").val() != $("#bowler1").val() &&
    $("#vice_captain").val() != $("#bowler2").val() &&
    $("#vice_captain").val() != $("#bowler3").val() &&
    $("#vice_captain").val() != $("#bowler4").val() &&
    $("#vice_captain").val() != $("#allRounder1").val() &&
    $("#vice_captain").val() != $("#allRounder2").val() &&
    $("#vice_captain").val() != $("#allRounder3").val() 
    ) {
        x = true
        $('#vice_captainErrorDiv').show();
    }
    else{
        
        $('#vice_captainErrorDiv').hide();
    }

    if($("#vice_captain").val() == $("#captain").val()){
        x = true
        $('#cvcErrorDiv').show();
    }
    else{
        
        $('#cvcErrorDiv').hide();
    }

    if(x){
        deactivateButton();
    }
    else{
        activateButton();
    }

}

$( document ).ready(function() {
    $('#captainErrorDiv').hide();
    $('#vice_captainErrorDiv').hide();
});

function activateButton(){
    $("#submitButton").removeAttr('disabled');$("#submitButton").css('background-color','#115385');    
}

function deactivateButton(){
    $("#submitButton").attr('disabled', 'disabled');$("#submitButton").css('background-color','grey');
}