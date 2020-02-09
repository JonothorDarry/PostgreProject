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
      if (xv[j].getAttribute("data-wisdom")==arr[ij]){
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
      if (day[j].getAttribute("data-wisdom")==arr[ij]){
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
    kv.setAttribute("type", "hidden");
    kv.setAttribute("name", hed[i].getAttribute("data-wisdom"));
    kv.setAttribute("value", elemz[i].innerText);
    document.getElementById("nonex").appendChild(kv);
  }
}

sorto=function(e){
	e = e || window.event;
  var target = e.target || e.srcElement,
    text = target.textContent || target.innerText;
  
  var lower=1;
  if (target.getAttribute("class")=="sbtnu"){lower=-1;}
  
  var arg=target.parentElement.parentElement.getAttribute("data-wisdom"), 
  trs=target.parentElement.parentElement.parentElement.parentElement.parentElement.getElementsByTagName("tr"),
  ths=target.parentElement.parentElement.parentElement.parentElement.parentElement.getElementsByTagName("th"),
  i=0, jj=0, ij=0, ptr=0, tmp=0, tmp2;
  
  for (i = 0; i < ths.length; i++) {
    tmp=ths[i].getAttribute("data-wisdom");
    if (tmp==arg){
    	ptr=i;
      break;
    }
  }
  var x = new Array(trs.length), numa=1;
  for (i = 0; i < x.length; i++) {x[i] = new Array(ths.length);}
  
  for (i = 1; i < trs.length; i++) {
  	tmp=trs[i].getElementsByTagName("td");
    for (jj=0;jj<tmp.length;jj++){      
    	x[i-1][jj]=tmp[jj].innerText;
    }
    
    tmp2=tmp[ptr].innerText;
    for (ij=0;ij<tmp2.length;ij++){
      if (tmp2.charCodeAt(ij)<48 || tmp2.charCodeAt(ij)>57){
      	numa=0;
        break;
      }
    }
  }
  
  if (numa==0){
  	myfunct=function(a, b){
    	  return (a[ptr]<b[ptr]?(-lower):(a[ptr]>b[ptr]?lower:0)); 
    }
  }
  else{
    myfunct=function(a, b){
      return lower*(parseInt(a[ptr])-parseInt(b[ptr]));
    }
  }
  
  x.sort(myfunct);
 
  for (i=1;i<trs.length;i++){
  	tmp=trs[i].getElementsByTagName("td");
    for (jj=0;jj<tmp.length;jj++){
    	tmp[jj].innerText=x[i-1][jj];
    }
  }
}

starter=function(){
	var i=0, j=0, x=document.getElementsByTagName("th"), y, z, res="";
  for (i=0;i<x.length;i++){
  	y=x[i].childNodes[0].nodeValue.trim().split("_");
    for (j=0;j<y.length;j++){
    	z=y[j][0].toUpperCase()+y[j].substr(1, y[j].length-1);
      res=res+z;
      if (j<y.length-1) res=res+' ';
    }
    x[i].setAttribute("data-wisdom", x[i].childNodes[0].nodeValue.trim());
    x[i].childNodes[0].nodeValue=res;
    res="";
  }
}

//Ceremonia Otwarcia kodu strony
starter()
var j=0;
//Linia kluczowa - lista tablic do orania
//let docs = ["hero", "army", "army_connect"];
for (j=0;j<docs.length;j+=1){
  for (i = 0; i < document.getElementById(docs[j]).getElementsByTagName("tr").length; i += 1) {
    document.getElementById(docs[j]).getElementsByTagName("tr")[i].addEventListener('click', evefun, false);
  }
}

var morbidu=document.getElementsByClassName("sbtnu");
var morbidd=document.getElementsByClassName("sbtnd");
for (i = 0; i < morbidu.length; i += 1) {
  morbidu[i].addEventListener('click', sorto, false);
  morbidd[i].addEventListener('click', sorto, false);
}
