from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection
import json
import calendar
from datetime import date, timedelta

# Create your views here.
@login_required
def emp_report(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		# print(data)
		emp_id    = int(data['emp_id'])
		from_date = data['from_date']
		to_date   = data['to_date']
		args = [int(emp_id),from_date,to_date]
		# print(args)
		cursor = connection.cursor()
		cursor.callproc('sproc_getempattendance',args)
		results = cursor.fetchall()
		cursor.close()
		# print(results)
		if len(results)==0:
			# return render(request=request,template_name ='Employee_attendance/employee_report.html', context = {"msg":"No Records found!\nProvide Correct date range.",'active':True})
			return JsonResponse({"data":"outofrange"})
		if len(results[0]) == 1:
			# return render(request=request,template_name ='Employee_attendance/employee_report.html', context = {"msg":"Employee number is not found!\nProvide Correct Employee number.",'active':True})
			return JsonResponse({"data":"notfound"})
		
		return JsonResponse({"data":results})

	
	mydict 		= {'active':True}
	return render(request=request,template_name ='Employee_attendance/employee_report.html',context = mydict)

@login_required
def all_emp_reports(request):
	if request.method == 'POST':
		post_data = request.POST
		args = []
		for key, value in post_data.items():
			args.append(value)
		print(args[1::])
		cursor = connection.cursor()
		cursor.callproc('sproc_getallemprecords',args[1::])
		results = cursor.fetchall()
		cursor.close()
		total = len(results)
		p = 0
		a = 0
		for i in results:
			print(i)
			if i[-1] == 1:
				p += 1
			else:
				a += 1
		print(p,a)
		mydict = {'active':True,'result':results,'date':args[1],"total":total,"pr":p,"ab":a}

		return render(request=request,template_name ='Employee_attendance/all_empreports.html',context = mydict)

	mydict = {'active':True}
	return render(request=request,template_name ='Employee_attendance/all_empreports.html',context = mydict)

@login_required
def count_reports(request):
	if request.method == 'POST':
		post_data = request.POST
		data = []
		for key, value in post_data.items():
			data.append(value)
		print(data[1::])
		f_d = list(map(int,data[1].split("-")))
		t_d = list(map(int,data[2].split("-")))
		dep = data[3]

		d1 = date(f_d[0], f_d[1], f_d[2]) 
		d2 = date(t_d[0], t_d[1], t_d[2])
		d = d2-d1
		date_list = []
		for i in range(d.days + 1):
		    day = d1 + timedelta(days=i)
		    date_list.append(day)
		results = []
		for i in date_list:
			print(i)
			args = [i,dep]
			cursor = connection.cursor()
			cursor.callproc('sproc_allempcount',args)
			res = cursor.fetchall()
			print(res)
			results.append(res)
			cursor.close()
		mydict = {'active':True,'result':results,'fd':data[1],'td':data[2]}

		return render(request=request,template_name ='Employee_attendance/count.html',context = mydict)

	mydict = {'active':True}
	return render(request=request,template_name ='Employee_attendance/count.html',context = mydict)


@login_required
def ManualAttendanceUpdate(request):
	mydict = {'active':True}

	if request.method == "POST":
		data = dict(request.POST)
		empid = data['empid']
		year = data['year']
		month = data['months']
		del data['empid']
		del data['year']
		del data['months']
		del data['csrfmiddlewaretoken']
		num_days = calendar.monthrange(int(year[0]), int(month[0]))[1]
		res = {}
		for i in range(1,num_days):
			if "date"+str(i) in data:
				res['day'+str(i)] = "P"
			else:
				res['day'+str(i)] = "A"
		print(res)
		args = [empid,year[0]+'-'+month[0]+"-01",json.dumps(res)]
		# print(args)
		cursor = connection.cursor()
		cursor.callproc('sproc_manualupdate',args)
		results = cursor.fetchall()
		cursor.close()
		print(results)
		res = results[0][0]
		if res == 'inserted':
			mydict["inserted"] = True
		elif res == 'updated':
			mydict["updated"] = True
		else:
			mydict["notfound"] = True

		return render(request,'Manual_attendance/Attendance_upadate.html', mydict)

	return render(request=request,template_name ='Manual_attendance/Attendance_upadate.html',context = mydict)


@login_required
def ManualAttendanceDisplay(request):
	mydict = {'active':True}
	if request.method == "POST":
		data = request.POST
		print(data)
	return render(request=request,template_name ='Manual_attendance/Attendance_display.html',context = mydict)

@login_required
def demo(request,dep,dt):
	dt = dt.split("-")
	dt = dt[2]+'-'+dt[1]+'-'+dt[0]
	args = [dt,dep]
	print(args)
	cursor = connection.cursor()
	cursor.callproc('sproc_getallemprecords',args)
	results = cursor.fetchall()
	cursor.close()
	print(results)
	total = len(results)
	p,a = 0
	
	for i in results:
		print(i)
		if i[-1] == 1:
			p += 1
		else:
			a += 1
	print(p,a)
	mydict = {'active':True,'result':results,'date':dt,"total":total,"pr":p,"ab":a}

	return render(request=request,template_name ='Employee_attendance/all_empreports.html',context = mydict)
	# return JsonResponse(r, safe=False)6