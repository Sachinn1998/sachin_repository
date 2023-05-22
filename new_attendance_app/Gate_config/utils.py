def gate_configuration(data):
	r_id = int(data.get("readerid"))
	imei = int(data.get("imei"))
	r_name = data.get("readername")
	simno = int(data.get("simno"))
	ipadd = data.get("ipaddress")
	ssid = data.get("ssid")
	subnet = data.get("subnetmask")
	def_gataway = data.get("defaultgateway")
	r_pass = data.get("routerpassword")
	lat = float(data.get("lat"))
	lang = float(data.get("lang"))
	result=[r_id,imei,r_name,simno,ipadd,ssid,subnet,def_gataway,r_pass,lat,lang]
	return result