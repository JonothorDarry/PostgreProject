//Dostaje td, kryje/odkrywa śmieci z acona albo builda
armist = function(target) {
  var text = target.textContent || target.innerText, j=0, ij=0;
  var arr, mn;
  if (document.getElementById("army_connect")){
  	mn=document.getElementById("army_connect");
    arr = ['id_army'];
  }
  
  else{
  	mn=document.getElementById("building_in_castle_on_map");
    arr = ['x', 'y'];
  }
  var pnt=[0, 0];
  
  
  if (target.parentElement.style.backgroundColor == "rgb(85, 85, 85)"){
  	//Kod odkrycia army connecta - działa
    var unhid=mn.getElementsByTagName("tr");
    //Bez headera
    for (j=1;j<unhid.length;j+=1){
    	unhid[j].style.display="";
    }
    return;
  }
  
  //xv poszukuje w army/hero nr kolumny z id-army albo x, y w zamku: pnt jest tą liczbą(liczbami)
	var xv=target.parentElement.parentElement.parentElement.getElementsByTagName("th");
  
  for (ij=0;ij<arr.length;ij+=1){
  	for (j=0;j<xv.length;j+=1){
      if (xv[j].innerText==arr[ij]){
        pnt[ij]=j;
        break;
      }
    }
  }
  
  
  //xs zawiera oczekiwaną wartość id_army...
  var xs=[0, 0];
  for (ij=0;ij<arr.length;ij+=1){
    xs[ij]=parseInt(target.parentElement.getElementsByTagName("td")[pnt[ij]].innerText);
  }
  
  
  //xv poszukuje w armyconie nr kolumny z id-army: apnt jest tą liczbą  
	var day=mn.getElementsByTagName("th"), apnt=[0,0];
  for (ij=0;ij<arr.length;ij+=1){
  	for (j=0;j<day.length;j+=1){
      if (day[j].innerText==arr[ij]){
        apnt[ij]=j;
        break;
      }
    }
  }
  
  //xd to elementy do modyfki w aconie
  var xd=mn.getElementsByTagName("tr"), vl=[0,0];
  for (j=1;j<xd.length;j+=1){
  	for (ij=0;ij<arr.length;ij+=1){
      vl[ij]=parseInt(xd[j].getElementsByTagName("td")[apnt[ij]].innerText);
      if (vl[ij]!=xs[ij]){break;}
    }
    
    if (ij<arr.length){xd[j].style.display="none";}
    else{xd[j].style.display="";}
  }

}

//Co się dzieje po kliknięciu td?
evefun = function(e) {
  e = e || window.event;
  var target = e.target || e.srcElement,
    text = target.textContent || target.innerText;

  if (target.nodeName != "TD") {return;}
	document.getElementById("nonex").innerHTML="";
  
  //real - nazwa tablicy, ln - długość tr-ów, 
  var ln = target.parentElement.parentElement.parentElement.getElementsByTagName("tr").length;
  var real=target.parentElement.parentElement.parentElement.getAttribute("id");
  
  if (real=="army" || real=="hero" || real=="castle_on_map"){armist(target);}
  
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
