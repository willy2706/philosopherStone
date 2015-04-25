package com.sisteritb.philosopherstone;

import com.sisteritb.philosopherstone.connection.PhilosopherStoneServer;

public class GameState {
    public static PhilosopherStoneServer philosopherStoneServer;
    public static String loginToken;
    public static long location_x, location_y;
    public static long arrivedTime;
    public static long syncTime;
    public static boolean USE_STUB = false;
}
