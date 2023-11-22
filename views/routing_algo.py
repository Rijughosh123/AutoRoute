# This function use for check the time. you pass the limit.
def check_time_back_to_depot(total_time, time_matrix, depot, target_index, working_hours):
    check_time = total_time + time_matrix[target_index][depot]
    if check_time > working_hours:
        return False
    return True

# if you pass the hour_list(like 9am to 10pm), and time in minutes then it's return the time in time_format(like am and pm)
def format_time(hour_list_minutes, start_time_minutes):
    start_time = hour_list_minutes[0] + start_time_minutes
    hours = start_time // 60
    minutes = start_time % 60
    if hours >= 12:
        meridian = 'pm'
        if hours > 12:
            hours -= 12
    else:
        meridian = 'am'
        if hours == 0:
            hours = 12
    formatted_time = f"{int(hours):02d}.{int(minutes):02d}{meridian}"
    return formatted_time

def split_tuples(sorted_list):
    first_elements = [item[0] for item in sorted_list]
    second_elements = [item[1] for item in sorted_list]
    return [first_elements, second_elements]

# if you pass the time_window, and distance_list(one location to all location distance list) and unique time slote 
# then it's sort the distance with unique time slot
def sort_elements_by_time_slot(dis_list, unique_time_slote, time_window):
    time_slot_dict = {slot: [] for slot in unique_time_slote}
    for sh in range(len(dis_list)):
        time_slot = time_window[sh][0]
        if time_slot in time_slot_dict:
            time_slot_dict[time_slot].append((dis_list[sh], sh))  # Store both value and index
    sorted_list = [item for slot in unique_time_slote for item in sorted(time_slot_dict[slot])] 
    sort_list_final = split_tuples(sorted_list)
    return sort_list_final


# If you pass the time windows then it's return the unique time slote
def extract_unique_time_slots(time_window):
    time_slots = set()
    for slot in time_window:
        start_time, end_time = slot
        time_slots.add(start_time)
        time_slots.add(end_time)

    unique_time_slots = sorted(time_slots)
    return unique_time_slots


# If provide the proper data and pass the target node then it's return the nearest location where you can 
# rech with time. which time mention in time_window.
# fix_data means this data not be change when you call the function for a solution.
# update_data means all time change the data when you call the function for a solution.
def find_next_node(fix_data, update_data):
    nocount_list = update_data["nocount_list"]
    # target_node to all location distance list
    dis_list = fix_data["time_matrix"][update_data["target_node"]]
    select_node = None

    sorted_list = dis_list.copy()
    sorted_list.sort()

    unique_sort = sort_elements_by_time_slot(dis_list, fix_data["unique_time_slot"], fix_data["time_window"])
    if fix_data["depot"] == update_data["target_node"]:
        for i in range(len(unique_sort[0])):
            for j in range(len(dis_list)):
                if j not in nocount_list:
                    if dis_list[j] == unique_sort[0][i] and unique_sort[1][i] not in nocount_list:
                        select_node = unique_sort[1][i]
                        distance = dis_list[select_node]
                        # print(select_node, distance)
                        now_select_node = select_node
                        now_total_time = update_data["total_time"] + distance
                        now_rech_time = fix_data["time_window"][select_node][0]
                        now_route = update_data["route"]+[select_node]
                        now_nocount_list = update_data["nocount_list"]+[select_node]
                        return_value = {"selected_node":now_select_node, "total_time": now_total_time, "rech_time": now_rech_time, "route": now_route, "nocount_list":now_nocount_list, "break_index": None}
                        return return_value
        return_value = {"selected_node":select_node, "total_time": update_data["total_time"], "rech_time": update_data["rech_time"], "route": update_data["route"], "nocount_list": update_data["nocount_list"], "break_index": None}
        return return_value
    
    for i in range(len(sorted_list)):
        for j in range(len(dis_list)):
            if j not in nocount_list:
                if dis_list[j] == sorted_list[i]:
                    this_index_rech_time = update_data["rech_time"] + dis_list[j]
                    this_index_total_time = update_data["total_time"] + dis_list[j]
                    now_break_index = update_data["break_index"]
                    if update_data["total_time"] > fix_data["break_after_time"] and update_data["break_index"] == None:
                        this_index_rech_time = this_index_rech_time + fix_data["break_time"]
                        this_index_total_time = this_index_total_time + fix_data["break_time"]
                        now_break_index = update_data["route"][-1]
                    if fix_data["time_window"][j][0] <= this_index_rech_time <= fix_data["time_window"][j][1]:
                        check = check_time_back_to_depot(this_index_total_time, fix_data["time_matrix"], fix_data["depot"], j, fix_data["working_hours"])
                        if check == True:
                            now_select_node = j
                            now_total_time = this_index_total_time
                            now_rech_time = this_index_rech_time
                            now_route = update_data["route"]+[j]
                            now_nocount_list = update_data["nocount_list"]+[j]
                            return_value = {"selected_node":now_select_node, "total_time": now_total_time, "rech_time": now_rech_time, "route": now_route, "nocount_list":now_nocount_list, "break_index": now_break_index}
                            return return_value
                    
    return_value = {"selected_node":select_node, "total_time": update_data["total_time"], "rech_time": update_data["rech_time"], "route": update_data["route"], "nocount_list": update_data["nocount_list"], "break_index": update_data["break_index"]}
    return return_value

def check_nearest_location(fix_data, update_data):
    nocount_list = update_data["nocount_list"]
    dis_list = fix_data["time_matrix"][update_data["target_node"]]
    select_node = None
    sorted_list = dis_list.copy()
    sorted_list.sort()
    
    for i in range(len(sorted_list)):
        for j in range(len(dis_list)):
            if j not in nocount_list:
                if dis_list[j] == sorted_list[i]:
                    now_total_time = update_data["total_time"] + dis_list[j]
                    check = check_time_back_to_depot(now_total_time, fix_data["time_matrix"], fix_data["depot"], j, fix_data["working_hours"])
                    if check == True:
                        nearest_node = j
                        now_reach_min_time = fix_data["time_window"][j][0]
                        now_route = update_data["route"] + [j]
                        now_nocount_list = update_data["nocount_list"] + [j]
                        return_value = {"selected_node":nearest_node, "total_time": now_total_time, "rech_time": now_reach_min_time, "route": now_route, "nocount_list": now_nocount_list, "break_index": None}
                        return return_value
                    
    return_value = {"selected_node":select_node, "total_time": update_data["total_time"], "rech_time": update_data["rech_time"], "route": update_data["route"], "nocount_list": update_data["nocount_list"], "break_index": None}
    return return_value


def AutoRouteAlgo(data):
    start_time_per_vehicles = []
    vehicles_total_time = []
    routes = []
    vehicles_break_time_index_list = []
    hour_list = data['hour_list']
    num_vehicles = data['num_vehicles']
    time_matrix= data['time_matrix']
    time_window = data['time_windows']
    depot = data['depot']
    unique_time_slot = extract_unique_time_slots(time_window)
    break_time = data['break_time']
    break_after_time = data['break_after_time']
    if isinstance(data['working_hours'], str):
        working_hours_arr = data['working_hours'].split(':')
        working_hours = int(working_hours_arr[0]) * 60 + int(working_hours_arr[1]) + int(break_time)
    else:
        working_hours = data['working_hours'] + int(break_time)   
    nocount_list = [depot]

    fix_data = {"time_matrix": time_matrix, "time_window": time_window, "depot":depot, "working_hours": working_hours, "break_time": break_time, "break_after_time":break_after_time,"unique_time_slot": unique_time_slot }
    
    for vehicles in range(num_vehicles):
        update_data = {"target_node":depot, "total_time": 0, "rech_time": 0, "route": [depot], "nocount_list": nocount_list,"break_index": None}
        selected_data = find_next_node(fix_data, update_data)
        if selected_data["selected_node"] == None:
            break
        #update pass data
        update_data["target_node"] = selected_data["selected_node"]
        update_data["total_time"] = selected_data["total_time"]
        update_data["rech_time"] = selected_data["rech_time"]
        update_data["route"] = selected_data["route"]
        update_data["break_index"] = selected_data["break_index"]
        nocount_list = selected_data["nocount_list"]
        update_data["nocount_list"] = nocount_list

        
        # vehicles start_time
        start_time = selected_data["rech_time"] - selected_data["total_time"]
        vehicles_start_time = format_time(hour_list, start_time)
        start_time_per_vehicles.append(vehicles_start_time)

        check = 0
        while check == 0:
            selected_data = find_next_node(fix_data, update_data)
            if selected_data['selected_node'] == None and (selected_data["total_time"]+time_matrix[selected_data["route"][-1]][depot]) < 450:
                record_select_data = selected_data
                start_time = selected_data["rech_time"] - selected_data["total_time"]
                selected_data["target_node"] = selected_data["route"][-1]
                record_rech_time = selected_data["rech_time"]
                selected_data = check_nearest_location(fix_data, selected_data)
                if record_rech_time < selected_data["rech_time"]:
                    if selected_data['selected_node'] != None:
                        start_time = selected_data["rech_time"] - selected_data["total_time"]
                        vehicles_start_time = format_time(hour_list, start_time)
                        start_time_per_vehicles[-1] = vehicles_start_time
                else:
                    selected_data = record_select_data
            if selected_data['selected_node'] != None:
                update_data["target_node"] = selected_data["selected_node"]
                update_data["total_time"] = selected_data["total_time"]
                update_data["rech_time"] = selected_data["rech_time"]
                update_data["route"] = selected_data["route"]
                update_data["break_index"] = selected_data["break_index"]
                nocount_list = selected_data["nocount_list"]
                update_data["nocount_list"] = nocount_list
            else:
                
                final_total_time = selected_data["total_time"]+time_matrix[selected_data["route"][-1]][depot]
                final_route = selected_data["route"]+[depot]
                # append vehicles total_time
                vehicles_total_time.append(final_total_time)
                #append vehicles route
                routes.append(final_route)
                # append vehicles break time index
                vehicles_break_time_index_list.append(selected_data["break_index"])
                check = 1


    result = {
        "create_by" : "Create By Time-window Algo",
        "result": routes,
        "vehicles_total_time_list": vehicles_total_time,
        "vehicles_start_time_list": start_time_per_vehicles,
        "break_index": vehicles_break_time_index_list,
       
    }
    return result

