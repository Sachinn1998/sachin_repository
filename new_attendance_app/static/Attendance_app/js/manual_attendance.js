function create_attendence(){
	let emp = document.getElementById('employee_id').value;
	let month = document.getElementById('month').value;
	console.log(emp,month);
	let mt = Number(month.slice(0,4));
	let dt = Number(month.slice(5,7));
	var day = new Date(month + "-01").getDay();
	let ld = new Date(mt,dt, 0).getDate();
	var nxt_day;
	console.log(day,ld,dt,mt);
	if(mt == '0'){
		alert("Please select month!");
	}
	else{
		cal_tbl = '<br><table id= "clndr"><tr><th>SUN</th><th>MON</th><th>TUE</th><th>WED</th><th>THU</th><th>FRI</th><th>SAT</th></tr>';
	if (day==0){
		cal_tbl += '<tr><td>1 <input type="checkbox" id="1"></td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td>';
		nxt_day = 8;
	}
	else if (day==1){
		cal_tbl += '<tr><td></td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td>';
		nxt_day = 7;
	}
	else if (day==2){
		cal_tbl += '<tr><td></td><td></td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td>';
		nxt_day = 6;
	}
	else if (day==3){
		cal_tbl += '<tr><td></td><td></td><td></td><td>1</td><td>2</td><td>3</td><td>4</td>';
		nxt_day = 5;
	}
	else if (day==4){
		cal_tbl += '<tr><td></td><td></td><td></td><td></td><td>1</td><td>2</td><td>3</td>';
		nxt_day = 4;
	}
	else if (day==5){
		cal_tbl += '<tr><td></td><td></td><td></td><td></td><td></td><td>1</td><td>2</td>';
		nxt_day = 3;
	}
	else{
		cal_tbl += '<tr><td></td><td></td><td></td><td></td><td></td><td></td><td>1</td>';
		nxt_day = 2;
	}
	let ref = 1;
	for(let i=nxt_day; i<=ld; i++){
		if(ref == 1 || ref == 8 || ref == 15 || ref == 22 || ref == 29){
			cal_tbl += '<tr><td>'+String(i)+'</td>';
		}
		else{
			cal_tbl += '<td>'+String(i)+'</td>';
		}
		ref +=1;
	}
	cal_tbl += '</tr></table>'
	document.getElementById('calander').innerHTML = cal_tbl;
	}
	
}