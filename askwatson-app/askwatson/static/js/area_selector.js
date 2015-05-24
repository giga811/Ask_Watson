JH = {};

JH.d = document;
JH.obj = {};
JH.defaultText = {};
JH.comment = {
    defaultText : ''
};

JH.ua = navigator.userAgent.toLowerCase();
JH.browser = {
    isIE : function() {
	return /msie/.test(JH.ua);
    },
    isIE6 : function() {
	return ( typeof document.documentElement.style.maxHeight == "undefined");
    }
};

JH.init = function(obj) {
    JH.obj = obj;
    if(JH.browser.isIE6()) {
	JH.setIframeToPanel(JH.getId(obj.panel));
    }
    JH.hidePanel(JH.getId(obj.panel));
    JH.bindCloseBtn(JH.getId(obj.close));
    JH.bindTrigger(JH.getId(obj.dispArea), JH.getId(obj.panel));
    JH.bindAreaEvent(JH.getId(obj.panel), obj.rel);
};

JH.setIframeToPanel = function(a) {
    var elems=JH.getTag(document.body,'select');
    for (var i=0;i<elems.length;i++){
	elems[i].style.zIndex = '1';
    }
    if (!JH.getId('ifrm')) {
	var element = document.createElement('iframe');
	element.setAttribute();
	element.setAttribute('scrolling', 'no');
	element.setAttribute('frameborder', '0');
	element.setAttribute('id', 'ifrm');
	element.style.zIndex = '998';
	element.style.position = 'absolute';
	element.style.display = 'none';
	element.style.left = '0px';
	element.style.top  = '0px';
	element.style.width = '437px';
	element.style.height  = '421px';
	document.body.appendChild(element);
    }
};

JH.hidePanel = function(a) {
    a.style.display = 'none';
    if(JH.getId('ifrm')){
	JH.getId('ifrm').style.display='none';
    }
};

JH.bindCloseBtn = function(a) {
    a.onclick = function() {
	JH.closePanel();
    };
};

JH.bindTrigger = function(a, b) {
    a.onclick = function() {
	if(b.style.display === 'none') {
	    b.style.display = 'block';
	    if(JH.getId('ifrm')){
		JH.getId('ifrm').style.display='block';
	    }
	    //document.onclick=function(){JH.closePanel()}
	} else if(b.style.display === 'block') {
	    b.style.display = 'none';
	    //document.onclick=null
	    if(JH.getId('ifrm')){
		JH.getId('ifrm').style.display='none';
	    }
	}
    };
};

JH.closePanel = function() {
    JH.getId(JH.obj.panel).style.display = 'none';
    if(JH.getId('ifrm')){
	JH.getId('ifrm').style.display='none';
    }
}
JH.bindAreaEvent = function(a, b) {
    var e = new Array();
    e = JH.getElementsByAttr(a, 'a', 'rel', b);
    for(var i = 0; i < e.length; i++) {
	e[i].onclick = function() {
	    //JH.changeText(this.parentNode.getAttribute('rel'), this.innerHTML.slice(4, this.innerHTML.length));
	    JH.changeText(this.parentNode.parentNode.parentNode.getAttribute('rel'), this.innerHTML, this.getAttribute('id'));
	    JH.closePanel();
	};
    }
};

JH.changeText = function(a, b, c) {
    var c_id = c.split("_");
    setCookie_2012(header_cookieA_name, c_id[1], getExpDate_2012(header_target_cookie_day, 0, 0), "/", header_target_cookie_domain, "");
    if( typeof onLoad_a != "undefined") {
	onLoad_a();
    }
    JH.getId(JH.obj.dispCategory).innerHTML = a;
    JH.getId(JH.obj.dispArea).innerHTML = 'お住まいの地域｜' + b;
};

JH.getId = function(id) {
    return JH.d.getElementById(id);
};

JH.getTag = function(elm, tag) {
    return elm.getElementsByTagName(tag);
};

JH.getElementsByAttr = function(wrapElem, getElm, attrName, attrParam) {
    var e = new Array();
    var elms = wrapElem.getElementsByTagName(getElm);
    for(var i = 0; i < elms.length; i++) {
	if(elms[i].getAttribute(attrName) && elms[i].getAttribute(attrName).indexOf(attrParam) != -1) {
	    e.push(elms[i]);
	};
    };
    return e.length == 0 ? null : e;
};

JH.ready = function(callback) {
    var isLoaded = false;
    if(document.addEventListener) {
	document.addEventListener("DOMContentLoaded", function() {
	    callback();
	    isLoaded = true;
	}, false);
	window.addEventListener("load", function() {
	    if(!isLoaded)
		callback();
	}, false);
    } else if(window.attachEvent) {
	if(window.ActiveXObject && window === window.top) {
	    _ie();
	} else {
	    window.attachEvent("onload", callback);
	}
    } else {
	var _onload = window.onload;
	window.onload = function() {
	    if( typeof _onload === 'function') {
		_onload();
	    }
	    callback();
	};
    }
    function _ie() {
	try {
	    document.documentElement.doScroll("left");
	} catch( error ) {
	    setTimeout(_ie, 0);
	    return;
	}
	callback();
    }

};

JH.ready(function() {
    JH.init({
	dispCategory : 'areatype',
	dispArea : 'area_selected',
	panel : 'area_selector',
	close : 'btn_close',
	rel : 'areaselector'
    });
});

// 設定の定義
if (!window.$$Dept_Setting) {
    window.$$Dept_Setting = {};
}
// インスタンスの定義
if (!window.$$Dept_Instance) {
    window.$$Dept_Instance = {};
}

window.$$Dept_Setting.Live = {
    'CSS1': {
	type: 'css',
	prefix: 'target_live',
	prefs: 'prefs_css',
	values: 'values_css',
	defaultValue: function () {
	    var ret = this.functions.getCookieA();
	    if (this.values) {
		ret = this.values[ret];
	    }
	    return ret;
	}
    },
    conversion: {
	'prefs_css': {
	    'SPK': '1',
	    'SDJ': '4',
	    'TYO': '13',
	    'NGO': '23',
	    'HKJ': '17',
	    'OSA': '27',
	    'HIJ': '37',
	    'TMT': '34',
	    'FUK': '40'
	},
	'values_css': {
	    '1': 'SPK',
	    '2': 'SDJ',
	    '3': 'SDJ',
	    '4': 'SDJ',
	    '5': 'SDJ',
	    '6': 'SDJ',
	    '7': 'SDJ',
	    '8': 'TYO',
	    '9': 'TYO',
	    '10': 'TYO',
	    '11': 'TYO',
	    '12': 'TYO',
	    '13': 'TYO',
	    '14': 'TYO',
	    '15': 'TYO',
	    '16': 'HKJ',
	    '17': 'HKJ',
	    '18': 'HKJ',
	    '19': 'TYO',
	    '20': 'NGO',
	    '21': 'NGO',
	    '22': 'NGO',
	    '23': 'NGO',
	    '24': 'NGO',
	    '25': 'OSA',
	    '26': 'OSA',
	    '27': 'OSA',
	    '28': 'OSA',
	    '29': 'OSA',
	    '30': 'OSA',
	    '31': 'HIJ',
	    '32': 'HIJ',
	    '33': 'HIJ',
	    '34': 'HIJ',
	    '35': 'HIJ',
	    '36': 'HIJ',
	    '37': 'HIJ',
	    '38': 'HIJ',
	    '39': 'HIJ',
	    '40': 'FUK',
	    '41': 'FUK',
	    '42': 'FUK',
	    '43': 'FUK',
	    '44': 'FUK',
	    '45': 'FUK',
	    '46': 'FUK',
	    '47': 'FUK'
	}
    }
};

// 商材ごとのインスタンス生成
(function () {
    for (var s in window.$$Dept_Setting) {
	if (!window.$$Dept_Instance[s]) {
	    window.$$Dept_Instance[s] = new $$Dept(window.$$Dept_Setting[s]);
	}
    }
})();
