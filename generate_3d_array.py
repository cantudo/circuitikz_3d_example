from math import sqrt
header = """
\\documentclass[]{standalone}
\\usepackage{tikz}
\\usetikzlibrary{intersections,decorations.markings,positioning,3d}
\\usetikzlibrary{circuits.ee.IEC.relay, arrows.meta}
\\usepackage{circuitikz}
\\usepackage{fix-cm}


\\makeatletter
\\newcommand\\HUGE{\\@setfontsize\\Huge{50}{60}}
\\makeatother

\\makeatletter
\\newcommand\\HUGEE{\\@setfontsize\\Huge{35}{60}}
\\makeatother

\\makeatletter
\\newcommand\\HUGER{\\@setfontsize\\Huge{80}{90}}
\\makeatother


\\tikzset{
    bigV/.style={V, sources/scale=1.5},
    scaled V/.style={V, sources/scale=#1},
    scaled/.default=1, % or whatever
}

\\tikzset{
    bigsV/.style={sV, sources/scale=1.5},
    scaled sV/.style={sV, sources/scale=#1},
    scaled/.default=1, % or whatever
}

\\tikzset{
    bigR/.style={resistor, resistors/scale=1.5},
    scaled R/.style={resistor, resistors/scale=#1},
    scaled/.default=1, % or whatever
}

\\begin{document}

%\\begin{tikzpicture}[x={({cos(20)},{-sin(20)},0)},z={({-sin(40)},{-cos(40)},0)},scale=0.7,
\\begin{tikzpicture}[x={(-10:1cm)}, y={(225:0.8cm)}, z={(90:1cm)},scale=0.7,
  point/.style={minimum  size=1pt,inner  sep=2pt, circle, draw, red},
  line join=round,
  cont/.style={contact, draw, thick},
%  circuit ee IEC,
  thick,
  ]
  \\ctikzset{resistor = american, voltage = american}
  \\begin{scope}[line width=1.5pt]
  \\ctikzset{bipoles/thickness=1.5}
  \\ctikzset{bipoles/vsourceam/inner plus={\\HUGEE $+$}}
  \\ctikzset{bipoles/vsourceam/inner minus={\\HUGEE $-$}}
"""

footer = """
\\end{scope}
\\end{tikzpicture}
\\end{document}
"""


def draw_qpc(array_length, array_width, array_height, scale=1):
    document = ""

    qpc_dist = 1.2/3 * array_length
    qpc_size = 1

    x_quarter = (array_length - 1 + 0) / 4
    y_quarter = (array_width - 1 + 0) / 4

    square = [
        reorder_coords(
            [x_quarter * scale, y_quarter * scale, -qpc_dist * scale]),
        reorder_coords(
            [(array_length - 1 - x_quarter) * scale, y_quarter * scale, -
             qpc_dist * scale]),
        reorder_coords(
            [(array_length - 1 - x_quarter) * scale,
             (array_width - 1 - y_quarter) * scale, -qpc_dist * scale]),
        reorder_coords(
            [x_quarter * scale, (array_width - 1 - y_quarter) * scale, -
             qpc_dist * scale]),]

    final_qpc = reorder_coords(
        [(array_length - 1) / 2 * scale, (array_width - 1) / 2 * scale, -
         (qpc_dist + qpc_size) * scale])

    print('final_qpc: ', final_qpc)
#   for i in range(0, 4):
#       document += "\\draw ({},{},{}) -- ({},{},{});\n".format(
#           square[i][0], square[i][1], square[i][2],
#           final_qpc[0], final_qpc[1], final_qpc[2])

    for i in [0, 1, 3, 2]:
        document += "\\filldraw[draw=black,fill=blue!30,opacity=0.8] ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
            square[i][0], square[i][1], square[i][2],
            square[(i+1) % 4][0], square[(i+1) % 4][1], square[(i+1) % 4][2],
            final_qpc[0], final_qpc[1], final_qpc[2])

    document += "\\filldraw[draw=black,fill=blue!30,opacity=0.8] ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
        square[0][0], square[0][1], square[0][2],
        square[1][0], square[1][1], square[1][2],
        square[2][0], square[2][1], square[2][2],
        square[3][0], square[3][1], square[3][2])

    document += f"\\begin{{scope}}[canvas is xy plane at z={-qpc_dist * scale}]\n"

    document += "\\node[draw=black, circle, transform shape, yscale=-1] at ({},{}) {{\\HUGER QPC}};\n".format(
        (array_length - 1) / 2 * scale, (array_width - 1) / 4 * 2 * scale)

    document += "\\end{scope}\n"

    document += "\\draw[] ({},{},{}) -- ({},{},{});\n".format(
        *
        reorder_coords(
            [(array_length - 1) / 2 * scale, (array_width - 1) / 2 * scale, 0]),
        *
        reorder_coords(
            [(array_length - 1) / 2 * scale, (array_width - 1) / 2 * scale, -
             qpc_dist * scale]),)

    return document, final_qpc


"""
    z
  |
  |
  |
  / ------- x
 /
/ y

p6     p5,..
|
|   p4     p1
|   ______
|  /     /
| /     /
|______/
p2    p3

"""


def draw_cube(p1, p2, p6):

    document = ""

    p4 = [p2[0], p1[1], p1[2]]
    p3 = [p1[0], p2[1], p1[2]]
    p5 = [p1[0], p1[1], p6[2]]
    p7 = [p3[0], p3[1], p6[2]]
    p8 = [p4[0], p4[1], p6[2]]

    commands = "draw=black,fill=gray!50,opacity=0.7"
    base = f"\\filldraw[{commands}] "

    # Base
    document += base + " ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
        *reorder_coords(p1), *reorder_coords(p3), *reorder_coords(p2), *reorder_coords(p4))
    # Back
    document += base + " ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
        *reorder_coords(p1), *reorder_coords(p4), *reorder_coords(p8), *reorder_coords(p5))
    # Left side
    document += base + " ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
        *reorder_coords(p4), *reorder_coords(p2), *reorder_coords(p6), *reorder_coords(p8))
    # Right side
    document += base + " ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
        *reorder_coords(p1), *reorder_coords(p3), *reorder_coords(p7), *reorder_coords(p5))
    # Top
    document += base + " ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
        *reorder_coords(p5), *reorder_coords(p7), *reorder_coords(p6), *reorder_coords(p8))
    # Front
    document += base + " ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
        *reorder_coords(p2), *reorder_coords(p3), *reorder_coords(p7), *reorder_coords(p6))

    return document


def get_orig_dest_from_len(orig, dest, res_len, scale=1):
    orig = [orig[0]*scale, orig[1]*scale, orig[2]*scale]
    dest = [dest[0]*scale, dest[1]*scale, dest[2]*scale]
    mid_point = [(orig[0] + dest[0])/2, (orig[1] + dest[1])/2,
                 (orig[2] + dest[2])/2]

    orig_diff_mid = [-orig[0] + mid_point[0], -orig[1]
                     + mid_point[1], -orig[2] + mid_point[2]]
    orig_diff_mid_norm = sqrt(
        orig_diff_mid[0]**2 + orig_diff_mid[1]**2 + orig_diff_mid[2]**2)
    orig_diff_mid = [
        orig_diff_mid[0] / orig_diff_mid_norm, orig_diff_mid[1] /
        orig_diff_mid_norm, orig_diff_mid[2] / orig_diff_mid_norm]
    new_orig = [
        mid_point[0] - orig_diff_mid[0] * res_len / 2, mid_point[1] -
        orig_diff_mid[1] * res_len / 2, mid_point[2] - orig_diff_mid[2] * res_len /
        2]

    dest_diff_mid = [
        dest[0] - mid_point[0],
        dest[1] - mid_point[1],
        dest[2] - mid_point[2]]
    dest_diff_mid_norm = sqrt(
        dest_diff_mid[0]**2 + dest_diff_mid[1]**2 + dest_diff_mid[2]**2)
    dest_diff_mid = [
        dest_diff_mid[0] / dest_diff_mid_norm, dest_diff_mid[1] /
        dest_diff_mid_norm, dest_diff_mid[2] / dest_diff_mid_norm]
    new_dest = [
        mid_point[0] + dest_diff_mid[0] * res_len / 2, mid_point[1] +
        dest_diff_mid[1] * res_len / 2, mid_point[2] + dest_diff_mid[2] * res_len /
        2]

    # return [new_orig, new_dest]
    return [orig, dest]


def reorder_coords(coord):
    # return [coord[0], coord[2], coord[1]]
    return [coord[0], coord[1], coord[2]]


def generate_3d_array(
        m: int, n: int, z: int, filename: str, res_len=2, scale=1):

    array_width = m  # vertical
    array_length = n  # horizontal
    array_height = z  # 3D

    pairs = []
    extra_pairs = []

    def pairs_action(orig, dest): return pairs.append(
        get_orig_dest_from_len(orig, dest, res_len, scale))
    # pairs_action = lambda orig, dest: pairs.append([orig, dest])

    for z in range(1, array_height):
        if z > 0 and z < array_height-1:
            for y in range(array_width-1):
                for x in range(array_length-1):
                    # Vertical resistors
                    orig = [x, y, z]
                    dest = [x, y+1, z]
                    pairs_action(orig, dest)

                    # Horizontal resistors
                    orig = [x, y, z]
                    dest = [x+1, y, z]
                    pairs_action(orig, dest)

                    if y == array_width-2:
                        # Last in column
                        orig = [x, y+1, z]
                        dest = [x+1, y+1, z]
                        pairs_action(orig, dest)

                # Last in column
                orig = [array_length-1, y, z]
                dest = [array_length-1, y+1, z]
                pairs_action(orig, dest)

        # for y in range(array_width-1):

        # # Residual node 0
        # for k in range(array_length-1):
        #   orig = [array_width-1, k, z]
        #   dest = [array_width, k, z]
        #   pairs_action(orig, dest)

        if z > 0:
            # Vertical resistors
            for y in range(array_width):
                for x in range(array_length):
                    orig = [x, y, z]
                    dest = [x, y, z-1]
                    pairs_action(orig, dest)

    document = header

    pad_height = 0.2

    d, final_qpc = draw_qpc(array_length, array_width, array_height, scale)

    document += d

    document += draw_cube(
        [(array_length - 1) * scale, 0, (-pad_height) * scale],
        [0, (array_width - 1) * scale, (-pad_height) * scale],
        [0, (array_width - 1) * scale, 0 * scale],
    )

    painted_pairs = []

    # for idx, pair in enumerate(pairs):

    #     if idx in painted_pairs:
    #         continue

    #     orig = reorder_coords(pair[0])
    #     dest = reorder_coords(pair[1])

    #     if orig[2] == dest[2]:
    #         color = "blue"
    #         if orig[0] == dest[0] and orig[1] == dest[1]:
    #             color = "red"
    #         document += "\\draw ({},{},{}) to [resistor, color={}, *-*] ({},{},{});\n".format(
    #             orig[0], orig[1], orig[2], color, dest[0], dest[1], dest[2])
    #         painted_pairs.append(idx)

    for z in range(0, array_height-1):
        point1 = reorder_coords([0, 0, z*scale])
        point2 = reorder_coords([0, (array_width-1)*scale, z*scale])
        point3 = reorder_coords(
            [(array_length-1)*scale, (array_width-1)*scale, z*scale])
        point4 = reorder_coords([(array_length-1)*scale, 0, z*scale])

        for idx, pair in enumerate(pairs):

            if idx in painted_pairs:
                continue

            orig = reorder_coords(pair[0])
            dest = reorder_coords(pair[1])

            if (orig[2] + dest[2])/2 < point1[2]:
                color = "blue"
                if orig[0] == dest[0] and orig[1] == dest[1]:
                    color = "red"
                document += "\\draw ({},{},{}) to [resistor, color={}, *-*] ({},{},{});\n".format(
                    orig[0], orig[1], orig[2], color, dest[0], dest[1], dest[2])
                painted_pairs.append(idx)

        document += "\\fill[fill=blue!15,opacity=0.7] ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
            point1[0], point1[1], point1[2], point2[0], point2[1], point2[2], point3[0], point3[1], point3[2], point4[0], point4[1], point4[2])


        for idx, pair in enumerate(pairs):

            if idx in painted_pairs:
                continue

            orig = reorder_coords(pair[0])
            dest = reorder_coords(pair[1])

            if (orig[2] + dest[2])/2 == point1[2] and orig[0] != dest[0]:
                color = "blue"
                if orig[0] == dest[0] and orig[1] == dest[1]:
                    color = "red"
                document += "\\draw ({},{},{}) to [resistor, color={}, *-*] ({},{},{});\n".format(
                    orig[0], orig[1], orig[2], color, dest[0], dest[1], dest[2])
                painted_pairs.append(idx)

        # for idx, pair in enumerate(pairs):

        #     if idx in painted_pairs:
        #         continue

        #     orig = reorder_coords(pair[0])
        #     dest = reorder_coords(pair[1])

        #     if (orig[2] + dest[2])/2 == point1[2]:
        #         color = "blue"
        #         if orig[0] == dest[0] and orig[1] == dest[1]:
        #             color = "red"
        #         document += "\\draw ({},{},{}) to [resistor, color={}, *-*] ({},{},{});\n".format(
        #             orig[0], orig[1], orig[2], color, dest[0], dest[1], dest[2])
        #         painted_pairs.append(idx)

        for x in reversed(range(0, array_length)):
            # x=x-0.1
            point1_xz = reorder_coords([x*scale, 0, z*scale])
            point2_xz = reorder_coords(
                [x*scale, (array_width-1)*scale, z*scale])
            point3_xz = reorder_coords(
                [x*scale, (array_width-1)*scale, (z+1)*scale])
            point4_xz = reorder_coords([x*scale, 0, (z+1)*scale])

            document += "\\fill[fill=orange!30,opacity=0.7] ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
                point1_xz[0], point1_xz[1], point1_xz[2], point2_xz[0], point2_xz[1], point2_xz[2], point3_xz[0], point3_xz[1], point3_xz[2], point4_xz[0], point4_xz[1], point4_xz[2])

    # for x in reversed(range(0, array_length)):
    #     point1 = reorder_coords([x*scale, 0, 0])
    #     point2 = reorder_coords([x*scale, (array_width-1)*scale, 0])
    #     point3 = reorder_coords(
    #         [x*scale, (array_width-1)*scale, (array_height-1)*scale])
    #     point4 = reorder_coords([x*scale, 0, (array_height-1)*scale])

    #     document += "\\fill[fill=orange!30,opacity=0.7] ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- ({},{},{}) -- cycle;\n".format(
    #         point1[0], point1[1], point1[2], point2[0], point2[1], point2[2], point3[0], point3[1], point3[2], point4[0], point4[1], point4[2])

    for idx, pair in enumerate(pairs):
        if idx in painted_pairs:
            continue
        orig = reorder_coords(pair[0])
        dest = reorder_coords(pair[1])
        color = "blue"
        if orig[0] == dest[0] and orig[1] == dest[1]:
            color = "red"
        document += "\\draw ({},{},{}) to [resistor, color={}, *-*] ({},{},{});\n".format(
            orig[0], orig[1], orig[2], color, dest[0], dest[1], dest[2])

    document += draw_cube(
        [(array_length - 1) * scale, 0, (array_height - 1) * scale],
        [0, (array_width - 1) * scale, (array_height - 1) * scale],
        [0, (array_width - 1) * scale, (array_height - 1 + pad_height) * scale],
    )

    dist_arrow = 2.5
    margin_arrow = 0.5

    midpoint_x_start = reorder_coords(
        [(array_length - 1 + 0) / 2 * scale, (array_width - 1 + margin_arrow) * scale, 0])
    midpoint_x_end = reorder_coords(
        [(array_length - 1 + 0) / 2 * scale, ((array_width - 1) + dist_arrow) * scale, 0])

    midpoint_y_start = reorder_coords(
        [(array_length - 1 + margin_arrow) * scale, (array_width - 1 + 0) / 2 * scale, 0])
    midpoint_y_end = reorder_coords(
        [(array_length - 1 + dist_arrow) * scale, (array_width - 1 + 0) / 2 * scale, 0])

    document += "\\begin{scope}[canvas is xy plane at z=0]\n"

    from math import pi, atan

    document += "\\draw[-{{Triangle[scale=2,round,length=3.3mm]}}] ({},{}) -- ({},{}) node[midway, above, transform shape, yscale=-1, rotate={}] {{\\HUGER M rows}};\n".format(
        midpoint_x_start[0], midpoint_x_start[1], midpoint_x_end[0], midpoint_x_end[1], 90)
    document += "\\draw[-{{Triangle[scale=2,round,length=3.3mm]}}] ({},{}) -- ({},{}) node[midway, above, transform shape, yscale=-1, rotate={}] {{\\HUGER N columns}};\n".format(
        midpoint_y_start[0], midpoint_y_start[1], midpoint_y_end[0], midpoint_y_end[1], 0)

    document += "\\end{scope}\n"

    midpoint_z_start = reorder_coords(
        [(array_length - 1 + 0) / 2 * scale, 0,
         (array_height - 1 + margin_arrow) * scale])
    midpoint_z_end = reorder_coords(
        [(array_length - 1 + 0) / 2 * scale, 0, (array_height - 1 + dist_arrow*0.8) * scale])

    document += "\\begin{scope}[canvas is xz plane at y=0]\n"
    document += "\\draw[-{{Triangle[scale=2,round,length=3.3mm]}}] ({},{}) -- ({},{}) node[midway, above, yscale=-1, transform shape , rotate={}, yscale=-1] {{\\HUGER Z layers}};\n".format(
        midpoint_z_start[0], midpoint_z_start[2], midpoint_z_end[0], midpoint_z_end[2], 270)
    document += "\\end{scope}\n"

    from math import cos, sin, pi, atan, tan
    ang = 0
    guiding_vector = [cos(ang*pi/180)/0.8, -sin(ang*pi/180), 0]

    x_orig = (array_length-1)/2*scale
    y_orig = (array_width - 1)/2*scale

    x_mov = 1*scale
    # ang = atan(y_mov/x_mov)
    y_mov = tan(ang*pi/180) * x_mov

    # document += "\\draw[->] ({},{},{}) -- ({},{},{});\n".format(
    #     *reorder_coords([x_orig, y_orig, 0]),
    #     *reorder_coords([
    #     x_orig - x_mov,
    #     y_orig - y_mov, 0]),
    # )
    bottom = reorder_coords([-3*scale, final_qpc[1], final_qpc[2]*1.1])

    top = reorder_coords(
        [bottom[0],
         bottom[1],
         (array_height - 1 + 2 * pad_height) * scale])

    document += "\\draw ({},{},{}) to [scaled sV=5, l={{\\HUGE $V_\\mathrm{{app}}$}}, i={{\\hspace{{20pt}}\HUGE $I_\\mathrm{{RRAM}}$}}, current arrow scale=4] ({},{},{});\n".format(
        *top,
        *bottom,
    )

    document += "\\draw ({},{},{}) -- ({},{},{});\n".format(
        *bottom,
        *reorder_coords([final_qpc[0], final_qpc[1], final_qpc[2]*1.1]),
    )

    document += "\\draw ({},{},{}) -- ({},{},{});\n".format(
        *reorder_coords([final_qpc[0], final_qpc[1], final_qpc[2]*1.1]),
        *reorder_coords(final_qpc),
    )

    final_top_pad = reorder_coords(
        [(array_length - 1) / 2 * scale, (array_width - 1) / 2 * scale,
         (array_height - 1 + 2 * pad_height) * scale])

    document += "\\draw ({},{},{}) to[scaled R=4, color=orange, bipoles/thickness=4,l={{\\begin{{tabular}}{{ c }}\\HUGE $R_\\mathrm{{series}}$\\\\ \\vspace{{15pt}}\end{{tabular}}}}] ({},{},{});\n".format(
        *top,
        *final_top_pad
    )
    #   \\ctikzset{bipoles/thickness=1.5}


    document += "\\draw ({},{},{}) -- ({},{},{});\n".format(
        *final_top_pad,
        *reorder_coords([final_top_pad[0], final_top_pad[1],
                        final_top_pad[2]-(2*pad_height*scale)]),
    )

    print('final_qpc: ', final_qpc)

    document += footer

    with open(filename, "w+") as f:
        f.write(document)


if __name__ == "__main__":
    generate_3d_array(3, 3, 3, "main.tex", res_len=2, scale=8)
