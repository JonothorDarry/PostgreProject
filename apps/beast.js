   let docs = ['army', 'hero', 'army_connect'];
   
//Dostaje td, kryje/odkrywa śmieci
armist = function(target) {
  var text = target.textContent || target.innerText, j=0;
	if (target.parentElement.style.backgroundColor == "rgb(85, 85, 85)"){
  	//Kod odkrycia army connecta
    unhid=document.getElementById("army_connect").getElementsByTagName("td");
    for (j=0;j<unhid.length;j+=1){
    	unhid[j].style.display="none";
    }
    return;
  }
  
	var xv=target.parentElement.parentElement.parentElement.getElementsByTagName("th"), j=0, pnt;
  for (j=0;j<xv.length;j+=1){
  	if (xv[j].innerText=="id_army"){
    	pnt=j;
      break;
    }
  }
  
  var xs=target.parentElement.getElementsByTagName("td")[pnt];
  
  
  
}


evefun = function(e) {
  e = e || window.event;
  var target = e.target || e.srcElement,
    text = target.textContent || target.innerText;

  if (target.nodeName != "TD") {return;}
	document.getElementById("nonex").innerHTML="";
  
  //real - nazwa tablicy, ln - długość tr-ów, 
  var ln = target.parentElement.parentElement.parentElement.getElementsByTagName("tr").length;
  var real=target.parentElement.parentElement.parentElement.getAttribute("id");
  
  if (real=="army" || real=="hero"){armist(target);}
  
  target = target.parentElement;
  if (target.style.backgroundColor == "rgb(85, 85, 85)"){
  	target.style.backgroundColor = "#FFFFFF";
  	target.style.color = "#000000";
    return;
  }
  
  for (i = 0; i < ln; i += 1) {
    document.getElementById(real).getElementsByTagName("tr")[i].style.color="#000000";
    document.getElementById(real).getElementsByTagName("tr")[i].style.backgroundColor="#FFFFFF";
  }
	
  var hed=target.parentElement.parentElement.getElementsByTagName("th");
  var elemz=target.getElementsByTagName("td");


  target.style.backgroundColor = "#555555";
  target.style.color = "#FFFFFF";

  var lh=hed.length, i=0;
  for (i=0;i<lh;i+=1){
    var kv=document.createElement("input");
    kv.setAttribute("type", "text");
    kv.setAttribute("name", hed[i].innerText);
    kv.setAttribute("value", elemz[i].innerText);
    document.getElementById("nonex").appendChild(kv);
  }
}









var j=0;
//Linia kluczowa - lista tablic do orania
//let docs = ["hero", "army", "army_connect"];
for (j=0;j<docs.length;j+=1){
  for (i = 0; i < document.getElementById(docs[j]).getElementsByTagName("tr").length; i += 1) {
    document.getElementById(docs[j]).getElementsByTagName("tr")[i].addEventListener('click', evefun, false);
  }
}


