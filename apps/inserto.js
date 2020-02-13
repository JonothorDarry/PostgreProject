terminal_insert=function(){
  var i=0, j=0, cnt=0, fls, x=document.querySelectorAll('select[name="building_in_castle_on_map-build_name-castle"]')[0].getElementsByTagName("option");
  var abase=document.querySelectorAll('select[name="building_in_castle_on_map-x-y-castle"]')[0].value, base=new Array(20), last;
  
  for (i=0;i<abase.length;i++){
  	if (abase[i]=='-')	cnt+=1;
    if (cnt>=2) break;
  }
 	
  for (i=i+1;i<abase.length;i++)	base[j]=abase[i], j++;
  base=base.join('');
  
  for (i=0;i<x.length;i++){
  	fls=x[i].getAttribute('value').substr(1,).includes(base);
    if (!fls) x[i].setAttribute('hidden', '');
    else x[i].removeAttribute('hidden'), last=i;
  }
  
  //Zmiana wartości selecta, jeśli nieodpowiedni
  var ct=document.querySelectorAll('select[name="building_in_castle_on_map-build_name-castle"]')[0].value
  if(!ct.substr(1,).includes(base)) document.querySelectorAll('select[name="building_in_castle_on_map-build_name-castle"]')[0].value=x[last].getAttribute('value')
  
}

terminal_insert()
document.querySelectorAll('select[name="building_in_castle_on_map-x-y-castle"]')[0].addEventListener('ValueChange', terminal_insert, false);

