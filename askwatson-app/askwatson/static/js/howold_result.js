// Ask Watson, Howold show result
// handles json
function howold_result (dataJson) {

    var j = dataJson;

    var out = $("#howold_result");
    out.empty();

    // error handle
    if (!("status" in j)){
        out.append('Data error please try again.');
    } else {
        if (j.status != "OK"){
            out.append('API error please try again.<br>');
            out.append(j.statusInfo)
        } else {
            // input is ok
            if (j.imageFaces.length < 1){
                out.append('Sorry No Faces Detected :( Please try another photo.')
            } else {
                // for each faces
                $.each(j.imageFaces, function(i, face) {
                    out.append('Face ' + (i + 1) + '：<br>');
                    // gender
                    var x = parseFloat(face.gender.score) * 100;
                    out.append("You are " + face.gender.gender + " (" + x.toFixed(0) + "%)<br>");
                    // age
                    x = parseFloat(face.age.score) * 100;
                    out.append("Your age is " + face.age.ageRange + " (" + x.toFixed(0) + "%)<br>" );
                    // if identity
                    if ("identity" in face){
                        out.append("Wait a minute are you famous person?<br>");
                        out.append("You are " + face.identity.name + ".<br>");
                        out.append("Watson knows you. You are " + face.identity.disambiguated.subType.toString() + ".<br>");
                    }
                });
            }
        }
    }
}
function loader () {
    $('#loading-indicator').show();
    $('#submit').hide();
}
