"""
Utilities to create a user-defined name for a GeoServer component, with optional
validation.
"""

from PyQt4 import QtGui, QtCore

APP = None
if __name__ == '__main__':
    import sys
    # instantiate QApplication before importing QtGui subclasses
    APP = QtGui.QApplication(sys.argv)

from opengeo.gui.contextualhelp import InfoIcon


# noinspection PyPep8Naming
def xmlNameFixUp(name):
    return name.lower().replace(' ', '_')


# noinspection PyPep8Naming
def xmlNameRegex():
    # return r'^(?!XML)[a-z][\w0-9-\.]'
    # return r'^(?!XML|\d|\W)\S+'
    return r'^(?!XML|\d|\W)[a-z]\S*'


# noinspection PyPep8Naming
def xmlNameRegexMsg():
    return (
        'Text must be a valid XML name:\n\n'
        '* Can contain letters, numbers, and other characters\n'
        '* Cannot start with a number or punctuation character\n'
        '* Cannot start with the letters \'xml\' (case-insensitive)\n'
        '* Cannot contain spaces'
    )


# noinspection PyAttributeOutsideInit, PyPep8Naming
class GSNameWidget(QtGui.QWidget):

    nameValidityChanged = QtCore.pyqtSignal(bool)

    def __init__(self, name='', namemsg='', nameregex='', nameregexmsg='',
                 names=None, uniquename=False, maxlength=0, parent=None):
        super(GSNameWidget, self).__init__(parent)
        self.name = name
        self.namemsg = namemsg
        self.nameregex = nameregex
        self.nameregexmsg = nameregexmsg if nameregex else ''
        self.names = names if names is not None else []
        self.hasnames = len(self.names) > 0
        self.uniquename = self.hasnames and uniquename
        self.maxlength = maxlength if maxlength >= 0 else 0  # no negatives
        self.valid = True  # False will not trigger signal for setEnabled slots
        self.initGui()
        self.validateName()
        
    def initGui(self):
        layout = QtGui.QHBoxLayout()
        layout.setMargin(0)
        layout.setSpacing(6)

        self.nameBox = QtGui.QComboBox(self)
        self.nameBox.setEditable(True)
        if self.hasnames:
            self.nameBox.addItems(self.names)
        self.nameBox.setCurrentIndex(-1)

        self.nameBox.lineEdit().setText(self.name)
        self.nameBox.lineEdit().textChanged.connect(self.validateName)
        self.nameValidityChanged.connect(self.highlightName)
        layout.addWidget(self.nameBox)

        tip = 'Define a{0}{1} name'.format(' valid' if self.nameregex else '',
                                           ' unique' if self.uniquename else '')
        if self.maxlength > 0:
            tip += ' <= {0} characters'.format(self.maxlength)
        if self.hasnames and not self.uniquename:
            tip += ' or choose from existing'

        if self.namemsg:
            if tip:
                tip += '\n\n'
            tip += self.namemsg

        if self.nameregexmsg:
            if tip:
                tip += '\n\n'
            tip += self.nameregexmsg

        if self.namemsg or self.nameregex or self.nameregexmsg or self.hasnames:
            infolabel = InfoIcon(tip, self)
            layout.addWidget(infolabel)

        self.setLayout(layout)

    def isValid(self):
        return self.valid

    def definedName(self):
        return unicode(self.nameBox.lineEdit().text()) if self.valid else None

    @QtCore.pyqtSlot()
    def validateName(self, name=None):
        if name is None:
            name = self.nameBox.lineEdit().text()
        curvalid = self.valid

        # no zero char names allowed
        valid = len(name) > 0

        # check if character limit reached
        if valid and self.maxlength > 0:
            valid = len(name) <= self.maxlength

        # validate regex, if defined
        if valid and self.nameregex:
            rx = QtCore.QRegExp(self.nameregex, 0)
            valid = rx.exactMatch(name)

        # crosscheck for unique name
        if valid and self.uniquename:
            valid = name not in self.names

        if curvalid != valid:
            self.valid = valid
            self.nameValidityChanged.emit(valid)

    @QtCore.pyqtSlot()
    def highlightName(self):
        self.nameBox.lineEdit().setStyleSheet(
            '' if self.valid else 'QLineEdit {color: rgb(200, 0, 0)}')


if __name__ == '__main__':
    gdlg = GSNameWidget(
        namemsg='Sample is generated from PostgreSQL connection name',
        name=xmlNameFixUp('My PG connection'),
        nameregex=xmlNameRegex(),
        nameregexmsg=xmlNameRegexMsg(),
        names=['name_one', 'name_two'],
        uniquename=True,
        maxlength=10)
    gdlg.show()
    gdlg.raise_()
    gdlg.activateWindow()
    sys.exit(APP.exec_())
