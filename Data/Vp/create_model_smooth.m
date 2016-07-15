function create_model_smooth(Vp, input_model)
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

for i = 1 : NX,
    Vp0 = Vp(:, i);
    Vp1 = Vp0;
    Vp1(200:700) = interp1([z0(200); z0(700)], [Vp0(200); Vp0(700)], z0(200:700), 'spline');
    Vp(:, i) = Vp1;
end

Vs = (1.0 / sqrt(3)) * Vp; % Poisson solid
Rho = 1000.0 * 0.31 * (Vp .^ 0.25); % Gardner relationship

% reshaping the model for the output file
Vp = reshape(Vp, [NZ * NX, 1]);
Vs = reshape(Vs, [NZ * NX, 1]);
Rho = reshape(Rho, [NZ * NX, 1]);
x = reshape(x, [NZ * NX, 1]);
z = reshape(z, [NZ * NX, 1]);
M = [x z Rho Vp Vs];

% write file
dlmwrite(input_model, M, 'delimiter', ' ', 'precision', '%15.4f');

