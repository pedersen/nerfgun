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
        tbl = {}
        tree = self.conf.get('btemu.keyboard.pins')
        for key in tree:
            pin = int(key.replace('pin_', ''))
            key = tree.get(key).upper()
            code = keytable.get(f'KEY_{key}', None)
            if code is None:
                code = modkeys.getf('KEY_{key}', None)
            if code is not None:
                tbl[pin] = code
        return tbl

    @property
    def mousepins(self):
        tbl = {}
        tree = self.conf.get('btemu.mouse.pins')
        for key in tree:
            pin = int(key.replace('pin_', ''))
            tbl[pin] = int(tree.get(key))
        return tbl
