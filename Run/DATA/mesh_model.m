function mesh_model(input_model, temp_model, output_model)
% mesh input model to SPECFEM model on gll grids
% any questions, contact yanhuay@princeton.edu

    NX = 1910;       % number of spectral elements in x
    NZ = 240;        % number of spectral elements in z
    GLLX = 5;        % number of gll points in x
    GLLZ = 5;        % numner of gll points in z

% input template
temp0 = dlmread(temp_model);
NT = size(temp0, 1);
NZT = NZ * GLLZ;
NXT = ceil(NT / NZT);
index = temp0(:, 1);
x0 = temp0(:, 2);
z0 = temp0(:, 3);
Vrho0 = temp0(:, 4);
Vp0 = temp0(:, 5);
Vs0 = temp0(:, 6);
[X0, Z0] = meshgrid([min(x0) : (max(x0) - min(x0)) / (NXT - 1) : max(x0)], [min(z0) : (max(z0) - min(z0)) / (NZT - 1) : max(z0)]);
 
% input models for meshing
temp1 = dlmread(input_model);
x1 = temp1(:, 1);
z1 = temp1(:, 2);
Vrho1 = temp1(:, 3);
Vp1 = temp1(:, 4);
Vs1 = temp1(:, 5);
% map model from (x1 z1) to (X0 Z0)
V1 = griddata(x1, z1, Vrho1, X0, Z0, 'nearest');
V2 = griddata(x1, z1, Vp1, X0, Z0, 'nearest');
V3 = griddata(x1, z1, Vs1, X0, Z0, 'nearest');
% interp from (X0 Z0) to (x0 z0)
VV1 = interp2(X0, Z0, V1, x0, z0, 'nearest');
VV2 = interp2(X0, Z0, V2, x0, z0, 'nearest');
VV3 = interp2(X0, Z0, V3, x0, z0, 'nearest');

sea = find(Vs0 < 1.0);
VV1(sea) = 1025.0;
VV2(sea) = 1510.0;
VV3(sea) = 0.0;

% full elastic case
%VV3(sea) = 1510.0 / sqrt(3.0);

% acoustic case
%VV3(:) = 0.0;

model = [x0 x0 z0 VV1 VV2 VV3];

% save  
dlmwrite(output_model, model, 'delimiter', ' ', 'precision', '%20.10e %20.10e %20.10e %20.10e %20.10e %20.10e');

