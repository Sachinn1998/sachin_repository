from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from Gate_config.utils import gate_configuration
import json

# Create your views here.
@login_required
def gate_configurations(request):
	if request.method == "POST":
		res = request.POST
		args = gate_configuration(res)
		cursor = connection.cursor()
		cursor.callproc('sprcc_gateconfigmaster',args)
		results = cursor.fetchall()
		print(results)
		cursor.close()
		return render(request=request,template_name ='Gate_config/gate_config.html', context={'activate':True})

	mydict       = {'activate':True,'options':True}
	return render(request=request,template_name ='Gate_config/gate_config.html',context = mydict)


@csrf_exempt
def collect_data(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		details = str(data['Data'])
		tagid = data['Data']['TagID']
		args = []
		
		try:
			for i in data["DeviceInfo"].values():
				args.append(i)
			args.append(tagid)
			args.append(details)
			print(args)
			cursor = connection.cursor()
			cursor.callproc('sproc_dataupdation',args)
			res = cursor.fetchall()[0]

			# print(res,len(res))
			if len(res) == 1:
				msg = '$+ReaderId:%s,+Imei:%s,+ReaderName:%s,+Simno:%s,+Ipaddress:%s,+Ssid:%s,+SubnetMask:%s,+DefaultGateway:%s,+RouterPassword:%s,+Latitude:%s,+Logitude:%s,+UpadateStatus:%s,UpadatedTime:%s#'%res
				status =404
			else:
				msg = '$+ReaderId:%s,+Imei:%s,+ReaderName:%s,+Simno:%s,+Ipaddress:%s,+Ssid:%s,+SubnetMask:%s,+DefaultGateway:%s,+RouterPassword:%s,+Latitude:%s,+Logitude:%s,+UpadateStatus:%s,UpadatedTime:%s#'%res
				status = 200	
			
			return HttpResponse(msg, content_type='text/plain', status = status)
			
		except Exception as e:
			print(e)
			return JsonResponse({'error': str(e)})
	else:
		return JsonResponse({'error': 'Invalid request method'})
		safe=False

@csrf_exempt
def site_data(request):
	cursor = connection.cursor()
	cursor.callproc('sproc_sitedata')
	res = cursor.fetchall()
	print(res)
	cursor.close()
	lst = ["sitename","siteid","lat","lng","enable"]
	res_lst = []
	for i in res:
		res_dct = {lst[k]:i[k]  for k in range(0, len(lst))}
		res_lst.append(res_dct)
	# print(res_lst)
	return JsonResponse(res_lst, safe=False)


@login_required
def live(request):
	mydict       = {'active':True}
	return render(request=request,template_name ='Gate_config/live.html',context = mydict)