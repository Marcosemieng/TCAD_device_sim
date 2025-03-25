////  Gmsh project created on Sun Mar 23 20:06:07 2025
SetFactory("OpenCASCADE");

cd = 1e-6;

//// Text here
Point(1) = {0, 0, 0};
Point(2) = {0.5e-5, 0, 0};
Point(3) = {1.0e-5, 0, 0};
Point(4) = {1.0e-5, 0.2e-5, 0};
Point(5) = {1.0e-5, 1.0e-5, 0};
Point(6) = {0.5e-5, 1.0e-5, 0};
Point(7) = {0, 1.0e-5, 0};
Point(8) = {0, 0.8e-5, 0};


Line(1) = {1, 3};
// Line(2) = {2, 3};
Line(3) = {3, 5};
Line(4) = {3, 4};
// Line(5) = {5, 6};
Line(6) = {5, 7};
Line(7) = {7, 1};
Line(8) = {7, 8};
// Line(9) = {2, 6};
// Line(10) = {6, 2};

//// Bulk area
Curve Loop(4) = {1, 3, 6, 7};
Plane Surface(1) = {4};
Physical Surface("Bulk") = {1};

//// Metal contacts area
Physical Curve("Base", 13) = {7};
Physical Curve("Emitter", 14) = {3};


////  Transfinite Mesh
Transfinite Curve {7, 8, 1, 2, 3, 4, 5, 6} = 100;
Transfinite Surface{1};
// Mesh.Smoothing = 100;


//// PN junction mesh
// Field[1] = Distance;
// Field[1].CurvesList = {3,7,9};
// Field[1].Sampling = 500;

// Field[2] = Threshold;
// Field[2].InField = 1;
// Field[2].SizeMin = cd / 50;
// Field[2].SizeMax = cd / 1;
// Field[2].DistMin = cd * 0.1;
// Field[2].DistMax = 500 * cd;

// Field[3] = Distance;
// Field[3].CurvesList = {3,7};
// Field[3].Sampling = 100;

// Field[4] = Threshold;
// Field[4].InField = 1;
// Field[4].SizeMin = cd / 30;
// Field[4].SizeMax = cd / 2;
// Field[4].DistMin = cd * 0.15;
// Field[4].DistMax = cd * 5;

////  Use minimum of all the fields as the background field
// Field[7] = Min;
// Field[7].FieldsList = {4};
// Background Field = 7;


////  File version save
Mesh.MshFileVersion = 2.1;



