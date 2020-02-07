evefun = function(e) {
  e = e || window.event;
  var target = e.target || e.srcElement,
    text = target.textContent || target.innerText;

  if (target.nodeName != "TD") {return;}
  
  var ln = document.getElementsByTagName("tr").length;
  for (i = 0; i < ln; i += 1) {
    document.getElementById("thetable").getElementsByTagName("tr")[i].style.color="#000000";
    document.getElementById("thetable").getElementsByTagName("tr")[i].style.backgroundColor="#FFFFFF";
  }
  
  target = target.parentElement;
  var hed=target.parentElement.parentElement.getElementsByTagName("th");
    var elemz=target.getElementsByTagName("td");
  

  target.style.backgroundColor = "#555555";
  target.style.color = "#FFFFFF";
  
  document.getElementById("Beniz").innerHTML="";
  var lh=hed.length, i=0;
  for (i=0;i<lh;i+=1){
		var kv=document.createElement("input");
  	kv.setAttribute("type", "hidden");
  	kv.setAttribute("name", hed[i].innerHTML);
    kv.setAttribute("value", elemz[i].innerHTML);
    document.getElementById("Beniz").appendChild(kv);
  }
 	
}


var ln = document.getElementsByTagName("tr").length;
document.getElementById("debug").innerHTML = ln;
for (i = 0; i < ln; i += 1) {
  document.getElementById("thetable").getElementsByTagName("tr")[i].addEventListener('click', evefun, false);
}
