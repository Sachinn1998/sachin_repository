async function getdata(){
	var empid = document.getElementById("employee_id").value;
	var f_date = document.getElementById("from_dt").value;
	var t_date = document.getElementById("to_dt").value;
	console.log(empid,f_date,t_date);
	const data = {"emp_id":empid,"from_date":f_date,"to_date":t_date}
	console.log(data);

	const response = await fetch("http://127.0.0.1:8000/emp_report/", {
    method: "POST",
    
    headers: {
      "Content-Type": "application/json",
             },
    body: JSON.stringify(data),
    });

    const result = await response.json();
    console.log(result.data)
   if (result.data == "outofrange") {
   		var tbl = "";
   		document.getElementById("Attendance_tbl").innerHTML = tbl;
   		document.getElementById("alrt").style.display = "inline-block";
   		document.getElementById("alrt").innerHTML = "No Records found! <br> Provide Correct date range. "
      document.getElementById("dropdownMenuButton").style.display = "none";
   } 
   else if(result.data == "notfound"){
   	var tbl = "";
   	document.getElementById("Attendance_tbl").innerHTML = tbl;
   	document.getElementById("alrt").style.display = "inline-block";
   	document.getElementById("alrt").innerHTML = "Employee number is not found! <br> Provide Correct Employee number."
    document.getElementById("dropdownMenuButton").style.display = "none";
   }
   else{
   	var tbl = "<table id='employee'><thead><tr id='table_header'><th>Date</th><th>Time</th><th>Event</th><th>Details</th></tr></thead><tbody>";
   	document.getElementById("alrt").style.display = "none";


   	for(let i in result.data){
   		console.log(result.data[i][2]);
   		var event = ""
   		if (result.data[i][2] == 1) {
   			event = "OUT";
   		} 
   		else {
   			event = "IN";
   		}
   		tbl += "<tr><td>"+result.data[i][0]+"</td><td>"+result.data[i][1]+"</td><td>"+event+"</td><td>"+result.data[i][3]+"</td></tr>";
   	}
    
   	tbl += "</tbody></table>";

   	document.getElementById("Attendance_tbl").innerHTML = tbl;
    document.getElementById("dropdownMenuButton").style.display = "inline-block";
   }
}

function ExportToExcel(type, fn, dl) {
	var elt = document.getElementById('employee');
	var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
	return dl ?
	  XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
	  XLSX.writeFile(wb, fn || ('Attendance_report.' + (type || 'xlsx')));
}

function ExportToCsv(type, fn, dl) {
	var elt = document.getElementById('employee');
	var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
	return dl ?
	  XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
	  XLSX.writeFile(wb, fn || ('Attendance_report.' + (type || 'csv')));
}
