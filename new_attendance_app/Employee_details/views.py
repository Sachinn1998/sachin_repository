from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection
import json

# Create your views here.
@login_required
def emp_list(request):
	cursor = connection.cursor()
	cursor.callproc('sproc_getempdetails',(0,))
	results = cursor.fetchall()
	print(results)
	cursor.close()	
	mydict       = {'active':True,'result':results}
	return render(request=request,template_name ='Employee_details/emp_list.html',context = mydict)


@login_required
def emp_details(request,empid):
	empid= int(empid)
	cursor = connection.cursor()
	cursor.callproc('sproc_getempdetails',(empid,))
	results = cursor.fetchall()
	print(results)
	cursor.close()	
	mydict       = {'active':True,'result':results[0]}
	return render(request=request,template_name ='Employee_details/emp_details.html',context = mydict)

@login_required
def emp_update(request,empid):
	if request.method == "POST":
		res = request.POST
		lst = ["name","email","pid","dob","mob","address","empid","tagid","designation","department","doj","enabled"]
		name = res.get("name")
		email = res.get("email")
		pid = res.get("pid")
		dob = res.get("dob")
		mob = int(res.get("mob"))
		address = res.get("address")
		empid = int(res.get("empid"))
		tagid = int(res.get("tagid"))
		designation = res.get("designation")
		department = res.get("department")
		doj = res.get("doj")
		try:
			enabled = res.get("enabled")
			if enabled=="1":
				enabled = True
			else: 
				enabled = False	
		except:
			enabled = False
			
		finally:	
			args = [name,email,pid,dob,mob,address,empid,tagid,designation,department,doj,enabled]
			print(args)
			
		# print(res.get("name"))
		# print(emp_details(res))
		# args = emp_details(res)
		args.append(1)
		cursor = connection.cursor()
		cursor.callproc('sprcc_insertempdetails',args)
		results = cursor.fetchall()
		print(results)
		cursor.close()
		# results = [[1,],]
		if results[0][0] == 1:
			return render(request=request,template_name ='Employee_details/emp_update.html', context={'active':True,"success":True})
		else:
			mydict = {'active':True,"msg":"Employee Id Already Exists!","result":args}
			return render(request=request,template_name ='Employee_details/emp_update.html', context=mydict)


	empid= int(empid)
	cursor = connection.cursor()
	cursor.callproc('sproc_getempdetails',(empid,))
	results = cursor.fetchall()
	results = list(results[0])
	results[3] = str(results[3])
	results[10] = str(results[10])
	print(results)
	cursor.close()	
	mydict       = {'active':True,'result':results}
	return render(request=request,template_name ='Employee_details/emp_update.html',context = mydict)

@login_required
def employee_registration(request):
	if request.method == "POST":
		res = request.POST
		name = res.get("name")
		email = res.get("email")
		pid = res.get("pid")
		dob = res.get("dob")
		mob = int(res.get("mob"))
		address = res.get("address")
		empid = int(res.get("empid"))
		tagid = int(res.get("tagid"))
		designation = res.get("designation")
		department = res.get("department")
		doj = res.get("doj")
		try:
			enabled = res.get("enabled")
			if enabled=="1":
				enabled = True
			else: 
				enabled = False	
		except:
			enabled = False
			
		finally:	
			args = [name,email,pid,dob,mob,address,empid,tagid,designation,department,doj,enabled]
			print(args)
			
		args.append(0)
		cursor = connection.cursor()
		cursor.callproc('sprcc_insertempdetails',args)
		results = cursor.fetchall()
		print(results)
		cursor.close()
		if results[0][0] == 1:
			return render(request=request,template_name ='Employee_details/emp_registration.html', context={'active':True,"success":True})
		else:
			mydict = {'active':True,"msg":"Employee Id Already Exists!","fail":True}
			for i in range(len(args)):
				mydict["res"+str(i)] = args[i]

			print(mydict)
			return render(request=request,template_name ='Employee_details/emp_registration.html', context=mydict)

	mydict       = {'active':True,}
	return render(request=request,template_name ='Employee_details/emp_registration.html',context = mydict)

@login_required
def emp_delete(request,empid):
	empid= int(empid)
	cursor = connection.cursor()
	cursor.execute('delete from tblemployeedetails where empid = %s',(empid,))
	cursor.close()	
	return redirect("/employee_details/emp_list/")