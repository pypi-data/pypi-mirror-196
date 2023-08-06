from JazzNote import JazzNote
from Change import Change
from Fretboard import Fretboard
from Utility import Utility
from Graphics import Graphics
input = Utility.input
print = Utility.print
import math, PIL, os
from PIL import ImageDraw, Image
class Accordion:
    height = 256
    standard120buttons = True
    buttonsAcross = 20
    buttonMarginX = 0.618 / 2
    buttonMarginY = buttonMarginX
    canvasBGColour = (255, 255, 255, 0)
    buttonBGColour = (255, 255, 255, 255)
    buttonIndicatedBGColour = (0, 0, 0, 255)
    buttonOutlineColour = (0, 0, 0, 255)
    buttonIndicatedOutlineColour = (255, 255, 255, 255)
    rowOffsetByButtons = 0.333
    indicateNotes = ["C", "Eb", "Gb", "A"]
    indicateRow = 1
    if standard120buttons:
        buttonRows = [["Db"]]
        buttonRows = [
            [["Db"]],
            [["A"]],
            [["A", "C#", "E"]],
            [["A", "C", "E"]],
            [["A", "C#", "G"]],
            [["A", "C", "F#"]],
        ]

        for r, row in enumerate(buttonRows):
            # input('row {}'.format(row))
            for b in range(buttonsAcross):
                _firstButton = row[0]
                # input('b {} firstbutton {}'.format(b,_firstButton))
                if b != 0:
                    buttonRows[r].append([])
                    for note in _firstButton:
                        buttonRows[r][-1].append(
                            JazzNote.noteNameFlats[
                                (JazzNote.distanceFromC(note) + 7 * b) % 12
                            ]
                        )

        for row in buttonRows:
            print(row)
            print()
        print("generated accordion notes")

    @classmethod
    def getAccordionPath(
        cls,
        change: Change,
        key: str,
        greyScale,
        invertColour,
        returnName=True,
        returnDirectory=True,
        pathSeperator="/",
        resolution: int = None,
        filetype: str = "png",
        includeGraphicsDirectory=True,
        externalGraphicsPath=False,
        includeFileExtension=True,
    ) -> str:
        from Graphics import Graphics
        key = JazzNote.noteNameFlats[JazzNote.distanceFromC(key)]
        if resolution is None:
            resolution = Fretboard.height
        _str = ""
        if returnDirectory:
            if greyScale:
                if invertColour:
                    _str += Graphics.accordionsBWInvDirectory
                else:
                    _str += Graphics.accordionsBWDirectory
            else:
                if invertColour:
                    _str += Graphics.accordionsInvDirectory
                else:
                    _str += Graphics.accordionsDirectory
            if includeGraphicsDirectory:
                _str = os.path.join(_str,Graphics.getFiletypeResolutionFolderName(
                    filetype=filetype, resolution=resolution
                ))
                _str += "/" + key + "/"
                if externalGraphicsPath:
                    _str = _str.replace(Graphics.directory, Graphics.directoryExternal)
            else:
                _str = (
                    "Accordion/"
                    + Graphics.getFiletypeResolutionFolderName(
                        filetype=filetype, resolution=resolution
                    )
                    + "/"
                    + key
                    + "/"
                )
        if returnName:
            _str += "Accordion_{}".format(
                change.getChangeNumber(decorateChapter=False, addOneToBookPage=True),
            )
            if includeFileExtension:
                _str += "." + filetype
        _str = _str.replace("\\", pathSeperator)
        _str = _str.replace("/", pathSeperator)
        return _str

    @classmethod
    def renderAccordion(
        cls,
        change: Change,
        key: str,
        greyScale,
        invertColour,
        indicateNotesWithCircle=True,
        indicateNotesWithFCircle=True,
        showIm=False,
    ):
        Image = PIL.Image

        #raise TypeError("asdfasdf")
        _buttonHeight = 2 * Accordion.height / 12 / (1 + Accordion.buttonMarginY)
        _buttonWidth = _buttonHeight
        _imWidth = (_buttonWidth * (1 + Accordion.buttonMarginX)) * len(
            Accordion.buttonRows[0]
        )  # (Accordion.rowOffsetByButtons) * r
        _imWidth += (
            _buttonWidth
            * (Accordion.rowOffsetByButtons)
            * (len(Accordion.buttonRows) - 1)
        )
        # input('{}'.format(len(Accordion.buttonRows)))
        _im = Image.new(
            "RGBA", (round(_imWidth), round(Accordion.height)), Accordion.canvasBGColour
        )
        _draw = ImageDraw.Draw(_im)
        _buttonY = Accordion.buttonMarginY * _buttonHeight / 2
        _changeNotes = [
            JazzNote.noteNameFlats[JazzNote.distanceFromC(i)]
            for i in change.byWays(key)
        ]
        # input('pirateship {}'.format(_changeNotes))
        for r, row in enumerate(Accordion.buttonRows):
            _buttonX = (
                _buttonWidth * (Accordion.rowOffsetByButtons) * r
                + _buttonWidth * Accordion.buttonMarginX / 2
            )
            for button in row:

                if all(
                    [
                        JazzNote.noteNameFlats[JazzNote.distanceFromC(n)]
                        in _changeNotes
                        for n in button
                    ]
                ):
                    # print('button{} x{} y{}'.format(button, _buttonX, _buttonY))
                    # print('button {} key{} FCircle{}'.format(button,key,[JazzNote.distanceFromC(i) - JazzNote.distanceFromC(key) for i in button]))
                    _changeButton: Change = Change.makeFromSet(
                        [
                            (JazzNote.distanceFromC(i) - JazzNote.distanceFromC(key))
                            % 12
                            for i in button
                        ]
                    )
                    _changeButton = _changeButton.sortBySemitonePosition()
                    # print('changeButton',_changeButton)
                    if indicateNotesWithCircle:
                        _draw.ellipse(
                            (
                                _buttonX,
                                _buttonY,
                                _buttonX + _buttonWidth,
                                _buttonY + _buttonHeight,
                            ),
                            fill=Accordion.buttonIndicatedBGColour,
                            outline=Accordion.buttonIndicatedOutlineColour,
                        )

                    if indicateNotesWithFCircle:
                        Graphics.pasteFCircleOnIm(
                            im=_im,
                            xy=(
                                _buttonX,
                                _buttonY,
                                _buttonX + _buttonWidth,
                                _buttonY + _buttonHeight,
                            ),
                            change=_changeButton,
                            key=key,
                            greyScale=False,
                            invertColour=False,
                        )
                        # input('indicating.......')

                else:

                    _draw.ellipse(
                        (
                            _buttonX,
                            _buttonY,
                            _buttonX + _buttonWidth,
                            _buttonY + _buttonHeight,
                        ),
                        fill=Accordion.buttonBGColour,
                        outline=Accordion.buttonOutlineColour,
                    )
                _buttonX += _buttonWidth * (1 + Accordion.buttonMarginX)
            # _buttonX += _buttonWidth * (Accordion.rowOffsetByButtons)
            _buttonY += _buttonHeight * (1 + Accordion.buttonMarginY)
        _fullname = Accordion.getAccordionPath(
            change, key, greyScale, invertColour=invertColour
        )
        _pathname = Accordion.getAccordionPath(
            change, key, greyScale, invertColour=invertColour, returnName=False
        )
        if os.path.isdir(_pathname):
            pass
        else:
            Utility.makeDirectory(_pathname)
        print("saving {} to {}".format(_fullname, _pathname))
        _im.save(_fullname)
        Graphics.transposeColourSchemes(_im, _fullname, keyOrig=key)
        if showIm:
            _im.show()
        _im.save(_fullname)
        # Colour trranspose