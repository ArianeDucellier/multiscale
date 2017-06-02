function create_source(input_source, output_source, dt, nt)
% interpolate source function to get the selected time step and number of steps

    dt0 = (2.0 / 3.0) * 0.001;

% input source
temp1 = dlmread(input_source);
s1 = temp1(:, 1);
nt0 = size(temp1, 1);
t1 = transpose(linspace(0.0, (nt0 - 1) * dt0, nt0));

% interpolation
t2 = transpose(linspace(0.0, (nt - 1) * dt, nt));
s2 = interp1(t1, s1, t2, 'spline');

% last points
s2(t2 > (nt0 - 1) * dt0) = 0.0;

source = [t2 s2];
% save  
dlmwrite(output_source, source, 'delimiter', ' ', 'precision', '%20.10f %20.10f');

