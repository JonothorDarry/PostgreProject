evefun = function(e) {
  e = e || window.event;
  var target = e.target || e.srcElement,
    text = target.textContent || target.innerText;

  if (target.nodeName != "TD") {return;}

	document.getElementById("nonex").innerHTML+="Beniz";
  var ln = target.parentElement.parentElement.parentElement.getElementsByTagName("tr").length;
  var real=target.parentElement.parentElement.parentElement.getAttribute("id");
  
  for (i = 0; i < ln; i += 1) {
    document.getElementById(real).getElementsByTagName("tr")[i].style.color="#000000";
    document.getElementById(real).getElementsByTagName("tr")[i].style.backgroundColor="#FFFFFF";
  }
	
  target = target.parentElement;
  var hed=target.parentElement.parentElement.getElementsByTagName("th");
  var elemz=target.getElementsByTagName("td");


  target.style.backgroundColor = "#555555";
  target.style.color = "#FFFFFF";

  document.getElementById("nonex").innerHTML="";
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
