from wfs20.error import WFSError
from wfs20.util import _PostElement, WFS_NAMESPACE

import sys
import requests
from lxml import etree
from urllib.parse import parse_qsl, urlencode

def _BaseRequestURL(url):
	"""Separate the url in a base-url and parameters
	"""
	
	par = []
	if url.find("?") != -1:
		par = parse_qsl(url.split("?")[1])
	return url.split("?")[0],par

def _ServiceURL(url, version):
	"""Ensure a suitable url for the service GetCapabilities request
	"""

	base,par = _BaseRequestURL(url)
	key = [item[0] for item in par]
	if "service" not in key:
		par += [("service","WFS")]
	if "request" not in key:
		par += [("request","GetCapabilities")]
	if "version" not in key:
		par += [("version",version)]
	urlpar = urlencode(par)
	return "?".join([url.split("?")[0],urlpar])

def GetResponse(
	url: str,
	timeout: int,
	method: str ="GET",
	data: str=None,
) -> requests.models.Response:
	"""Get the response from a url to be requested

	Parameters
	----------
	url : str
		url to be requested
	timeout : int
		Allowed timeout after which an Exception is raised
	method : str, optional
		Request method, either 'GET' or 'POST'
	data : str, optional
		Parameters in xml format

	Returns
	-------
	requests.models.Response
		object holding the response data
	"""

	params = {}
	params["timeout"] = timeout

	if data is not None:
		params["data"] = data

	r = requests.request(method,url,**params)

	if r.status_code in range(400,451,1):
		raise WFSError("Client Error", r.status_code, r.text)
	elif r.status_code in range(500,511,1):
		raise WFSError("Server Error", r.status_code, r.text)

	if "Content-Type" in r.headers and \
			r.headers['Content-Type'] in ['text/xml', 'application/xml', 'application/vnd.ogc.se_xml']:
		wfse = etree.fromstring(r.content)
		exceptions = [
            '{http://www.opengis.net/ows}Exception',
            '{http://www.opengis.net/ows/1.1}Exception',
            '{http://www.opengis.net/ogc}ServiceException',
            'ServiceException'
        ]

		if any(map(wfse.find,exceptions)):
			raise WFSError("WFS Error", r.status_code, r.text)

	# sys.stdout.write(f"Status Code: {r.status_code}\n")

	return r

def BBOXGet(
	bbox: tuple,
	crs: int,
) -> str:
	"""Create string from bounding box tuple
	"""

	if crs.encoding == "urn":
		if crs.order == "xy":
			return "{},{},{},{},{}".format(
				*bbox,
				crs.GetURNCode()
				)
		else:
			return "{},{},{},{},{}".format(
				bbox[1],
				bbox[0],
				bbox[3],
				bbox[2],
				crs.GetURNCode()
				)
	else:
		return "{},{},{},{},{}".format(
			*bbox,
			crs.GetURICode1()
			)

def CreateGetRequest(
	url: str,
	version: str,
	featuretype: str,
	bbox: tuple,
	crs: 'wfs20.crs.CRS',
	startindex: int=None,
) -> str:
	"""Create a geospatial data get request-url

	Parameters
	----------
	url : str
		Service url
	version : str
		Service version
	featuretype : str
		Layer to be requested, mostly in the format of 'xxx:xxx'
	bbox : tuple
		Bounding box wherein the spatial data lies that is requested,
		e.g. (x1,y1,x2,y2)
	crs : wfs20.crs.CRS
		Object containing projection information
	startindex : int, optional
		Starting index of the feature count

	Returns
	-------
	str
		get request url
	"""

	base,_ = _BaseRequestURL(url)
	params = {
		"service":"WFS","version":f"{version}",
		"request":"GetFeature"
		}
	params["typenames"] = [featuretype] 
	params["bbox"] = BBOXGet(bbox, crs)
	if startindex is not None:
		params["startindex"] = startindex
	p = urlencode(params,doseq=True)
	return f"{base}?{p}"

# ToDo: Fix post requests for this library
def CreatePostRequest(
	url: str,
	version: str,
	featuretype: str,
	bbox: tuple,
	crs: 'wfs20.crs.CRS',
	startindex: int=None,
) -> tuple:
	"""Generate post request-url & data

	Parameters
	----------
	url : str
		Service url
	version : str
		Service version
	featuretype : str
		Layer to be requested, mostly in the format of 'xxx:xxx'
	bbox : tuple
		Bounding box wherein the spatial data lies that is requested,
		e.g. (x1,y1,x2,y2)
	crs : wfs20.crs.CRS
		Object containing projection information
	startindex : int, optional
		Starting index of the feature count

	Returns
	-------
	tuple
		Containing base url and the data in XML format
	"""

	base, _ = _BaseRequestURL(url)
	elem = _PostElement(WFS_NAMESPACE, "GetFeature")
	# set the data
	elem.FeatureType(featuretype)
	elem.BBOXPost(bbox, crs)
	if startindex is not None:
		elem.StartIndex(startindex)

	return base, elem.ToString()
