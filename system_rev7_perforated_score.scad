
// Cleaned clip-unit + mold + panel system
//
// What this version does:
// - Removes the molded panel backing entirely.
// - Keeps the original pad + column + fin unit structure.
// - Adds a separate PRINTED panel with ball-snap posts.
// - Uses ball-post geometry directly on the TOP LID to create molded snap sockets.
// - Uses the same ball-post geometry on the final printed panel.
// - Adds 4 alignment fins/ribs on each ball-post stem for orientation/keying.
// - No insert carrier array is used in this revision.
// - The bottom lid is flat.
// - The center mold has bleed channels on BOTH faces.
// - Both lids get matching seating walls that fit into the bleed channels.
// - Adds real matched score teeth + pockets around the top and bottom parting-face edges.
// - Variables are grouped at the top and unused legacy modules were removed.
//
// Suggested workflow:
// 1) Print top lid, center piece, bottom lid.
// 2) Fill/close mold with silicone in the cavities; overflow gets captured in bleed channels.
// 3) The top-lid ball posts create the pop-in/pop-out socket shape in the silicone.
// 4) Demold the silicone units.
// 5) Print the separate panel with the same ball-post array and snap the silicone units onto it.

$fn = 72;
EPS = 0.001;

// ============================================================
// TOOL / VIEW
// ============================================================
tool_mode = "silicone_positive";
// "silicone_positive", "center_piece", "top_lid", "bottom_lid",
// "panel", "exploded_mold", "exploded_system"

show_exploded_gap = 18.0;

// ============================================================
// ARRAY / UNIT GEOMETRY
// ============================================================
rows = 4;
cols = 4;

top_size          = 22.0; //change to 20, already printed top_lid.
top_corner_radius = 6.0;
top_thickness     = 3.0; //3.4
top_bevel_inset   = 0.0;

unit_height       = 16.0;

edge_gap_x        = 1.40; //1.2
edge_gap_y        = 1.40; //1.2
pitch_x           = top_size + edge_gap_x;
pitch_y           = top_size + edge_gap_y;

field_margin_x    = 1.2;//3.8
field_margin_y    = 1.2;
field_corner_radius = 5.0;

// ============================================================
// COLUMN / FIN GEOMETRY
// ============================================================
column_d             = 9.0;//8
fin_count            = 8;
fin_thickness        = 1.2;
fin_neck_extra       = 0.10;
fin_attach_bot_frac  = 0.60; //0.60
fin_attach_top_frac  = 0.80; //0.99
fin_root_overlap     = 0.35;
fin_end_overlap      = 0.20;
fin_steps            = 40;

// ============================================================
// MOLD GEOMETRY
// ============================================================
mold_wall          = 0.0; //4.0
clamp_flange       = 18.0;
lid_thickness      = 8.0;

// Chamfer on outside edges of center_piece, top_lid, and bottom_lid.
// This gives a small pry/spatula lead-in at the mold split lines.
mold_edge_bevel    = 2.0;

// Tiny overcut at the two mold faces to prevent exact-coplanar preview skins
// from making the center-piece cavities look closed.
cavity_face_relief = 0.08;

fit_clearance      = 0.20;

bleed_channel_w    = 3.0;
bleed_channel_depth= 3.0; //3.0

// Flash scoring / perforation control.
// Previous revision made a gutter, which could make the flash thicker.
// This version creates MATCHED mold teeth + pockets. The remaining silicone
// between them is controlled by score_web_thickness, like dotted rip-paper.
score_enable          = false; // true
score_top_enable      = false;   // silicone top-pad side / bottom_lid side
score_bottom_enable   = false;   // ball-post/column side / top_lid side //true

score_offset          = 1.2;   // distance from actual part edge before score line begins
score_line_width      = 0.0;   // width of continuous score rib
score_pocket_depth    = 0.60;   // depth of matching pocket cut into center piece
score_web_thickness   = 0.08;   // silicone left between lid tooth and center pocket
score_tooth_height    = max(score_pocket_depth - score_web_thickness, EPS);

score_fit_clearance   = 0.20;   // extra XY clearance so score teeth fit into pockets
score_dot_enable      = true;   // adds dotted/perforated rip-paper style teeth
score_dot_d           = 0.80;
score_dot_pitch       = 4.00;   // spacing for square-side dots
score_dot_count       = 18;     // circular dots around column/ball side

bolt_hole_enable   = true;
bolt_hole_d        = 6.7; //6.8
bolt_edge_margin   = 7.5;

// shared ball-snap post geometry
// Used on BOTH the top lid and the final printed panel.
snap_stem_d        = 1.6;
snap_stem_h        = 6; //1.8
snap_ball_d        = 5.0;
snap_ball_sink     = 0.4;  // how much the ball blends into the stem 0.6

// 4 alignment fins/ribs that run up the stick toward the ball.
// Used on BOTH the top lid and the final printed panel because both use ball_snap_post().
snap_fin_enable        = true;
snap_fin_count         = 4;
snap_fin_thickness     = 0.6;  // tangential fin thickness
snap_fin_outer_d       = 4.6;   // how far the fins extend outward from the stem center
snap_fin_stem_overlap  = 0.12;  // radial overlap into the stem so fins print as one body
snap_fin_base_overlap  = 0.10;  // z-overlap into lid/panel surface for stronger base fusion
snap_fin_top_clearance = 0.10;  // gap before ball blend area
snap_fin_tip_taper     = 0.00;  // top of fin narrows slightly as it reaches the ball
// ============================================================
// PANEL GEOMETRY
// ============================================================
// The final panel uses the SAME ball-post structure as the top lid.
panel_thickness       = 2.0;

// ============================================================
// DERIVED
// ============================================================
field_w = (cols - 1) * pitch_x + top_size + 2 * field_margin_x;
field_d = (rows - 1) * pitch_y + top_size + 2 * field_margin_y;

tool_w  = field_w + 2 * mold_wall + 2 * clamp_flange;
tool_d  = field_d + 2 * mold_wall + 2 * clamp_flange;

pad_top_face_size = max(top_size - 2 * top_bevel_inset, 0.1);
pad_top_face_r    = max(top_corner_radius - 0.55 * top_bevel_inset, 0.25);

snap_post_drop = snap_stem_h - snap_ball_sink + snap_ball_d / 2;

bolt_x = tool_w / 2 - bolt_edge_margin - bolt_hole_d / 2;
bolt_y = tool_d / 2 - bolt_edge_margin - bolt_hole_d / 2;

// ============================================================
// HELPERS
// ============================================================
function clamp(v, lo, hi) = min(max(v, lo), hi);
function bez2(t, p0, p1, p2, p3) = [
    pow(1 - t, 3) * p0[0] + 3 * pow(1 - t, 2) * t * p1[0] + 3 * (1 - t) * pow(t, 2) * p2[0] + pow(t, 3) * p3[0],
    pow(1 - t, 3) * p0[1] + 3 * pow(1 - t, 2) * t * p1[1] + 3 * (1 - t) * pow(t, 2) * p2[1] + pow(t, 3) * p3[1]
];
function bezier_pts(p0, p1, p2, p3, steps=16) = [for (i = [0:steps]) bez2(i / steps, p0, p1, p2, p3)];
function fin_angles(n) = [for (i = [0 : n - 1]) i * 360 / n];

module rounded_rect_2d(w, d, r) {
    rr = clamp(r, 0.01, min(w, d) / 2 - 0.01);
    offset(r = rr)
        square([max(w - 2 * rr, 0.01), max(d - 2 * rr, 0.01)], center = true);
}

module rounded_square_2d(s, r) {
    rounded_rect_2d(s, s, r);
}

module field_outline_2d() {
    rounded_rect_2d(field_w, field_d, field_corner_radius);
}

module place_units() {
    for (r = [0 : rows - 1])
        for (c = [0 : cols - 1])
            translate([
                (c - (cols - 1) / 2) * pitch_x,
                (r - (rows - 1) / 2) * pitch_y,
                0
            ])
                children();
}

module bleed_channel_2d() {
    difference() {
        offset(delta = bleed_channel_w)
            field_outline_2d();
        field_outline_2d();
    }
}

module seal_wall_2d(clearance = fit_clearance) {
    difference() {
        offset(delta = max(bleed_channel_w - clearance, EPS))
            field_outline_2d();
        offset(delta = clearance)
            field_outline_2d();
    }
}

module corner_bolt_holes(z0, h) {
    if (bolt_hole_enable && bolt_hole_d > EPS)
        for (sx = [-1, 1])
            for (sy = [-1, 1])
                translate([sx * bolt_x, sy * bolt_y, z0])
                    cylinder(h = h, d = bolt_hole_d);
}

module beveled_tool_body(h) {
    b = clamp(mold_edge_bevel, 0, min(min(tool_w, tool_d) / 2 - EPS, h / 2 - EPS));

    if (b <= EPS) {
        translate([-tool_w / 2, -tool_d / 2, 0])
            cube([tool_w, tool_d, h]);
    } else {
        hull() {
            translate([0, 0, 0])
                linear_extrude(height = EPS)
                    square([tool_w - 2 * b, tool_d - 2 * b], center = true);
            translate([0, 0, b])
                linear_extrude(height = EPS)
                    square([tool_w, tool_d], center = true);
            translate([0, 0, h - b])
                linear_extrude(height = EPS)
                    square([tool_w, tool_d], center = true);
            translate([0, 0, h - EPS])
                linear_extrude(height = EPS)
                    square([tool_w - 2 * b, tool_d - 2 * b], center = true);
        }
    }
}

module snap_stem_alignment_fin() {
    fin_z0 = -snap_fin_base_overlap;
    fin_z1 = max(snap_stem_h - snap_ball_sink - snap_fin_top_clearance, EPS);
    inner_r = max(snap_stem_d / 2 - snap_fin_stem_overlap, 0.01);
    outer_r0 = max(snap_fin_outer_d / 2, inner_r + 0.05);
    outer_r1 = max(outer_r0 - snap_fin_tip_taper, inner_r + 0.05);

    rotate([90, 0, 0])
        linear_extrude(height = snap_fin_thickness, center = true)
            polygon(points = [
                [inner_r, fin_z0],
                [outer_r0, fin_z0],
                [outer_r1, fin_z1],
                [inner_r, fin_z1]
            ]);
}

module ball_snap_post() {
    union() {
        cylinder(h = snap_stem_h, d = snap_stem_d);

        if (snap_fin_enable)
            for (a = fin_angles(snap_fin_count))
                rotate([0, 0, a])
                    snap_stem_alignment_fin();

        translate([0, 0, snap_stem_h - snap_ball_sink])
            sphere(d = snap_ball_d);
    }
}

module top_lid_snap_posts() {
    place_units()
        ball_snap_post();
}

// ============================================================
// TRUE SCORED / PERFORATED FLASH CONTROL
// ============================================================
module outline_ring_2d(offset_amt, width_amt) {
    difference() {
        offset(delta = offset_amt + width_amt)
            children();
        offset(delta = offset_amt)
            children();
    }
}

module unit_top_split_outline_2d() {
    // Silicone top-pad side; appears on the BOTTOM face of the center piece
    // because the silicone cavity is mirrored in center_piece_assembly().
    rounded_square_2d(pad_top_face_size, pad_top_face_r);
}

module unit_bottom_split_outline_2d() {
    // Silicone column/ball-post side; appears on the TOP face of the center piece.
    inner_r = max(column_d / 2 - fin_root_overlap, 0);
    outer_r = (top_size / 2) * fin_attach_bot_frac;

    union() {
        circle(d = column_d);

        for (a = fin_angles(fin_count))
            rotate([0, 0, a])
                translate([(inner_r + outer_r) / 2, 0, 0])
                    square([max(outer_r - inner_r, EPS), fin_thickness], center = true);
    }
}

module top_pad_score_dots_2d() {
    half = pad_top_face_size / 2 + score_offset + score_line_width / 2;
    for (x = [-half : score_dot_pitch : half]) {
        translate([x,  half]) circle(d = score_dot_d);
        translate([x, -half]) circle(d = score_dot_d);
    }
    for (y = [-half : score_dot_pitch : half]) {
        translate([ half, y]) circle(d = score_dot_d);
        translate([-half, y]) circle(d = score_dot_d);
    }
}

module bottom_interface_score_dots_2d() {
    r = (top_size / 2) * fin_attach_bot_frac + score_offset + score_line_width / 2;
    for (a = [0 : 360 / score_dot_count : 360 - 360 / score_dot_count])
        rotate([0, 0, a])
            translate([r, 0, 0])
                circle(d = score_dot_d);
}

module top_face_score_shape_2d(extra_clearance = 0) {
    // Score shape for silicone top-pad side / bottom_lid side.
    if (score_enable && score_top_enable)
        offset(delta = extra_clearance)
            union() {
                outline_ring_2d(score_offset, score_line_width)
                    unit_top_split_outline_2d();

                if (score_dot_enable)
                    top_pad_score_dots_2d();
            }
}

module bottom_face_score_shape_2d(extra_clearance = 0) {
    // Score shape for silicone column/ball side / top_lid side.
    if (score_enable && score_bottom_enable)
        offset(delta = extra_clearance)
            union() {
                outline_ring_2d(score_offset, score_line_width)
                    unit_bottom_split_outline_2d();

                if (score_dot_enable)
                    bottom_interface_score_dots_2d();
            }
}

module center_bottom_score_pockets_3d() {
    // Pockets in center piece BOTTOM face.
    // These accept bottom_lid score teeth.
    if (score_enable && score_top_enable && score_pocket_depth > EPS)
        translate([0, 0, -EPS])
            linear_extrude(height = score_pocket_depth + EPS)
                place_units()
                    top_face_score_shape_2d(score_fit_clearance);
}

module center_top_score_pockets_3d() {
    // Pockets in center piece TOP face.
    // These accept top_lid score teeth.
    if (score_enable && score_bottom_enable && score_pocket_depth > EPS)
        translate([0, 0, unit_height - score_pocket_depth])
            linear_extrude(height = score_pocket_depth + EPS)
                place_units()
                    bottom_face_score_shape_2d(score_fit_clearance);
}

module bottom_lid_score_teeth_3d() {
    // Teeth on bottom lid contact face, going UP into center-piece bottom pockets.
    if (score_enable && score_top_enable && score_tooth_height > EPS)
        linear_extrude(height = score_tooth_height)
            place_units()
                top_face_score_shape_2d(0);
}

module top_lid_score_teeth_3d() {
    // Teeth on top lid contact face, going DOWN into center-piece top pockets.
    if (score_enable && score_bottom_enable && score_tooth_height > EPS)
        translate([0, 0, -score_tooth_height])
            linear_extrude(height = score_tooth_height)
                place_units()
                    bottom_face_score_shape_2d(0);
}

// ============================================================
// SILICONE UNIT POSITIVE
// ============================================================
module top_pad() {
    hull() {
        translate([0, 0, 0])
            linear_extrude(height = EPS)
                rounded_square_2d(top_size, top_corner_radius);
        translate([0, 0, max(top_thickness - EPS, EPS)])
            linear_extrude(height = EPS)
                rounded_square_2d(pad_top_face_size, pad_top_face_r);
    }
}

module curved_fin(z0, z1, outer_r0, outer_r1, th = fin_thickness) {
    inner_r  = max(column_d / 2 - fin_root_overlap, 0);
    throat_r = max(column_d / 2 + fin_neck_extra, inner_r + 0.05);

    outer_curve = bezier_pts(
        [outer_r0, z0],
        [throat_r, z0 + (z1 - z0) * 0.34],
        [throat_r, z0 + (z1 - z0) * 0.66],
        [outer_r1, z1],
        fin_steps
    );

    poly_pts = concat(
        [[inner_r, z0], [outer_r0, z0]],
        [for (i = [1 : len(outer_curve) - 2]) outer_curve[i]],
        [[outer_r1, z1], [inner_r, z1]]
    );

    rotate([90, 0, 0])
        linear_extrude(height = th, center = true)
            polygon(points = poly_pts);
}

module silicone_unit() {
    stem_h = max(unit_height - top_thickness, EPS);
    fin_z0 = 0;
    fin_z1 = min(stem_h + fin_end_overlap, unit_height - EPS);
    fin_outer_bottom = (top_size / 2) * fin_attach_bot_frac;
    fin_outer_top    = (top_size / 2) * fin_attach_top_frac;

    union() {
        cylinder(h = stem_h, d = column_d);

        translate([0, 0, stem_h])
            top_pad();

        for (a = fin_angles(fin_count))
            rotate([0, 0, a])
                curved_fin(fin_z0, fin_z1, fin_outer_bottom, fin_outer_top, fin_thickness);
    }
}

module silicone_array() {
    place_units()
        silicone_unit();
}

module silicone_bottom_interface_slice() {
    big = max(tool_w, tool_d) + 10;
    if (cavity_face_relief > EPS)
        intersection() {
            silicone_array();
            translate([-big / 2, -big / 2, 0])
                cube([big, big, 2 * cavity_face_relief]);
        }
}

module silicone_top_interface_slice() {
    big = max(tool_w, tool_d) + 10;
    if (cavity_face_relief > EPS)
        intersection() {
            silicone_array();
            translate([-big / 2, -big / 2, unit_height - 2 * cavity_face_relief])
                cube([big, big, 2 * cavity_face_relief]);
        }
}

// ============================================================
// PANEL WITH MALE SNAP STUDS
// ============================================================
module panel_part() {
    union() {
        linear_extrude(height = panel_thickness)
            field_outline_2d();

        translate([0, 0, panel_thickness])
            place_units()
                ball_snap_post();
    }
}

// ============================================================
// MOLD COMPONENTS (ASSEMBLY COORDINATES)
// ============================================================
// center piece:
//   z = 0 ............ bottom face
//   z = unit_height .. top face
//
// top lid:
//   contact plane is z = 0
//   wall goes down to z = -bleed_channel_depth
//   body goes up to z = lid_thickness
//
// bottom lid:
//   contact plane is z = 0
//   wall goes up to z = bleed_channel_depth
//   body goes down to z = -lid_thickness

module center_piece_assembly() {
    difference() {
        beveled_tool_body(unit_height);

        // main silicone unit cavities
        translate([0, 0, unit_height])
            mirror([0, 0, 1])
                silicone_array();

        // small face-relief overcuts to avoid exact coplanar skins in OpenSCAD preview/render
        translate([0, 0, unit_height + cavity_face_relief])
            mirror([0, 0, 1])
                silicone_bottom_interface_slice();
        translate([0, 0, unit_height - cavity_face_relief])
            mirror([0, 0, 1])
                silicone_top_interface_slice();

        // matched scoring pockets for the lid teeth.
        // These do NOT create a thick overflow gutter; instead they leave only
        // score_web_thickness of silicone at the tear line.
        center_bottom_score_pockets_3d();
        center_top_score_pockets_3d();

        // top bleed trench
        translate([0, 0, unit_height - bleed_channel_depth])
            linear_extrude(height = bleed_channel_depth + EPS)
                bleed_channel_2d();

        // bottom bleed trench
        translate([0, 0, -EPS])
            linear_extrude(height = bleed_channel_depth + EPS)
                bleed_channel_2d();

        corner_bolt_holes(-EPS, unit_height + 2 * EPS);
    }
}

module top_lid_assembly() {
    difference() {
        union() {
            // main body with outer pry/chamfer bevels
            beveled_tool_body(lid_thickness);

            // seating wall into top bleed channel
            translate([0, 0, -bleed_channel_depth])
                linear_extrude(height = bleed_channel_depth)
                    seal_wall_2d(fit_clearance);

            // dotted/continuous score teeth on the top lid contact face
            top_lid_score_teeth_3d();

            // ball-post array on mold side. These posts dip into the silicone
            // and form the snap sockets directly.
            mirror([0, 0, 1])
                top_lid_snap_posts();
        }

        corner_bolt_holes(-max(bleed_channel_depth, snap_post_drop) - EPS,
                          lid_thickness + max(bleed_channel_depth, snap_post_drop) + 2 * EPS);
    }
}

module bottom_lid_assembly() {
    difference() {
        union() {
            // flat bottom lid body with outer pry/chamfer bevels
            translate([0, 0, -lid_thickness])
                beveled_tool_body(lid_thickness);

            // seating wall into bottom bleed channel
            linear_extrude(height = bleed_channel_depth)
                seal_wall_2d(fit_clearance);

            // dotted/continuous score teeth on the bottom lid contact face
            bottom_lid_score_teeth_3d();
        }

        corner_bolt_holes(-lid_thickness - EPS, lid_thickness + max(bleed_channel_depth, score_tooth_height) + 2 * EPS);
    }
}

// ============================================================
// EXPORT WRAPPERS (lowest z at 0 for convenience)
// ============================================================
module center_piece_part() {
    center_piece_assembly();
}

module top_lid_part() {
    translate([0, 0, max(bleed_channel_depth, snap_post_drop)])
        top_lid_assembly();
}

module bottom_lid_part() {
    translate([0, 0, lid_thickness])
        bottom_lid_assembly();
}

// ============================================================
// EXPLODED VIEWS
// ============================================================
module exploded_mold() {
    // bottom lid
    translate([0, 0, -lid_thickness - show_exploded_gap])
        color([0.75, 0.85, 0.95, 0.60])
            bottom_lid_assembly();

    // center piece
    color([0.92, 0.92, 0.92, 0.65])
        center_piece_assembly();

    // top lid
    translate([0, 0, unit_height + show_exploded_gap])
        color([0.70, 0.75, 0.95, 0.55])
            top_lid_assembly();
}

module exploded_system() {
    exploded_mold();

    // silicone units
    translate([tool_w * 0.72, 0, 0])
        color([0.90, 0.90, 0.90, 0.65])
            silicone_array();

    // panel with male studs
    translate([-tool_w * 0.72, 0, 0])
        color([0.60, 0.80, 0.95, 0.75])
            panel_part();
}

// ============================================================
// TOOL MODE SWITCH
// ============================================================
if (tool_mode == "silicone_positive") {
    silicone_array();
} else if (tool_mode == "center_piece") {
    center_piece_part();
} else if (tool_mode == "top_lid") {
    top_lid_part();
} else if (tool_mode == "bottom_lid") {
    bottom_lid_part();
} else if (tool_mode == "panel") {
    panel_part();
} else if (tool_mode == "exploded_mold") {
    exploded_mold();
} else {
    exploded_system();
}
