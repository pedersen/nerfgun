#ifndef KEYBOARD_H
#define KEYBOARD_H

const byte KEY_RESERVED = 0;
const byte KEY_ESC = 41;
const byte KEY_1 = 30;
const byte KEY_2 = 31;
const byte KEY_3 = 32;
const byte KEY_4 = 33;
const byte KEY_5 = 34;
const byte KEY_6 = 35;
const byte KEY_7 = 36;
const byte KEY_8 = 37;
const byte KEY_9 = 38;
const byte KEY_0 = 39;
const byte KEY_MINUS = 45;
const byte KEY_EQUAL = 46;
const byte KEY_BACKSPACE = 42;
const byte KEY_TAB = 43;
const byte KEY_Q = 20;
const byte KEY_W = 26;
const byte KEY_E = 8;
const byte KEY_R = 21;
const byte KEY_T = 23;
const byte KEY_Y = 28;
const byte KEY_U = 24;
const byte KEY_I = 12;
const byte KEY_O = 18;
const byte KEY_P = 19;
const byte KEY_LEFTBRACE = 47;
const byte KEY_RIGHTBRACE = 48;
const byte KEY_ENTER = 40;
const byte KEY_LEFTCTRL = 224;
const byte KEY_A = 4;
const byte KEY_S = 22;
const byte KEY_D = 7;
const byte KEY_F = 9;
const byte KEY_G = 10;
const byte KEY_H = 11;
const byte KEY_J = 13;
const byte KEY_K = 14;
const byte KEY_L = 15;
const byte KEY_SEMICOLON = 51;
const byte KEY_APOSTROPHE = 52;
const byte KEY_GRAVE = 53;
const byte KEY_LEFTSHIFT = 225;
const byte KEY_BACKSLASH = 50;
const byte KEY_Z = 29;
const byte KEY_X = 27;
const byte KEY_C = 6;
const byte KEY_V = 25;
const byte KEY_B = 5;
const byte KEY_N = 17;
const byte KEY_M = 16;
const byte KEY_COMMA = 54;
const byte KEY_DOT = 55;
const byte KEY_SLASH = 56;
const byte KEY_RIGHTSHIFT = 229;
const byte KEY_KPASTERISK = 85;
const byte KEY_LEFTALT = 226;
const byte KEY_SPACE = 44;
const byte KEY_CAPSLOCK = 57;
const byte KEY_F1 = 58;
const byte KEY_F2 = 59;
const byte KEY_F3 = 60;
const byte KEY_F4 = 61;
const byte KEY_F5 = 62;
const byte KEY_F6 = 63;
const byte KEY_F7 = 64;
const byte KEY_F8 = 65;
const byte KEY_F9 = 66;
const byte KEY_F10 = 67;
const byte KEY_NUMLOCK = 83;
const byte KEY_SCROLLLOCK = 71;
const byte KEY_KP7 = 95;
const byte KEY_KP8 = 96;
const byte KEY_KP9 = 97;
const byte KEY_KPMINUS = 86;
const byte KEY_KP4 = 92;
const byte KEY_KP5 = 93;
const byte KEY_KP6 = 94;
const byte KEY_KPPLUS = 87;
const byte KEY_KP1 = 89;
const byte KEY_KP2 = 90;
const byte KEY_KP3 = 91;
const byte KEY_KP0 = 98;
const byte KEY_KPDOT = 99;
const byte KEY_ZENKAKUHANKAKU = 148;
const byte KEY_102ND = 100;
const byte KEY_F11 = 68;
const byte KEY_F12 = 69;
const byte KEY_RO = 135;
const byte KEY_KATAKANA = 146;
const byte KEY_HIRAGANA = 147;
const byte KEY_HENKAN = 138;
const byte KEY_KATAKANAHIRAGANA = 136;
const byte KEY_MUHENKAN = 139;
const byte KEY_KPJPCOMMA = 140;
const byte KEY_KPENTER = 88;
const byte KEY_RIGHTCTRL = 228;
const byte KEY_KPSLASH = 84;
const byte KEY_SYSRQ = 70;
const byte KEY_RIGHTALT = 230;
const byte KEY_HOME = 74;
const byte KEY_UP = 82;
const byte KEY_PAGEUP = 75;
const byte KEY_LEFT = 80;
const byte KEY_RIGHT = 79;
const byte KEY_END = 77;
const byte KEY_DOWN = 81;
const byte KEY_PAGEDOWN = 78;
const byte KEY_INSERT = 73;
const byte KEY_DELETE = 76;
const byte KEY_MUTE = 239;
const byte KEY_VOLUMEDOWN = 238;
const byte KEY_VOLUMEUP = 237;
const byte KEY_POWER = 102;
const byte KEY_KPEQUAL = 103;
const byte KEY_PAUSE = 72;
const byte KEY_KPCOMMA = 133;
const byte KEY_HANGEUL = 144;
const byte KEY_HANJA = 145;
const byte KEY_YEN = 137;
const byte KEY_LEFTMETA = 227;
const byte KEY_RIGHTMETA = 231;
const byte KEY_COMPOSE = 101;
const byte KEY_STOP = 243;
const byte KEY_AGAIN = 121;
const byte KEY_PROPS = 118;
const byte KEY_UNDO = 122;
const byte KEY_FRONT = 119;
const byte KEY_COPY = 124;
const byte KEY_OPEN = 116;
const byte KEY_PASTE = 125;
const byte KEY_FIND = 244;
const byte KEY_CUT = 123;
const byte KEY_HELP = 117;
const byte KEY_CALC = 251;
const byte KEY_SLEEP = 248;
const byte KEY_WWW = 240;
const byte KEY_COFFEE = 249;
const byte KEY_BACK = 241;
const byte KEY_FORWARD = 242;
const byte KEY_EJECTCD = 236;
const byte KEY_NEXTSONG = 235;
const byte KEY_PLAYPAUSE = 232;
const byte KEY_PREVIOUSSONG = 234;
const byte KEY_STOPCD = 233;
const byte KEY_REFRESH = 250;
const byte KEY_EDIT = 247;
const byte KEY_SCROLLUP = 245;
const byte KEY_SCROLLDOWN = 246;
const byte KEY_F13 = 104;
const byte KEY_F14 = 105;
const byte KEY_F15 = 106;
const byte KEY_F16 = 107;
const byte KEY_F17 = 108;
const byte KEY_F18 = 109;
const byte KEY_F19 = 110;
const byte KEY_F20 = 111;
const byte KEY_F21 = 112;
const byte KEY_F22 = 113;
const byte KEY_F23 = 114;
const byte KEY_F24 = 115;

const byte MOD_RIGHTMETA  = 0x01;
const byte MOD_RIGHTALT   = 0x02;
const byte MOD_RIGHTSHIFT = 0x04;
const byte MOD_RIGHTCTRL  = 0x08;
const byte MOD_LEFTMETA   = 0x10;
const byte MOD_LEFTALT    = 0x20;
const byte MOD_LEFTSHIFT  = 0x40;
const byte MOD_LEFTCTRL   = 0x80;

#endif