//// Mesh MOSFET BG 2D : v17.1
//// 1) Optimised structure Back Gate MOSFET; 2) no S/D doping junctions
//// 3) Channel thickness = 10 nm; 4) Oxide thickness = 20 nm;
//// 5) Lch = 400nm


contact_width =    500e-7; // 500nm
channel_length =   400e-7;
device_width =     2*contact_width + channel_length;
gate_width =       device_width;
device_thickness =     10e-7;

cd = device_thickness;

diffusion_width =  0.4; // this parameter might be unused

air_thickness =        1e-7;
oxide_thickness =      20e-7;
gate_thickness =       20e-7;
diffusion_thickness =  1e-6;


//////////////////////////////////


y_channel_spacing =      1e-7;
y_diffusion_spacing =    1e-6;
y_gate_top_spacing =     1e-8;
y_gate_mid_spacing =     gate_thickness * 0.25;
y_gate_bot_spacing =     1e-8;
y_oxide_mid_spacing =    oxide_thickness * 0.25;
x_channel_spacing =    1e-6;
x_diffusion_spacing =  1e-5;
max_y_spacing =        1e-4;
max_x_spacing =        1e-2;
y_bulk_mid_spacing =  device_thickness * 0.25;
y_bulk_bottom_spacing =  1e-8;

x_bulk_left =    0.0;
x_bulk_right =   x_bulk_left + device_width;
x_center =       0.5 * (x_bulk_left + x_bulk_right);
x_gate_left =    x_center - 0.5 * (gate_width);
x_gate_right =   x_center + 0.5 * (gate_width);
x_channel_left =    x_center - 0.5 * (channel_length); // MM: decoupling back gate from channel length
x_channel_right =   x_center + 0.5 * (channel_length); // MM: decoupling back gate from channel length
x_device_left =  x_bulk_left - air_thickness;
x_device_right = x_bulk_right + air_thickness;

y_bulk_top =       0.0;
y_oxide_top =      y_bulk_top - oxide_thickness;
y_oxide_mid =      0.5 * (y_oxide_top + y_bulk_top);
y_gate_top =       y_oxide_top - gate_thickness;
y_gate_mid =       0.5 * (y_gate_top + y_oxide_top);
y_device_top =     y_gate_top - air_thickness;
y_bulk_bottom =    y_bulk_top + device_thickness;
y_bulk_mid =       0.5 * (y_bulk_top + y_bulk_bottom);
y_device_bottom =  y_bulk_bottom + air_thickness;
// y_diffusion =      y_bulk_top + diffusion_thickness;
y_diffusion =      y_bulk_bottom - diffusion_thickness; // MM: for S/D at the top


//////////////////////////////////


//// Bulk
// Point(1) = {x_bulk_left, y_bulk_top, 0, x_diffusion_spacing}; // MM: for extended back gate
Point(3) = {x_gate_left, y_bulk_top, 0, x_diffusion_spacing};
Point(4) = {x_gate_right, y_bulk_top, 0, x_diffusion_spacing};
// Point(6) = {x_bulk_right, y_bulk_top, 0, x_diffusion_spacing}; // MM: for extended back gate
Point(7) = {x_bulk_right, y_bulk_bottom, 0, x_diffusion_spacing};
Point(8) = {x_bulk_left, y_bulk_bottom,0, x_diffusion_spacing};

Point(9) = {x_gate_left, y_gate_top, 0, x_diffusion_spacing};
Point(10) = {x_gate_right, y_gate_top, 0, x_diffusion_spacing};
Point(11) = {x_gate_right, y_oxide_top, 0, x_diffusion_spacing};
Point(12) = {x_gate_left, y_oxide_top, 0, x_diffusion_spacing};

Point(15) = {x_gate_right, y_bulk_top, 0, x_diffusion_spacing};
Point(16) = {x_gate_left, y_bulk_top, 0, x_diffusion_spacing};

//// Bulk for S/D at the top
Point(17) = {x_channel_right, y_bulk_bottom, 0, x_diffusion_spacing}; // MM
Point(18) = {x_channel_left, y_bulk_bottom, 0, x_diffusion_spacing}; // MM


//////////////////////////////////


Line(1) = {8, 18}; // MM: for S/D at the top
Line(16) = {18, 17}; // MM: for S/D at the top
Line(17) = {17, 7}; // MM: for S/D at the top
Line(2) = {7, 4};
// Line(3) = {6, 4}; // MM: for extended back gate
Line(4) = {4, 3};
// Line(5) = {3, 1};  // MM: for extended back gate
Line(6) = {3, 8};
Line Loop(7) = {1, 16, 17, 2, 4, 6}; // MM: for S/D at the top
Plane Surface(8) = {7};
Line(9) = {10, 11};
// Line(10) = {12, 12}; // not used
Line(11) = {11, 12};
Line(12) = {9, 12};
Line(13) = {9, 10};
Line(14) = {11, 4};
Line(15) = {3, 12};
Line Loop(16) = {13, 9, 11, -12};
Plane Surface(17) = {16};
Line Loop(18) = {15, -11, 14, 4};
Plane Surface(19) = {18};


//////////////////////////////////


// Channel-to-Air interface
Field[5] = Distance;
Field[5].CurvesList = {16};
Field[5].Sampling = 1000;

Field[7] = Threshold;
Field[7].InField = 5;
Field[7].SizeMin = cd/15;
Field[7].SizeMax = cd/2;
Field[7].DistMin = cd/10;
Field[7].DistMax = cd;


// SizeMax -                     /------------------
//                              /
//                             /
//                            /
// SizeMin -o----------------/
//          |                |    |
//        Point         DistMin  DistMax


//////////////////////////////////


// S/D interface (OFF)
Field[3] = Attractor;
Field[3].EdgesList = {1,17}; // {1,16,17};
Field[4] = Threshold;
Field[4].IField = 3;
Field[4].LcMin = cd/10;
Field[4].LcMax = cd;
Field[4].DistMin = cd/2;
Field[4].DistMax = cd;


// Si-to-Sio2 interface
Field[1] = Attractor;
Field[1].EdgesList = {4};
Field[2] = Threshold;
Field[2].IField = 1;
Field[2].LcMin = cd/2;
Field[2].LcMax = cd;
Field[2].DistMin = 1 * cd;
Field[2].DistMax = 2 * cd;


// Box field - S/D influence (OFF)
Field[6] = Box;
Field[6].VIn = cd/5; // x_diffusion_spacing/5;
Field[6].VOut = cd; // x_diffusion_spacing;
Field[6].XMin = x_device_left; 
Field[6].XMax = x_device_right;
Field[6].YMax = y_bulk_bottom;
Field[6].YMin = y_bulk_bottom - device_thickness; // - y_diffusion_spacing;


// Box field - SiO2 & Gate influence
Field[9] = Box;
Field[9].VIn = cd/2;
Field[9].VOut = cd/1;
Field[9].XMin = x_device_left; 
Field[9].XMax = x_device_right;
Field[9].YMin = y_gate_top;
Field[9].YMax = y_bulk_top;


// Use minimum of all the fields as the background field
Field[8] = Min;
Field[8].FieldsList = {7,2,9};
Background Field = 8;


//////////////////////////////////


Mesh.CharacteristicLengthFromPoints = 0;
Mesh.CharacteristicLengthFromCurvature = 0;
Mesh.CharacteristicLengthExtendFromBoundary = 0;
Mesh.Algorithm=5; /*Delaunay*/


//////////////////////////////////


Physical Line("gate_contact") = {13};
Physical Line("gate_oxide_interface") = {11};
Physical Line("bulk_oxide_interface") = {4};
Physical Line("source_contact") = {1};  // MM: for S/D at the top
Physical Line("drain_contact") = {17}; // MM: for S/D at the top

Physical Surface("gate") = {17};
Physical Surface("oxide") = {19};
Physical Surface("bulk") = {8};

