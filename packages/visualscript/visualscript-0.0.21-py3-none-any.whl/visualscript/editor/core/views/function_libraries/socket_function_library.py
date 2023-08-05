import typing
import types
from PyQt5.QtGui import QPainterPath, QPainter, QBrush, QPen, QColor
from visualscript.editor.core.views.data_types import TYPE_COLORS, OBJECT_COLOR, UNION_COLOR


def setup_pen_and_brush(allowed_type, fill, painter, outline_width):
    if typing.get_origin(allowed_type):
        color_outline = UNION_COLOR
    else:
        color_outline = TYPE_COLORS[allowed_type] if TYPE_COLORS.__contains__(allowed_type) else OBJECT_COLOR
    if fill is not None:
        color_background = TYPE_COLORS[fill] if TYPE_COLORS.__contains__(fill) else OBJECT_COLOR
        painter.setBrush(QBrush(color_background))
    else:
        painter.setBrush(QBrush((QColor("#FF000000"))))
    painter.setPen(QPen(color_outline, outline_width))

def CircleSocketGraphics(socket, painter: QPainter, radius, outline_width):
    data_type = socket.data_type

    if isinstance(data_type, types.UnionType):
        allowed_types = data_type.__args__
    else:
        allowed_types = [data_type]

    for i, allowed_type in enumerate(allowed_types):
        fill = socket.edges[0].start_socket.data_type if len(socket.edges) and socket.edges[0].start_socket else None
        setup_pen_and_brush(allowed_type, fill, painter, outline_width)
    radius = radius - outline_width//2
    painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)

def SquareSocketGraphics(socket, painter: QPainter, radius, outline_width):
    radius = radius - outline_width // 2
    fill = socket.edges[0].start_socket.data_type if len(socket.edges) else None
    setup_pen_and_brush(socket.data_type, fill, painter, outline_width)
    shape_path = QPainterPath()
    shape_path.moveTo(-radius, -radius)
    shape_path.lineTo(radius, -radius)
    shape_path.lineTo(radius, radius)
    shape_path.lineTo(-radius, radius)
    painter.drawPath(shape_path.simplified())

def TriangleSocketGraphics(socket, painter, radius, outline_width):
    radius = radius - outline_width // 2
    fill = socket.edges[0].start_socket.data_type if len(socket.edges) else None
    setup_pen_and_brush(socket.data_type, fill, painter, outline_width)
    shape_path = QPainterPath()
    shape_path.moveTo(radius, 0)
    shape_path.lineTo(-radius, -radius)
    shape_path.lineTo(-radius, radius)
    painter.drawPath(shape_path.simplified())
