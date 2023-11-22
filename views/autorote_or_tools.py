from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

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
    formatted_time = f"{int(hours):02d}.{int(minutes):02d} {meridian}"
    return formatted_time


def create_return_formet(routes, times, data):
    result = {}
    start_time_list = []
    break_index = []
    if data['calculate_driver_starting_time'].lower() == "y":
        for i in routes:
            pass_time = -data["time_matrix"][int(i[0])][int(i[1])]
            start_time_format = format_time(data["hour_list"], pass_time)
            start_time_list.append(str(start_time_format))
    else:
        for i in routes:
            pass_time = 0
            start_time_format = format_time(data["hour_list"], pass_time)
            start_time_list.append(str(start_time_format))
    
    for j in range(len(routes)):
        total_time = 0
        bi = []
        for k in range(len(routes[j])):
            total_time = total_time + data["time_matrix"][int(routes[j][k])][int(routes[j][k-1])]
            if total_time > data["break_after_time"] and len(bi) == 0:
                bi.append(int(routes[j][k])) 
        if len(bi) == 0:
            break_index.append(None)
        else:
            break_index.append(bi[0])


    result["create_by"] = "Create By OR-Tools"
    result["result"] = [[int(value) for value in sublist] for sublist in routes]
    result["vehicles_total_time_list"] = times
    result["break_index"] = break_index
    result["vehicles_start_time_list"] = start_time_list
    return result

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    # print(f'Objective: {solution.ObjectiveValue()}')
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    
    routes = [None] * data['num_vehicles']
    distances = [None] * data['num_vehicles']
    times = [None] * data['num_vehicles']
    for vehicle_id in range(data['num_vehicles']):
        route_distance = 0
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        routes[vehicle_id]=[]
        distances[vehicle_id]=0
        times[vehicle_id]=0
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            routes[vehicle_id].append(format(manager.IndexToNode(index)))
            plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var),
                solution.Max(time_var))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        routes[vehicle_id].append(format(manager.IndexToNode(index)))
        distances[vehicle_id]=route_distance
        times[vehicle_id] = format(solution.Min(time_var))
        plan_output += 'Time of the route: {}min\n'.format(solution.Min(time_var))
        # print(plan_output)
        total_time += solution.Min(time_var)
    
    routes_updated = [sublist for sublist in routes if len(sublist) != 2]
    times_updated = [sublist for sublist in times if int(sublist) >= 10]
    result = create_return_formet(routes_updated, times_updated, data)
    return result


def AutorouteOR(data):
    if len(data) == 0:
        res ={"res": "no-data"}
        return res
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['time_matrix']), data['num_vehicles'], data['depot']
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = "Time"
    routing.AddDimension(
        transit_callback_index,
        0,  # allow waiting time
        data["working_hours"],  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time,
    )
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    depot_idx = data['depot']
    

    # Instantiate route start and end times to produce feasible times.
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.time_limit.seconds = 50
    search_parameters.solution_limit = 1000
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        res= print_solution(data, manager, routing, solution)
        return res
    
    res = {"res": "no-data"}
    return res