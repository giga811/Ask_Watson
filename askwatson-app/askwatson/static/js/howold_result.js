// Ask Watson, Howold show result
// handles json
//

var tooltips = [];
{

}
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
                tooltips = [];
                $.each(j.imageFaces, function(i, face) {
                    out.append('Face ' + (i + 1) + '：<br>');
                    // gender
                    var x = parseFloat(face.gender.score) * 100;
                    out.append("You are " + face.gender.gender + " (" + x.toFixed(0) + "%)<br>");
                    // age
                    // age calculation
                    x = parseFloat(face.age.score) * 100;
                    var ages = face.age.ageRange.split("-");
                    var age;
                    if (ages.length == 2){
                        var age0 = parseInt(ages[0]);
                        var age1 = parseInt(ages[1]);
                        age = (age1 - (age1 - age0) * x / 100).toFixed(0);
                    } else {
                        age = ages[0];
                    }
                    out.append("Your age is " + age + " (" + x.toFixed(0) + "%)<br>" );
                    // get x, y pos
                    var img  = document.getElementById('result_image');
                    var imW = img.naturalWidth;
                    var imH = img.naturalHeight;
                    var tooltip = {
                        "relX": parseFloat(face.positionX) / imW,
                        "relY": parseFloat(face.positionY) / imH,
                        "relfW": parseFloat(face.width) / imW,
                        "relfH": parseFloat(face.height) / imH,
                        "age": age,
                        "gender": face.gender.gender
                    };
                    tooltips.push(tooltip);
                    // if identity
                    if ("identity" in face){
                        out.append("Wait a minute are you famous person?<br>");
                        out.append("You are " + face.identity.name + ".<br>");
                        out.append("Watson knows you. You are " + face.identity.disambiguated.subType.toString() + ".<br>");
                    }
                });
                draw_tooltips();
            }
        }
    }
}
function loader () {
    $('#loading-indicator').show();
    $('#submit').hide();
}

function draw_tooltips() {
    // get image, respW respH
    // responsive adjustive sizes
    var img  = document.getElementById('result_image');
    var respW = img.clientWidth;
    var respH = img.clientHeight;

    // get div
    var out = $("#tooltips");
    out.empty();

    // for each tooltips
    $.each(tooltips, function(i, t) {
        // vars
        var respX = respW * t.relX;
        var respY = respH * t.relY;
        var respfW = respW * t.relfW;
        var respfH = respH * t.relfH;

        // append rectangle
        out.append('<div data-html="true" class="child face-tooltip small-face-tooltip " style="left: '
         + respX + 'px; top: ' + respY + 'px; width: ' + respfW
         + 'px; height: ' + respfH
         + 'px; border: 1px solid white; position: absolute;" data-original-title="" title="" aria-describedby="tooltip"></div>\n');
        // console.log(respX, respY, respfW, respfH);

        // append tooltip
        var genderimg = 'watson.png'
        if (t.gender == "MALE"){
            genderimg = "watson-male.png";
        }
        if (t.gender == "FEMALE"){
            genderimg = "watson-female.png";
        }
        out.append('<div class="tooltip fade top in" role="tooltip" style="top: ' + (respY - 63) +
            'px; left: ' + (respX + respfW/2 - 42) + 'px; display: block;">\n<div class="tooltip-arrow" style="left: 50%;"></div>\n<div class="tooltip-inner">\n<nobr><img style="display:inline; vertical-align: middle;" height="30" src="/img/' + genderimg + '" class="small-face-tooltip">'
             + t.age + '</nobr>\n</div></div>');
    });
}

var timer = false;
$(window).resize(function() {
    if (timer !== false) {
        clearTimeout(timer);
    }
    timer = setTimeout(function() {
        console.log('resized');
        // 何らかの処理
        draw_tooltips();
    }, 200);
});
