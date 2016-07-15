function create_model(Vp, input_model, bathy)
% create full x,z,vp,vs,rho model from the binary P-wave velocity file (from SEGY data)

    NX = 3820; % number of data in x direction
    NZ = 1200; % number of data in z direction
    dx = 12.5; % spacing in x direction
    dz =  5.0; % spacing in z direction

% read file
fp = fopen(Vp, 'rb');
Vp = fread(fp, [NZ, NX], 'float32');

% defining the matrix model
x0 = [0 : dx : (dx * (NX - 1))];
z0 = transpose([(dz * (NZ - 1)) : (-dz) : 0]);

x = zeros(NZ, NX);
for i = 1 : NZ,
    x(i, :) = x0;
end
z = zeros(NZ, NX);
for i = 1 : NX,
    z(:, i) = z0;
end
Vs = (1.0 / sqrt(3)) * Vp; % Poisson solid
Rho = 1000.0 * 0.31 * (Vp .^ 0.25); % Gardner relationship

% finding the bathymetry
xb = x(1, :);
zb = zeros(1, NX);
for i = 1 : NX,
    Vp0 = Vp(:, i);    
    sea = find(Vp0 < 1511.0);
    zs = z(sea, i);
    zb(i) = min(zs);
end

% reshaping the model for the output file
Vp = reshape(Vp, [NZ * NX, 1]);
Vs = reshape(Vs, [NZ * NX, 1]);
Rho = reshape(Rho, [NZ * NX, 1]);
x = reshape(x, [NZ * NX, 1]);
z = reshape(z, [NZ * NX, 1]);
M = [x z Rho Vp Vs];
B = [transpose(xb) transpose(zb)];

% write file
dlmwrite(input_model, M, 'delimiter', ' ', 'precision', '%15.4f');
dlmwrite(bathy, B, 'delimiter', ' ', 'precision', '%15.4f');

