function toggleTOC(){
	if(document.getElementById("toc").style.display == "none"){
		document.getElementById("toc").style.display = "inline";
		document.getElementById("toctoggle").className = "glyphicon glyphicon-eye-open";
	} else {
		document.getElementById("toc").style.display = "none";
		document.getElementById("toctoggle").className = "glyphicon glyphicon-eye-close";
	}
}