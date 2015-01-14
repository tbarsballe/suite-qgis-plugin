"""
Dialog to create a user-defined name for a GeoServer component, with optional
validation.
"""

from PyQt4 import QtGui

APP = None
if __name__ == '__main__':
    import sys
    # instantiate QApplication before importing QtGui subclasses
    APP = QtGui.QApplication(sys.argv)

from opengeo.gui.gsnameutils import GSNameWidget


# noinspection PyAttributeOutsideInit, PyPep8Naming
class GSNameDialog(QtGui.QDialog):

    def __init__(self, nametitle="", name='', namemsg='',
                 nameregex='', nameregexmsg='', names=None,
                 uniquename=False, maxlength=0, parent=None):
        super(GSNameDialog, self).__init__(parent)
        self.nametitle = nametitle
        self.nameBox = GSNameWidget(
            name=name,
            namemsg=namemsg,
            nameregex=nameregex,
            nameregexmsg=nameregexmsg,
            names=names,
            uniquename=uniquename,
            maxlength=maxlength
        )
        self.initGui()

    def initGui(self):
        self.setWindowTitle('Define name')
        vertlayout = QtGui.QVBoxLayout()

        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setTitle(self.nametitle)
        self.groupBox.setLayout(vertlayout)

        self.groupBox.layout().addWidget(self.nameBox)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.okButton = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

        self.nameBox.nameValidityChanged.connect(self.okButton.setEnabled)

        # noinspection PyUnresolvedReferences
        self.buttonBox.accepted.connect(self.accept)
        # noinspection PyUnresolvedReferences
        self.buttonBox.rejected.connect(self.reject)

        self.setMinimumWidth(240)

        # do intial validation
        self.okButton.setEnabled(self.nameBox.isValid())

    def definedName(self):
        return self.nameBox.definedName()


if __name__ == '__main__':
    from opengeo.gui.gsnameutils import \
        xmlNameFixUp,  xmlNameRegex, xmlNameRegexMsg
    gdlg = GSNameDialog(
        nametitle='GeoServer data store name',
        namemsg='Sample is generated from PostgreSQL connection name.',
        name=xmlNameFixUp('My PG connection'),
        nameregex=xmlNameRegex(),
        nameregexmsg=xmlNameRegexMsg(),
        names=['name_one', 'name_two'],
        uniquename=False,
        maxlength=10)
    gdlg = GSNameDialog()
    if gdlg.exec_():
        print gdlg.definedName()
    # gdlg.show()
    # gdlg.raise_()
    # gdlg.activateWindow()
    # sys.exit(APP.exec_())
