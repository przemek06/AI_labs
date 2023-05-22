% devices
system(windows).
computer(hp_laptop, linux).
computer(dell_laptop, windows).
device(hp_laptop).
device(dell_laptop).
device(printer).
device(power_supply).

% elements

power_switch(btn_1).
usb_cable(cable_1).
power_cable(cable_2).
size(a3).
size(a4).
size(a5).

% components of the printer

component(printer, output_cover).
switch(printer, btn_1).
light(printer, alarm_light).
page_size(printer, a4).

% connected to the printer
connected(printer, cable_2).
connected(power_supply, cable_2).
connected(printer, cable_1).

% state
switched(btn_1, on).

% rules
device_switched_on(A) :- switch(A, B), switched(B, on), power_switch(B).
device_conntected_to_power(A) :- connected(A, B), power_cable(B), connected(power_supply, B), device(A).
usb_connections_possible(A, B, C) :- connected(A, C), usb_cable(C), device(A), device(B).
accepted_system(A) :- computer(A, B), system(B).
communication_available(A, B, C) :- accepted_system(B), usb_connections_possible(A, B, C).
powered(A) :- device_conntected_to_power(A), device_switched_on(A).
light_switched(A, B, C) :- C =\= -1, light(A, B).

% Problem 1: catridge holder is not moving 
% A - alarm code
% B - how long paper output cover has been left open (in minutes)
% C - has the printer been printing for a long time

fix_power(A) :- not(device_conntected_to_power(A)),  write('The device is not connected to the power source.').
fix_power(A) :- not(device_switched_on(A)),  write('The switch is off.').

fix_catridge_holder(_, _, _) :- not(powered(printer)), fix_power(printer).
fix_catridge_holder(A, _, _) :- light_switched(printer, alarm_light , A), write('Check alarm error code').
fix_catridge_holder(_, B, _) :- B >= 10; not(component(printer, output_cover)), write('Close and open the paper output cover').
fix_catridge_holder(_, _, C) :- C =:= 1, write('Let the printer cool down').

% Problem 2: Page size is wrong
% A - error code
% B - page size

fix_page_size(A, _) :- not(light_switched(printer, alarm_light, A)), write('Page size is fine').
fix_page_size(_, B) :- not(size(B)), write('Page size is not recognized'). 
fix_page_size(A, B) :- A=:=103, not(page_size(printer, B)), write("Configure the printer's page size").
fix_page_size(A, _) :- A=\=103, write('Page size is not a problem').

% Problem 3: Communication error
% A - computer connected to the usb cable
% B - cable used for connection

fix_communication_error(A, B) :- communication_available(printer, A, B), write('There is no cummunication problems.').
fix_communication_error(A, B) :- not(usb_connections_possible(printer, A, B)), write('Devices are not properly connected').
fix_communication_error(A, _) :- not(accepted_system(A)), write('System is not accepted by this printer').

