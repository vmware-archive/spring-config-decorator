import os
import sys
import json
import urllib2
import base64

def main():
	appinfo = get_application_info()
	service = find_spring_config_service(appinfo)
	if service != None:
		get_spring_cloud_config(service, appinfo)

def detect():
	appinfo = get_application_info()
	service = find_spring_config_service(appinfo)
	if service == None:
		sys.exit(1)
	print 'spring-config'

# Get Application Info
#
# Certain information about the application is used in
# the query to the configuration servers, to allow them
# to return config values dependent on the application
# instance deployment
#
def get_application_info():
	appinfo = {}
	vcap_application = json.loads(os.getenv('VCAP_APPLICATION', '{}'))
	appinfo['name'] = vcap_application.get('application_name')
	if appinfo['name'] == None:
		print >> sys.stderr, "VCAP_APPLICATION must specify application_name"
		sys.exit(1)
	appinfo['profile'] = vcap_application.get('space_name', 'default')
	return appinfo

# Find bound configuration service
# 
# We only read configuration from bound config services that
# are appropriately tagged. And since, for user-provided services,
# tags can only be set inside the credentials dict, not in the
# top-level one, we check for tags in both places.
#
def find_spring_config_service(appinfo):
	vcap_services = json.loads(os.getenv('VCAP_SERVICES', '{}'))
	for service in vcap_services:
		service_instances = vcap_services[service]
		for instance in service_instances:
			tags = instance.get('tags', []) + instance.get('credentials',{}).get('tags',[])
			if 'spring-cloud' in tags and 'configuration' in tags:
				return instance
		return None

def get_access_token(credentials):
	client_id = credentials.get('client_id','')
	client_secret = credentials.get('client_secret','')
	access_token_uri = credentials.get('access_token_uri')
	if access_token_uri is None:
		return None
	req = urllib2.Request(access_token_uri)
	req.add_header('Authorization', 'Basic ' + base64.b64encode(client_id + ":" + client_secret))
	body = "grant_type=client_credentials"
	response = json.load(urllib2.urlopen(req, data=body))
	access_token = response.get('access_token')
	token_type = response.get('token_type')
	return token_type + " " + access_token

def get_spring_cloud_config(service, appinfo):
	print >> sys.stderr, "spring-cloud-config:"
	json.dump(service, sys.stderr, indent=4)
	print >> sys.stderr
	credentials = service.get('credentials', {})
	access_token = get_access_token(credentials)
	uri = credentials.get('uri')
	if uri is None:
		print >> sys.stderr, "services of type spring-config-server must specify a uri"
		return
	uri += "/" + appinfo['name']
	uri += "/" + appinfo['profile']
	try:
		print >> sys.stderr, "GET", uri
		req = urllib2.Request(uri)
		if access_token is not None:
			req.add_header('Authorization', access_token)
		config = json.load(urllib2.urlopen(req))
	except urllib2.URLError as err:
		print >> sys.stderr, err
		return
	json.dump(config, sys.stderr, indent=4)
	print >> sys.stderr
	#
	# We iterate through the list in reversed order, as it looks like the
	# Spring Cloud Config Server always returns the most specific context
	# first. So this order leads to the correct merge result if the same
	# property appears in multiple contexts.
	#
	for sources in reversed(config.get('propertySources', [])):
		for key, value in sources.get('source', {}).items():
			write_config_property(service, key, value)

# Write Configuration
#
# Regardless of the source, configuration properties can be added to a
# number of destinations. Which property goes where will ultimately be
# determined by rules that can be configured for each application.
#
def write_config_property(service, key, value):
	#
	# Ultimately, we want to allow configurable rules to drive the
	# destinations of our properties. For now, we simply put them
	# everywhere.
	#
	add_environment_variable(key, value)

def add_environment_variable(key, value):
	#
	# There's no point sticking the property into our own environment
	# since we are a child of the process we want to affect. So instead,
	# for environment variables, we depend on our caller to set and
	# export the real environment variables. We simply place them on our
	# stdout for the caller to consume.
	#
	print key.replace('.', '_'), value

if __name__ == "__main__":
	main()
