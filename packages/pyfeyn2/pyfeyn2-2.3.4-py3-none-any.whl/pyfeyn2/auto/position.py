from pyfeyn2.feynmandiagram import Propagator
from pyfeyn2.interface.dot import dot_to_positions, feynman_to_dot


def auto_position(fd, layout="neato", clear_vertices=True):
    """Automatically position the vertices and legs."""
    # fd = scale_positions(fd, 10)
    fd = fd.with_style(f"layout : {layout}")
    fd = incoming_to_left(fd)
    fd = outgoing_to_right(fd)
    fd = feynman_adjust_points(fd, size=5, clear_vertices=clear_vertices)
    # fd = remove_unnecessary_vertices(fd)
    return fd


def incoming_to_left(fd):
    """Set the incoming legs to the left."""
    n = 0
    for l in fd.legs:
        if l.is_incoming():
            l.x = -2
            n = n + 1
    i = 0
    for l in fd.legs:
        if l.is_incoming():
            l.y = 4 / n * i
            i = i + 1

    return fd


def outgoing_to_right(fd):
    """Set the outgoing legs to the right."""
    n = 0
    for l in fd.legs:
        if not l.is_incoming():
            l.x = 2
            n = n + 1
    i = 0
    for l in fd.legs:
        if not l.is_incoming():
            l.y = 4 / n * i
            i = i + 1
    return fd


def scale_positions(fd, scale):
    """Scale the positions of the vertices and legs."""
    for v in fd.vertices:
        v.x *= scale
        v.y *= scale
    return fd


def feynman_adjust_points(feyndiag, size=5, clear_vertices=False):
    """Adjust the points of the vertices and legs using Dot language algorithms."""
    fd = feyndiag
    if clear_vertices:
        for v in fd.vertices:
            v.x = None
            v.y = None
    norm = size
    dot = feynman_to_dot(fd, resubstituteslash=False)
    positions = dot_to_positions(dot)
    mmax = 0
    for _, p in positions.items():
        if p[0] > mmax:
            mmax = p[0]
        if p[1] > mmax:
            mmax = p[1]
    for v in fd.vertices:
        if v.id in positions:
            v.x = positions[v.id][0] / mmax * norm
            v.y = positions[v.id][1] / mmax * norm
    for l in fd.legs:
        l.x = positions[l.id][0] / mmax * norm
        l.y = positions[l.id][1] / mmax * norm
    return fd


def remove_unnecessary_vertices(feyndiag):
    """Remove vertices that are only connected to two vertices with the same propagator."""
    fd = feyndiag
    vertices = []
    for v in fd.vertices:
        ps = fd.get_connections(v)
        if (
            len(ps) == 2
            and ps[0].pdgid == ps[1].pdgid
            and isinstance(ps[0], Propagator)
            and isinstance(ps[1], Propagator)
        ):
            if ps[0].source == v.id and ps[1].target == v.id:
                ps[0].source = ps[1].source
                fd.remove_propagator(ps[1])
            elif ps[0].target == v.id and ps[1].source == v.id:
                ps[1].source = ps[0].source
                fd.remove_propagator(ps[0])
            else:
                raise Exception(
                    f"Unknown case, source == source or target == target, {v} {ps[0]} {ps[1]}"
                )
            continue
        vertices.append(v)
    fd.vertices = vertices
    return fd
