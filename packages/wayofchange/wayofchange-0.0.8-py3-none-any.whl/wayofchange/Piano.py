from Utility import Utility
from Change import Change
from Key import Key
from JazzNote import JazzNote
from Colour import Colour
import pyx,os,math
input = Utility.input

class Piano:
    height = 256
    fCircleVectorResolution = 64
    defaultVectorResolution = fCircleVectorResolution
    lineWidth = round(height / 64)
    lineWidthProportion = 1 / 64
    octaveWidthProportion = 2  # 1.8
    lineColour = (0, 0, 0, 255)
    lineColourInvert = (255, 255, 255, 255)
    indicationColour = (255, 255, 255, 255)
    indicationColourInvert = (255, 255, 255, 255)
    indicationLineColour = (0, 0, 0, 255)  # (128,128,128,255)
    indicationLineColourInvert = (0, 0, 0, 255)  # (128,128,128,255)
    canvasBGColour = (255, 255, 255, 0)
    blackKeyProportion = 0.61832  # 0.56
    evenlySpacedWhites = True
    if evenlySpacedWhites:
        CtoEWhites = 35
        FtoBWhites = 35
        CtoEBlacks = 21
        FtoBBlacks = 20
    elif not evenlySpacedWhites:
        # Evenly-spaced blacks
        CtoEWhites = 20
        FtoBWhites = 21
        CtoEBlacks = 12
        FtoBBlacks = 12

    def __init__(
        self,
        keyboardHeightPx=None,
        octaveWidthProportion=None,
        lineColour=None,
        lineWidthProportion=1 / 64,
        canvasBGColour=None,
        blackKeyProportion=None,  # 0.61832
        evenlySpacedWhites=None,
    ):

        if keyboardHeightPx is None:
            self.height = Piano.height
        else:
            self.height = keyboardHeightPx
        if octaveWidthProportion is None:
            self.octaveWidthProportion = Piano.octaveWidthProportion
        else:
            self.octaveWidthProportion = octaveWidthProportion
        if lineColour is None:
            self.lineColour = Piano.lineColour
        else:
            self.lineColour = lineColour
        if canvasBGColour is None:
            self.canvasBGColour = Piano.canvasBGColour
        else:
            self.canvasBGColour = canvasBGColour
        if blackKeyProportion is None:
            self.blackKeyProportion = Piano.blackKeyProportion
        else:
            self.blackKeyProportion = blackKeyProportion
        if evenlySpacedWhites is None:
            self.evenlySpacedWhites = Piano.evenlySpacedWhites
        else:
            self.evenlySpacedWhites = evenlySpacedWhites
        if lineWidthProportion is None:
            self.lineWidthProportion = Piano.lineWidthProportion
        else:
            self.lineWidthProportion = lineWidthProportion
        if evenlySpacedWhites:
            self.CtoEWhites = 35
            self.FtoBWhites = 35
            self.CtoEBlacks = 21
            self.FtoBBlacks = 20
        elif not evenlySpacedWhites:
            # Evenly-spaced blacks
            self.CtoEWhites = 20
            self.FtoBWhites = 21
            self.CtoEBlacks = 12
            self.FtoBBlacks = 12
        _octaveWidthBefore = 3 * self.CtoEWhites + 4 * self.FtoBWhites
        self.octaveWidth = round(self.height) * self.octaveWidthProportion
        _resProportion = self.octaveWidth / _octaveWidthBefore
        self.CtoEWhites = round(self.CtoEWhites * _resProportion)
        self.FtoBWhites = round(self.FtoBWhites * _resProportion)
        self.CtoEBlacks = round(self.CtoEBlacks * _resProportion)
        self.FtoBBlacks = round(self.FtoBBlacks * _resProportion)
        self.blackKeyLength = round(self.height * self.blackKeyProportion)

        self.lineWidth = round(self.height * self.lineWidthProportion)

    def insertGraphic(
        self,
        change: Change,
        key: str,
        resolution=None,
        greyScale=None,
        filetype="pdf",
        includeFiletypeExtension=False,
    ):
        if resolution is None:
            if filetype == "png":
                resolution = Piano.height
            else:
                resolution = Piano.defaultVectorResolution
        if greyScale is None:
            greyScale = not Colour.makeGraphicsColoured
        _filename = Piano.getPianoPath(
            change,
            key,
            resolution,
            greyScale=greyScale,
            includeGraphicsPath=not Latex.useRelativeGraphicsPath,
            filetype=filetype,
            includeFiletypeExtension=includeFiletypeExtension,
        )
        latexCommand = (
            Latex.commandStrings["Small Piano Command Start"]
            if filetype != "svg"
            else Latex.commandStrings["Small Piano Command Start Svg"]
        )
        return (
            latexCommand + _filename + Latex.commandStrings["Small Piano Command End"]
        )

    def makePianoFiles(
        self,
        changes: [Change],
        keys: [str],
        voicingType="Scale",
        startingKey=None,
        greyScale=False,
        alwaysFromCorF=False,
        invertColour=True,
        showDebug=False,
        indicateNotesWithDiagramType=False,
        makeNewIndicatorDiagrams=False,
        filetypes=["png"],
    ): #TODO: Make it support non fcircle. indicatorDiagramType does nothing currently

        # _polys = {}
        from Graphics import Graphics
        if changes == None:
            changes = range(-2048,2049)
        _useVector = any([f in Graphics.vectorFiletypes for f in filetypes])
        _useRaster = "png" in filetypes
        _startingKeyInitial = startingKey
        for key in keys:
            startingKey = _startingKeyInitial
            if alwaysFromCorF:
                if key in (
                    "C",
                    "Db",
                    "D",
                    "Eb",
                    "E",
                ):
                    startingKey = "C"
                    _totalKeys = 17
                else:
                    startingKey = "F"
                    _totalKeys = 19
            else:
                if startingKey == None:
                    startingKey = key
                else:
                    startingKey = key#raise ValueError('wtf {} {}'.format(startingKey,key))
                _totalKeys = 12
            if voicingType == "Thirds":
                _totalKeys += 12
            elif voicingType == 'Scale':
                pass
            else:
                raise ValueError('{} not a supported voicingType.'.format(voicingType))
            print(alwaysFromCorF,startingKey,_totalKeys)
            #input()
            # This is inefficient to have here
            _polys = self.getPianoKeyPolygons(
                startingKey=startingKey, totalKeys=_totalKeys
            )

            _pianoWidthPx = max([i for i in _polys[-1][::2]])
            fCircleCanvases = []
            fCircleCanvasesInv = []
            if indicateNotesWithDiagramType == False:
                pass
            else:
                for st in range(12):
                    #if True:
                    if any([st in Change.makeFromChangeNumber(c).getSemitones() for c in changes]):
                        print("rendering FCircle for piano")
                        fCircleCanvases.append(
                            Graphics.renderFCircle(
                                change=Change.makeFromSet([st]),
                                greyScale=greyScale,
                                invertColour=invertColour,
                                rootColourKey=key,
                                resolution=Piano.fCircleVectorResolution,
                                saveOnlyOneKey=True,
                                returnAsPyXCanvas=True,
                                filetypes=[],
                            )
                        )
                        fCircleCanvasesInv.append(
                            Graphics.renderFCircle(
                                change=Change.makeFromSet([st]),
                                greyScale=greyScale,
                                invertColour=not invertColour,
                                rootColourKey=key,
                                resolution=Piano.fCircleVectorResolution,
                                saveOnlyOneKey=True,
                                returnAsPyXCanvas=True,
                                filetypes=[],
                            )
                        )
                    else:
                        fCircleCanvases.append(None)
                        fCircleCanvasesInv.append(None)
            if type(changes[0]) == Change:
                changes = [c.getChangeNumber() for c in changes]
            for c in changes:
                
                change = Change.makeFromChangeNumber(c)
                if _useVector:
                    _c = pyx.canvas.canvas()

                if _useRaster:
                    _im = Image.new(
                        "RGBA",
                        (round(_pianoWidthPx), round(self.height)),
                        Piano.canvasBGColour,
                    )
                    _draw = ImageDraw.Draw(_im)

                self.drawPianoToIm(
                    im=_im if _useRaster else None,
                    canvas=_c if _useVector else None,
                    indicatorCanvasesSet=fCircleCanvases if (_useVector and indicateNotesWithDiagramType) else None,
                    indicatorCanvasesSetInv=fCircleCanvasesInv if (_useVector and indicateNotesWithDiagramType) else None,
                    change=change,
                    key=key,
                    octave=1,
                    startingKey=startingKey,
                    totalKeys=_totalKeys,
                    greyScale=greyScale,
                    invertColour=invertColour,
                    makeNewIndicatorDiagrams=makeNewIndicatorDiagrams,indicateNotesWithDiagramType=indicateNotesWithDiagramType,
                    voicingType=voicingType
                )

                for filetype in filetypes:
                    _fullname = Piano.getPianoPath(
                        change=change,
                        key=key,
                        resolution=self.defaultVectorResolution,
                        greyScale=greyScale,
                        invertColour=invertColour,
                        filetype=filetype,
                        voicingType=voicingType
                    )
                    _pathname = Piano.getPianoPath(
                        change=change,
                        key=key,
                        resolution=self.defaultVectorResolution,
                        greyScale=greyScale,
                        invertColour=invertColour,
                        includeFilename=False,
                        filetype=filetype,
                        voicingType=voicingType
                    )
                    if os.path.isdir(_pathname):
                        pass
                    else:
                        Utility.makeDirectory(_pathname)
                    if filetype == "png":
                        _im.save(_fullname)
                    else:
                        _finished = False
                        while not _finished:
                            try:
                                _c.writetofile(_fullname)
                                _finished = True
                            except PermissionError as e:
                                input(
                                    "{}\nTry to delete the file? If it does not work you may have to manually delete it. It may have gotten stuck. Windows thumbnail in exploror will do it if file is selected.".format(
                                        e
                                    )
                                )
                                if os.path.isfile(_fullname):
                                    os.remove(_fullname)
                                print("Removed the file.")

                    print(
                        "finished Making file:///"
                        + _fullname
                        + " . It used greyscale = {}, invertColour = {}".format(
                            greyScale, invertColour
                        )
                    )

    def drawPianoToIm(
        self,
        im,
        canvas: pyx.canvas.canvas,
        change: Change,
        key: Key,
        octave: int,
        startingKey: Key,
        totalKeys: int,
        greyScale,
        invertColour,
        voicingType: int = None,
        indicatorCanvasesSet: [pyx.canvas.canvas] = None,
        indicatorCanvasesSetInv: [pyx.canvas.canvas] = None,
        indicateNotesWithCircle=True,
        indicateNotesWithDiagramType=False,#"FCircle",
        showEachNoteOnce=True,
        makeBlackKeyIndicatorsAsBigAsWhites=True,
        showDebug=False,
        makeNewIndicatorDiagrams=False,
        useRadiusLines=True,
        fillInPartialKeys=True
    ):
        #assert type(change) == Change, 'fuck'
        
        if voicingType == 'Thirds':
            change = change.getVoicing(voicingType)
            #input(change)
        startingKey = Key(startingKey)
        if all([i == None for i in (im, canvas)]):
            raise ValueError("expecting im of type thingy or pyx.canvas")
        

        if canvas != None and len(change) > 0:
            if indicateNotesWithDiagramType not in (False,[]) and indicatorCanvasesSet == None:
                raise ValueError("Supply canvases for indicators.")
        canvas.layer("whiteKeys")
        canvas.layer("blackKeys")
        _useVector = canvas != None
        _useRaster = im != None
        _lineWidth = 3
        _startingDistFromC = Key(startingKey).distanceFromC()
        #input(key)
        _keyDistFromC = Key(key).distanceFromC()
        _colours = Colour.getTransposedColours(
            _startingDistFromC,
            greyScale=greyScale,
            invertColour=invertColour,
            pianoKeys=True,
        )

        _polys = self.getPianoKeyPolygons(startingKey=startingKey, totalKeys=totalKeys)
        _notes = [
            JazzNote.noteNameFlats[(i + _keyDistFromC) % 12]
            for i in change.getSemitones()
        ]
        # input('rah rah_polys {} \nlen \n{} \nkey {} \ndist from c{} \nnotes {}'.format(_polys,len(_polys),key,_keyDistFromC,_notes))
        if _useRaster:
            _draw = ImageDraw.Draw(im)
        if _useVector:
            _canvasScale = 1 / 48
            _lineWidthVec = pyx.style.linewidth(_canvasScale * 10)
            _lineWidthIndicatorCircleVec = pyx.style.linewidth(_canvasScale * 10 * 1)
            _trafo = pyx.trafo.scale(sx=_canvasScale, sy=-_canvasScale, x=0, y=0)
        _notesIndicated = 0
        _keysToIndicate = [
            i + _keyDistFromC - _startingDistFromC for i in change.getSemitones()
        ]
        _indicatorWhiteBoxes = []
        _indicatorBlackBoxes = []
        if not invertColour:
            _lineColour = Piano.lineColour
            _lineColourInvert = Piano.lineColourInvert
            _indicationColour = Piano.indicationColour
            _indicationColourInvert = Piano.indicationColourInvert
            _indicationLineColour = Piano.indicationLineColour
            _indicationLineColourInvert = Piano.indicationLineColourInvert
        else:
            _lineColour = Piano.lineColourInvert
            _lineColourInvert = Piano.lineColour
            _indicationColour = Piano.indicationColourInvert
            _indicationColourInvert = Piano.indicationColour
            _indicationLineColour = Piano.indicationLineColourInvert
            _indicationLineColourInvert = Piano.indicationLineColour
        _lineColourVec = pyx.color.rgb(
            _lineColour[0] / 255, _lineColour[1] / 255, _lineColour[2] / 255
        )
        _lineColourInvertVec = pyx.color.rgb(
            _lineColourInvert[0] / 255,
            _lineColourInvert[1] / 255,
            _lineColourInvert[2] / 255,
        )
        _indicationColourVec = pyx.color.rgb(
            _indicationColour[0] / 255,
            _indicationColour[1] / 255,
            _indicationColour[2] / 255,
        )
        _indicationColourInvertVec = pyx.color.rgb(
            _indicationColourInvert[0] / 255,
            _indicationColourInvert[1] / 255,
            _indicationColourInvert[2] / 255,
        )

        _indicationLineColourVec = pyx.color.rgb(
            _indicationLineColour[0] / 255,
            _indicationLineColour[1] / 255,
            _indicationLineColour[2] / 255,
        )
        _indicationLineColourInvertVec = pyx.color.rgb(
            _indicationLineColourInvert[0] / 255,
            _indicationLineColourInvert[1] / 255,
            _indicationLineColourInvert[2] / 255,
        )

        if fillInPartialKeys:
            def _partialKeyPath():
                polyPath = pyx.path.path()
                polyPath.append(pyx.path.moveto(_L, _T))
                polyPath.append(pyx.path.lineto(_L, _B))
                polyPath.append(pyx.path.lineto(_R, _B))
                polyPath.append(pyx.path.lineto(_R, _T))
                polyPath.append(pyx.path.closepath())
                return polyPath
            def _drawPartialWhiteKey():
                polyPath = _partialKeyPath()
                layCanvas = canvas.layer(
                    "whiteKeys",
                )

                layCanvas.stroke(
                    polyPath,
                    [
                        _lineWidthVec, _trafo, pyx.deco.stroked([_lineColourVec]),
                        pyx.deco.filled([_lineColourInvertVec]),
                    ],
                )
                return polyPath
            def _drawPartialBlackKey():
                polyPath = _partialKeyPath()
                layCanvas = canvas.layer(
                    "blackKeys",
                )

                layCanvas.stroke(
                    polyPath,
                    [
                        _lineWidthVec, _trafo, pyx.deco.stroked([_lineColourVec]),
                        pyx.deco.filled([_lineColourVec]),
                    ],
                )
                return polyPath

            # Right white key part
            if (startingKey + totalKeys - 1).isBlack():
                _L = max(_polys[-2][::2])
                _T = 0
                _B = max(_polys[totalKeys-2][1::2])
                if makeBlackKeyIndicatorsAsBigAsWhites == True:
                    _whitePoly = self.getPianoKeyPolygons(startingKey + totalKeys,1)[0]
                    _whiteW = max([i for i in _whitePoly[::2]]) - min(
                        [i for i in _whitePoly[::2]]
                    )
                    _R = (min(_polys[-1][::2]) + max(_polys[-1][::2])) / 2 + _whiteW /2
                else:
                    _R = max(_polys[totalKeys-2][::2])
                _drawPartialWhiteKey()
            # Left white key part
            if startingKey.isBlack():
                if makeBlackKeyIndicatorsAsBigAsWhites == True:
                    _whitePoly = _polys[1]
                    _whiteW = max([i for i in _whitePoly[::2]]) - min(
                        [i for i in _whitePoly[::2]]
                    )
                    _L = (min(_polys[0][::2]) + max(_polys[0][::2])) / 2 - _whiteW /2
                else:
                    _L = min(_polys[0][::2])

                #_L = -self.getPianoKeyPolygons(startingKey=startingKey-1, totalKeys=2)[1][::2]

                _R = min(_polys[1][::2])
                _T = 0
                _B = max(_polys[1][1::2])
                _drawPartialWhiteKey()
            # Right black key part
            if (startingKey + totalKeys ).isBlack():
                poly = _polys[-1]
                _L = Utility.secondBiggest(poly[::2])
                _R = max(poly[::2])
                _T = 0
                _B = Utility.secondBiggest(poly[1::2])
                _drawPartialBlackKey()
            #Left black key part
            if (startingKey - 1).isBlack():
                poly = self.getPianoKeyPolygons(startingKey - 1,1)[0]
                _T = 0
                _B = max(poly[1::2])
                _L = min(_polys[0][::2])
                _R = Utility.secondSmallest(_polys[0][::2])
                #input(_lineWidthVec)
                _drawPartialBlackKey()

        for idx, poly in enumerate(_polys):
            _note = JazzNote.noteNameFlats[(idx + _startingDistFromC) % 12]
            _note = Key(_note)

            # input(_note)

            ###DRAW KEYS
            if _useRaster:
                _draw.polygon(
                    poly,
                    fill=_colours[idx % 12],
                    outline=_lineColour,
                )
                Graphics.drawFatPolygonToIm(
                    im=im,
                    poly=poly,
                    outline=_lineColour,
                    width=_lineWidth,
                )
            if _useVector:

                polyPath = pyx.path.path()
                polyPath.append(pyx.path.moveto(poly[0], poly[1]))
                for p in range(2, len(poly), 2):
                    polyPath.append(pyx.path.lineto(poly[p], poly[p + 1]))

                polyPath.append(pyx.path.closepath())
                # input(_lineColour)

                # input('{} is whyte? {}'.format(_note,Key(_note).isWhite()))
                layCanvas = (
                    canvas.layer("whiteKeys")
                    if Key(_note).isWhite()
                    else canvas.layer(
                        "blackKeys",
                    )
                )

                layCanvas.stroke(
                    polyPath,
                    [
                        _lineWidthVec,
                        _trafo,
                        pyx.deco.stroked(
                            [_lineColourVec]
                            if Key(_note).isWhite()
                            else [_lineColourVec]
                        ),
                        pyx.deco.filled(
                            [_lineColourInvertVec]
                            if Key(_note).isWhite()
                            else [_lineColourVec]
                        ),
                    ],
                )

            if showDebug:
                print("_notes {} notes indicated {}".format(_notes, _notesIndicated))
            if (
                indicateNotesWithCircle
                and len(_notes) > 0
                and Key(_note) == Key(_notes[_notesIndicated % len(_notes)])
                and _notesIndicated < len(change)
            ):
                # print(len(change),'dfghdfghy')
                # input('this note {} is in {}'.format(_note, _notes))
                _iL = min([i for i in poly[::2]])
                _iR = max([i for i in poly[::2]])
                _iWidth = _iR - _iL
                _iB = max([i for i in poly[1::2]])
                _iT = _iB - _iWidth
                
                if _note.isWhite():
                    _indicatorWhiteBoxes.append(
                        {"L": _iL, "R": _iR, "T": _iT, "B": _iB, "N": _notesIndicated}
                    )
                    _notesIndicated += 1
                else:  # black note
                    if makeBlackKeyIndicatorsAsBigAsWhites == True:
                        if idx == 0:
                            _whitePoly = _polys[idx + 1]
                        else:
                            _whitePoly = _polys[idx - 1]
                        _whiteW = max([i for i in _whitePoly[::2]]) - min(
                            [i for i in _whitePoly[::2]]
                        )
                        _whiteDiff = (_whiteW - _iWidth) / 2
                        _iL -= _whiteDiff
                        _iR += _whiteDiff
                        _iT -= 2 * _whiteDiff
                        _iB += 0
                        _iWidth = _iR - _iL

                    _indicatorBlackBoxes.append(
                        {"L": _iL, "R": _iR, "T": _iT, "B": _iB, "N": _notesIndicated}
                    )
                    _notesIndicated += 1

        for indicators in [_indicatorBlackBoxes, _indicatorWhiteBoxes]:
            for indicator in indicators:
                _iL = indicator["L"]
                _iR = indicator["R"]
                _iT = indicator["T"]
                _iB = indicator["B"]
                _iN = indicator['N']
                #input(_iNote)
                _iWidth = _iR - _iL
                if indicators == _indicatorBlackBoxes:
                    _indicationColour = _indicationColour
                    _indicationLineColour = _indicationLineColour
                    _indicationColourVec = _indicationColourVec
                    _indicationLineColourVec = _indicationLineColourVec
                    _indicatorCanvasesSet = indicatorCanvasesSet

                else:
                    _indicationColour = _indicationColourInvert
                    _indicationLineColour = _indicationLineColourInvert
                    _indicationColourVec = _indicationColourInvertVec
                    _indicationLineColourVec = _indicationLineColourVec
                    _indicatorCanvasesSet = indicatorCanvasesSet  # Inv
                #input(indicateNotesWithDiagramType)
                if indicateNotesWithDiagramType in ([],False,None):
                    _indicationColour = Colour.getTransposedColours(
                        colourTranspose=Key(key).distanceFromC(),
                        greyScale=greyScale,neutralColours=True)[change[_iN].semitonesFromOne()]
                    #input(_indicationColour)
                    #input([i/255 for i in _indicationColour])
                    _indicationColourVec = pyx.color.rgb(_indicationColour[0]/255,
                                        _indicationColour[1]/255,
                                        _indicationColour[2]/255)
                    #input('indicator: {} _indicationColourVec: {}'.format(indicator, _indicationColour))

                    
                    
                
                if _useRaster:
                    _draw.ellipse(
                        [_iL, _iT, _iR, _iB],
                        fill=_indicationColour,
                        outline=_indicationLineColour,
                        width=_lineWidth,
                    )
                if _useVector:
                    # canvas.draw(pyx.path.circle((_iL+_iR)/2,(_iT+_iB)/2,_iWidth),
                    #            [_lineWidthVec,_trafo])

                    #print('iL iR',_iL,_iR)
                    _circleCanvas = pyx.canvas.canvas()
                    _circleCanvas.stroke(
                        pyx.path.circle((_iL + _iR) / 2, (_iT + _iB) / 2, _iWidth / 2),
                        [
                            _lineWidthIndicatorCircleVec,
                            _trafo,
                            pyx.deco.stroked(
                                [_lineColourVec]
                            ),
                            pyx.deco.filled(
                                [_indicationColourVec]

                            ),
                        ],
                    )
                    if useRadiusLines:
                        _noteChange = Change(change[_iN])
                        print(_iN)
                        #input(_noteChange)
                        _rad = abs(_iR - ((_iR + _iL) / 2))

                        _circleCanvas.stroke(pyx.path.line(
                            (_iR + _iL) / 2,
                            (_iT + _iB) / 2,
                            (_iR + _iL) / 2 + _rad * math.cos(
                                _noteChange.getAngles(returnDegrees=False, goQuarterTurnAnticlockwise=True)[0]),
                            (_iT + _iB) / 2 + _rad * math.sin(
                                _noteChange.getAngles(returnDegrees=False, goQuarterTurnAnticlockwise=True)[0]),
                        ),
                            [_lineWidthIndicatorCircleVec, pyx.style.linecap.round,
                             _trafo, _lineColourVec])
                    #print('iwidthvec :',_circleCanvas.bbox().right_pt() - _circleCanvas.bbox().left_pt())
                    _iWidthVec = (
                        _circleCanvas.bbox().right_pt() - _circleCanvas.bbox().left_pt()
                    )
                    # input(_iWidthVec)
                    canvas.insert(_circleCanvas)

                if indicateNotesWithDiagramType not in (None, [], False):

                    # _DiagramColourKey = key#JazzNote.noteNameFlats[(JazzNote.noteNameFlats.index(_note) )%12]# + _startingDistFromC

                    _changeToIndicate = Change(change.notes[indicator["N"]])
                    _distFromOne = _changeToIndicate[0].semitonesFromOne()
                    if _useVector:

                        _iCanvas = pyx.canvas.canvas()
                        _canvasWidth = (
                            canvas.bbox().left_pt() - canvas.bbox().right_pt()
                        )
                        # input(Key.allFlats[startingKey.distanceFromC()])

                        # _iTargetVectorWidth = _canvasWidth / _totalWhiteKeys

                        _iTranslateTrafo = pyx.trafo.translate(_iL, _iT)
                        _iCanvas.insert(
                            indicatorCanvasesSet[_distFromOne],
                            [_iTranslateTrafo,_trafo],
                        )
                        _iVectorWidth = (
                            _iCanvas.bbox().top_pt() - _iCanvas.bbox().bottom_pt()
                        )
                        _iScale = _iWidthVec / _iVectorWidth
                        #_iScale = _iVectorWidth/_iWidthVec 
                        _iScaleTrafo = pyx.trafo.scale(abs(_iScale), -abs(_iScale))
                        _iScaledCanvas = pyx.canvas.canvas()
                        _iScaledCanvas.insert(
                            _indicatorCanvasesSet[_distFromOne],
                            [
                                _iScaleTrafo,
                                _iTranslateTrafo,
                                _trafo
                            ],
                        )

                        # print(len(indicators),_iScaledCanvas.bbox().right_pt()-_iScaledCanvas.bbox().left_pt(),'is width')
                        if 0:

                            input(
                                "_iCanvas: {}, {} width: {}\ncanvas: {}, {} {} \n_iL: {}, _iR: {}".format(
                                    _iCanvas.bbox().top_pt(),
                                    _iCanvas.bbox().bottom_pt(),
                                    _iVectorWidth,
                                    canvas.bbox().top_pt(),
                                    canvas.bbox().bottom_pt(),
                                    _canvasWidth,
                                    _iL,
                                    _iR,
                                )
                            )

                        canvas = canvas.insert(_iScaledCanvas)
                        #canvas = canvas.insert(_iScaledCanvas,[_trafo])

                        """canvas.stroke(pyx.path.line(_iL, _iB,_iR, _iB) +
                                 pyx.path.line(_iR, _iB, _iR, _iT) +
                                 pyx.path.line(_iR, _iT, _iL, _iT) +
                                 pyx.path.line(_iL, _iT, _iL, _iB),[_trafo])"""
                        # print(change)
                        # input(_changeToIndicate)

                    if _useRaster:
                        _diagramPath = Graphics.getDiagramPath(
                            _changeToIndicate,
                            _FCircleColourKey,
                            int(_iWidth),
                            includeFilename=True,
                            greyScale=greyScale,
                            filetype="png",
                            diagramType=indicateNotesWithDiagramType,
                        )

                        if (not makeNewIndicatorDiagrams) and Graphics.seeIfDiagramExists(
                            _changeToIndicate,
                            _FCircleColourKey,
                            int(_iWidth),
                            greyScale=greyScale,
                            invertColour=invertColour,
                            impatientSkip=False,
                            filetype="png",
                            diagramType=indicateNotesWithDiagramType,
                        ):
                            pass
                        else:
                            # raise TypeError('{} Does not exist.'.format(_FCirclePath))
                            if makeNewDiagrams:
                                if diagramType == "FCircle":
                                    Graphics.renderFCircle(
                                        change=_changeToIndicate,
                                        resolution=int(_iWidth),
                                        rootColourKey="C",
                                        saveOnlyOneKey=False,
                                        filetypes=["png"],
                                    )
                                else:
                                    raise NotImplementedError(
                                        "change renderFCircle to Graphics.renderDiagram() once you make this"
                                    )
                            # raise TypeError('That FCircle don\'t exist: {}'.format(_FCirclePath))
                        _diagramFile = Image.open(_diagramPath).convert("RGBA")

                        im.paste(_diagramFile, (int(_iL), int(_iT)), _diagramFile)
                        # im.alpha_composite(_FCircleFile, dest=(int(_iL), int(_iT)), source=(0, 0))

                        # print('circle width'+str(_iWidth))
                        # print('just drew '+_FCirclePath+' '+' '.join([str(i) for i in [_iL,_iT,_iR,_iB]]))
        if _useRaster:
            # bottom line
            _draw.line(
                (0, self.height - _lineWidth / 2, 0, self.height - _lineWidth / 2),
                fill=_lineColour,
                width=_lineWidth,
            )
            # right line
            _draw.line(
                (
                    im.size[0] - _lineWidth / 2,
                    0,
                    im.size[0] - _lineWidth / 2,
                    self.height,
                ),
                fill=_lineColour,
                width=_lineWidth,
            )
            if showDebug:
                im.show()
            im = im.convert()
        returnDict = {}
        if _useRaster:
            returnDict["im"] = im
        if _useVector:
            returnDict["canvas"] = canvas
        return returnDict

    def getPianoKeyPolygons(
        self,
        startingKey: str,
        totalKeys: int,
    ) -> []:
        _keyPolys = []
        for keyname in (startingKey,):
            if keyname not in JazzNote.noteNameFlats:
                
                startingKey = Key(startingKey).inAllFlats().note
                #except:
                 #   raise TypeError("{} not in ".format(startingKey, JazzNote.noteNameFlats))
        # First we'll make it in C then we'll move it over
        # First lets make the first octave  of whites
        # C
        _Ckey = [
            0,
            0,
            0,
            self.height,
            self.CtoEWhites,
            self.height,
            self.CtoEWhites,
            self.blackKeyLength,
            self.CtoEBlacks,
            self.blackKeyLength,
            self.CtoEBlacks,
            0,
            0,
            0,
        ]
        # D
        _whiteL = self.CtoEWhites
        _whiteR = _whiteL + self.CtoEWhites
        _blackL = self.CtoEBlacks * 2
        _blackR = self.CtoEBlacks * 3

        _Dkey = [
            _blackL,
            0,
            _blackL,
            self.blackKeyLength,
            _whiteL,
            self.blackKeyLength,
            _whiteL,
            self.height,
            _whiteR,
            self.height,
            _whiteR,
            self.blackKeyLength,
            _blackR,
            self.blackKeyLength,
            _blackR,
            0,
            _blackL,
            0,
        ]
        # E
        _whiteL += self.CtoEWhites
        _whiteR = _whiteL + self.CtoEWhites
        _blackL += self.CtoEBlacks * 2
        # _blackR = _blackL + self.CtoEBlacks
        _Ekey = [
            _blackL,
            0,
            _blackL,
            self.blackKeyLength,
            _whiteL,
            self.blackKeyLength,
            _whiteL,
            self.height,
            _whiteR,
            self.height,
            _whiteR,
            0,
            _blackL,
            0,
        ]
        # F
        _whiteL += self.CtoEWhites
        _whiteR = _whiteL + self.FtoBWhites
        _blackL += self.CtoEBlacks * 2  # + self.FtoEBlacks
        # _blackR = _blackL + self.CtoEBlacks
        _Fkey = [
            _whiteL,
            0,
            _whiteL,
            self.height,
            _whiteR,
            self.height,
            _whiteR,
            self.blackKeyLength,
            _blackL,
            self.blackKeyLength,
            _blackL,
            0,
            _whiteL,
            0,
        ]
        # G
        _whiteL += self.FtoBWhites
        _whiteR = _whiteL + self.FtoBWhites
        _blackL += self.FtoBBlacks
        _blackR = _blackL + self.FtoBBlacks
        _Gkey = [
            _blackL,
            0,
            _blackL,
            self.blackKeyLength,
            _whiteL,
            self.blackKeyLength,
            _whiteL,
            self.height,
            _whiteR,
            self.height,
            _whiteR,
            self.blackKeyLength,
            _blackR,
            self.blackKeyLength,
            _blackR,
            0,
            _blackL,
            0,
        ]
        # A
        _whiteL += self.FtoBWhites
        _whiteR = _whiteL + self.FtoBWhites
        _blackL += self.FtoBBlacks * 2
        _blackR = _blackL + self.FtoBBlacks
        _Akey = [
            _blackL,
            0,
            _blackL,
            self.blackKeyLength,
            _whiteL,
            self.blackKeyLength,
            _whiteL,
            self.height,
            _whiteR,
            self.height,
            _whiteR,
            self.blackKeyLength,
            _blackR,
            self.blackKeyLength,
            _blackR,
            0,
            _blackL,
            0,
        ]
        # B
        _whiteL += self.FtoBWhites
        _whiteR = _whiteL + self.FtoBWhites
        _blackL += self.FtoBBlacks * 2
        # _blackR = _blackL + self.CtoEBlacks
        _Bkey = [
            _blackL,
            0,
            _blackL,
            self.blackKeyLength,
            _whiteL,
            self.blackKeyLength,
            _whiteL,
            self.height,
            _whiteR,
            self.height,
            _whiteR,
            0,
            _blackL,
            0,
        ]
        # Next make black keys
        # Db
        _blackL = self.CtoEBlacks
        _blackR = self.CtoEBlacks * 2
        _Dbkey = [
            _blackL,
            0,
            _blackL,
            self.blackKeyLength,
            _blackR,
            self.blackKeyLength,
            _blackR,
            0,
            _blackL,
            0,
        ]
        # Eb
        _blackL = self.CtoEBlacks * 3
        _blackR = self.CtoEBlacks * 4
        _Ebkey = [
            _blackL,
            0,
            _blackL,
            self.blackKeyLength,
            _blackR,
            self.blackKeyLength,
            _blackR,
            0,
            _blackL,
            0,
        ]
        # Gb
        _blackL = self.CtoEBlacks * 5 + self.FtoBBlacks
        _blackR = _blackL + self.FtoBBlacks
        _Gbkey = [
            _blackL,
            0,
            _blackL,
            self.blackKeyLength,
            _blackR,
            self.blackKeyLength,
            _blackR,
            0,
            _blackL,
            0,
        ]

        # Ab
        _blackL += self.FtoBBlacks * 2
        _blackR = _blackL + self.FtoBBlacks
        _Abkey = [
            _blackL,
            0,
            _blackL,
            self.blackKeyLength,
            _blackR,
            self.blackKeyLength,
            _blackR,
            0,
            _blackL,
            0,
        ]
        # Bb
        _blackL += self.FtoBBlacks * 2
        _blackR = _blackL + self.FtoBBlacks
        _Bbkey = [
            _blackL,
            0,
            _blackL,
            self.blackKeyLength,
            _blackR,
            self.blackKeyLength,
            _blackR,
            0,
            _blackL,
            0,
        ]

        # for key in (_Fkey,_Gbkey,):
        for idx, key in enumerate(
            (
                _Ckey,
                _Dbkey,
                _Dkey,
                _Ebkey,
                _Ekey,
                _Fkey,
                _Gbkey,
                _Gkey,
                _Abkey,
                _Akey,
                _Bbkey,
                _Bkey,
            )
        ):
            _keyName = JazzNote.noteNameFlats[idx]
            _keyPolys.append(key)
        _keyTransposition = JazzNote.noteNameFlats.index(startingKey)
        _xShift = min([x for x in _keyPolys[_keyTransposition][::2]])
        # print('xShift {}. startomgKey {}'.format(_xShift,startingKey))
        _firstPolys = _keyPolys[_keyTransposition:]
        _lastPolys = _keyPolys[0:_keyTransposition]
        for i in range(len(_firstPolys)):
            _poly = _firstPolys[i]
            for p, point in enumerate(_poly):
                if p % 2 == 0:
                    _poly[p] -= _xShift
            _firstPolys[i] = _poly
        for i in range(len(_lastPolys)):
            _poly = _lastPolys[i]
            for p, point in enumerate(_poly):
                if p % 2 == 0:
                    _poly[p] += -_xShift + self.octaveWidth
            _lastPolys[i] = _poly
        _keyPolys = _firstPolys + _lastPolys
        if totalKeys <= 12:
            return _keyPolys[:totalKeys]
        else:
            for nextKey in range(totalKeys - 12):
                _octavesUp = math.floor((nextKey + 12) / 12)
                _poly = _keyPolys[nextKey % 12][:]
                for p, point in enumerate(_poly):
                    if p % 2 == 0:
                        _poly[p] += self.octaveWidth * _octavesUp
                _keyPolys.append(_poly)
        # input('keypolys {}'.format(_keyPolys))
        return _keyPolys
        # return _firstPolys + _lastPolys
        # return _lastPolys

    @classmethod
    def getPianoPath(
        cls,
        change: Change,
        key: str,
        resolution: int = None,
        includeFilename=True,
        pathSeperator="/",
        greyScale=False,
        invertColour=False,
        filetype="pdf",
        includeFileExtension=True,
        includeGraphicsPath=True,
        externalGraphicsPath=False,
        voicingType=1
    ) -> str:

        if filetype == "pdf":
            if resolution == 256:
                raise ValueError("Piano only works in pdf at 64")
                print("256 not a valid resolution for Piano. Using 64")
        if resolution == None:
            resolution = Piano.defaultVectorResolution
        key = JazzNote.makeAlphabetNoteUseSingleFlats(key)


        _filename = "Piano"+("Thirds" if voicingType == 'Thirds' else '')+"_" + str(
            change.removeDuplicateNotes().getOctaveLimited().getChangeNumber(decorateChapter=False,)
        )
        from Graphics import Graphics
        if includeFileExtension:
            _filename += "." + filetype
        if greyScale:
            if invertColour:
                _path = Graphics.pianosBWInvDirectory
            else:
                _path = Graphics.pianosBWDirectory
        else:
            if invertColour:
                _path = Graphics.pianosInvDirectory
            else:
                _path = Graphics.pianosDirectory
        if externalGraphicsPath:
            _path = _path.replace(Graphics.directory, Graphics.directoryExternal)
        if not includeGraphicsPath:
            _path = "Piano"
        _path = os.path.join(_path,Graphics.getFiletypeResolutionFolderName(
            filetype=filetype, resolution=resolution
        ))
        _path = os.path.join(_path,key )

        # I did put key in filename
        if includeFilename:
            _str = os.path.join(_path , _filename)
        else:
            _str = _path
        _str = _str.replace("\\", pathSeperator)
        _str = _str.replace("/", pathSeperator)
        return _str