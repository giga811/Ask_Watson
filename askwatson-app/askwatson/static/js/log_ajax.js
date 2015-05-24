// Geo var
var latitude = 0;
var longitude = 0;
var sensordata = {};
var date = "";
var N = 0;

// accel event listener
var x = 0;
var y = 0;
var z = 0;
window.addEventListener("devicemotion", function(event1){
    x = event1.acceleration.x;
    y = event1.acceleration.y;
    z = event1.acceleration.z;
}, true);

function show_accel(){
    var result1 = document.getElementById("show_accel");
    result1.innerHTML =
        "accelX："+ Math.round(x * 10) / 10 +"<br>" +
        "accelY："+ Math.round(y * 10) / 10 +"<br>" +
        "accelZ："+ Math.round(z * 10) / 10;
}

function ajax_search() {
    var d = new Date();
    var month = d.getMonth()+1, day = d.getDate();
    var hours = d.getHours(), minutes = d.getMinutes(), seconds = d.getSeconds();
    date = d.getFullYear() + '/' +
        (month<10 ? '0' : '') + month + '/' +
        (day<10 ? '0' : '') + day + (hours < 10 ? " 0" : " ") + hours + (minutes < 10 ? ":0" : ":") + minutes + (seconds < 10 ? ":0" : ":") + seconds;
    ajax_sensor();
    ajax_api();
}

var timer1;

//setInterval()を使ったタイマーの起動関数
function tmstr()
{
    $('#start-button').hide();
    $('#stop-button').show();
    timer1 = setInterval("tmrOn()",5000);
}

function tmrOn()
{
    var d = new Date();
    var month = d.getMonth()+1, day = d.getDate();
    var hours = d.getHours(), minutes = d.getMinutes(), seconds = d.getSeconds();
    date = d.getFullYear() + '/' +
        (month<10 ? '0' : '') + month + '/' +
        (day<10 ? '0' : '') + day + (hours < 10 ? " 0" : " ") + hours + (minutes < 10 ? ":0" : ":") + minutes + (seconds < 10 ? ":0" : ":") + seconds;
    N++;
    ajax_sensor();
    ajax_api();
}

function tmrOff()
{
    //タイマーを停止する
    $('#stop-button').hide();
    $('#start-button').show();
    clearInterval(timer1);
}

// get sensor data
function ajax_sensor() {
    $.ajax({
        url: "/api/get_sensor",
        dataType: 'json',
        async: false,
        data: { "data" : "data" },
        success: function(json) {
            sensordata = json;
        }
    });
}

function ajax_api() {

    // Geo location
    //ユーザーの現在の位置情報を取得
    navigator.geolocation.getCurrentPosition(successCallback, errorCallback);

    // get id
    var id = $('input#id').val();
    console.log(id, latitude, longitude);

    // Query Values
    var query = new Object();
    query.id = id
    query.latitude = latitude;
    query.longitude = longitude;
    query.date = date;
    query.accelX = x;
    query.accelY = y;
    query.accelZ = z;


    console.log(JSON.stringify(query));
    console.log(sensordata);

    // 送信
    $.ajax({
        url: "/api/logging",
        type: "get",
        data: {q: JSON.stringify(query), sensordata: JSON.stringify(sensordata)},
        timeout: 10000,  // 単位はミリ秒

        // 送信前
        beforeSend: function(xhr, settings) {
            $('#loading-indicator').show();
        },
        // 応答後
        complete: function(xhr, textStatus) {

            $('#loading-indicator').hide();
        },

        // 通信成功時の処理
        success: function(result, textStatus, xhr) {

            // show_result container reset
            var out = $("#show_result")
            out.empty();
            out.append('N = ' + N + '<br>');
            out.append('<p>Date: ' + date + '</p>');
            out.append('<p>あなたの現在位置</p>');
            out.append('<p>latitude: ' + latitude + '</p>');
            out.append('<p>longitude' + longitude + '</p>');

            var sdata = sensordata;
            var items = [];
            $.each(sdata, function(key, val) {
              items.push('<p id="' + key + '">' + key + ': ' + val + '</p>');
            });
            //サーバから受け取った値をULリストにしてBody内に挿入
            $('<h4/>', {
              'class': 'my-new-list',
              html: items.join('')
            }).appendTo(out);

            console.log(result);

            var datas = result.data

        },

        // 通信失敗時の処理
        error: function(xhr, textStatus, error) {}
    });

}

// init run
// ajax_search();

/***** ユーザーの現在の位置情報を取得 *****/
function successCallback(position) {
  latitude = position.coords.latitude;
  longitude = position.coords.longitude;
}

/***** 位置情報が取得できない場合 *****/
function errorCallback(error) {
  var err_msg = "";
  switch(error.code)
  {
    case 1:
      err_msg = "位置情報の利用が許可されていません";
      break;
    case 2:
      err_msg = "デバイスの位置が判定できません";
      break;
    case 3:
      err_msg = "タイムアウトしました";
      break;
  }
  document.getElementById("show_result").innerHTML = err_msg;
  //デバッグ用→　document.getElementById("show_result").innerHTML = error.message;
}
