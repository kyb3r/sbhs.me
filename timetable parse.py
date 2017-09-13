import json
def edit_timetable(default_periods,class_variation,room_variation):
	for changed_class in class_variation:
		period = int(changed_class[2])
		default_periods[period] = changed_class
	for changed_room in room_variation:
		period = int(changed_room[0])
		default_periods[period][1] = str(default_periods[period][1]) + ' room change to: ' + changed_room[2]
	return default_periods
	
def parse_timetable_json(json_file):
	information = json.dumps(json_file)
	bell_times = information['bells']
	class_variation = information['classVariations']
	room_variation = information['roomVariation']
	default_periods = information['timetable']['timetable']['periods']
	final_periods = edit_timetable(default_periods,class_variation,room_variation)
