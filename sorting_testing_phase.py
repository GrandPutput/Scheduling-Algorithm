import random
import copy
    
class Employee:
    def __init__(self, name, availability, full_time=True):
        self.name = name
        self.availability = availability
        self.full_time = full_time
        self.assigned_shifts = 0

    def __repr__(self):
        availability_str = ', '.join([f'Day {day}: {shift}' for day, shift in self.availability])
        return f'{self.name} ({'Full-time' if self.full_time else 'Part-time'}) - Availabile Shifts: [{availability_str}] - Amount of Shifts: {self.assigned_shifts}'


def create_employees(names):
    employees = []
    for name in names:
        full_time = random.choice([True, False])
        availability = []
        if full_time:
            days = random.sample(range(1, 8), random.randint(5, 7))  # Random amout of days
        else:
            days = random.sample(range(1, 8), random.randint(1, 4))  # Random amount of days
        for day in days:
            shift = random.choice(['morning', 'night'])
            availability.append((day, shift))
        
        # Create Employee object
        employee = Employee(name, availability, full_time)
        employees.append(employee)
    return employees


def create_calendar(weeks=1, days_per_week=7):
    shifts = ['morning', 'night']
    calendar = {}

    for week in range(1, weeks + 1):
        week_name = f'Week {week}'
        calendar[week_name] = {}

        for day in range(1, days_per_week + 1):
            day_name = f'Day {day}'
            calendar[week_name][day_name] = {shift: {'needed': random.randint(3, 6), 'assigned': []} for shift in shifts}

    return calendar

def print_calendar(calendar):
    print('Shift Schedule\n' + '=' * 40)
    
    for week, days in calendar.items():
        print(f'\n{week}')
        print('-' * 40)
        
        for day, shifts in days.items():
            print(f'\n  {day}')
            print('    Shift     | Needed | Assigned Employees')
            print('    ----------|--------|-------------------')
            
            for shift_name, shift_info in shifts.items():
                needed = shift_info['needed']
                assigned = ', '.join(shift_info['assigned']) if shift_info['assigned'] else 'None'
                
                print(f'    {shift_name.capitalize():<10} | {needed:<6} | {assigned}')
        print('-' * 40)

# Sorting Algorithms for testing

# Greedy Algorithm
def fill_calendar_greedy(calendar, employees):
    for week, days in calendar.items():
        for day, shifts in days.items():
            for shift_name, shift_info in shifts.items():
                needed = shift_info['needed']

                # Find available employees for this shift
                available_employees = [
                    emp for emp in employees 
                    if (int(day.split()[1]), shift_name) in emp.availability and emp.name not in shift_info['assigned']
                ]

                # Randomize lists so testing is more random
                random.shuffle(available_employees)

                # Fill the shift with available employees
                for emp in available_employees[:needed]:
                    shift_info['assigned'].append(emp.name)
                    # # Mark the employee as unavailable once assined that shift
                    emp.availability.remove((int(day.split()[1]), shift_name))
                    emp.assigned_shifts += 1
                    
                # If not enough employees were assigned, mark as urgent
                # Marks entire shift as urgent remove if a bad idea
                '''if len(shift_info['assigned']) < needed:
                    shift_info['assigned'] = ['Urgent']'''
                # Marks only need spots as urgent
                if len(shift_info['assigned']) < needed:
                    shift_info['assigned'].append('urgent')
                    
    return calendar

# EDF Algorithm
def fill_calendar_edf(calendar, employees):
    for week, days in calendar.items():
        for day, shifts in days.items():
            for shift_name, shift_info in shifts.items():
                needed = shift_info['needed']
                assigned_count = 0

                # Sort employees based on availability for the current shift
                available_employees = [
                    employee for employee in employees if (int(day.split()[1]), shift_name) in employee.availability
                ]

                # Randomize lists so testing is more random
                random.shuffle(available_employees)

                # Assign employees until the needed count is met
                for employee in available_employees:
                    if assigned_count < needed and employee.name not in shift_info['assigned']:
                        shift_info['assigned'].append(employee.name)
                        assigned_count += 1
                        # Mark the employee as unavailable once assined that shift
                        employee.availability.remove((int(day.split()[1]), shift_name))
                        employee.assigned_shifts += 1

                # Marks empty shifts as urgent
                if len(shift_info['assigned']) < needed:
                    shift_info['assigned'].append('urgent')

    return calendar

# Round Robin Algorithm
def fill_calendar_round_robin(calendar, employees):    
    for week, days in calendar.items():
        for day, shifts in days.items():
            for shift_name, shift_info in shifts.items():
                needed = shift_info['needed']
                assigned_count = 0
                index = 0
                
                available_employees = [
                    employee for employee in employees if (int(day.split()[1]), shift_name) in employee.availability
                ]

                # Randomize lists so testing is more random
                random.shuffle(available_employees)

                # Round robin sorting
                while assigned_count < needed and available_employees:
                    employee = available_employees[index % len(available_employees)]
                    
                    # Check if the employee is available for this shift
                    if (int(day.split()[1]), shift_name) in employee.availability and employee.name not in shift_info['assigned']:
                        shift_info['assigned'].append(employee.name)
                        assigned_count += 1
                        # Mark the employee as unavailable once assined that shift
                        employee.availability.remove((int(day.split()[1]), shift_name))
                        employee.assigned_shifts += 1
                    
                    index += 1
                    
                    # Check if all employees have been considered
                    if index >= len(available_employees) and assigned_count < needed:
                        # If unable to fill completely, mark the rest as urgent
                        shift_info['assigned'].append('Urgent')
                        break
                    
    return calendar




# Test Names
# Mutiple samples created fo future testing
employee_names1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J' , 'K', 'L', 'M', 'N', 'O', 'P', 'q', 'r', 's', 't', 'u', 'v']
employee_names2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J' , 'K', 'L', 'M', 'N', 'O', 'P']
employee_names3 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


# Create Random Availabilities
employees1_test1 = create_employees(employee_names1)
employees2_test1 = copy.deepcopy(employees1_test1)
employees3_test1 = copy.deepcopy(employees1_test1)
for i in employees1_test1:
    print(i)
print('---------------')

# Method Calls
calendar1 = create_calendar()
calendar2 = copy.deepcopy(calendar1)  # Clone 1
calendar3 = copy.deepcopy(calendar1)  # Clone 2

# Greedy Test
filled_calendar1 = fill_calendar_greedy(calendar1, employees1_test1)
print('Filled Calendar 1 (Greedy):')
print_calendar(filled_calendar1)

# Round Robin Test
filled_calendar2 = fill_calendar_round_robin(calendar2, employees2_test1)
print('Filled Calendar 2 (Round Robin):')
print_calendar(filled_calendar2)

# EDF Test
filled_calendar3 = fill_calendar_edf(calendar3, employees3_test1)
print('Filled Calendar 3 (EDF):')
print_calendar(filled_calendar3)

# Re-output employee data to compare shift data
print('Greedy')
for i in employees1_test1:
    print(f'{i}')
print('---------------')

print('Round Robin')
for i in employees2_test1:
    print(f'{i}')
print('---------------')

print('EDF')
for i in employees3_test1:
    print(f'{i}')
print('---------------')