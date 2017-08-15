"""PyDM State Button Class."""

import numpy as _np
from pydm.PyQt.QtGui import QPainter, QStyleOption, QAbstractButton
from pydm.PyQt.QtCore import (pyqtSignal, pyqtSlot, pyqtProperty, Q_ENUMS,
                              QByteArray, QRectF, QSize)
from pydm.PyQt.QtSvg import QSvgRenderer
from pydm.widgets.channel import PyDMChannel


BUTTONSHAPE = {'Squared': 0, 'Rounded': 1}


class PyDMStateButton(QAbstractButton):
    """PyDM State Button Class."""

    __pyqtSignals__ = ("connected_signal()",
                       "disconnected_signal()",
                       "no_alarm_signal()",
                       "minor_alarm_signal()",
                       "major_alarm_signal()",
                       "invalid_alarm_signal()")

    # Emitted when the user changes the value.
    send_value_signal = pyqtSignal(int)
    send_waveform_signal = pyqtSignal(_np.ndarray)

    class buttonShapeMap:
        """Enum class of shapes of button."""

        locals().update(**BUTTONSHAPE)

    Q_ENUMS(buttonShapeMap)

    # enumMap for buttonShapeMap
    locals().update(**BUTTONSHAPE)

    squaredbuttonstatesdict = {
                            'On': """
                                  <svg
                                       xmlns:osb="http://www.openswatchbook.org/uri/2009/osb"
                                       xmlns:dc="http://purl.org/dc/elements/1.1/"
                                       xmlns:cc="http://creativecommons.org/ns#"
                                       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                                       xmlns:svg="http://www.w3.org/2000/svg"
                                       xmlns="http://www.w3.org/2000/svg"
                                       xmlns:xlink="http://www.w3.org/1999/xlink"
                                       xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
                                       xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
                                       width="256"
                                       height="129"
                                       viewBox="0 0 67.73248 34.13082"
                                       version="1.1"
                                       id="svg8"
                                       inkscape:version="0.92.1 unknown"
                                       sodipodi:docname="SquaredOnButton.svg">
                                      <defs
                                         id="defs2">
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="linearGradient7945">
                                          <stop
                                             style="stop-color:#02bb00;stop-opacity:1;"
                                             offset="0"
                                             id="stop7941" />
                                          <stop
                                             style="stop-color:#02dc00;stop-opacity:0"
                                             offset="1"
                                             id="stop7943" />
                                        </linearGradient>
                                        <linearGradient
                                           id="linearGradient46973"
                                           osb:paint="gradient">
                                          <stop
                                             style="stop-color:#000000;stop-opacity:1;"
                                             offset="0"
                                             id="stop46969" />
                                          <stop
                                             style="stop-color:#000000;stop-opacity:0;"
                                             offset="1"
                                             id="stop46971" />
                                        </linearGradient>
                                        <linearGradient
                                           id="linearGradient46862"
                                           osb:paint="solid">
                                          <stop
                                             style="stop-color:#ececec;stop-opacity:1;"
                                             offset="0"
                                             id="stop46860" />
                                        </linearGradient>
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient7945"
                                           id="radialGradient44460"
                                           cx="27.781246"
                                           cy="262.60416"
                                           fx="27.781246"
                                           fy="262.60416"
                                           r="33.337498"
                                           gradientTransform="matrix(1.265934,0.00400069,-0.00133016,0.41922258,-7.0386749,169.37154)"
                                           gradientUnits="userSpaceOnUse" />
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119-6"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.214836"
                                           y2="256.65088"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.0160315,0,0,0.99800908,-2.3970673,17.666294)" />
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="linearGradient47117">
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:1;"
                                             offset="0"
                                             id="stop47113" />
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:0;"
                                             offset="1"
                                             id="stop47115" />
                                        </linearGradient>
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.067112"
                                           y2="255.32812"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.0160706,0,0,0.99800796,-85.934367,-541.14776)" />
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient7945"
                                           id="radialGradient7947"
                                           cx="27.781244"
                                           cy="279.53748"
                                           fx="27.781244"
                                           fy="279.53748"
                                           r="33.072918"
                                           gradientTransform="matrix(1.2760614,0.00403273,-0.0013408,0.42257607,-7.2945254,161.33439)"
                                           gradientUnits="userSpaceOnUse" />
                                      </defs>
                                      <sodipodi:namedview
                                         id="base"
                                         pagecolor="#ffffff"
                                         bordercolor="#666666"
                                         borderopacity="1.0"
                                         inkscape:pageopacity="0.0"
                                         inkscape:pageshadow="2"
                                         inkscape:zoom="1.4"
                                         inkscape:cx="-183.72506"
                                         inkscape:cy="27.966236"
                                         inkscape:document-units="px"
                                         inkscape:current-layer="layer1"
                                         showgrid="false"
                                         units="px"
                                         inkscape:window-width="1916"
                                         inkscape:window-height="1057"
                                         inkscape:window-x="1920"
                                         inkscape:window-y="0"
                                         inkscape:window-maximized="0" />
                                      <metadata
                                         id="metadata5">
                                        <rdf:RDF>
                                          <cc:Work
                                             rdf:about="">
                                            <dc:format>image/svg+xml</dc:format>
                                            <dc:type
                                               rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
                                            <dc:title></dc:title>
                                          </cc:Work>
                                        </rdf:RDF>
                                      </metadata>
                                      <g
                                         inkscape:label="Layer 1"
                                         inkscape:groupmode="layer"
                                         id="layer1"
                                         transform="translate(0,-262.86875)">
                                        <g
                                           id="g8126"
                                           transform="matrix(0.99996583,0,0,0.999987,6.0852108,0.00344901)">
                                          <rect
                                             ry="3.9920318"
                                             rx="4"
                                             y="263.20078"
                                             x="-6.0854187"
                                             height="33.799206"
                                             width="67.733337"
                                             id="rect42330"
                                             style="opacity:1;fill:#666666;stroke-width:0.26431969" />
                                          <rect
                                             ry="3.9920318"
                                             rx="4"
                                             y="263.20078"
                                             x="-6.0854187"
                                             height="32.742977"
                                             width="67.733337"
                                             id="rect42330-3"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.29037923" />
                                          <rect
                                             style="opacity:1;fill:#0c5a00;fill-opacity:1;stroke-width:0.27992758"
                                             id="rect42373"
                                             width="66.145836"
                                             height="31.158642"
                                             x="-5.2916684"
                                             y="263.99295"
                                             rx="3.9682539"
                                             ry="3.925498" />
                                          <rect
                                             style="opacity:1;fill:url(#radialGradient7947);fill-opacity:1;stroke:url(#radialGradient44460);stroke-width:0.2804423;stroke-opacity:0.93956042"
                                             id="rect42373-3"
                                             width="65.865112"
                                             height="31.40659"
                                             x="-5.1513071"
                                             y="263.86899"
                                             rx="3.96875"
                                             ry="3.960844" />
                                          <rect
                                             ry="3.8672791"
                                             rx="4"
                                             y="263.13333"
                                             x="23.303688"
                                             height="32.742962"
                                             width="38.345688"
                                             id="rect42330-6"
                                             style="opacity:1;fill:#0c5a00;fill-opacity:1;stroke-width:0.19574571" />
                                          <rect
                                             ry="3.9920316"
                                             rx="3.9014249"
                                             y="263.1333"
                                             x="24.248667"
                                             height="32.742977"
                                             width="37.400707"
                                             id="rect42330-3-2"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.21577652" />
                                          <rect
                                             ry="3.7988689"
                                             rx="3.735826"
                                             y="263.86899"
                                             x="24.9006"
                                             height="31.158642"
                                             width="35.813206"
                                             id="rect42330-3-2-2"
                                             style="opacity:1;fill:#ececec;stroke-width:0.20597573" />
                                          <rect
                                             style="opacity:1;fill:url(#linearGradient47119);fill-opacity:1;stroke-width:0.1318209"
                                             id="rect42330-3-2-2-3"
                                             width="33.796402"
                                             height="13.523456"
                                             x="-59.770969"
                                             y="-293.09958"
                                             rx="3.5254459"
                                             ry="1.6487827"
                                             transform="scale(-1)" />
                                          <rect
                                             transform="matrix(0.99997067,-0.00765955,0.0079387,0.99996849,0,0)"
                                             ry="1.6487846"
                                             rx="3.5253103"
                                             y="265.71469"
                                             x="23.765352"
                                             height="13.523471"
                                             width="33.795101"
                                             id="rect42330-3-2-2-3-2"
                                             style="opacity:1;fill:url(#linearGradient47119-6);fill-opacity:1;stroke-width:0.13181843" />
                                        </g>
                                      </g>
                                    </svg>
                                  """,
                            'Off': """
                                    <svg
                                       xmlns:osb="http://www.openswatchbook.org/uri/2009/osb"
                                       xmlns:dc="http://purl.org/dc/elements/1.1/"
                                       xmlns:cc="http://creativecommons.org/ns#"
                                       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                                       xmlns:svg="http://www.w3.org/2000/svg"
                                       xmlns="http://www.w3.org/2000/svg"
                                       xmlns:xlink="http://www.w3.org/1999/xlink"
                                       xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
                                       xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
                                       width="256"
                                       height="129"
                                       viewBox="0 0 67.73248 34.13082"
                                       version="1.1"
                                       id="svg8"
                                       inkscape:version="0.92.1 unknown"
                                       sodipodi:docname="SquaredOffButton.svg">
                                      <defs
                                         id="defs2">
                                        <linearGradient
                                           id="linearGradient7812"
                                           inkscape:collect="always">
                                          <stop
                                             id="stop7808"
                                             offset="0"
                                             style="stop-color:#0c5a00;stop-opacity:1;" />
                                          <stop
                                             id="stop7810"
                                             offset="1"
                                             style="stop-color:#0caa00;stop-opacity:0" />
                                        </linearGradient>
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="linearGradient7744">
                                          <stop
                                             style="stop-color:#0c5a00;stop-opacity:1;"
                                             offset="0"
                                             id="stop7740" />
                                          <stop
                                             style="stop-color:#0caa00;stop-opacity:0"
                                             offset="1"
                                             id="stop7742" />
                                        </linearGradient>
                                        <linearGradient
                                           id="linearGradient46973"
                                           osb:paint="gradient">
                                          <stop
                                             style="stop-color:#000000;stop-opacity:1;"
                                             offset="0"
                                             id="stop46969" />
                                          <stop
                                             style="stop-color:#000000;stop-opacity:0;"
                                             offset="1"
                                             id="stop46971" />
                                        </linearGradient>
                                        <linearGradient
                                           id="linearGradient46862"
                                           osb:paint="solid">
                                          <stop
                                             style="stop-color:#ececec;stop-opacity:1;"
                                             offset="0"
                                             id="stop46860" />
                                        </linearGradient>
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient7812"
                                           id="radialGradient44460"
                                           cx="29.12948"
                                           cy="262.3385"
                                           fx="29.12948"
                                           fy="262.3385"
                                           r="33.337498"
                                           gradientTransform="matrix(1.2611975,8.860821e-5,-1.7345515e-4,0.42019677,-6.9344364,169.17227)"
                                           gradientUnits="userSpaceOnUse" />
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.067112"
                                           y2="255.32812"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.0160706,0,0,1,-55.921487,-541.86646)" />
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="linearGradient47117">
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:1;"
                                             offset="0"
                                             id="stop47113" />
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:0;"
                                             offset="1"
                                             id="stop47115" />
                                        </linearGradient>
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119-6"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.214836"
                                           y2="256.65088"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.0160316,1.8494843e-8,-1.761654e-8,1.000001,-32.406146,17.109837)" />
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient7744"
                                           id="radialGradient7746"
                                           cx="28.309671"
                                           cy="263.13199"
                                           fx="28.309669"
                                           fy="263.13199"
                                           r="32.525963"
                                           gradientTransform="matrix(1.2926649,9.0635818e-5,-1.7773402e-4,0.43068093,-6.7900645,166.08015)"
                                           gradientUnits="userSpaceOnUse" />
                                      </defs>
                                      <sodipodi:namedview
                                         id="base"
                                         pagecolor="#ffffff"
                                         bordercolor="#666666"
                                         borderopacity="1.0"
                                         inkscape:pageopacity="0.0"
                                         inkscape:pageshadow="2"
                                         inkscape:zoom="1.4"
                                         inkscape:cx="-191.45853"
                                         inkscape:cy="155.11743"
                                         inkscape:document-units="px"
                                         inkscape:current-layer="layer1"
                                         showgrid="false"
                                         units="px"
                                         inkscape:window-width="1916"
                                         inkscape:window-height="1057"
                                         inkscape:window-x="0"
                                         inkscape:window-y="0"
                                         inkscape:window-maximized="0" />
                                      <metadata
                                         id="metadata5">
                                        <rdf:RDF>
                                          <cc:Work
                                             rdf:about="">
                                            <dc:format>image/svg+xml</dc:format>
                                            <dc:type
                                               rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
                                            <dc:title></dc:title>
                                          </cc:Work>
                                        </rdf:RDF>
                                      </metadata>
                                      <g
                                         inkscape:label="Layer 1"
                                         inkscape:groupmode="layer"
                                         id="layer1"
                                         transform="translate(0,-262.86875)">
                                        <g
                                           id="g8095"
                                           transform="matrix(0.99998734,0,0,0.99998734,6.0853417,0.00336009)">
                                          <rect
                                             ry="4"
                                             rx="4"
                                             y="263.1333"
                                             x="-6.0854187"
                                             height="33.866669"
                                             width="67.733337"
                                             id="rect42330"
                                             style="opacity:1;fill:#666666;stroke-width:0.26458335" />
                                          <rect
                                             ry="4"
                                             rx="4"
                                             y="263.1333"
                                             x="-6.0854187"
                                             height="32.808334"
                                             width="67.733337"
                                             id="rect42330-3"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.29066887" />
                                          <rect
                                             style="opacity:1;fill:#112b0b;fill-opacity:1;stroke-width:0.2802068"
                                             id="rect42373"
                                             width="66.145836"
                                             height="31.220835"
                                             x="-5.2916684"
                                             y="263.92706"
                                             rx="3.9682539"
                                             ry="3.9333334" />
                                          <rect
                                             style="opacity:1;fill:url(#radialGradient7746);fill-opacity:1;stroke:url(#radialGradient44460);stroke-width:0;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:0.93956042"
                                             id="rect42373-3"
                                             width="66.004013"
                                             height="31.22084"
                                             x="-5.1498489"
                                             y="263.98398"
                                             rx="3.96875"
                                             ry="3.96875" />
                                          <rect
                                             transform="scale(-1)"
                                             ry="3.8749981"
                                             rx="4"
                                             y="-295.94189"
                                             x="-32.260269"
                                             height="32.808319"
                                             width="38.345688"
                                             id="rect42330-6"
                                             style="opacity:1;fill:#2d0000;fill-opacity:1;stroke-width:0.19594097" />
                                          <rect
                                             transform="scale(-1)"
                                             ry="3.9999998"
                                             rx="3.9014249"
                                             y="-295.94193"
                                             x="-31.31529"
                                             height="32.808334"
                                             width="37.400707"
                                             id="rect42330-3-2"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.21599175" />
                                          <rect
                                             transform="scale(-1)"
                                             ry="3.8064516"
                                             rx="3.735826"
                                             y="-295.2048"
                                             x="-30.663357"
                                             height="31.220835"
                                             width="35.813206"
                                             id="rect42330-3-2-2"
                                             style="opacity:1;fill:#ececec;stroke-width:0.20618118" />
                                          <path
                                             inkscape:connector-curvature="0"
                                             id="path47770"
                                             d="m 28.568313,295.81625 c 1.202298,-0.40774 2.117958,-1.32506 2.568641,-2.5733 l 0.218935,-0.60638 0.02726,-12.56771 c 0.01741,-8.03138 -0.0071,-12.85052 -0.06793,-13.35123 -0.132868,-1.09372 -0.497509,-1.82286 -1.275633,-2.55076 -0.385392,-0.36052 -0.793109,-0.64034 -1.110927,-0.76245 -0.409467,-0.15731 -0.453599,-0.19381 -0.239244,-0.19782 0.401873,-0.008 1.330227,0.33665 1.912181,0.70892 0.595537,0.38096 1.079971,0.98808 1.390771,1.743 l 0.213969,0.51972 v 13.32366 c 0,12.67866 -0.0084,13.34773 -0.173326,13.82086 -0.45992,1.31932 -1.798839,2.3509 -3.275706,2.52382 -0.30358,0.0355 -0.357645,0.0269 -0.188989,-0.0303 z"
                                             style="opacity:1;fill:#17280b;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:0.10063617;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" />
                                          <rect
                                             style="opacity:1;fill:url(#linearGradient47119);fill-opacity:1;stroke-width:0.13195239"
                                             id="rect42330-3-2-2-3"
                                             width="33.796402"
                                             height="13.550448"
                                             x="-29.758087"
                                             y="-293.32312"
                                             rx="3.5254459"
                                             ry="1.6520737"
                                             transform="scale(-1)" />
                                          <rect
                                             transform="matrix(0.99997055,-0.00767484,0.00792289,0.99996861,0,0)"
                                             ry="1.6520754"
                                             rx="3.5253108"
                                             y="265.65341"
                                             x="-6.2437177"
                                             height="13.550462"
                                             width="33.795105"
                                             id="rect42330-3-2-2-3-2"
                                             style="opacity:1;fill:url(#linearGradient47119-6);fill-opacity:1;stroke-width:0.13194992" />
                                        </g>
                                      </g>
                                    </svg>
                                   """,
                            'Disconnected': """
                                    <svg
                                       xmlns:dc="http://purl.org/dc/elements/1.1/"
                                       xmlns:cc="http://creativecommons.org/ns#"
                                       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                                       xmlns:svg="http://www.w3.org/2000/svg"
                                       xmlns="http://www.w3.org/2000/svg"
                                       xmlns:xlink="http://www.w3.org/1999/xlink"
                                       xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
                                       xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
                                       width="256"
                                       height="129"
                                       viewBox="0 0 67.733331 34.131251"
                                       version="1.1"
                                       id="svg159"
                                       inkscape:version="0.92.1 unknown"
                                       sodipodi:docname="DisconnectButton.svg">
                                      <defs
                                         id="defs153">
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119-6"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.214836"
                                           y2="256.65088"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.020653,1.8200125e-8,-1.7696669e-8,1.0000013,-11.68118,17.105496)" />
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="linearGradient47117">
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:1;"
                                             offset="0"
                                             id="stop47113" />
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:0;"
                                             offset="1"
                                             id="stop47115" />
                                        </linearGradient>
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.067112"
                                           y2="255.32812"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.0206925,0,0,0.99999997,-77.047571,-541.70269)" />
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="radialGradient44460"
                                           cx="27.781246"
                                           cy="262.60416"
                                           fx="27.781246"
                                           fy="262.60416"
                                           r="33.337498"
                                           gradientTransform="matrix(1.176961,2.4123198e-7,-8.8978764e-8,0.41608433,1.1684521,170.27202)"
                                           gradientUnits="userSpaceOnUse" />
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="radialGradient8012"
                                           cx="33.865871"
                                           cy="279.53751"
                                           fx="33.865871"
                                           fy="279.53751"
                                           r="33.072918"
                                           gradientTransform="matrix(1.1863765,3.4113101e-7,-1.1988375e-7,0.41941276,-6.3117695,162.29589)"
                                           gradientUnits="userSpaceOnUse" />
                                      </defs>
                                      <sodipodi:namedview
                                         id="base"
                                         pagecolor="#ffffff"
                                         bordercolor="#666666"
                                         borderopacity="1.0"
                                         inkscape:pageopacity="0.0"
                                         inkscape:pageshadow="2"
                                         inkscape:zoom="1.7167969"
                                         inkscape:cx="-13.13681"
                                         inkscape:cy="92.021553"
                                         inkscape:document-units="px"
                                         inkscape:current-layer="layer1"
                                         showgrid="false"
                                         units="px"
                                         inkscape:window-width="1916"
                                         inkscape:window-height="1057"
                                         inkscape:window-x="3840"
                                         inkscape:window-y="0"
                                         inkscape:window-maximized="0" />
                                      <metadata
                                         id="metadata156">
                                        <rdf:RDF>
                                          <cc:Work
                                             rdf:about="">
                                            <dc:format>image/svg+xml</dc:format>
                                            <dc:type
                                               rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
                                            <dc:title />
                                          </cc:Work>
                                        </rdf:RDF>
                                      </metadata>
                                      <g
                                         inkscape:label="Layer 1"
                                         inkscape:groupmode="layer"
                                         id="layer1"
                                         transform="translate(0,-262.86873)">
                                        <g
                                           id="g8050">
                                          <rect
                                             ry="3.9999998"
                                             rx="3.9999998"
                                             y="263.1333"
                                             x="1.110223e-16"
                                             height="33.866665"
                                             width="67.73333"
                                             id="rect42330"
                                             style="opacity:1;fill:#666666;stroke-width:0.26458332" />
                                          <rect
                                             ry="3.9999998"
                                             rx="3.9999998"
                                             y="263.1333"
                                             x="1.110223e-16"
                                             height="32.808334"
                                             width="67.73333"
                                             id="rect42330-3"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.29066887" />
                                          <rect
                                             style="opacity:1;fill:#333333;fill-opacity:1;stroke-width:0.28020677"
                                             id="rect42373"
                                             width="66.145836"
                                             height="31.220833"
                                             x="0.79370123"
                                             y="263.92706"
                                             rx="3.9682536"
                                             ry="3.9333332" />
                                          <rect
                                             style="opacity:1;fill:url(#radialGradient8012);fill-opacity:1;stroke:url(#radialGradient44460);stroke-width:0.2807219;stroke-opacity:0.93956042"
                                             id="rect42373-3"
                                             width="65.865112"
                                             height="31.469278"
                                             x="0.9333176"
                                             y="263.80286"
                                             rx="3.96875"
                                             ry="3.96875" />
                                          <rect
                                             ry="3.8749981"
                                             rx="4.0847697"
                                             y="263.13333"
                                             x="14.2875"
                                             height="32.808319"
                                             width="39.158333"
                                             id="rect42330-6"
                                             style="opacity:1;fill:#333333;fill-opacity:1;stroke-width:0.19800633" />
                                          <rect
                                             ry="3.9999995"
                                             rx="3.9191716"
                                             y="263.13333"
                                             x="15.081249"
                                             height="32.808334"
                                             width="37.570831"
                                             id="rect42330-3-2"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.21648245" />
                                          <rect
                                             ry="3.8064513"
                                             rx="3.7528198"
                                             y="263.87045"
                                             x="15.736193"
                                             height="31.220833"
                                             width="35.976112"
                                             id="rect42330-3-2-2"
                                             style="opacity:1;fill:#ececec;stroke-width:0.20664957" />
                                          <rect
                                             style="opacity:1;fill:url(#linearGradient47119);fill-opacity:1;stroke-width:0.13225216"
                                             id="rect42330-3-2-2-3"
                                             width="33.950134"
                                             height="13.550447"
                                             x="-50.765167"
                                             y="-293.15945"
                                             rx="3.5414824"
                                             ry="1.6520737"
                                             transform="scale(-1)" />
                                          <rect
                                             transform="matrix(0.99997081,-0.00764009,0.00795893,0.99996833,0,0)"
                                             ry="1.6520758"
                                             rx="3.5413456"
                                             y="265.64908"
                                             x="14.600234"
                                             height="13.550466"
                                             width="33.948822"
                                             id="rect42330-3-2-2-3-2"
                                             style="opacity:1;fill:url(#linearGradient47119-6);fill-opacity:1;stroke-width:0.13224968" />
                                        </g>
                                      </g>
                                    </svg>
                                            """
                               }

    roundedbuttonstatesdict = {
                            'On': """
                                    <svg
                                       xmlns:osb="http://www.openswatchbook.org/uri/2009/osb"
                                       xmlns:dc="http://purl.org/dc/elements/1.1/"
                                       xmlns:cc="http://creativecommons.org/ns#"
                                       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                                       xmlns:svg="http://www.w3.org/2000/svg"
                                       xmlns="http://www.w3.org/2000/svg"
                                       xmlns:xlink="http://www.w3.org/1999/xlink"
                                       xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
                                       xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
                                       width="256"
                                       height="129"
                                       viewBox="0 0 67.73248 34.13082"
                                       version="1.1"
                                       id="svg8"
                                       inkscape:version="0.92.1 unknown"
                                       sodipodi:docname="RoundedOnButton.svg">
                                      <defs
                                         id="defs2">
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="7945">
                                          <stop
                                             style="stop-color:#02bb00;stop-opacity:1;"
                                             offset="0"
                                             id="stop7956" />
                                          <stop
                                             style="stop-color:#02dc00;stop-opacity:0"
                                             offset="1"
                                             id="stop7958" />
                                        </linearGradient>
                                        <linearGradient
                                           id="linearGradient46973"
                                           osb:paint="gradient">
                                          <stop
                                             style="stop-color:#000000;stop-opacity:1;"
                                             offset="0"
                                             id="stop46969" />
                                          <stop
                                             style="stop-color:#000000;stop-opacity:0;"
                                             offset="1"
                                             id="stop46971" />
                                        </linearGradient>
                                        <linearGradient
                                           id="linearGradient46862"
                                           osb:paint="solid">
                                          <stop
                                             style="stop-color:#ececec;stop-opacity:1;"
                                             offset="0"
                                             id="stop46860" />
                                        </linearGradient>
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="linearGradient47117">
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:1;"
                                             offset="0"
                                             id="stop47113" />
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:0;"
                                             offset="1"
                                             id="stop47115" />
                                        </linearGradient>
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119-6-0"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.214836"
                                           y2="256.65088"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.0160316,3.6400241e-8,-3.523308e-8,1.000001,-2.3943416,17.176351)" />
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119-5"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.067112"
                                           y2="255.32812"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.0160706,0,0,1,-85.93292,-541.70271)" />
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#7945"
                                           id="radialGradient44460-5"
                                           cx="27.781246"
                                           cy="262.60416"
                                           fx="27.781246"
                                           fy="262.60416"
                                           r="33.337498"
                                           gradientTransform="matrix(1.0561833,5.0746782e-7,-2.0568588e-7,0.42809017,-1.5607877,167.11932)"
                                           gradientUnits="userSpaceOnUse" />
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#7945"
                                           id="radialGradient7962"
                                           cx="27.781244"
                                           cy="279.53772"
                                           fx="27.781242"
                                           fy="279.53769"
                                           r="33.072922"
                                           gradientTransform="matrix(1.0646326,4.3379072e-7,-1.7582324e-7,0.43151489,-1.7955236,158.91289)"
                                           gradientUnits="userSpaceOnUse" />
                                      </defs>
                                      <sodipodi:namedview
                                         id="base"
                                         pagecolor="#ffffff"
                                         bordercolor="#666666"
                                         borderopacity="1.0"
                                         inkscape:pageopacity="0.0"
                                         inkscape:pageshadow="2"
                                         inkscape:zoom="1.979899"
                                         inkscape:cx="155.59416"
                                         inkscape:cy="22.850702"
                                         inkscape:document-units="px"
                                         inkscape:current-layer="layer1"
                                         showgrid="false"
                                         units="px"
                                         inkscape:window-width="1916"
                                         inkscape:window-height="1057"
                                         inkscape:window-x="1920"
                                         inkscape:window-y="1080"
                                         inkscape:window-maximized="0"
                                         scale-x="0.26458" />
                                      <metadata
                                         id="metadata5">
                                        <rdf:RDF>
                                          <cc:Work
                                             rdf:about="">
                                            <dc:format>image/svg+xml</dc:format>
                                            <dc:type
                                               rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
                                            <dc:title></dc:title>
                                          </cc:Work>
                                        </rdf:RDF>
                                      </metadata>
                                      <g
                                         inkscape:label="Layer 1"
                                         inkscape:groupmode="layer"
                                         id="layer1"
                                         transform="translate(0,-262.86875)">
                                        <g
                                           id="g8072"
                                           transform="matrix(0.9999871,0,0,0.99998712,6.0853392,0.00338885)">
                                          <rect
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="263.13333"
                                             x="-6.0854177"
                                             height="33.866676"
                                             width="67.733353"
                                             id="rect42330-69"
                                             style="opacity:1;fill:#666666;stroke-width:0.26458341" />
                                          <rect
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="263.13333"
                                             x="-6.0854177"
                                             height="32.808334"
                                             width="67.733353"
                                             id="rect42330-3-3"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.2906689" />
                                          <rect
                                             style="opacity:1;fill:#0c5a00;fill-opacity:1;stroke-width:0.2802068"
                                             id="rect42373-7"
                                             width="66.145836"
                                             height="31.220835"
                                             x="-5.2916708"
                                             y="263.92709"
                                             rx="13.229167"
                                             ry="13.229167" />
                                          <rect
                                             style="opacity:1;fill:url(#radialGradient7962);fill-opacity:1;stroke:url(#radialGradient44460-5);stroke-width:0.2807219;stroke-opacity:0.93956042"
                                             id="rect42373-3-4"
                                             width="65.86512"
                                             height="31.469278"
                                             x="-5.1513066"
                                             y="263.80283"
                                             rx="13.229167"
                                             ry="13.229167" />
                                          <rect
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="263.13336"
                                             x="23.302248"
                                             height="32.808319"
                                             width="38.345688"
                                             id="rect42330-6-5"
                                             style="opacity:1;fill:#0c5a00;fill-opacity:1;stroke-width:0.19594097" />
                                          <rect
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="263.13333"
                                             x="24.247225"
                                             height="32.808334"
                                             width="37.400707"
                                             id="rect42330-3-2-25"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.21599175" />
                                          <rect
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="263.87048"
                                             x="24.899157"
                                             height="31.220835"
                                             width="35.813206"
                                             id="rect42330-3-2-2-4"
                                             style="opacity:1;fill:#ececec;stroke-width:0.20618118" />
                                          <rect
                                             style="opacity:1;fill:url(#linearGradient47119-5);fill-opacity:1;stroke-width:0.13195239"
                                             id="rect42330-3-2-2-3-7"
                                             width="33.796406"
                                             height="13.550448"
                                             x="-59.769516"
                                             y="-293.15939"
                                             rx="13.229167"
                                             ry="13.229167"
                                             transform="scale(-1)" />
                                          <rect
                                             transform="matrix(0.99997055,-0.00767484,0.00792289,0.99996861,0,0)"
                                             ry="13.229167"
                                             rx="13.229168"
                                             y="265.71979"
                                             x="23.76807"
                                             height="13.550463"
                                             width="33.795105"
                                             id="rect42330-3-2-2-3-2-4"
                                             style="opacity:1;fill:url(#linearGradient47119-6-0);fill-opacity:1;stroke-width:0.13194992" />
                                        </g>
                                      </g>
                                    </svg>
                                    """,
                            'Off': """
                                   <svg
                                       xmlns:osb="http://www.openswatchbook.org/uri/2009/osb"
                                       xmlns:dc="http://purl.org/dc/elements/1.1/"
                                       xmlns:cc="http://creativecommons.org/ns#"
                                       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                                       xmlns:svg="http://www.w3.org/2000/svg"
                                       xmlns="http://www.w3.org/2000/svg"
                                       xmlns:xlink="http://www.w3.org/1999/xlink"
                                       xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
                                       xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
                                       width="256"
                                       height="129"
                                       viewBox="0 0 67.73248 34.13082"
                                       version="1.1"
                                       id="svg8"
                                       inkscape:version="0.92.1 unknown"
                                       sodipodi:docname="RoundedOffButton.svg">
                                      <defs
                                         id="defs2">
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="7812">
                                          <stop
                                             style="stop-color:#005000;stop-opacity:1;"
                                             offset="0"
                                             id="stop7933" />
                                          <stop
                                             style="stop-color:#005000;stop-opacity:0;"
                                             offset="1"
                                             id="stop7935" />
                                        </linearGradient>
                                        <linearGradient
                                           id="linearGradient46973"
                                           osb:paint="gradient">
                                          <stop
                                             style="stop-color:#000000;stop-opacity:1;"
                                             offset="0"
                                             id="stop46969" />
                                          <stop
                                             style="stop-color:#000000;stop-opacity:0;"
                                             offset="1"
                                             id="stop46971" />
                                        </linearGradient>
                                        <linearGradient
                                           id="linearGradient46862"
                                           osb:paint="solid">
                                          <stop
                                             style="stop-color:#ececec;stop-opacity:1;"
                                             offset="0"
                                             id="stop46860" />
                                        </linearGradient>
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119-6-1"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.214836"
                                           y2="256.65088"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.0160316,5.4895083e-8,-5.2849621e-8,1.000001,-32.40613,17.109559)" />
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="linearGradient47117">
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:1;"
                                             offset="0"
                                             id="stop47113" />
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:0;"
                                             offset="1"
                                             id="stop47115" />
                                        </linearGradient>
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119-3"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.067112"
                                           y2="255.32812"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.0160706,0,0,1,-55.921493,-541.86621)" />
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="7744">
                                          <stop
                                             style="stop-color:#005000;stop-opacity:1;"
                                             offset="0"
                                             id="stop44454" />
                                          <stop
                                             style="stop-color:#0caa00;stop-opacity:0"
                                             offset="1"
                                             id="stop44456" />
                                        </linearGradient>
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#7744"
                                           id="radialGradient7910"
                                           cx="27.780457"
                                           cy="279.53751"
                                           fx="27.780457"
                                           fy="279.53751"
                                           r="33.072918"
                                           gradientTransform="matrix(1.0606091,0,0,0.43151274,-1.6837499,158.91351)"
                                           gradientUnits="userSpaceOnUse" />
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#7812"
                                           id="radialGradient7939"
                                           cx="27.780457"
                                           cy="279.53751"
                                           fx="27.780457"
                                           fy="279.53751"
                                           r="32.932556"
                                           gradientTransform="matrix(1,0,0,0.47778373,0,145.97903)"
                                           gradientUnits="userSpaceOnUse" />
                                      </defs>
                                      <sodipodi:namedview
                                         id="base"
                                         pagecolor="#ffffff"
                                         bordercolor="#666666"
                                         borderopacity="1.0"
                                         inkscape:pageopacity="0.0"
                                         inkscape:pageshadow="2"
                                         inkscape:zoom="1.4"
                                         inkscape:cx="-73.602269"
                                         inkscape:cy="-6.8966862"
                                         inkscape:document-units="px"
                                         inkscape:current-layer="layer1"
                                         showgrid="false"
                                         units="px"
                                         inkscape:window-width="1916"
                                         inkscape:window-height="1057"
                                         inkscape:window-x="0"
                                         inkscape:window-y="1080"
                                         inkscape:window-maximized="0" />
                                      <metadata
                                         id="metadata5">
                                        <rdf:RDF>
                                          <cc:Work
                                             rdf:about="">
                                            <dc:format>image/svg+xml</dc:format>
                                            <dc:type
                                               rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
                                            <dc:title></dc:title>
                                          </cc:Work>
                                        </rdf:RDF>
                                      </metadata>
                                      <g
                                         inkscape:label="Layer 1"
                                         inkscape:groupmode="layer"
                                         id="layer1"
                                         transform="translate(0,-262.86875)">
                                        <g
                                           id="g8106"
                                           transform="matrix(0.9999871,0,0,0.99998712,6.0853402,0.00338885)">
                                          <rect
                                             rx="13.229167"
                                             ry="13.229167"
                                             y="263.13333"
                                             x="-6.0854177"
                                             height="33.866676"
                                             width="67.733353"
                                             id="rect42330-4"
                                             style="opacity:1;fill:#666666;stroke-width:0.26458341" />
                                          <rect
                                             rx="13.229167"
                                             ry="13.229167"
                                             y="263.13333"
                                             x="-6.0854177"
                                             height="32.808334"
                                             width="67.733353"
                                             id="rect42330-3-5"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.2906689" />
                                          <rect
                                             rx="13.229167"
                                             ry="13.229167"
                                             style="opacity:1;fill:#112b0b;fill-opacity:1;stroke-width:0.2802068"
                                             id="rect42373-0"
                                             width="66.145836"
                                             height="31.220835"
                                             x="-5.2916555"
                                             y="263.92709" />
                                          <rect
                                             rx="13.229167"
                                             ry="13.229167"
                                             style="opacity:1;fill:url(#radialGradient7910);fill-opacity:1;stroke:url(#radialGradient7939);stroke-width:0;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
                                             id="rect42373-3-3"
                                             width="65.865112"
                                             height="31.469278"
                                             x="-5.1521001"
                                             y="263.80286" />
                                          <rect
                                             rx="13.229167"
                                             ry="13.229167"
                                             transform="scale(-1)"
                                             y="-295.94165"
                                             x="-32.260269"
                                             height="32.808319"
                                             width="38.345688"
                                             id="rect42330-6-6"
                                             style="opacity:1;fill:#2d0000;fill-opacity:1;stroke-width:0.19594097" />
                                          <rect
                                             rx="13.229167"
                                             ry="13.229167"
                                             transform="scale(-1)"
                                             y="-295.94168"
                                             x="-31.3153"
                                             height="32.808334"
                                             width="37.400707"
                                             id="rect42330-3-2-1"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.21599175" />
                                          <rect
                                             rx="13.229167"
                                             ry="13.229167"
                                             transform="scale(-1)"
                                             y="-295.20456"
                                             x="-30.663368"
                                             height="31.220835"
                                             width="35.813206"
                                             id="rect42330-3-2-2-0"
                                             style="opacity:1;fill:#ececec;stroke-width:0.20618118" />
                                          <rect
                                             rx="13.229167"
                                             ry="13.229167"
                                             style="opacity:1;fill:url(#linearGradient47119-3);fill-opacity:1;stroke-width:0.13195239"
                                             id="rect42330-3-2-2-3-3"
                                             width="33.796406"
                                             height="13.550448"
                                             x="-29.758095"
                                             y="-293.32288"
                                             transform="scale(-1)" />
                                          <rect
                                             rx="13.229168"
                                             ry="13.229167"
                                             transform="matrix(0.99997055,-0.00767484,0.00792289,0.99996861,0,0)"
                                             y="265.65314"
                                             x="-6.2437172"
                                             height="13.550462"
                                             width="33.795105"
                                             id="rect42330-3-2-2-3-2-2"
                                             style="opacity:1;fill:url(#linearGradient47119-6-1);fill-opacity:1;stroke-width:0.13194992" />
                                        </g>
                                      </g>
                                    </svg>
                                   """,
                            'Disconnected': """
                                    <svg
                                       xmlns:dc="http://purl.org/dc/elements/1.1/"
                                       xmlns:cc="http://creativecommons.org/ns#"
                                       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                                       xmlns:svg="http://www.w3.org/2000/svg"
                                       xmlns="http://www.w3.org/2000/svg"
                                       xmlns:xlink="http://www.w3.org/1999/xlink"
                                       xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
                                       xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
                                       width="256"
                                       height="129"
                                       viewBox="0 0 67.733331 34.131251"
                                       version="1.1"
                                       id="svg159"
                                       inkscape:version="0.92.1 unknown"
                                       sodipodi:docname="RoundedDisconnectButton.svg">
                                      <defs
                                         id="defs153">
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient47119-6-7"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.214836"
                                           y2="256.65088"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.020653,2.00442e-8,-1.8443087e-8,1.0000013,-11.68959,18.163804)" />
                                        <linearGradient
                                           inkscape:collect="always"
                                           id="linearGradient47117">
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:1;"
                                             offset="0"
                                             id="stop47113" />
                                          <stop
                                             style="stop-color:#cccccc;stop-opacity:0;"
                                             offset="1"
                                             id="stop47115" />
                                        </linearGradient>
                                        <linearGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="linearGradient1689"
                                           gradientUnits="userSpaceOnUse"
                                           gradientTransform="matrix(1.0206925,0,0,0.99999997,-77.047569,-541.17351)"
                                           x1="41.2561"
                                           y1="248.90253"
                                           x2="41.067112"
                                           y2="255.32812" />
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="radialGradient44460-5"
                                           cx="27.781246"
                                           cy="262.60416"
                                           fx="27.781246"
                                           fy="262.60416"
                                           r="33.337498"
                                           gradientTransform="matrix(1.1815126,-0.01290238,0.00424111,0.38837207,-0.07175464,177.9078)"
                                           gradientUnits="userSpaceOnUse" />
                                        <radialGradient
                                           inkscape:collect="always"
                                           xlink:href="#linearGradient47117"
                                           id="radialGradient8020"
                                           cx="33.865868"
                                           cy="279.53745"
                                           fx="33.865868"
                                           fy="279.53748"
                                           r="33.072918"
                                           gradientTransform="matrix(1.1909647,-0.01300556,0.00427502,0.39147863,-7.6622104,170.54499)"
                                           gradientUnits="userSpaceOnUse" />
                                      </defs>
                                      <sodipodi:namedview
                                         id="base"
                                         pagecolor="#ffffff"
                                         bordercolor="#666666"
                                         borderopacity="1.0"
                                         inkscape:pageopacity="0.0"
                                         inkscape:pageshadow="2"
                                         inkscape:zoom="1.7167969"
                                         inkscape:cx="29.397033"
                                         inkscape:cy="-30.019748"
                                         inkscape:document-units="px"
                                         inkscape:current-layer="layer1"
                                         showgrid="false"
                                         units="px"
                                         inkscape:window-width="1916"
                                         inkscape:window-height="1057"
                                         inkscape:window-x="3840"
                                         inkscape:window-y="1080"
                                         inkscape:window-maximized="0"
                                         inkscape:measure-start="0,0"
                                         inkscape:measure-end="0,0" />
                                      <metadata
                                         id="metadata156">
                                        <rdf:RDF>
                                          <cc:Work
                                             rdf:about="">
                                            <dc:format>image/svg+xml</dc:format>
                                            <dc:type
                                               rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
                                            <dc:title />
                                          </cc:Work>
                                        </rdf:RDF>
                                      </metadata>
                                      <g
                                         inkscape:label="Layer 1"
                                         inkscape:groupmode="layer"
                                         id="layer1"
                                         transform="translate(0,-262.86873)">
                                        <g
                                           id="g8061">
                                          <rect
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="263.1333"
                                             x="0"
                                             height="33.866665"
                                             width="67.73333"
                                             id="rect42330-9"
                                             style="opacity:1;fill:#666666;stroke-width:0.26458332" />
                                          <rect
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="263.1333"
                                             x="0"
                                             height="32.808334"
                                             width="67.73333"
                                             id="rect42330-3-1"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.2906689" />
                                          <rect
                                             style="opacity:1;fill:#333333;fill-opacity:1;stroke-width:0.28020677"
                                             id="rect42373-2"
                                             width="66.145836"
                                             height="31.220833"
                                             x="0.79370117"
                                             y="263.92706"
                                             rx="13.229167"
                                             ry="13.229167" />
                                          <rect
                                             style="opacity:1;fill:url(#radialGradient8020);fill-opacity:1;stroke:url(#radialGradient44460-5);stroke-width:0.2807219;stroke-opacity:0.93956042"
                                             id="rect42373-3-7"
                                             width="65.865112"
                                             height="31.469278"
                                             x="0.9333176"
                                             y="263.80286"
                                             rx="13.229167"
                                             ry="13.229167" />
                                          <rect
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="263.13333"
                                             x="14.287506"
                                             height="32.808319"
                                             width="39.158333"
                                             id="rect42330-6-0"
                                             style="opacity:1;fill:#333333;fill-opacity:1;stroke-width:0.19800633" />
                                          <rect
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="263.1333"
                                             x="15.081253"
                                             height="32.808334"
                                             width="37.570835"
                                             id="rect42330-3-2-3"
                                             style="opacity:1;fill:#b3b3b3;stroke-width:0.21648245" />
                                          <rect
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="263.87042"
                                             x="15.736191"
                                             height="31.220833"
                                             width="35.976112"
                                             id="rect42330-3-2-2-6"
                                             style="opacity:1;fill:#ececec;stroke-width:0.20664957" />
                                          <rect
                                             style="opacity:1;fill:url(#linearGradient1689);fill-opacity:1;stroke-width:0.13225216"
                                             id="rect42330-3-2-2-3-0"
                                             width="33.950134"
                                             height="13.550447"
                                             x="-50.765179"
                                             y="-292.63028"
                                             rx="13.229167"
                                             ry="13.229167"
                                             transform="scale(-1)" />
                                          <rect
                                             transform="matrix(0.99997081,-0.00764009,0.00795893,0.99996833,0,0)"
                                             ry="13.229167"
                                             rx="13.229167"
                                             y="266.70746"
                                             x="14.591808"
                                             height="13.550466"
                                             width="33.948818"
                                             id="rect42330-3-2-2-3-2-6"
                                             style="opacity:1;fill:url(#linearGradient47119-6-7);fill-opacity:1;stroke-width:0.13224968" />
                                        </g>
                                      </g>
                                    </svg>
                                    """
                               }

    def __init__(self, parent=None, init_channel=None, bit=-1, shape=0):
        """Initialize all internal states and properties."""
        super(PyDMStateButton, self).__init__(parent)
        self._channel = init_channel
        self._channels = None
        self._connected = False
        self._write_access = False
        self.checkEnableState()
        self.pvbit = bit
        self._value = 0
        self._count = -2
        self._isArray = False
        self.clicked.connect(self.sendValue)
        self.clicked.connect(self.sendWaveform)
        self._shape = shape
        self.renderer = QSvgRenderer()
        self.setCheckable(True)

    @pyqtProperty(bool)
    def value(self):
        """Property which corresponds to the state of the button."""
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.update()

    @pyqtProperty(buttonShapeMap)
    def shape(self):
        """Property which corresponds to the shape of the button."""
        return self._shape

    @shape.setter
    def shape(self, new_shape):
        self._shape = new_shape
        self.update()

    @pyqtSlot(int)
    @pyqtSlot(float)
    @pyqtSlot(str)
    def receiveValue(self, value):
        """Pyqt slot to receive PyDM channel value."""
        self._isArray = False
        self.value = int(value)
        value = int(value)
        if self._bit >= 0:
            value = (value >> self._bit) & 1
        self.update()

    @pyqtSlot(_np.ndarray)
    def receiveWaveform(self, value):
        """Pyqt slot to receive PyDM channel array."""
        self._isArray = True
        self._value = value
        if self._bit < 0 or self._count is None:
            return
        if self._bit >= self._count:
            return
        self.update()

    @pyqtSlot(int)
    def receiveCount(self, value):
        """Pyqt slot to receive PyDM channel count."""
        self._count = int(value)

    @pyqtSlot(bool)
    def sendValue(self, checked):
        """Pyqt slot to send new value to PyDM channel."""
        if self._isArray:
            return
        new_val = 1 if checked else 0
        if self._bit >= 0:
            new_val = int(self._value)
            new_val ^= (-checked ^ new_val) & (1 << self._bit)
            # I didn't try to understand:
            # https://stackoverflow.com/questions/47981/how-do-you-set-clear-and-toggle-a-single-bit
        self.send_value_signal.emit(new_val)

    @pyqtSlot(bool)
    def sendWaveform(self, checked):
        """Pyqt slot to send new array value to PyDM channel."""
        if self._bit < 0 or not self._isArray:
            return
        if self._bit >= self._count:
            return
        wave = self._value.copy()
        wave[self._bit] = 1 if checked else 0
        self.send_waveform_signal.emit(wave)

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        """Pyqt slot to receive connection state changes."""
        self._connected = connected
        self.checkEnableState()

    @pyqtSlot(bool)
    def writeAccessChanged(self, write_access):
        """Pyqt slot to receive write acces changes."""
        self._write_access = write_access
        self.checkEnableState()

    def checkEnableState(self):
        """Check if PV is connected and if writing is enabled."""
        self.setEnabled(self._write_access and self._connected)

    def sizeHint(self):
        """Return size hint to define size on initialization."""
        return QSize(48, 24)

    def paintEvent(self, event):
        """Treat appearence changes based on connection state and value."""
        if self._connected is False:
            state = 'Disconnected'
        elif self._value == 1:
            state = 'On'
        elif self._value == 0:
            state = 'Off'

        if self.shape == 0:
            shape_dict = PyDMStateButton.squaredbuttonstatesdict
        elif self.shape == 1:
            shape_dict = PyDMStateButton.roundedbuttonstatesdict

        option = QStyleOption()
        option.initFrom(self)
        h = option.rect.height()
        w = option.rect.width()
        aspect = 2.0
        ah = w/aspect
        aw = w
        if ah > h:
            ah = h
            aw = h*aspect
        x = abs(aw-w)/2.0
        y = abs(ah-h)/2.0
        bounds = QRectF(x, y, aw, ah)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        shape_str = shape_dict[state]
        buttonstate_bytearray = bytes(shape_str, 'utf-8')
        self.renderer.load(QByteArray(buttonstate_bytearray))
        self.renderer.render(painter, bounds)

    @pyqtProperty(str)
    def channel(self):
        """Property to define PyDM channel."""
        return str(self._channel)

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = str(value)

    @pyqtProperty(int)
    def pvbit(self):
        """Property to define which PV bit to control."""
        return int(self._bit)

    @pvbit.setter
    def pvbit(self, bit):
        self._bit = -1
        if bit >= 0:
            self._bit = int(bit)

    def channels(self):
        """Module that defines slots to PyDM Applicaiton."""
        if self._channels is None:
            self._channels = [PyDMChannel(
                                address=self.channel,
                                connection_slot=self.connectionStateChanged,
                                value_slot=self.receiveValue,
                                waveform_slot=self.receiveWaveform,
                                count_slot=self.receiveCount,
                                write_access_slot=self.writeAccessChanged,
                                value_signal=self.send_value_signal,
                                waveform_signal=self.send_waveform_signal)]
        return self._channels
