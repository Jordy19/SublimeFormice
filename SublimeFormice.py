import sublime, sublime_plugin, os, re, threading
from os.path import basename
import json
import sys
#
# Method Class
#
class Funct:
	name = ""
	arguments = ""
	description = ""
	def __init__(self, function_name, language_string):
		self.name        = function_name
		self.arguments   = str(language_string["args"])
		self.description = language_string["description"]
	def name(self):
		return self.name

	def arguments(self):
		return self.arguments

	def description(self):
		return self.description
#
# TFM helpers
#
class TFM:
	transformice_func     = []
	transformice_func_lst = []
	transformice_obj      = []
	transformice_obj_lst  = []
	transformice_methods  = []
	settings              = None
	transformice_api_data = None
	def __init__(self):
		try:
			self.settings = sublime.load_settings("SublimeFormice.sublime-setting")
			self.transformice_api_data = sublime.load_settings(self.settings.get("language") + "-SublimeFormice.sublime-language")		
		except: pass
		if self.transformice_api_data != "":
			list_of_func = get_json(self.transformice_api_data.get("functions"))
			for function_name in list_of_func:
				funcType = list_of_func[function_name]
				try:
					list_of_func[function_name]["type"]
				except KeyError:
					print("Unknown type: %s" % list_of_func[function_name])
				else:
					if list_of_func[function_name]["type"] == "function":
						self.add_function(function_name, list_of_func[function_name])		
					if list_of_func[function_name]["type"] == "method":
						self.add_method(function_name, list_of_func[function_name])	

	def add_function(self, function_name, language_string):
		self.transformice_func.append( Funct( function_name, language_string ) )	

	def add_object(self, function_name, language_string):
		self.transformice_obj.append( Obj( function_name, language_string ) )

	def add_method(self, function_name, language_string):
		self.transformice_methods.append( Funct( function_name, language_string ) )


	def get_autocomplete(self, word):
		autocomplete_list = []

		for function_name in self.transformice_func:
			if word in function_name.name:
				method_str_to_append = function_name.name + '(' + function_name.arguments+ ')'
				method_file_location = function_name.description;
				autocomplete_list.append(("{0:70}\t{0}".format(method_str_to_append, method_file_location),method_str_to_append)) 		
		for function_name in self.transformice_methods:
			if word in function_name.name:
				method_str_to_append = function_name.name
				method_file_location = function_name.description
				autocomplete_list.append(("{0:70}\t{1}".format(method_str_to_append, method_file_location),method_str_to_append)) 		
													
		return autocomplete_list	

def is_lua(filename):
	return '.lua' in filename

def get_json(s_string):
	return json.loads(json.dumps(s_string))


class SublimeFormiceEvent(TFM, sublime_plugin.EventListener):

	def on_query_completions(self, view, prefix, locations):
		curr_file = view.file_name()
		completions = []
		if is_lua(curr_file):
			return self.get_autocomplete(prefix)
			completions.sort()
		return (completions,sublime.INHIBIT_EXPLICIT_COMPLETIONS)