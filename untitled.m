% Solar Panel Parameters
P_max = 300; % Nominal power in Watts
I_STC = 1000; % Light intensity at STC in W/m^2
panel_efficiency = 0.18; % Panel efficiency (if given)
panel_area = 1.6; % Panel area in m^2 (if needed)

% Measured Data (example data)
I = [500, 600, 700, 800, 900, 1000, 950, 850, 750, 600]; % Light intensity in W/m^2
dt = 1; % Time interval in hours (can be minutes, but ensure units match)

% Calculate Power Output
P = P_max * (I / I_STC); % Power generated at each time interval

% Optional: If efficiency is provided, use this instead:
% P = panel_efficiency * panel_area * I;

% Calculate Energy Output
E = sum(P) * dt; % Total energy in Watt-hours (Wh)

% Display Results
disp(['Total Energy Output: ', num2str(E), ' Wh']);

% Plot Results
time = 1:length(I); % Assuming time intervals are uniform
figure;
plot(time, P, '-o');
xlabel('Time (hours)');
ylabel('Power Output (W)');
title('Solar Panel Power Output');
grid on;
