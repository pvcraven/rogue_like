import arcade

BRICK_WALL                     = arcade.LBWH(1*32, 1*32, 32, 32)
BRICK_WALL_WITH_BOTTOM_EDGE    = arcade.LBWH(1*32, 5*32, 32, 32)
BRICK_WALL_WITH_LEFT_EDGE      = arcade.LBWH(0*32, 1*32, 32, 32)
BRICK_WALL_WITH_RIGHT_EDGE     = arcade.LBWH(2*32, 1*32, 32, 32)
BRICK_WALL_WITH_TOP_EDGE       = arcade.LBWH(1*32, 0*32, 32, 32)
BRICK_WALL_WITH_BOTTOM_EDGE    = arcade.LBWH(1*32, 2*32, 32, 32)
BRICK_WALL_TOP_LEFT_CORNER     = arcade.LBWH(0*32, 0*32, 32, 32)
BRICK_WALL_TOP_RIGHT_CORNER    = arcade.LBWH(2*32, 0*32, 32, 32)
BRICK_WALL_BOTTOM_RIGHT_CORNER = arcade.LBWH(2*32, 2*32, 32, 32)
BRICK_WALL_BOTTOM_LEFT_CORNER  = arcade.LBWH(0*32, 2*32, 32, 32)
BRICK_WALL_TOP_NS_COLUMN       = arcade.LBWH(3*32, 0*32, 32, 32)
BRICK_WALL_MIDDLE_NS_COLUMN    = arcade.LBWH(3*32, 1*32, 32, 32)
BRICK_WALL_BOTTOM_NS_COLUMN    = arcade.LBWH(3*32, 2*32, 32, 32)
BRICK_WALL_LEFT_EW_COLUMN      = arcade.LBWH(0*32, 3*32, 32, 32)
BRICK_WALL_MIDDLE_EW_COLUMN    = arcade.LBWH(1*32, 3*32, 32, 32)
BRICK_WALL_RIGHT_EW_COLUMN     = arcade.LBWH(2*32, 3*32, 32, 32)
BRICK_WALL_TOP_BOTTOM_EDGE     = arcade.LBWH(1*32, 3*32, 32, 32)
BRICK_WALL_ONLY_LEFT           = arcade.LBWH(2*32, 3*32, 32, 32)
BRICK_WALL_ONLY_RIGHT          = arcade.LBWH(0*32, 3*32, 32, 32)
BRICK_WALL_CORNER_1            = arcade.LBWH(4*32, 0*32, 32, 32)
BRICK_WALL_CORNER_2            = arcade.LBWH(5*32, 0*32, 32, 32)
BRICK_WALL_CORNER_3            = arcade.LBWH(4*32, 1*32, 32, 32)
BRICK_WALL_CORNER_4            = arcade.LBWH(5*32, 1*32, 32, 32)
BRICK_WALL_CORNER_5            = arcade.LBWH(6*32, 0*32, 32, 32)
BRICK_WALL_SOLO                = arcade.LBWH(3*32, 3*32, 32, 32)
COLUMN_TURN_1                  = arcade.LBWH(4*32, 2*32, 32, 32)
COLUMN_TURN_2                  = arcade.LBWH(5*32, 2*32, 32, 32)
COLUMN_TURN_3                  = arcade.LBWH(6*32, 2*32, 32, 32)
COLUMN_TURN_4                  = arcade.LBWH(4*32, 3*32, 32, 32)
COLUMN_TURN_5                  = arcade.LBWH(5*32, 3*32, 32, 32)
COLUMN_TURN_6                  = arcade.LBWH(6*32, 3*32, 32, 32)
COLUMN_TURN_7                  = arcade.LBWH(4*32, 4*32, 32, 32)
COLUMN_TURN_8                  = arcade.LBWH(5*32, 4*32, 32, 32)
COLUMN_TURN_9                  = arcade.LBWH(6*32, 4*32, 32, 32)
EW_CORNER_1                    = arcade.LBWH(0*32, 4*32, 32, 32)
EW_CORNER_2                    = arcade.LBWH(1*32, 4*32, 32, 32)
EW_CORNER_3                    = arcade.LBWH(0*32, 5*32, 32, 32)
EW_CORNER_4                    = arcade.LBWH(1*32, 5*32, 32, 32)
NS_CORNER_1                    = arcade.LBWH(2*32, 4*32, 32, 32)
NS_CORNER_2                    = arcade.LBWH(3*32, 4*32, 32, 32)
NS_CORNER_3                    = arcade.LBWH(2*32, 5*32, 32, 32)
NS_CORNER_4                    = arcade.LBWH(3*32, 5*32, 32, 32)
CORNERS_NE_SE                  = arcade.LBWH(4*32, 5*32, 32, 32)
CORNERS_NW_SW                  = arcade.LBWH(5*32, 5*32, 32, 32)
CORNERS_NW_NE                  = arcade.LBWH(8*32, 2*32, 32, 32)
CORNERS_SW_SE                  = arcade.LBWH(8*32, 1*32, 32, 32)
CORNERS_NE_SE_SW               = arcade.LBWH(8*32, 4*32, 32, 32)
CORNERS_NW_SE                  = arcade.LBWH(7*32, 4*32, 32, 32)
UNKNOWN                        = arcade.LBWH(7*32, 2*32, 32, 32)
FLOOR_TILE_1                   = arcade.LBWH(8*32, 0*32, 32, 32)
FLOOR_TILE_2                   = arcade.LBWH(6*32, 4*32, 32, 32)

# Wall texture mapping dictionary
WALL_TEXTURE_MAP = {
    "inside_wall": BRICK_WALL,
    "top_edge": BRICK_WALL_WITH_TOP_EDGE,
    "bottom_edge": BRICK_WALL_WITH_BOTTOM_EDGE,
    "left_edge": BRICK_WALL_WITH_LEFT_EDGE,
    "right_edge": BRICK_WALL_WITH_RIGHT_EDGE,
    "top_left_corner": BRICK_WALL_TOP_LEFT_CORNER,
    "top_right_corner": BRICK_WALL_TOP_RIGHT_CORNER,
    "bottom_right_corner": BRICK_WALL_BOTTOM_RIGHT_CORNER,
    "bottom_left_corner": BRICK_WALL_BOTTOM_LEFT_CORNER,
    "top_ns_column": BRICK_WALL_TOP_NS_COLUMN,
    "middle_ns_column": BRICK_WALL_MIDDLE_NS_COLUMN,
    "bottom_ns_column": BRICK_WALL_BOTTOM_NS_COLUMN,
    "left_ew_column": BRICK_WALL_LEFT_EW_COLUMN,
    "middle_ew_column": BRICK_WALL_MIDDLE_EW_COLUMN,
    "right_ew_column": BRICK_WALL_RIGHT_EW_COLUMN,
    "corner_1": BRICK_WALL_CORNER_1,
    "corner_2": BRICK_WALL_CORNER_2,
    "corner_3": BRICK_WALL_CORNER_3,
    "corner_4": BRICK_WALL_CORNER_4,
    "column_turn_1": COLUMN_TURN_1,
    "column_turn_2": COLUMN_TURN_2,
    "column_turn_3": COLUMN_TURN_3,
    "column_turn_4": COLUMN_TURN_4,
    "column_turn_5": COLUMN_TURN_5,
    "column_turn_6": COLUMN_TURN_6,
    "column_turn_7": COLUMN_TURN_7,
    "column_turn_8": COLUMN_TURN_8,
    "column_turn_9": COLUMN_TURN_9,
    "ew_corner_1": EW_CORNER_1,
    "ew_corner_2": EW_CORNER_2,
    "ew_corner_3": EW_CORNER_3,
    "ew_corner_4": EW_CORNER_4,
    "ns_corner_1": NS_CORNER_1,
    "ns_corner_2": NS_CORNER_2,
    "ns_corner_3": NS_CORNER_3,
    "ns_corner_4": NS_CORNER_4,
    "corners_ne_se": CORNERS_NE_SE,
    "corners_nw_sw": CORNERS_NW_SW,
    "corners_nw_ne": CORNERS_NW_NE,
    "corners_sw_se": CORNERS_SW_SE,
    "corners_ne_se_sw": CORNERS_NE_SE_SW,
    "corners_nw_se": CORNERS_NW_SE,
    "solo": BRICK_WALL_SOLO,
}
