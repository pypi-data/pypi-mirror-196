from __future__ import annotations

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.bend_euler import bend_euler
from gdsfactory.components.bend_s import bend_s
from gdsfactory.components.straight import straight
from gdsfactory.typings import ComponentFactory, CrossSectionSpec, Floats, Optional
from scipy.interpolate import interp1d

# import matplotlib.pyplot as plt


@gf.cell
def spiral_racetrack(
    min_radius: float = 5,
    straight_length: float = 10.0,
    spacings: Floats = (2, 2, 3, 3, 2, 2),
    straight_factory: ComponentFactory = straight,
    bend_factory: ComponentFactory = bend_euler,
    bend_s_factory: ComponentFactory = bend_s,
    cross_section: CrossSectionSpec = "strip",
    cross_section_s: CrossSectionSpec = None,
    n_bend_points: Optional[int] = None,
    with_inner_ports: bool = False,
) -> Component:
    """Returns Racetrack-Spiral.

    Args:
        min_radius: smallest radius in um.
        straight_length: length of the straight segments in um.
        spacings: space between the center of neighboring waveguides in um.
        straight_factory: factory to generate the straight segments.
        bend_factory: factory to generate the bend segments.
        bend_s_factory: factory to generate the s-bend segments.
        cross_section: cross-section of the waveguides.
        n_bend_points: optional bend points.
        with_inner_ports: if True, will build the spiral, but expose the inner ports where the S-bend would be.
    """
    c = gf.Component()

    if with_inner_ports:
        bend_s_component = bend_s_factory(
            (straight_length, -min_radius * 2 + 1 * spacings[0]),
            cross_section=cross_section_s or cross_section,
            **({"nb_points": n_bend_points} if n_bend_points else {})
        )
        bend_s = type("obj", (object,), {"ports": bend_s_component.ports})
        c.info["length"] = 0
        c.add_port(
            "o3",
            center=bend_s.ports["o1"].center,
            orientation=0,
            cross_section=bend_s.ports["o1"].cross_section,
        )
        c.add_port(
            "o4",
            center=bend_s.ports["o2"].center,
            orientation=180,
            cross_section=bend_s.ports["o2"].cross_section,
        )
    else:
        bend_s = c << bend_s_factory(
            (straight_length, -min_radius * 2 + 1 * spacings[0]),
            cross_section=cross_section_s or cross_section,
            **({"nb_points": n_bend_points} if n_bend_points else {})
        )
        c.info["length"] = bend_s.info["length"]

    ports = []
    for port in bend_s.ports.values():
        for i in range(len(spacings)):
            bend = c << bend_factory(
                angle=180,
                radius=min_radius + np.sum(spacings[:i]),
                p=0,
                cross_section=cross_section,
                **({"npoints": n_bend_points} if n_bend_points else {}),
            )
            bend.connect("o1", port)

            straight = c << straight_factory(
                straight_length, cross_section=cross_section
            )
            straight.connect("o1", bend.ports["o2"])
            port = straight.ports["o2"]

            c.info["length"] += bend.info["length"] + straight.info["length"]
        ports.append(port)

    c.add_port("o1", port=ports[0])
    c.add_port("o2", port=ports[1])
    return c


@gf.cell
def spiral_racetrack_fixed_length(
    total_length: float = 1000,
    in_out_port_spacing: float = 150,
    n_straight_sections: int = 8,
    min_radius: float = 5,
    min_spacing: float = 5.0,
    straight_factory: ComponentFactory = straight,
    bend_factory: ComponentFactory = bend_euler,
    bend_s_factory: ComponentFactory = bend_s,
    cross_section: CrossSectionSpec = "strip",
    cross_section_s: CrossSectionSpec = None,
    n_bend_points: Optional[int] = None,
    with_inner_ports: bool = False,
) -> Component:
    """Returns Racetrack-Spiral with a specified total length.

    The input and output ports are aligned in y. This class is meant to
    be used for generating interferometers with long waveguide lengths, where
    the most important parameter is the length difference between the arms.

    Args:
        total_length: total length of the spiral from input to output ports in um.
        in_out_port_spacing: spacing between input and output ports of the spiral in um.
        n_straight_sections: total number of straight sections for the racetrack spiral. Has to be even.
        min_radius: smallest radius in um.
        min_spacing: minimum center-center spacing between adjacent waveguides.
        straight_factory: factory to generate the straight segments.
        bend_factory: factory to generate the bend segments.
        bend_s_factory: factory to generate the s-bend segments.
        cross_section: cross-section of the waveguides.
        cross_section_s: cross-section of the s bend waveguide (optional).
        n_bend_points: optional bend points.
        with_inner_ports: if True, will build the spiral, but expose the inner ports where the S-bend would be.
    """

    c = gf.Component()

    if np.mod(n_straight_sections, 2) != 0:
        raise ValueError("The number of straoght sections has to be even!")

    # First, we need to get the length of the straight sections to achieve the required length,
    # given the specified parameters
    spacings = [min_spacing] * (n_straight_sections // 2)

    straight_length = _req_straight_len(
        total_length,
        in_out_port_spacing,
        min_radius,
        spacings,
        bend_factory,
        bend_s_factory,
    )

    spiral = c << spiral_racetrack(
        min_radius=min_radius,
        straight_length=straight_length,
        spacings=spacings,
        straight_factory=straight_factory,
        bend_factory=bend_factory,
        bend_s_factory=bend_s_factory,
        cross_section=cross_section,
        cross_section_s=cross_section_s,
        n_bend_points=n_bend_points,
        with_inner_ports=with_inner_ports,
    )

    if spiral.ports["o1"].x > spiral.ports["o2"].x:
        spiral.mirror_x()

    # We need to add a bit more to the spiral racetrack to
    # make the in and out ports be aligned in y

    # Input waveguide
    in_wg = c << straight_factory(
        spiral.ports["o1"].x - spiral.xmin, cross_section=cross_section
    )
    in_wg.mirror_y()
    in_wg.connect("o2", spiral.ports["o1"])

    # Straight from "o2" to edge of spiral
    out_wg = c << straight_factory(
        spiral.xmax - spiral.ports["o2"].x, cross_section=cross_section
    )
    out_wg.connect("o1", spiral.ports["o2"])

    # S bend from out wg back to input height
    sbend_xspan = in_out_port_spacing - (out_wg.ports["o2"].x - in_wg.ports["o1"].x)
    final_sbend = c << bend_s_factory(
        (sbend_xspan, spiral.ports["o1"].y - spiral.ports["o2"].y),
        cross_section=cross_section_s or cross_section,
        **({"nb_points": n_bend_points} if n_bend_points else {})
    )

    final_sbend.connect("o1", out_wg.ports["o2"])

    # Ports
    c.add_port("o1", port=in_wg.ports["o1"])
    c.add_port("o2", port=final_sbend.ports["o2"])

    return c


def _req_straight_len(
    total_length: float = 1000,
    in_out_port_spacing: float = 100,
    min_radius: float = 5,
    spacings: Floats = (1.0, 1.0),
    bend_factory: ComponentFactory = bend_euler,
    bend_s_factory: ComponentFactory = bend_s,
):
    """Returns geometrical parameters to make a spiral of a given length.

    Args:
        total_length: total length of the spiral from input to output ports in um.
        in_out_port_spacing: spacing between input and output ports of the spiral in um.
        min_radius: smallest radius in um.
        spacings: spacings between adjacent waveguides.
        bend_factory: factory to generate the bend segments.
        bend_s_factory: factory to generate the s-bend segments.
    """

    # "Brute force" approach - sweep length and save total length

    lens = []

    straight_lengths = np.linspace(
        0.1 * in_out_port_spacing, 0.8 * in_out_port_spacing, 100
    )

    for str_len in straight_lengths:
        c = gf.Component()

        spiral = c << spiral_racetrack(
            min_radius=min_radius,
            straight_length=str_len,
            spacings=spacings,
            straight_factory=straight,
            bend_factory=bend_factory,
            bend_s_factory=bend_s_factory,
            cross_section="strip",
            cross_section_s="strip",
        )

        len = spiral.info["length"]

        # Input waveguide
        in_wg = c << straight(spiral.ports["o1"].x - spiral.xmin, cross_section="strip")
        in_wg.connect("o2", spiral.ports["o1"])
        len = len + spiral.ports["o1"].x - spiral.xmin

        # Straight from "o2" to edge of spiral
        out_wg = c << straight(
            spiral.xmax - spiral.ports["o2"].x, cross_section="strip"
        )
        out_wg.connect("o1", spiral.ports["o2"])
        len = len + spiral.xmax - spiral.ports["o2"].x

        # S bend from out wg back to input height
        sbend_xspan = in_out_port_spacing - (out_wg.ports["o2"].x - in_wg.ports["o1"].x)
        final_sbend = c << bend_s_factory(
            (sbend_xspan, spiral.ports["o1"].y - spiral.ports["o2"].y),
            cross_section="strip",
        )

        final_sbend.connect("o1", out_wg.ports["o2"])

        len = len + final_sbend.info["length"]

        lens.append(len)

    # plt.plot(straight_lengths, lens)
    # plt.show(block=True)

    # Now get the required spacing to achieve the required length (interpolate)
    f = interp1d(lens, straight_lengths)

    return f(total_length)


@gf.cell
def spiral_racetrack_heater_metal(
    min_radius: Optional[float] = None,
    straight_length: float = 30,
    spacing: float = 2,
    num: int = 8,
    straight_factory: ComponentFactory = straight,
    bend_factory: ComponentFactory = bend_euler,
    bend_s_factory: ComponentFactory = bend_s,
    waveguide_cross_section: CrossSectionSpec = "strip",
    heater_cross_section: CrossSectionSpec = "heater_metal",
) -> Component:
    """Returns spiral racetrack with a heater above.

    based on https://doi.org/10.1364/OL.400230 .

    Args:
        min_radius: smallest radius.
        straight_length: length of the straight segments.
        spacing: space between the center of neighboring waveguides.
        num: number.
        straight_factory: factory to generate the straight segments.
        bend_factory: factory to generate the bend segments.
        bend_s_factory: factory to generate the s-bend segments.
        waveguide_cross_section: cross-section of the waveguides.
        heater_cross_section: cross-section of the heater.
    """
    c = gf.Component()
    xs = gf.get_cross_section(waveguide_cross_section)
    min_radius = min_radius or xs.radius

    spiral = c << spiral_racetrack(
        min_radius,
        straight_length,
        (spacing,) * num,
        straight_factory,
        bend_factory,
        bend_s_factory,
        waveguide_cross_section,
    )

    heater_top = c << gf.components.straight(
        straight_length, cross_section=heater_cross_section
    )
    heater_top.connect("e1", spiral.ports["o1"].copy().rotate(180)).movey(
        spacing * num // 2
    )
    heater_bot = c << gf.components.straight(
        straight_length, cross_section=heater_cross_section
    )
    heater_bot.connect("e1", spiral.ports["o2"].copy().rotate(180)).movey(
        -spacing * num // 2
    )

    heater_bend = c << gf.components.bend_circular(
        angle=180,
        radius=min_radius + spacing * (num // 2 + 1),
        cross_section=heater_cross_section,
    )
    heater_bend.y = spiral.y
    heater_bend.x = spiral.x + min_radius + spacing * (num // 2 + 1)
    heater_top.connect("e1", heater_bend.ports["e1"])
    heater_bot.connect("e1", heater_bend.ports["e2"])

    c.add_ports(spiral.ports)
    c.add_port("e1", port=heater_bot["e2"])
    c.add_port("e2", port=heater_top["e2"])
    return c


@gf.cell
def spiral_racetrack_heater_doped(
    min_radius: Optional[float] = None,
    straight_length: float = 30,
    spacing: float = 2,
    num: int = 8,
    straight_factory: ComponentFactory = straight,
    bend_factory: ComponentFactory = bend_euler,
    bend_s_factory: ComponentFactory = bend_s,
    waveguide_cross_section: CrossSectionSpec = "strip",
    heater_cross_section: CrossSectionSpec = "npp",
) -> Component:
    """Returns spiral racetrack with a heater between the loops.

    based on https://doi.org/10.1364/OL.400230 but with the heater between the loops.

    Args:
        min_radius: smallest radius in um.
        straight_length: length of the straight segments in um.
        spacing: space between the center of neighboring waveguides in um.
        num: number.
        straight_factory: factory to generate the straight segments.
        bend_factory: factory to generate the bend segments.
        bend_s_factory: factory to generate the s-bend segments.
        waveguide_cross_section: cross-section of the waveguides.
        heater_cross_section: cross-section of the heater.
    """
    xs = gf.get_cross_section(waveguide_cross_section)
    min_radius = min_radius or xs.radius

    c = gf.Component()

    spiral = c << spiral_racetrack(
        min_radius=min_radius,
        straight_length=straight_length,
        spacings=(spacing,) * (num // 2)
        + (spacing + 1,) * 2
        + (spacing,) * (num // 2 - 2),
        straight_factory=straight_factory,
        bend_factory=bend_factory,
        bend_s_factory=bend_s_factory,
        cross_section=waveguide_cross_section,
    )

    heater_straight = gf.components.straight(
        straight_length, cross_section=heater_cross_section
    )

    heater_top = c << heater_straight
    heater_bot = c << heater_straight

    heater_bot.connect("e1", spiral.ports["o1"].copy().rotate(180)).movey(
        -spacing * (num // 2 - 1)
    )

    heater_top.connect("e1", spiral.ports["o2"].copy().rotate(180)).movey(
        spacing * (num // 2 - 1)
    )

    c.add_ports(spiral.ports)
    c.add_ports(prefix="top_", ports=heater_top.ports)
    c.add_ports(prefix="bot_", ports=heater_bot.ports)
    return c


if __name__ == "__main__":
    # heater = spiral_racetrack(
    #     min_radius=3.0, straight_length=30.0, spacings=(2, 2, 3, 3, 2, 2)
    # )
    # heater.show()

    # heater = spiral_racetrack_heater_metal(3, 30, 2, 5)
    # heater.show()

    # heater = spiral_racetrack_heater_doped(
    #     min_radius=3, straight_length=30, spacing=2, num=8
    # )
    # heater.show()
    # c = spiral_racetrack(with_inner_ports=True)
    c = spiral_racetrack_fixed_length(with_inner_ports=False)
    # c = spiral_racetrack_heater_doped()
    c.show(show_ports=True)
