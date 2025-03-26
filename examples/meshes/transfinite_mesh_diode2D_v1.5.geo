//// File: diode_2D Structured mesh - v1.5
//// objective: to get the same structured triangular matrix; but x&y aligned

// Mesh.Algorithm = 8;
// Mesh.Smoothing = 2;
// Mesh.MeshSizeFactor = 0.5;
// Mesh.RecombinationAlgorithm = 1;
// Mesh.RecombineAll = 1;
// Mesh.SubdivisionAlgorithm = 1;

lc = 1e-6;

//// Diode points
Point(1) = {0, 0, 0, lc};
Point(2) = {1.0e-5, 0, 0, lc};
Point(3) = {1.0e-5, 0.2e-5, 0, lc};
Point(4) = {1.0e-5, 1.0e-5, 0, lc};
Point(5) = {0, 1.0e-5, 0, lc};
Point(6) = {0, 0.8e-5, 0, lc};

//// Numb points
Point(7) = {1.0e-5, 0.8e-5, 0, lc};
Point(8) = {0, 0.2e-5, 0, lc};

//// Bulk lines
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 7};
Line(4) = {7, 4};
Line(5) = {4, 5};
Line(6) = {5, 6};
Line(7) = {6, 8}; // numb line, to make Transfinite connection
Line(8) = {8, 1}; // numb line, to make Transfinite connection


//// Pre-definition of "Structured triangular ordered grid" (Bulk area)
Curve Loop(1) = {1, 2, 3, 4, 5, 6, 7, 8};
Plane Surface(1) = {1};


//// Bulk area
Physical Surface("Bulk") = {1};


//// Contact metal lines
Physical Curve("Base", 7) = {6};
Physical Curve("Emitter", 8) = {2};


//// Transfinite (Structured triangular ordered grid)



////////////     


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
Mesh.MshFileVersion = 2.2;

//// Transfinite mesh definition (diode squared structure, 2 terminals)
Horizontal_mesh_dim = 50;
Transfinite Surface {1} = {1, 2, 4, 5};
Transfinite Curve {5, 1} = Horizontal_mesh_dim Using Progression 1; // Top & Bottom
Transfinite Curve {6, 4} = Horizontal_mesh_dim/5 Using Progression 1; // Upper terminal
Transfinite Curve {7, 3} = 3*Horizontal_mesh_dim/5 Using Progression 1; // Mid body
Transfinite Curve {8, 2} = Horizontal_mesh_dim/5 Using Progression 1; // Lower terminal
