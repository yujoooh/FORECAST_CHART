function getParams() {
	var param = new Array();

	var url = decodeURIComponent(location.href);
	url = decodeURIComponent(url);

	var params;
	params = url.substring(url.indexOf('?') + 1, url.length);
	params = params.split("&");

	var size = params.length;
	var key, value;
	for (var i = 0; i < size; i++) {
		key = params[i].split("=")[0];
		value = params[i].split("=")[1];

		param[key] = value;
	}

	return param;
}

var t_marker;
var t_canvas, t_ctx;
var mapImage;

function pageDownload() {
	var fileName;
	var temp = location.href;
	temp = temp.split('/');
	temp = temp[temp.length - 1].split('.');
	temp = temp[0];
	fileName = temp + ".png";


	var canvas = mapImage;
	html2canvas(document.body.getElementsByClassName("dailyOcean")[0]).then(function (canvas) {
		//document.body.appendChild(canvas);
		mapImage = canvas;
		var imageUrl = mapImage.toDataURL("image/png");
		imageUrl = atob(imageUrl.split(',')[1]);
		var len = imageUrl.length;
		var buf = new ArrayBuffer(len);
		var view = new Uint8Array(buf);
		var blob, i;

		for (i = 0; i < len; i++) {
			view[i] = imageUrl.charCodeAt(i) & 0xff;
		}

		blob = new Blob([view], {
			type: 'image/png'
		});
		console.log(URL.createObjectURL(blob));
		console.log(blob);

		var a = document.createElement('a');
		a.href = URL.createObjectURL(blob);
		a.download = fileName;

		a.click();
	});
}

function chartDownload() {
	var fileName;
	var temp = location.href;
	temp = temp.split('/');
	temp = temp[temp.length - 1].split('.');
	temp = temp[0];
	fileName = temp + ".png";


	var canvas = mapImage;
	html2canvas(document.body.getElementsByClassName("chartWrap")[0]).then(function (canvas) {
		//document.body.appendChild(canvas);
		mapImage = canvas;
		var imageUrl = mapImage.toDataURL("image/png");
		imageUrl = atob(imageUrl.split(',')[1]);
		var len = imageUrl.length;
		var buf = new ArrayBuffer(len);
		var view = new Uint8Array(buf);
		var blob, i;

		for (i = 0; i < len; i++) {
			view[i] = imageUrl.charCodeAt(i) & 0xff;
		}

		blob = new Blob([view], {
			type: 'image/png'
		});
		console.log(URL.createObjectURL(blob));
		console.log(blob);

		var a = document.createElement('a');
		a.href = URL.createObjectURL(blob);
		a.download = fileName;

		a.click();
	});
}

function on_map(area, area_width, area_height) {

	//온맵 캔버스
	$(".onMap").append('<canvas id="mapCanvas" width="1000" height="1000"></canvas>');
	$("#mapCanvas").attr("width", area_width);
	$("#mapCanvas").attr("height", area_height);
	t_canvas = document.getElementById('mapCanvas');
	t_ctx = t_canvas.getContext('2d');


	$.ajax({
		type: "GET",
		url: area + "/on_map.json",
		dataType: "json",
		contentType: "application/x-www-form-urlencoded; charset=UTF-8",
		success: function (data) {

			//지도 바운더리 꼭지점 좌표
			var latEnd = data.BASE_MAP[0].MAP_BOUNDARY_TL_LAT * 1000000;
			var lngStr = data.BASE_MAP[0].MAP_BOUNDARY_TL_LNG * 1000000;
			var latStr = data.BASE_MAP[0].MAP_BOUNDARY_BR_LAT * 1000000;
			var lngEnd = data.BASE_MAP[0].MAP_BOUNDARY_BR_LNG * 1000000;
			//온맵 이미지
			$(".onMap").append('<img src=' + area + '/' + data.BASE_MAP[0].MAP_URL + ' width=' + area_width + ' height=' + area_height + ' />');

			var mapWidth = $(".onMap").width();
			var mapHeight = $(".onMap").height();

			var baseWidth = mapWidth * 1 / (lngEnd - lngStr);
			var baseHeight = mapHeight * 1 / (latEnd - latStr);
			/* 지도 관련 끝 */

			// 오늘 날짜 및 시간
			$(".today .date").html(data.TODAY_DATE.DATE + '');
			$(".today .time").html(data.TODAY_DATE.TIME);
			$(".today .lunar_date").text("(" + data.TODAY_DATE.LUNAR_DATE + ")");

			var marker = "";

			// 수온,파고
			var cnt = data.WATER_TEMP_WAVE_HEIGHT.length;
			var winddir = "a";
			for (var i = 0; i < cnt; i++) {
				var markerH = data.WATER_TEMP_WAVE_HEIGHT[i].LAT * 1000000;
				var markerW = data.WATER_TEMP_WAVE_HEIGHT[i].LON * 1000000;
				var wdir = data.WATER_TEMP_WAVE_HEIGHT[i].WIND_DIR;

				var top = (latEnd - markerH) * baseHeight - 53;
				var left = mapWidth - ((lngEnd - markerW) * baseWidth) - 73;
				
				marker += '<div id="' + data.WATER_TEMP_WAVE_HEIGHT[i].ID + '" class="dataMarker todayInfo" style="top:' + top + 'px; left:' + left + 'px; z-index:3">';
				marker += '<div class="dataBar waterTemp"><span class="icon f_L"><img src="inc/img/icon_waterTemp.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WATER_TEMP).toFixed(1) + '</span>℃</div></div>';
				marker += '<div class="dataBar tide"><span class="icon f_L"><img src="inc/img/icon_waveHeight.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WAVE_HEIGHT).toFixed(1) + '</span>m</div></div>';
				
				if( wdir >= 0 && wdir < 22.5) {
					marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_W.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 22.5 && wdir < 67.5 ){
					marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_SW.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 67.5 && wdir < 112.5 ){
					marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_S.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 112.5 && wdir < 157.5 ){
					marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_SE.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 157.5 && wdir < 202.5){
					marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_E.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 202.5 && wdir < 247.5){
					marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_NE.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 247.5 && wdir < 292.5){
					marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_N.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 292.5 && wdir < 337.5){
					marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_NW.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 337.5 && wdir <= 360){
					marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_W.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				// } else {
				// 	marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				}

				// if(wdir >= 270 ){
				// 	marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_1.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				// } else if (wdir >= 250 ){
				// 	marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_2.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				// } else {
				// 	marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_3.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				// }
				marker += '</div>';
			}

			// 수온,파고 협역
			var cnt = data.LOCAL_WATER_TEMP_WAVE_HEIGHT.length;
			for (var i = 0; i < cnt; i++) {
				var markerH = data.LOCAL_WATER_TEMP_WAVE_HEIGHT[i].LAT * 1000000;
				var markerW = data.LOCAL_WATER_TEMP_WAVE_HEIGHT[i].LON * 1000000;

				var top = (latEnd - markerH) * baseHeight - 30;
				var left = mapWidth - ((lngEnd - markerW) * baseWidth) - 49;

				marker += '<div id="' + data.LOCAL_WATER_TEMP_WAVE_HEIGHT[i].ID + '" class="dataMarker todayLocalInfo" style="top:' + top + 'px; left:' + left + 'px; z-index:3">';
				marker += '<div class="dataLocalBar waterTemp"><span class="icon f_L"><img src="inc/img/icon_waterTemp.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT[i].WATER_TEMP).toFixed(1) + '</span>℃</div></div>';
				marker += '<div class="dataLocalBar tide"><span class="icon f_L"><img src="inc/img/icon_waveHeight.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT[i].WAVE_HEIGHT).toFixed(1) + '</span>m</div></div>';
				marker += '</div>';

			}

			// 수온,파고,바람 협역
			var cnt = data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND.length;
			for (var i = 0; i < cnt; i++) {
				var markerH = data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].LAT * 1000000;
				var markerW = data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].LON * 1000000;
				var wdir = data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WIND_DIR;

				var top = (latEnd - markerH) * baseHeight - 78;
				var left = mapWidth - ((lngEnd - markerW) * baseWidth) - 72;

				marker += '<div id="' + data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].ID + '" class="dataMarker todayLocalInfo" style="top:' + top + 'px; left:' + left + 'px; z-index:3">';
				marker += '<div class="dataLocalBar waterTemp"><span class="icon f_L"><img src="inc/img/icon_waterTemp.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WATER_TEMP).toFixed(1) + '</span>℃</div></div>';
				marker += '<div class="dataLocalBar tide"><span class="icon f_L"><img src="inc/img/icon_waveHeight.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WAVE_HEIGHT).toFixed(1) + '</span>m</div></div>';
				
				if( wdir >= 0 && wdir < 22.5) {
					marker 	+= '<div class="dataLocalBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_N.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 22.5 && wdir < 67.5 ){
					marker 	+= '<div class="dataLocalBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_NE.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 67.5 && wdir < 112.5 ){
					marker 	+= '<div class="dataLocalBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_E.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 112.5 && wdir < 157.5 ){
					marker 	+= '<div class="dataLocalBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_SE.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 157.5 && wdir < 202.5){
					marker 	+= '<div class="dataLocalBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_S.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 202.5 && wdir < 247.5){
					marker 	+= '<div class="dataLocalBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_SW.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 247.5 && wdir < 292.5){
					marker 	+= '<div class="dataLocalBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_W.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 292.5 && wdir < 337.5){
					marker 	+= '<div class="dataLocalBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_NW.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WIND) + '</span>m/s</div></div>';
				} else if (wdir >= 337.5 && wdir <= 360){
					marker 	+= '<div class="dataLocalBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_N.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.LOCAL_WATER_TEMP_WAVE_HEIGHT_WIND[i].WIND) + '</span>m/s</div></div>';
				}

				// if(wdir >= 270 ){
				// 	marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_1.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				// } else if (wdir >= 250 ){
				// 	marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_2.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				// } else {
				// 	marker 	+= '<div class="dataBar wind"><span class="icon f_L">'+'<img src="inc/img/icon_wind_3.png" /></span><div class="data f_L"><span class="value">' + parseFloat(data.WATER_TEMP_WAVE_HEIGHT[i].WIND) + '</span>m/s</div></div>';
				// }
				marker += '</div>';
			}

			// S111 유속
			var cnt = data.S111_CUR.length;
			for (var i = 0; i < cnt; i++) {
				var markerH = data.S111_CUR[i].LAT * 1000000;
				var markerW = data.S111_CUR[i].LON * 1000000;

				var top = (latEnd - markerH) * baseHeight;
				var left = mapWidth - ((lngEnd - markerW) * baseWidth);

				// Standard
				// var min_spd = 0.01; //kn
				// var ref_spd =  5.0; //kn
				// var max_spd = 13.0; //kn
				// var ref_hgt = 10.0; //mm

				// var min_spd = 0.97; //kn  = 0.5 m/s
				// var ref_spd = 1.94; //kn  = 1.0 m/s
				// var max_spd = 3.89; //kn  = 2.0 m/s
				// var ref_hgt = 2.0;  //mm

				// var min_spd = 0.97; //kn
				// var ref_spd = 1.94; //kn
				// var max_spd = 2.92; //kn
				// var ref_hgt = 1.5;  //mm
				
				var min_spd = 0.97; //kn
				var ref_spd = 1.94; //kn
				var max_spd = 2.92; //kn
				var ref_hgt = 1.5;  //mm

				var sym_hgt = ref_hgt * Math.min(Math.max(min_spd * 0.514444, parseFloat(data.S111_CUR[i].CUR_SPD)), max_spd * 0.514444) / (ref_spd * 0.514444);
				// console.log('spd_050 = ' + ref_hgt * Math.min(Math.max(min_spd * 0.514444, 0.5), max_spd * 0.514444) / (ref_spd * 0.514444)); // 0.5 m/s
				// console.log('spd_100 = ' + ref_hgt * Math.min(Math.max(min_spd * 0.514444, 1.0), max_spd * 0.514444) / (ref_spd * 0.514444)); // 1.0 m/s
				// console.log('spd_150 = ' + ref_hgt * Math.min(Math.max(min_spd * 0.514444, 1.5), max_spd * 0.514444) / (ref_spd * 0.514444)); // 1.5 m/s

				marker += '<div id="' + data.S111_CUR[i].ID + '" class="dataMarker" style="top:' + top + 'px; left:' + left + 'px; z-index:1">';


				if (Number(data.S111_CUR[i].CUR_SPD) < 1000.5 * 0.514444) {
					marker += '<img src="inc/img/SCAROW01.svg" ';
				} else if (Number(data.S111_CUR[i].CUR_SPD) < 1.0 * 0.514444) {
					marker += '<img src="inc/img/SCAROW02.svg" ';
				} else if (Number(data.S111_CUR[i].CUR_SPD) < 2.0 * 0.514444) {
					marker += '<img src="inc/img/SCAROW03.svg" ';
				} else if (Number(data.S111_CUR[i].CUR_SPD) < 3.0 * 0.514444) {
					marker += '<img src="inc/img/SCAROW04.svg" ';
				} else if (Number(data.S111_CUR[i].CUR_SPD) < 5.0 * 0.514444) {
					marker += '<img src="inc/img/SCAROW05.svg" ';
				} else if (Number(data.S111_CUR[i].CUR_SPD) < 7.0 * 0.514444) {
					marker += '<img src="inc/img/SCAROW06.svg" ';
				} else if (Number(data.S111_CUR[i].CUR_SPD) < 10.0 * 0.514444) {
					marker += '<img src="inc/img/SCAROW07.svg" ';
				} else if (Number(data.S111_CUR[i].CUR_SPD) < 13.0 * 0.514444) {
					marker += '<img src="inc/img/SCAROW08.svg" ';
				} else {
					marker += '<img src="inc/img/SCAROW09.svg" ';
				}

				marker += 'style="transform: scale(' + sym_hgt + ') rotate(' + data.S111_CUR[i].CUR_DIR + 'deg);">';
				marker += '</div>';

			}

			//침수지역
			var cnt = data.FLOOD_RISK_AREA.length;
			for (var i = 0; i < cnt; i++) {
				var markerH = data.FLOOD_RISK_AREA[i].LAT * 1000000;
				var markerW = data.FLOOD_RISK_AREA[i].LON * 1000000;

				if (data.FLOOD_RISK_AREA[i].DISPLAY == "Y") {
					var top = (latEnd - markerH) * baseHeight - 67;
					var left = mapWidth - ((lngEnd - markerW) * baseWidth) - 25;
				} else if (data.FLOOD_RISK_AREA[i].DISPLAY == "N") {
					var top = (latEnd - markerH) * baseHeight - 20;
					var left = mapWidth - ((lngEnd - markerW) * baseWidth) - 20;
				} else if (data.FLOOD_RISK_AREA[i].DISPLAY == "C") {
					var top = (latEnd - markerH) * baseHeight - 20;
					var left = mapWidth - ((lngEnd - markerW) * baseWidth) - 20;
				}

				if (data.FLOOD_RISK_AREA[i].DISPLAY == "Y") {
					if (data.FLOOD_RISK_AREA[i].FLOOD == "T") {
						marker += '<div id="' + data.FLOOD_RISK_AREA[i].ID + '" class="dataMarker floodingArea" style="top:' + top + 'px; left:' + left + 'px; z-index:1"><div class="faWrap">';
						marker += '<div class="icon"><img src="inc/img/icon_floodingArea.png" /></div>';
						if (data.FLOOD_RISK_AREA[i].MARKER_POS == "R") {
							marker += '<div class="dataPanel" style="left:-150px;">';
						} else if (data.FLOOD_RISK_AREA[i].MARKER_POS == "L") {
							marker += '<div class="dataPanel" style="right:-150px;">';
						}
						marker += '<div class="areaName t_C">' + data.FLOOD_RISK_AREA[i].NAME + '</div>';
						marker += '<div class="time t_C">' + data.FLOOD_RISK_AREA[i].ATTENTION_SPAN[0] + '-' + data.FLOOD_RISK_AREA[i].ATTENTION_SPAN[1] + '</div>';
						marker += '</div>';
						marker += '</div></div>';
					}
				} else if (data.FLOOD_RISK_AREA[i].DISPLAY == "N") {

					marker += '<div id="' + data.FLOOD_RISK_AREA[i].ID + '" class="dataMarker floodingArea_empty" style="top:' + top + 'px; left:' + left + 'px; z-index:1"><div class="faWrap">';
					//marker += '<div class="bullet"><svg height="20" width="20"><circle cx="10" cy="10" r="10" stroke="black" stroke-width="0" fill="#d24162" /></svg></div>'; //red
					marker += '<div class="bullet"><svg height="40" width="40"><circle cx="20" cy="20" r="10" stroke="white" stroke-width="3" fill="#067302" /></svg></div>'; //green border
					//marker += '<div class="bullet"><img src="inc/img/icon_DT_view.png" width="27px" height="30px" /></div>'; //icon
					//marker += '<div class="bullet"><svg height="20" width="20"><rect width="40" height="40" stroke="white" stroke-width="3" fill="#067302" /></svg></div>'; //rect
					//marker += '<div class="bullet"><svg height="20" width="20"><polygon points="10,0 20,20 0,20" stroke="white" stroke-width="3" fill="#067302" /></svg></div>'; //triangle
					if (data.FLOOD_RISK_AREA[i].MARKER_POS == "R") {
						marker += '<div class="dataPanel" style="right:40px;">';
						marker += '<div class="areaName t_L">' + data.FLOOD_RISK_AREA[i].NAME + '</div>';
					} else if (data.FLOOD_RISK_AREA[i].MARKER_POS == "L") {
						marker += '<div class="dataPanel" style="left:40px;">';
						marker += '<div class="areaName t_R">' + data.FLOOD_RISK_AREA[i].NAME + '</div>';
					}

					marker += '</div>';
					marker += '</div></div>';

				} else if (data.FLOOD_RISK_AREA[i].DISPLAY == "C") {

					marker += '<div id="' + data.FLOOD_RISK_AREA[i].ID + '" class="dataMarker floodingArea_empty floodingArea_empty_city" style="top:' + top + 'px; left:' + left + 'px; z-index:1"><div class="faWrap">';
					if (data.FLOOD_RISK_AREA[i].MARKER_POS == "R") {
						marker += '<div class="dataPanel" style="right:40px;">';
						marker += '<div class="areaName t_L">' + data.FLOOD_RISK_AREA[i].NAME + '</div>';
					} else if (data.FLOOD_RISK_AREA[i].MARKER_POS == "L") {
						marker += '<div class="dataPanel" style="left:40px;">';
						marker += '<div class="areaName t_R">' + data.FLOOD_RISK_AREA[i].NAME + '</div>';
					}

					marker += '</div>';
					marker += '</div></div>';

				}
			}

			//연안 저수온
			if (isEmpty(data.LOW_WATER_TEMPERATURE) == false) {

				var cnt = data.LOW_WATER_TEMPERATURE.length;
				for (var i = 0; i < cnt; i++) {
					var markerH = data.LOW_WATER_TEMPERATURE[i].LAT * 1000000;
					var markerW = data.LOW_WATER_TEMPERATURE[i].LON * 1000000;

					var top = (latEnd - markerH) * baseHeight - 10;
					var left = mapWidth - ((lngEnd - markerW) * baseWidth) - 10;

					if (data.LOW_WATER_TEMPERATURE[i].LOW_TEMP == "F") {
						if (data.FLOOD_RISK_AREA[i].FLOOD == "T") {
							marker += '<div id="' + data.FLOOD_RISK_AREA[i].ID + '" class="dataMarker lowWaterTemp_empty" style="top:' + top + 'px; left:' + left + 'px; z-index:1"><div class="faWrap">';

							marker += '</div></div>';
						}
					} else if (data.LOW_WATER_TEMPERATURE[i].LOW_TEMP == "T") {

						marker += '<div id="' + data.LOW_WATER_TEMPERATURE[i].ID + '" class="dataMarker lowWaterTemp" style="top:' + top + 'px; left:' + left + 'px; z-index:1"><div class="faWrap">';
						marker += '<div class="bullet"><svg height="20" width="20"><circle cx="10" cy="10" r="10" stroke="black" stroke-width="0" fill="#5f5b92" /></svg></div>';

						if (data.LOW_WATER_TEMPERATURE[i].MARKER_POS == "R") {
							marker += '<div class="icon" style="left:25px;">';
							marker += '<img src="inc/img/picker_lowWaterTemperature.png" width="60" height="34" />';
							marker += '</div>';
						} else if (data.LOW_WATER_TEMPERATURE[i].MARKER_POS == "L") {
							marker += '<div class="icon" style="right:25px;">';
							marker += '<img src="inc/img/picker_lowWaterTemperature_L.png" width="60" height="34" />';
							marker += '</div>';
						}

						marker += '</div></div>';

					}
				}
			}

			// 해무
			if (isEmpty(data.SEA_FOG) == false) {

				var cnt = data.SEA_FOG.length;
				for (var i = 0; i < cnt; i++) {
					var markerH = data.SEA_FOG[i].LAT * 1000000;
					var markerW = data.SEA_FOG[i].LON * 1000000;

					var top = (latEnd - markerH) * baseHeight - 27;
					var left = mapWidth - ((lngEnd - markerW) * baseWidth) - 73;

					marker += '<div id="' + data.SEA_FOG[i].ID + '" class="dataMarker seaFog sf_' + data.SEA_FOG[i].LEVEL + '" style="top:' + top + 'px; left:' + left + 'px; z-index:3">';
					marker += '<div class="dataBar"><span class="icon f_L"><img src="inc/img/seaFogIcon_0' + data.SEA_FOG[i].LEVEL + '.png" /></span><div class="data f_L"><span class="value">' + data.SEA_FOG[i].PERCENTAGE + '</span>%</div></div>';
					marker += '</div>';

				}
			}

			// 파향,파주기
			var wdpDirectIcons = [];
			var wdpIconDegrees = [];

			if (isEmpty(data.WAVE_DIRECT_PERIOD) == false) {

				var cnt = data.WAVE_DIRECT_PERIOD.length;
				for (var i = 0; i < cnt; i++) {
					var markerH = data.WAVE_DIRECT_PERIOD[i].LAT * 1000000;
					var markerW = data.WAVE_DIRECT_PERIOD[i].LON * 1000000;

					var top = (latEnd - markerH) * baseHeight - 27;
					var left = mapWidth - ((lngEnd - markerW) * baseWidth) - 74;

					marker += '<div id="' + data.WAVE_DIRECT_PERIOD[i].ID + '" class="dataMarker waveDirectPeriod" style="top:' + top + 'px; left:' + left + 'px; z-index:3">';
					marker += '<div class="dataBar"><span class="icon f_L"><img src="inc/img/wdpIcon_symbol.png" /></span><div class="data f_L"><div class="arrow" id="' + data.WAVE_DIRECT_PERIOD[i].ID + '_icon"><img src="inc/img/wdpIcon_arrow_3.png" width="40" height="40" /></div><span class="value">' + data.WAVE_DIRECT_PERIOD[i].WAVE_PERIOD + '</span>s</div></div>';
					marker += '</div>';

					wdpDirectIcons.push(data.WAVE_DIRECT_PERIOD[i].ID + "_icon");
					wdpIconDegrees.push(data.WAVE_DIRECT_PERIOD[i].WAVE_DIRECT);

				}
			}

			// 태풍 마커 생성
			if (isEmpty(data.TYPHOON) == false) {

				//태풍 범례 점선 라인
				var lgdCanvas = document.getElementById('lgdTypLine');
				var lgdCtx = lgdCanvas.getContext('2d');
				lgdCtx.beginPath();
				lgdCtx.lineWidth = 10;
				lgdCtx.strokeStyle = "red";
				lgdCtx.setLineDash([0, 22, 0, 22]);
				lgdCtx.lineCap = "round";
				lgdCtx.lineJoin = "round";
				lgdCtx.moveTo(150, 91);
				lgdCtx.lineTo(250, 0);
				lgdCtx.stroke();

				var t_top, t_left, t_pos, t_preTop, t_preLeft;

				t_ctx.beginPath();
				t_ctx.lineWidth = 10;
				t_ctx.strokeStyle = "red";
				t_ctx.setLineDash([0, 30, 0, 30]);
				t_ctx.lineCap = "round";
				t_ctx.lineJoin = "round";

				var cnt = data.TYPHOON.length;
				for (var i = 0; i < cnt; i++) {

					var itemNo = 0;

					// 범례 데이터
					$(".typLegend").css("display", "inline-block");
					$(".lgd_typ_name").text(data.TYPHOON[i].NAME);
					$(".lgd_typ_date").text(data.TYPHOON[i].ANNOUNCEMENT);

					if (isEmpty(data.TYPHOON[i].NAME) == false) {

						for (var j = 0; j < data.TYPHOON[i].LOCATION.length; j++) {

							var markerH = data.TYPHOON[i].LOCATION[j].LAT * 1000000;
							var markerW = data.TYPHOON[i].LOCATION[j].LON * 1000000;

							t_top = (latEnd - markerH) * baseHeight - 40;
							t_left = mapWidth - ((lngEnd - markerW) * baseWidth) - 40;


							if (itemNo == 0) {
								// 태풍 라인 이동
								console.log("itemNo", itemNo);
								t_ctx.moveTo(t_left, t_top);
							} else {
								t_ctx.lineTo(t_left, t_top);
							}

							marker += '<div class="dataMarker typhoon" style="top:' + t_top + 'px; left:' + t_left + 'px;">';
							marker += '<div class="markerWrap">';
							marker += '<div class="m_img"><img src="inc/img/typ_marker.png" /></div>';
							marker += '<div class="m_data pos_' + data.TYPHOON[i].LOCATION[j].MARKER_POS + '">' + data.TYPHOON[i].LOCATION[j].TIME + '<br />(' + data.TYPHOON[i].LOCATION[j].TEXT + ')' + '</div>';
							marker += '</div>';
							marker += '</div>';

							itemNo++;
							t_preTop = t_top;
							t_preLeft = t_left;

						}

					}
				}
				t_ctx.stroke();
			}


			//조류예보 정점
			var cnt = data.CURRENT_INFO.length;
			var curDirectIcons = [];
			var curIconDegrees = [];
			var dataWrapTopMargin = [];

			for (var i = 0; i < cnt; i++) {
				var markerH = data.CURRENT_INFO[i].LAT * 1000000;
				var markerW = data.CURRENT_INFO[i].LON * 1000000;

				var top = (latEnd - markerH) * baseHeight - 20;
				var left = mapWidth - ((lngEnd - markerW) * baseWidth) - 20;

				marker += '<div id="' + data.CURRENT_INFO[i].ID + '" class="dataMarker tideForecast" style="top:' + top + 'px; left:' + left + 'px; z-index:55">';
				//marker += '<div class="bullet"><svg height="40" width="40"><circle cx="20" cy="20" r="10" stroke="black" stroke-width="0" fill="#F9A01E" /></svg></div>';
				marker += '<div class="bullet"><svg height="40" width="40"><circle cx="20" cy="20" r="10" stroke="white" stroke-width="3" fill="#F9A01E" /></svg></div>';

				if (data.CURRENT_INFO[i].MARKER_POS == "L") {
					marker += '<div class="tfWrap left">';
					marker += '<div class="title accentBg f_R">' + data.CURRENT_INFO[i].NAME + '</div>';
					marker += '<div class="dataWrap f_R">';
				} else if (data.CURRENT_INFO[i].MARKER_POS == "R") {
					marker += '<div class="tfWrap">';
					marker += '<div class="title accentBg f_L">' + data.CURRENT_INFO[i].NAME + '</div>';
					marker += '<div class="dataWrap f_L">';
				}

				var jcnt = data.CURRENT_INFO[i].CUR_INFO.length;
				for (var j = 0; j < jcnt; j++) {
					marker += '<ul>';
					marker += '<li class="tBlue">' + checkEmpty(data.CURRENT_INFO[i].CUR_INFO[j].MIN_CUR_TIME) + '</li>';
					marker += '<li>' + checkEmpty(data.CURRENT_INFO[i].CUR_INFO[j].MAX_CUR_TIME) + '</li>';

					var compass = degToCompass(parseFloat(data.CURRENT_INFO[i].CUR_INFO[j].CUR_DIRECT));
					// marker += '<li class="accent">' + compass + '</li>';
					if (compass == "-") {
						marker += '<li>&nbsp;</li>';
					} else {
						var arrowImg = "";
						var curDirect = Number(data.CURRENT_INFO[i].CUR_INFO[j].CUR_DIRECT);
						var lowDeg = Number(data.CURRENT_INFO[i].DEG_FE[0]);
						var highDeg = Number(data.CURRENT_INFO[i].DEG_FE[1]);
						var typeFE = data.CURRENT_INFO[i].DEG_FE[2];
						if (curDirect >= lowDeg && curDirect < highDeg) {
							if (typeFE == "FLD") {
								arrowImg = "inc/img/FLDSTR.svg"
								console.log('1');
							} else {
								arrowImg = "inc/img/EBBSTR.svg"
								console.log('2');
							}
						} else {
							if (typeFE == "FLD") {
								arrowImg = "inc/img/EBBSTR.svg"
								console.log('3');
							} else {
								arrowImg = "inc/img/FLDSTR.svg"
								console.log('4');
							}
						}
						marker += '<li><div class="arrow"  id="' + data.CURRENT_INFO[i].ID + (j + 1).toString().padStart(2, '0') + '_icon"><img src="' + arrowImg + '" width="40" height="40" /></div></li>';
					}

					//marker += '<li>&nbsp;' + degToCompass(data.CURRENT_INFO[i].CUR_DIRECT_01) + '/' + checkEmpty(data.CURRENT_INFO[i].CUR_SPEED_01) + '</li>';
					marker += '<li>' + checkEmpty((51.44 * data.CURRENT_INFO[i].CUR_INFO[j].CUR_SPEED).toFixed(0)) + '&nbsp;</li>';
					marker += '</ul>';

					if (data.CURRENT_INFO[i].CUR_INFO[j].CUR_DIRECT.length != 0) {
						curDirectIcons.push(data.CURRENT_INFO[i].ID + (j + 1).toString().padStart(2, '0') + "_icon");
						curIconDegrees.push(data.CURRENT_INFO[i].CUR_INFO[j].CUR_DIRECT);
					}

					if (data.CURRENT_INFO[i].MARKER_V_POS == "B") {
						dataWrapTopMargin[i] = -84;
					} else {
						dataWrapTopMargin[i] = 0;
					}
				}

				marker += '</div>';
				marker += '</div></div>';

			}

			$(".onMap").append(marker);
			$.each(dataWrapTopMargin, function (index, item) {
				$(".onMap .tideForecast .dataWrap:eq(" + index + ")").css("margin-top", item + "px");
			});

			arrayRotate(curDirectIcons, curIconDegrees, "20px", "20px");
			curDirectIcons = [];
			curIconDegrees = [];


			arrayRotate(wdpDirectIcons, wdpIconDegrees, "20px", "20px");
			wdpDirectIcons = null;
			wdpIconDegrees = null;

		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			console.log("Status: " + textStatus + ":" + errorThrown);
		}
	});
}

function arrayRotate(objs, degrees, c_x, c_y) {
	for (var i = 0; i < objs.length; i++) {
		$("#" + objs[i]).rotate({
			angle: parseInt(degrees[i]),
			center: [c_x, c_y],
		});
		console.log($("#" + objs[i]));
	}
}

function degToCompass(num) {
	if (isNaN(num)) {
		return "-";
	} else {
		var val = Math.floor((num / 22.5) + 0.5);
		var arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
		return arr[(val % 16)];
	}
}

// 빈 값 체크
function isEmpty(value) {
	if (value == "" || value == null || value == undefined || (value != null && typeof value == "object" && !Object.keys(value).length)) {
		return true;
	} else {
		return false
	}
};

function checkEmpty(val) {
	if (val == "") {
		return "-";
	} else {
		return val;
	}
}

function fillRoundRect(ctx, l, t, w, h, r) {
    var pi = Math.PI;
    ctx.beginPath();
    ctx.arc(l + r, t + r, r, - pi, - 0.5 * pi, false);
    ctx.arc(l + w - r, t + r, r, - 0.5 * pi, 0, false);
    ctx.arc(l + w - r, t + h - r, r, 0, 0.5 * pi, false);
    ctx.arc(l + r, t + h - r, r, 0.5 * pi, pi, false);
    ctx.fillStyle = 'rgba(220,220,220,0.8)';
    ctx.closePath();
    ctx.fill();
}