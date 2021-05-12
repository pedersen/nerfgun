from enum import IntEnum, IntFlag, unique


# keyboard constants
@unique
class keytable(IntEnum):
    KEY_RESERVED = 0
    KEY_ESC = 41
    KEY_1 = 30
    KEY_2 = 31
    KEY_3 = 32
    KEY_4 = 33
    KEY_5 = 34
    KEY_6 = 35
    KEY_7 = 36
    KEY_8 = 37
    KEY_9 = 38
    KEY_0 = 39
    KEY_MINUS = 45
    KEY_EQUAL = 46
    KEY_BACKSPACE = 42
    KEY_TAB = 43
    KEY_Q = 20
    KEY_W = 26
    KEY_E = 8
    KEY_R = 21
    KEY_T = 23
    KEY_Y = 28
    KEY_U = 24
    KEY_I = 12
    KEY_O = 18
    KEY_P = 19
    KEY_LEFTBRACE = 47
    KEY_RIGHTBRACE = 48
    KEY_ENTER = 40
    KEY_LEFTCTRL = 224
    KEY_A = 4
    KEY_S = 22
    KEY_D = 7
    KEY_F = 9
    KEY_G = 10
    KEY_H = 11
    KEY_J = 13
    KEY_K = 14
    KEY_L = 15
    KEY_SEMICOLON = 51
    KEY_APOSTROPHE = 52
    KEY_GRAVE = 53
    KEY_LEFTSHIFT = 225
    KEY_BACKSLASH = 50
    KEY_Z = 29
    KEY_X = 27
    KEY_C = 6
    KEY_V = 25
    KEY_B = 5
    KEY_N = 17
    KEY_M = 16
    KEY_COMMA = 54
    KEY_DOT = 55
    KEY_SLASH = 56
    KEY_RIGHTSHIFT = 229
    KEY_KPASTERISK = 85
    KEY_LEFTALT = 226
    KEY_SPACE = 44
    KEY_CAPSLOCK = 57
    KEY_F1 = 58
    KEY_F2 = 59
    KEY_F3 = 60
    KEY_F4 = 61
    KEY_F5 = 62
    KEY_F6 = 63
    KEY_F7 = 64
    KEY_F8 = 65
    KEY_F9 = 66
    KEY_F10 = 67
    KEY_NUMLOCK = 83
    KEY_SCROLLLOCK = 71
    KEY_KP7 = 95
    KEY_KP8 = 96
    KEY_KP9 = 97
    KEY_KPMINUS = 86
    KEY_KP4 = 92
    KEY_KP5 = 93
    KEY_KP6 = 94
    KEY_KPPLUS = 87
    KEY_KP1 = 89
    KEY_KP2 = 90
    KEY_KP3 = 91
    KEY_KP0 = 98
    KEY_KPDOT = 99
    KEY_ZENKAKUHANKAKU = 148
    KEY_102ND = 100
    KEY_F11 = 68
    KEY_F12 = 69
    KEY_RO = 135
    KEY_KATAKANA = 146
    KEY_HIRAGANA = 147
    KEY_HENKAN = 138
    KEY_KATAKANAHIRAGANA = 136
    KEY_MUHENKAN = 139
    KEY_KPJPCOMMA = 140
    KEY_KPENTER = 88
    KEY_RIGHTCTRL = 228
    KEY_KPSLASH = 84
    KEY_SYSRQ = 70
    KEY_RIGHTALT = 230
    KEY_HOME = 74
    KEY_UP = 82
    KEY_PAGEUP = 75
    KEY_LEFT = 80
    KEY_RIGHT = 79
    KEY_END = 77
    KEY_DOWN = 81
    KEY_PAGEDOWN = 78
    KEY_INSERT = 73
    KEY_DELETE = 76
    KEY_MUTE = 239
    KEY_VOLUMEDOWN = 238
    KEY_VOLUMEUP = 237
    KEY_POWER = 102
    KEY_KPEQUAL = 103
    KEY_PAUSE = 72
    KEY_KPCOMMA = 133
    KEY_HANGEUL = 144
    KEY_HANJA = 145
    KEY_YEN = 137
    KEY_LEFTMETA = 227
    KEY_RIGHTMETA = 231
    KEY_COMPOSE = 101
    KEY_STOP = 243
    KEY_AGAIN = 121
    KEY_PROPS = 118
    KEY_UNDO = 122
    KEY_FRONT = 119
    KEY_COPY = 124
    KEY_OPEN = 116
    KEY_PASTE = 125
    KEY_FIND = 244
    KEY_CUT = 123
    KEY_HELP = 117
    KEY_CALC = 251
    KEY_SLEEP = 248
    KEY_WWW = 240
    KEY_COFFEE = 249
    KEY_BACK = 241
    KEY_FORWARD = 242
    KEY_EJECTCD = 236
    KEY_NEXTSONG = 235
    KEY_PLAYPAUSE = 232
    KEY_PREVIOUSSONG = 234
    KEY_STOPCD = 233
    KEY_REFRESH = 250
    KEY_EDIT = 247
    KEY_SCROLLUP = 245
    KEY_SCROLLDOWN = 246
    KEY_F13 = 104
    KEY_F14 = 105
    KEY_F15 = 106
    KEY_F16 = 107
    KEY_F17 = 108
    KEY_F18 = 109
    KEY_F19 = 110
    KEY_F20 = 111
    KEY_F21 = 112
    KEY_F22 = 113
    KEY_F23 = 114
    KEY_F24 = 115

# Map modifier keys to array element in the bit array
@unique
class modkeys(IntFlag):
    KEY_RIGHTMETA = 1
    KEY_RIGHTALT = 2
    KEY_RIGHTSHIFT = 3
    KEY_RIGHTCTRL = 4
    KEY_LEFTMETA = 5
    KEY_LEFTALT = 6
    KEY_LEFTSHIFT = 7
    KEY_LEFTCTRL = 8

KEY_DOWN_TIME = 0.01
KEY_DELAY = 0.01

# DBUS constants
DBUS_DOTTED_NAME = "org.thanhle.btkbservice"
DBUS_PATH_NAME = "/org/thanhle/btkbservice"
DBUS_OBJECT_MANAGER = "org.freedesktop.DBus.ObjectManager"
DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"

# bluetooth constants

INPUT_REPORT = 0xA1
KBD_EVENT = 1
MOUSE_EVENT = 2
UUID = "00001124-0000-1000-8000-00805f9b34fb"
P_CTRL = 17  # Service port - must match port configured in SDP record
P_INTR = 19  # Interrupt port - must match port configured in SDP record
DEV_NAME = "Raspberry Pi Custom Controller"
BUS_NAME = 'org.bluez'
BUS_NAME_PATH = '/org/bluez'
ADAPTER_INTERFACE = f"{BUS_NAME}.Adapter1"
DEVICE_INTERFACE = f"{BUS_NAME}.Device1"
PROFILE_MANAGER = f"{BUS_NAME}.ProfileManager1"
AGENT_INTERFACE = f'{BUS_NAME}.Agent1'
AGENT_MANAGER = f"{BUS_NAME}.AgentManager1"
AGENT_PATH = "/test/agent"
HCI_DEVICE = "/org/bluez/hci0"
sdp_record = """
<?xml version="1.0" encoding="UTF-8" ?>

<record>
	<attribute id="0x0001">
		<sequence>
			<uuid value="0x1124" />
		</sequence>
	</attribute>
	<attribute id="0x0004">
		<sequence>
			<sequence>
				<uuid value="0x0100" />
				<uint16 value="0x0011" />
			</sequence>
			<sequence>
				<uuid value="0x0011" />
			</sequence>
		</sequence>
	</attribute>
	<attribute id="0x0005">
		<sequence>
			<uuid value="0x1002" />
		</sequence>
	</attribute>
	<attribute id="0x0006">
		<sequence>
			<uint16 value="0x656e" />
			<uint16 value="0x006a" />
			<uint16 value="0x0100" />
		</sequence>
	</attribute>
	<attribute id="0x0009">
		<sequence>
			<sequence>
				<uuid value="0x1124" />
				<uint16 value="0x0100" />
			</sequence>
		</sequence>
	</attribute>
	<attribute id="0x000d">
		<sequence>
			<sequence>
				<sequence>
					<uuid value="0x0100" />
					<uint16 value="0x0013" />
				</sequence>
				<sequence>
					<uuid value="0x0011" />
				</sequence>
			</sequence>
		</sequence>
	</attribute>
	<attribute id="0x0100">
		<text value="Raspberry Pi Virtual Keyboard" />
	</attribute>
	<attribute id="0x0101">
		<text value="USB > BT Keyboard" />
	</attribute>
	<attribute id="0x0102">
		<text value="Raspberry Pi" />
	</attribute>
	<attribute id="0x0200">
		<uint16 value="0x0100" />
	</attribute>
	<attribute id="0x0201">
		<uint16 value="0x0111" />
	</attribute>
	<attribute id="0x0202">
		<uint8 value="0xC0" />
	</attribute>
	<attribute id="0x0203">
		<uint8 value="0x00" />
	</attribute>
	<attribute id="0x0204">
		<boolean value="false" />
	</attribute>
	<attribute id="0x0205">
		<boolean value="false" />
	</attribute>
	<attribute id="0x0206">
		<sequence>
			<sequence>
				<uint8 value="0x22" />
				<text encoding="hex" value="05010906a101850175019508050719e029e715002501810295017508810395057501050819012905910295017503910395067508150026ff000507190029ff8100c005010902a10185020901a100950575010509190129051500250181029501750381017508950305010930093109381581257f8106c0c0" />
			</sequence>
		</sequence>
	</attribute>
	<attribute id="0x0207">
		<sequence>
			<sequence>
				<uint16 value="0x0409" />
				<uint16 value="0x0100" />
			</sequence>
		</sequence>
	</attribute>
	<attribute id="0x020b">
		<uint16 value="0x0100" />
	</attribute>
	<attribute id="0x020c">
		<uint16 value="0x0c80" />
	</attribute>
	<attribute id="0x020d">
		<boolean value="false" />
	</attribute>
	<attribute id="0x020e">
		<boolean value="false" />
	</attribute>
	<attribute id="0x020f">
		<uint16 value="0x0640" />
	</attribute>
	<attribute id="0x0210">
		<uint16 value="0x0320" />
	</attribute>
</record>
"""
