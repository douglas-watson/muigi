/* 
	Receiving Data, and modifying the right places
*/
function awebRecv(data) {
	function gt(e, w) { 
		if (e.getElementsByTagName(w)[0].childNodes.item(0) == null) {
			return null;	
		}
		return e.getElementsByTagName(w)[0].childNodes.item(0).data;
	}
	var c = data.getElementsByTagName('cm');
	for (var x = 0; x < c.length; x++) { 
		var cmd = gt(c[x], 'd');
		if (cmd == 'assign') {
			awebDoAssign(gt(c[x], 'i'), gt(c[x], 'p'), gt(c[x], 'v'));
		} else if (cmd == 'append') {
			awebDoAppend(gt(c[x], 'i'), gt(c[x], 'p'), gt(c[x], 'v'));
		} else if (cmd == 'prepend') {
			awebDoPrepend(gt(c[x], 'i'), gt(c[x], 'p'), gt(c[x], 'v'));
		} else if (cmd == 'script') {
			awebDoScript(gt(c[x], 's'));
		} else if (cmd == 'alert') {
			awebDoAlert(gt(c[x], 'm'));
		} else if (cmd == 'checkbox') {
			awebDoCheckbox(gt(c[x], 'i'), gt(c[x], 'v'));
		} else if (cmd == 'remove') {
			awebDoRemove(gt(c[x], 'i'));
		} 
	}
	
}
function awebDoAssign(id, property, value) {
	document.getElementById(id)[property] = value;
}
function awebDoAppend(id, property, value) {
	document.getElementById(id)[property] += value;
}
function awebDoPrepend(id, property, value) {
	document.getElementById(id)[property] = value + document.getElementById(id)[property];
}
function awebDoScript(s) {
	eval(s);
}
function awebDoAlert(msg) {
	alert(msg);
}
function awebDoRemove(id) {
	document.getElementById(id).parentNode.removeChild(document.getElementById(id));
}
function awebDoCheckbox(id, v) {
	e = document.getElementById(id);
	if (v == 't') e.checked = true;
	else if (v =='f') e.checked = false;
}

/* 
	Generating and sending data 
*/
function aweb() {
	fun = arguments[0];
	vars = '';
	for (x = 1; x < arguments.length; x++) {
		vars = vars + arguments[x];
	}
	data = 'ajax=true&fun=' + fun + '&data=<data>' + vars + '</data>';
	awebFunction(document.URL, data);
}
function awebFunction(url, vars) {
	var xmlHttp;
	try {
	xmlHttp=new XMLHttpRequest();
	} 
	catch(e) {
		try {
			xmlHttp =new ActiveXObject("Msxml2.XMLHTTP");
		}
		catch (e)
		{
			try {
				xmlHttp= new ActiveXObject("Microsoft.XMLHTTP");
			}
			catch (e) {
				alert("No support for XMLHTTP");
				return false;
			}
		}
	}

	xmlHttp.onreadystatechange=function() {
		if (xmlHttp.readyState==4) {
			awebRecv(xmlHttp.responseXML);
		}
	}
	xmlHttp.open("POST", url, true);
	xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=utf-8");
	xmlHttp.send(vars);
}

/*
	Parsing data from inputs
*/
function awebPE(e) {
	return awebPV(e.name, awebGetRealValue(e));
}
function awebPV(id, data) {
	return '<var>' + awebParseData(id, data) + '</var>';
}
function awebGetRealValue(e) {
	if (e.type == 'checkbox') return e.checked;
	else return e.value;
}
function awebParseData(id, data) {
	return '<k>' + awebCdata(id) + '</k><v>' + awebCdata(data) + '</v>';
}
function awebIsInput(node) {
	if ((node == '[object HTMLInputElement]') || (node == '[object HTMLTextAreaElement]')) return true;
	else return false;
}
function awebParseNode(node) {
	var childNodes = node.childNodes;
	var inputNodes = new Array();
	for (var i = 0; i < childNodes.length; i++) {
		if (awebIsInput(childNodes[i]) == true) {
			inputNodes[inputNodes.length] = childNodes[i];
		}
		else inputNodes = inputNodes.concat(awebParseNode(childNodes[i]));
	}
	return inputNodes;
}
function awebPF(form) {
	var x = awebParseNode(form);
	var o = '<f>';
	o += '<fn>' + awebCdata(form.name) + '</fn>';
	o += '<fva>';
	for (i = 0; i < x.length; i++) {
		o += '<fv>' + awebParseData(x[i].name, awebGetRealValue(x[i])) + '</fv>';
	}
	o += '</fva>';
	o += '</f>';
	return o;
}
function awebCdata(text) {
	if (encodeURIComponent(text) != text)return '<![CDATA[' + text + ']]>';
	else return text;
}
