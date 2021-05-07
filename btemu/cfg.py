from pyhocon import ConfigFactory

from .constants import DEV_NAME, keytable, modkeys


class BtConfig:
    def __init__(self, fname):
        self.fname = fname
        self.conf = ConfigFactory.parse_file(self.fname)

    @property
    def devname(self):
        return self.conf.get_string('btemu.broadcast_dev_name', DEV_NAME)

    @property
    def keyboardpins(self):
        keytbl = {}
        modtbl = {}
        tree = self.conf.get('btemu.keyboard.pins')
        for key in tree:
            pin = int(key.replace('pin_', ''))
            key = tree.get(key).upper()
            code = keytable.get(f'KEY_{key}', None)
            if code is not None:
                keytbl[pin] = code
            code = modkeys.get(f'KEY_{key}', None)
            if code is not None:
                modtbl[pin] = code
        return keytbl, modtbl

    @property
    def mousepins(self):
        tbl = {}
        tree = self.conf.get('btemu.mouse.pins')
        for key in tree:
            pin = int(key.replace('pin_', ''))
            tbl[pin] = int(tree.get(key))
        return tbl

    @property
    def cycle(self):
        return 1000.0/float(self.conf.get('btemu.pollrate'))/1000.0  # number of ms between polling as part of a second

    @property
    def mouse_repeat(self):
        return float(self.conf.get('btemu.mouse-repeat'))/1000.0 # number of ms between repeat as part of a second