# -*- coding: utf-8 -*-
""" 
The ember module contains the basis elements to build IPCC-style 'burning ember diagrams'
Copyright (C) 2020  philippe.marbaix@uclouvain.be
"""

import numpy as np
from embermaker import helpers as hlp
from embermaker.helpers import norm, isempty
from embermaker.drawinglib import canvas
from embermaker.drawinglib.canvas_base import Color
from embermaker.drawinglib.helpers import cm, mm, stringwidth

def get_skeygroup(sortlist=None):
    """
    Gets a sort key function to sort embers by groups.
    :param sortlist: the ordered list of groups; if None, embers will be sorted by alphabetic order.
    :return: the sort key fct
    """
    def skeygroup(be):
        """
        Used for sorting embers by group. If sortlist is defined, tries to use the order defined in this list.
        :param be: an ember object
        :return: sort key value
        """
        if sortlist:
            try:
                pos = sortlist.index(be.group.lower())
            except ValueError:
                pos = -1
        else:  # sortlist is not defined: will sort by alphabetic order
            pos = be.group
        # hlp.addlogmes("Sort key for group:" + str(be.group.lower()) + "->" + str(pos))
        return pos
    skeygroup.haslist = sortlist is not None
    return skeygroup


def get_skeyname(sortlist=None):
    """
    Gets a sort key function to sort embers by name.
    :param sortlist: the ordered list of names; if None, embers will be sorted by alphabetic order.
    :return: the sort key fct
    """
    def skeyname(be):
        """
        Used for sorting embers by name. If sortlist is defined, tries to use the order defined in this list.
        :param be: an ember object
        :return: sort key value
        """
        if sortlist:
            try:
                pos = sortlist.index(be.name.lower())
            except ValueError:
                pos = -1
        else:  # sortlist is not defined: will sort by alphabetic order
            pos = be.name
        # hlp.addlogmes("Sort key for name:" + str(be.name.lower()) + "->" + str(pos))
        return pos
    skeyname.haslist = sortlist is not None
    return skeyname


def get_skeyrisk(sortrlev=None, sorthazl=None):
    """
    Gets a sort key based on risk or hazard levels
    :param sortrlev: the risk level for which hazard will be obtained, then used as sort criteria
    :param sorthazl: the hazard level for which risk will be obtained, then used as sort criteria
    :return:
    """
    def skeyrisk(be):
        """
        :param be: an ember object
        :return: sort key
        """
        try:
            hazl = be.levels_values("hazl")
            risk = be.levels_values("risk")
            if sortrlev is not None:
                if risk[-1] > sortrlev:
                    pos = np.interp(sortrlev, risk, hazl)
                else:
                    # Might be improved; idea is to keep a minimal sorting when the sort criteria cannot work...
                    pos = 5.0 + np.interp(sortrlev / 2.0, risk, hazl)
            elif sorthazl is not None:
                if hazl[-1] > sorthazl:
                    pos = np.interp(sorthazl, hazl, risk)
                else:
                    pos = risk[-1]
            else:
                raise Exception("Skeyrisk cannot generate a sort key because no sort level was provided.")
        except ValueError:
            pos = 999
        if be.getmeta("inclusion_level") == 0:  # Ignore embers with Inclusion Level = 0; could be improved?
            pos = -1  # ignore ember
        return pos
    skeyrisk.haslist = sortrlev is not None or sorthazl is not None
    return skeyrisk


def selecsort(lbes, fkey, reverse=False):
    """
    Sorts embers in lbes but ignores those absent from sortlist (=> fkey(be) = -1 above)
    (no ready-made option to do that?).
    :param lbes: a list of BEs
    :param fkey: the sort-key function
    :param reverse: reverses sorting order
    :return: sorted and filtered list of BEs
    """
    # Filtering
    if fkey.haslist:
        # Filtering occurs only if a sort criteria is defined (no sorting => no filtering)
        lbes = [be for be in lbes if fkey(be) != -1]
    # Sorting
    lbes.sort(key=fkey, reverse=reverse)
    return lbes


def cbyinterp(rlev, csys, cdefs):
    """
    Provides a color by interpolating between the defined color levels associated to risk levels within embers.

    :param rlev: the risk level for which a color is requested
    :param csys: the name of the color system (currently CMYK or RGB)
    :param cdefs: the definition of the colors associated to risk levels, such that
         - cdefs[0] : a risk level index (1D numpy array of risk indexes)
         - cdefs[1:]: the color densities for each value of the risk index :
                    (1D numpy array of color densities for each risk index; e.g. in RGB, the first 1D array is Red)
    :return: the color associated to the risk level
    """
    cvals = [np.interp(rlev, cdefs[0], cdefs[1 + i]) for i in range(len(csys))]
    if csys in ["CMYK", "RGB"]:
        thecol = Color(csys, *cvals, 1.0)  # Alpha is always 1 (no transparency) for embers
    else:
        raise Exception("Undefined color system")
    return thecol


def siz_legy(gp):
    """
    Height which needs to be added to the canvas for the legend, if any
    """
    if norm(gp['leg_pos']) == 'under':
        legy = gp['leg_bot_y'] + gp['leg_y'] + gp['leg_top_y']  # total height of the legend part
    else:
        legy = 0 * cm  # Legend is on the right: no need for vertical space
    return legy

def siz_legx(gp):
    """
    Width which needs to be added to the canvas for the legend, if any
    """
    if norm(gp['leg_pos']) == 'right':
        legx = gp['leg_bot_y'] + gp['leg_y'] + gp['leg_top_y']  # total height of the legend part
    else:
        legx = 0 * cm  # Legend is on the right: no need for vertical space
    return legx

def siz_gry(gp):
    """
    Height of a group of embers (without legend)
    """
    return gp['be_bot_y'] + gp['be_y'] + gp['be_top_y']

def siz_grx(gp, gbes):
    """
    Width of a group of embers
    """
    return gp['scale_x'] + len(gbes) * (gp['be_x'] + gp['be_int_x'])


def siz_glines(gp, glbes):
    """
    Number of ember lines
    """
    return np.ceil(len(glbes) / gp['max_gr_line'])

def siz_can(gp, glbes) -> ():
    """
    Minimal size of the Canvas to draw a set of ember groups
    """
    # Embers are drawn in one or mutiple lines
    # The full figure does not have a fixed size: it is simply of the size needed to draw all the provided embers.
    csz_x = 0
    mgl = int(gp['max_gr_line'])
    for i in range(0, len(glbes), mgl):
        csz_x = max( csz_x, siz_grx(gp, glbes[i:i+mgl]))
    csz_y = siz_glines(gp, glbes) * siz_gry(gp) + siz_legy(gp)
    return csz_x, csz_y


class Transition(object):
    """
    A transition is a fraction of an ember containing data about how risk changes from one level to the next.
    This concept was mostly absent from the first versions of EmberFactory because the risk changes were defined
    as unique, 'global' risk-hazard functions containing all changes.
    It is currently implemented as an addition to the initial framework with minimal interference with it:
    it will enable better documentation of transitions within the Ember class, but the existing EF code will continue
    to work without changes at least in a first step.
    A transition has a name and a list of levels.
    """

    # 'Synonyms', ie. values which can be used but will be substituted at reading:
    names_syn = {'white to yellow': 'undetectable to moderate',
                 'yellow to red': 'moderate to high',
                 'red to purple': 'high to very high'}
    # Phases are "steps" within transitions; they also have synonyms:
    phases_std = {'min': 0.0, 'median': 0.5, 'max': 1.0, 'mode': 'mode'}
    # mode is not an actual 'phase', it is only used for elicitation
    # the value provided above is the 'percentile' within the transition
    phases_syn = {'begin': 'min', 'end': 'max', 'most likely': 'mode'}
    # A risk level is attributed to each (transition, phase) pair, knowing that
    # Undetectable is level 0, Moderate is level 1, high is level 2 and very high is level 3.
    # Thus for example Undetectable to moderate = 0 -> 1, Moderate to high 1 -> 2...
    # *.5 = Median risk levels, and more generally *.# = percentile # within the transition, noted p#

    @classmethod
    def phaserisk(cls, phasename):
        """
        Phaserisk returns the value of the "risk index" relative to the bottom of a transition.
        "Phase" refers to a risk level within a transition for which the hazard is assessed, that is, a transition is
        assessed in several "phases".
        :param phasename: the name of the "phase" within a transition, such as min, median, max or percentile (p*)
        :return: the risk index, as fraction of the full transition [0-1], relative to the start of the transition
        """
        # Todo: shouldn't this be a method of the Levels instead of Transitions? (phase relates to levels)
        if phasename in cls.phases_syn:
            phasename = cls.phases_syn[phasename]

        if phasename in cls.phases_std:
            return cls.phases_std[phasename]
        elif phasename[0] == "p":
            try:
                return float(phasename[1:])/100.0
            except ValueError:
                pass
        # We get here in case of failure (the phasename isn't a defined phase name or a percentile).
        return None

    def __init__(self, name):
        """
        Creates standard attributes for transitions
        """
        self.levels = []
        if name in self.names_syn:
            name = self.names_syn[name]
        self.name = name
        self.meta = {}  # Metadata, as for embers
        # A mode may be attributed to transitions within the expert elicitation process;
        # In this context, the mode is the most likely value in a probability distribution.
        self.mode = None
        self.be = None  # Parent ember; set when the transition is added to an ember.

    def append_level(self, phase, hazl, conf):
        """
        Adds a level to this transition.
        :param str phase: the name of the phase (see Transition and Level)
        :param float hazl: the hazard level
        :param str conf: the confidence level
        :return:
        """
        level = Level(self, {"phase": phase, "hazl": float(hazl), "conf": conf})
        self.levels.append(level)

    def __getitem__(self, phase):
        """
        Returns the level object for the requested phase in this transition.
        :param phase:
        """
        level = None
        for level in self.levels:
            if level['phase'] == phase:
                break
        return level

    def __str__(self):
        """
        So that Transitions can 'pretty-print' themselves
        """
        return self.name

    def base_risk(self, vid):
        """
        Returns the risk index at the bottom of this transition
        :return:
        """
        if self.be is None or self.be.cpal is None:
            raise Exception(f"Transition '{self.name}' is not attached to an ember: "
                            f"base_risk cannot be provided because risk levels are not defined.")

        transnames_risk = self.be.cpal.transnames_risk
        if self.name not in transnames_risk:
            raise Exception(f"Unknown transition named '{self.name}'")

        return transnames_risk[self.name][vid]

    def phases(self):
        return [level['phase'] for level in self.levels]

    def getmeta(self, name, default=None, html=False):
        """
        Returns transition-related metadata (these differ from file- or ember- related metadata).
        :param name: the name of the parameter to be returned.
        :param default: a default value, for use when there is no metadata corresponding to this name
        :param html: process the value trough helper.htmlbreaks
        :return: the requested metadata, or None if the metadata is not defined.
        """
        try:
            value = self.meta[name]
            if value is not None and html:
                value = hlp.htmlbreaks(value)
        except KeyError:
            value = default
        if value is None and default is not None:
            value = default
        return value


class Level(dict):
    """
    A dictionnary providing data about a level (phase, hazl, conf), with additional specific features:
    - storing a reference to the parent transition
    - ability to respond to ['risk'] by calculating risk from phase and transition name
    Note: phases are "steps" within transitions (see Transition)
    """
    def __init__(self, trans, *args):
        """
        :param trans: the transition object within which this level resides
        :param args: at least this dictionnary: {"phase":phase, "hazl":hazl, "conf":conf}
        """
        super(Level, self).__init__(*args)
        self.trans = trans

    def __getitem__(self, key):
        if key in self:
            return super(Level, self).__getitem__(key)
        elif key == "risk":
            if "phase" not in self:
                raise Exception("'risk' is undefined because phase is undefined")
            return self.trans.base_risk(0) + Transition.phaserisk(self["phase"]) * self.trans.base_risk(1)
        else:
            raise KeyError(key)


class Ember(object):
    """
    An ember is one set of data in a "burning embers" diagram.
    It contains hazard levels and associated risk levels, as well as the 'draw' method to plot itself.
    """

    def __init__(self):
        """
        Initializes an ember, by creating standard attributes
        """
        self.name = ""
        self.long_name = ""
        self.group = ""
        self.trans = []  # Transitions
        self.haz_valid = [0, 0]  # Hazard range (min, max) for which this ember is assumed valid (= risk was assessed)
        self.hazn = None  # Standard name of the hazard variable
        self.meta = {}  # Dictionnary of ember-related metadata
        self._inited = True
        self.cpal = None  # Needs to be defined before rendering can be done

    def __str__(self):
        """
        So that embers can 'pretty-print' themselves
        :return: Ember name
        """
        return self.name

    def __repr__(self):
        """
        No known way to fully 'represent' embers so this gives a short preview of it
        :return: Ember name/group, 8 first characters
        """
        return f"Ember({self.name[0:8]}/{self.group[0:8]})"

    def __len__(self):
        """
        Returns the number of levels in this ember (total for all transitions)
        """
        # Note: it should be somewhat more efficient to just ask for len(hazl) when hazl is already available
        #       thus this might be useless
        return len(self.levels())

    def trans_append(self, trans):
        trans.be = self
        self.trans.append(trans)

    def levels(self):
        """
        Returns a flat list of levels
        :return:
        """
        # List comprehension can be applied successively: a loop is first done on .trans, then on levels it contains
        return [lv for tr in self.trans for lv in tr.levels]

    def levels_values(self, dname):
        """
        Returns a flat list or np array containing one of the data associated to the levels
        :param dname: the name of that data, that is 'risk' (risk index), 'hazl' (hazard level) or 'conf' (confidence)
        :return:
        """
        if dname in ('risk', 'hazl'):
            # Same method as for levels, but we apply it directly so that there is only one loop
            return np.array([lv[dname] for tr in self.trans for lv in tr.levels])
        elif dname == 'conf':
            return [lv[dname] for tr in self.trans for lv in tr.levels]
        else:
            raise ValueError(dname)

    def draw(self, egr, xpos):
        """
        Draws an ember, using parameters from egr.
        Note: there was an experimental option for "circular", pie-shaped embers;
        it is no longer supported at the moment (05/2023)

        :param egr: an ember graph (including the canvas to draw to and methods that deal with the entire graph)
        :param xpos: the x coordinates that define the ember's drawing area [x0, width]
        """
        c = egr.c
        plotlevels = []
        colorlevels = []

        xmin, xmax = xpos
        yamin = egr.get_y0()
        yamax = egr.get_y1()

        # Get risk and related hazard levels data
        risk = self.levels_values('risk')
        hazl = self.levels_values('hazl')

        # If there is no data, several of the following calculations would fail;
        # until a better solution would be possibly implemented => abort
        # (unfortunately this will not draw the frame around the ember)
        if len(hazl) == 0:
            return xmin + egr.gp['be_x'] / 2

        # Canvas range occupied by the gradients:
        ygmin = min(egr.haztocan(np.min(hazl)), yamin)
        ygmax = max(egr.haztocan(np.max(hazl)), yamax)
        # Canvas range for the "valid" area (intersection of the valid range and axis):
        yvmin = max(egr.get_y0(), egr.haztocan(self.haz_valid[0]))
        yvmax = min(egr.get_y1(), egr.haztocan(self.haz_valid[1]))
        if yvmin == yvmax:
            hlp.addlogfail(f"Critical error: no valid range for this ember.")
            return xmin

        # Remove any transition overlaps within the ember colours (do not change levels used to illustrate transitions)
        ahazl = hazl.copy()
        for ilev in np.arange(len(hazl) - 1):
            if hazl[ilev + 1] < hazl[ilev]:
                ahazl[ilev] = (hazl[ilev + 1] + hazl[ilev])/2.0
                ahazl[ilev+1] = ahazl[ilev]

        # To ensure full consistency, all hazard values are converted to canvas coordinates, and divided
        # by the range of each gradient in these coordinates (ygmax - ygmin) when plotting a gradient.

        # Generate the lists of colour change positions (plotlevels) and coulours (colorlevels):
        for ihaz in range(len(risk)):
            # Fractional position within a gradient of each colour change
            plotlevels.append((egr.haztocan(ahazl[ihaz]) - ygmin) / (ygmax - ygmin))
            # Associated colour
            color = cbyinterp(risk[ihaz], egr.csys, egr.cdefs)
            colorlevels.append(color)
        # Copy the start and end colors at both ends of the plot range
        # (= extend the last colour beyond the last transition):
        plotlevels.append(1.0)
        colorlevels.append(colorlevels[-1])
        plotlevels.insert(0, 0)
        colorlevels.insert(0, colorlevels[0])  # top (copy the last available colour to the 'top' level)

        hlp.addlogmes(f"Hazard range of the gradient: {egr.cantohaz(ygmin):6.2f} ->{egr.cantohaz(ygmax):6.2f} ")
        hlp.addlogmes("Position as % of gradient range: "+", ".join([f"{lv:.5f}" for lv in plotlevels]))
        hlp.addlogmes(f"Colors: {colorlevels}")

        self.drawlinear(egr, xmin, xmax, yamin, yamax, ygmin, ygmax, yvmin, yvmax, plotlevels, colorlevels)

        # Add the name of the BE
        # - - - - - - - - - - -
        if egr.gp['be_name_rotate'] > 0:
            align = 'right'
            # rough estimate of the available length (may be improved if used)
            namlen = np.sqrt((egr.gp['be_x'] + egr.gp['be_int_x'])**2 + egr.gp['be_bot_y'] ** 2)
        else:
            align = 'center'
            namlen = egr.gp['be_x'] + egr.gp['be_int_x'] * 0.95
        c.paragraph(xmin + egr.gp['be_x'] / 2.0, yamin - egr.gp['fnt_size'] * 0.15, self.name,
                          width=namlen, align=align, rotate=egr.gp['be_name_rotate'],
                          valign='top', font=("Helvetica", egr.gp['fnt_size']))

        # Note:
        # Annotating embers could possibly be useful to add information, but it produced PDF errors, hence disabled:
        # (it is an undocumented feature in ReportLab, labelled experimental although appears to be in for years)
        # c.textAnnotation(emb.desc, Rect=[xp, yp, xp+2*cm, yp+2*cm],relative=True)
        # Experimental
        #c.rect(xmin - egr.gp['be_x'] / 2.0, yamin - egr.gp['be_bot_y'], namlen, egr.gp['be_bot_y'],
        #       stroke="transparent", fill="transparent",
        #       tooltip=self.getmeta("description"))

        return xmin + egr.gp['be_x'] / 2

    @staticmethod
    def drawlinear(egr, xmin, xmax, yamin, yamax, ygmin, ygmax, yvmin, yvmax, plotlevels, colorlevels):
        """
        This method handles the drawing of a colour gradient in a box, to fulfill the common needs of
        drawing embers and drawing the legend.
        The arguments are explained in self.draw.
        """
        c = egr.c
        # Set the properties of the box around the ember:
        linewidth = 0.35 * mm
        c.set_stroke_width(linewidth)

        # Useful intermediary variable(s):
        xsiz = xmax - xmin

        # Draw the background grey area in case of 'missing data'
        c.rect(xmin, yamin, xsiz, yamax - yamin, stroke='black', fill='vlgrey')

        # Enclosing rectangle
        rect = (xmin, yvmin, xsiz, yvmax - yvmin)

        # Draw the color gradients
        if yamax - yamin > xmax - xmin:  # vertical (the criteria is based on the axis, regardless of the data)
            c.lin_gradient_rect(rect, (xmin, ygmin, xmin, ygmax), colorlevels, plotlevels)
        else:  # horizontal, for legend only (would not work for regular embers, as these are more complex)
            c.lin_gradient_rect(rect, (xmin, ygmin, xmax, ygmin), colorlevels, plotlevels)

        # Draw the surounding box
        c.rect(xmin, yamin, xsiz, yamax - yamin, stroke='black')

    def drawconf(self, egr, xbas):
        """
        Draws lines and marks indicating the confidence levels.
        :param egr: the EmberGraph object in which this ember is drawn.
        :param xbas: the bottom-left corner of the current ember.
        """
        c = egr.c
        hazl = self.levels_values('hazl')
        if hlp.isempty(hazl) or len(hazl) == 0: return
        color = 'black'

        if norm(egr.gp['show_confidence']) not in ('false', ''):
            # Set the font type and size for the symbols;
            # a scaling factor may be provided as attribute of conf_levels_graph
            fsize = egr.gp['fnt_size'] * egr.gp['conf_levels_graph']
            fname = (egr.gp.get('conf_fnt_name', default=egr.gp['fnt_name'])).strip()  # use specific font if defined
            c.set_stroke_width(0.3 * mm)
            # Get confidence level names and symbols:
            cffile = norm(egr.gp.lst('conf_levels_file'))
            cfgraph = egr.gp.lst('conf_levels_graph')

            # Define the 'gap' between confidence lines which make sures that they are not contiguous:
            ygap = egr.get_y() * 0.005
            maxychi = hazl[0]  # Top of uncertainty range lines so far, to detect overlaps (initial val for ember)
            midychi = hazl[0]  # Middle of uncertainty range lines so far, to detect large overlaps
            lconflen = 0  # Stores the length of the last uncertainty range mark, to help further staggering

            # Basis position of conf levels marks on the horizontal axis
            # (xconfstep is also used to stagger the lines showing uncertainty ranges)
            if norm(egr.gp['show_confidence']) == 'on top':
                xconfstep = min(0.1 * egr.gp['be_x'], 4 * mm)
                xconf = xbas + xconfstep
                otop = True
            else:
                xconfstep = min(0.1 * egr.gp['be_int_x'], 2 * mm)
                xconf = xbas + egr.gp['be_x'] + xconfstep
                otop = False

            # Plot the confidence markings
            # . . . . . . . . . . . . . . .
            # Confidence markings may be conceptually complex; a technical information note explains the rules.
            overlapstag = 0
            for tran in self.trans:
                plevels = tran.levels
                ilo = 0  # the index of the level, inside a transition, for the start of a potential conf line
                ihi = len(plevels) - 1  # the index for the end of a potential conf line
                while ilo < ihi:
                    levlo = plevels[ilo]
                    levhi = plevels[ihi]
                    if hlp.isempty(levlo['conf']) and hlp.isempty(levhi['conf']):
                        # No confidence statement on both low and high levels: do nothing
                        ilo += 1
                        ihi -= 1
                        continue
                    if hlp.isempty(levlo['conf']):
                        # Lower level has no confidence statement: skip (this can't be an uncertainty range)
                        ilo += 1
                        continue
                    if levlo['conf'] != levhi['conf'] and not hlp.isempty(levhi['conf']):
                        hlp.addlogwarn(f"Could not define an uncertainty range for {self.name}, {tran.name}",
                                       critical=True)
                        break

                    # Calculate limits of the colour transitions along the hazard axis
                    # Lower limit of the transition 'line' in canvas coordinate (+ygap = reduce length by 2*yap):
                    yclo = egr.haztocan(levlo['hazl']) + ygap
                    if yclo >= egr.get_y1():  # Skip any transition that would be entirely outside the plot range
                        hlp.addlogmes('A transition is above the top of the hazard axis => skipped')
                    else:
                        # The "min" below avoids extension of the shown line above the upper end of the graph (axis)
                        ychi = min(egr.haztocan(levhi['hazl']) - ygap, egr.get_y1())
                        yconf = (yclo + ychi) / 2.0 - fsize / 3.0

                        # Move the line and conf label to the right if there is an overlap:
                        # (1) only the lower end of the line has an overlap
                        if yclo <= maxychi:
                            overlapstag += xconfstep / 2.0
                        else:
                            overlapstag = 0
                        # (2) even the confidence level text mark has an overlap - further move to the right:
                        if yclo <= midychi:
                            overlapstag += lconflen * fsize / 2.0

                        # Updates to detect overlaps in the upcoming uncertainty ranges
                        maxychi = max(maxychi, ychi)
                        midychi = max(midychi, yconf)

                        # If 'on top' of ember, set confidence levels colour to ensure visibility:
                        if otop:
                            backcol = cbyinterp((levlo['risk'] + levhi['risk']) / 2, egr.csys, egr.cdefs)
                            if backcol.luminance() > 0.5:  # Bright background
                                color='black'
                            else:
                                color='white'
                        # Convert the confidence level name to the symbol from the graph parameters
                        lconf = levlo['conf']
                        try:
                            conf = cfgraph[cffile.index(lconf)]
                        except ValueError:
                            hlp.addlogwarn(
                                'Confidence level from file could not be converted to graph symbol: ' + lconf)
                            conf = ""
                        c.line(xconf + overlapstag, yclo, xconf + overlapstag, ychi, stroke=color)
                        c.string(xconf + fsize / 8 + overlapstag, yconf, conf, font=(fname, fsize), color=color)
                        lconflen = len(conf)  # To handle staggering of the next line, if needed

                    # End of the processing of this potential uncertainty range: get ready for the next one
                    ilo += 1
                    ihi -= 1

    def check(self, egr):
        """
        Checks consistency of the ember's data.
        Access to egr (ember graph) is needed because the color palette is in egr, while the last check relates
        to potential "missing levels", such as an ember which has data for "very high risk" but is missing a transition
        to moderate or to high risk. In the original EmberFactory, the sequence of risk levels was only defined in
        the colour palette; if that changes, i.e. there are fixed risk levels, access to egr may no longer be needed.
        :param egr: the EmberGraph object in which this ember is intended to be drawn.
        :return:
        """
        hazl = self.levels_values('hazl')
        risk = self.levels_values('risk')
        if len(self.trans) == 0 or len(self.trans[0].levels) < 2:
            hlp.addlogwarn("No data or insufficient data for an ember: " + self.name, critical=True)
        else:
            for ilev in np.arange(len(hazl) - 1):
                rdir = 1 if (risk[-1] >= risk[0]) else -1
                if ((hazl[ilev + 1] - hazl[ilev]) * rdir) < 0:
                    # While it might be that some risk decreases with hazard, this is unusual => issue warning
                    hlp.addlogwarn("Risk does not increase with hazard or a transition ends above the start of"
                                   " the next one [" + str(hazl[ilev]) + " then " + str(hazl[ilev + 1])
                                   + "] for ember: " + self.name)

            r0 = min(risk)
            r1 = max(risk)
            for irisk in egr.cpal.cdefs[0]:  # For all risk levels that are associated to a colour...
                # Catch any risk level that is within the range of this ember but not defined in this ember:
                if r0 <= irisk <= r1 and irisk not in risk:
                    hlp.addlogwarn(
                        "An intermediate risk level appears undefined; this will likely result in an abnormal "
                        "colour transition for ember: '" + self.name + "'", critical=True)

    def gethazl(self, itrans, phase):
        """
        Returns the hazard level for a given transition and phase
        :param itrans: # or name of transition in the ember
        :param phase:  name of the transition phase (min, max, median...)
        """
        trans = self.trans[itrans] if type(itrans) is int else self.transbyname(itrans)
        return trans[phase]["hazl"]

    def transnames(self):
        return [trans.name for trans in self.trans]

    def transbyname(self, name):
        try:
            itrans = self.transnames().index(name)
        except KeyError:
            return None
        return self.trans[itrans]

    def getmeta(self, name, default=None, html=False):
        """
        Returns ember-related metadata (these differ from file-related metadata).
        :param name: the name of the parameter to be returned.
        :param html: replace all linebreaks with <br>
        :param default: a default value, for use when there is no metadata corresponding to this name
        :return: the requested metadata, or None if the metadata is not defined.
        """
        try:
            value = self.meta[name]
            if value is not None and html:
                value = hlp.htmlbreaks(value)
        except KeyError:
            value = default
        if value is None and default is not None:
            value = default
        return value


class EmberGraph(object):
    """
    EmberGraphs stores the general information on a graphic containing embers,
    and provides methods for drawing such graphs (except for the embers themselves, which are dealt with
    in the Ember class)
    We have included the creation of the drawing canvas here because we want to perfom some intialisation
    before the main program can access the canvas; before that, it could draw RGB color on an otherwise CMYK figure,
    now the main drawing parameters are set here to prevent that.
    """

    def __init__(self, outfile, cpal, gp, size=(1,1), circular=False, grformat="PDF"):
        """
        :param outfile: the intended outfile path
        :param cpal: a dict defining a color palette
        :param gp: a dict of graphic parameters
        :param circular: draws a 'circular' version of the embers; the distance to the center represents 'hazard',
                         and the coulour gradients remain identical to what they are in the 'straight ember' version;
                         this differs from a polar diagram, in which distance to the center may represent risk.
                         Circular diagrams are at alpha dev. stage for the moment.
        """
        self._protected = ()  # Will include the names of protected parameters once set (see pincoord)
        self._y0 = 0.0
        self._y1 = 0.0
        self._y = 0.0
        self._hz0 = 0.0
        self._hz1 = 0.0
        self._hz = 0.0

        self.cpal = cpal
        self.csys = cpal.csys
        self.cdefs = cpal.cdefs
        self.cnames = cpal.cnames
        self.gp = gp
        self.circular = circular
        self.glen = 10  # Default number of embers in the current group; needed for circular diagrams.

        # Define the drawing canvas
        self.c = canvas.get_canvas(outfile, colorsys=self.csys, size=size, grformat=grformat)  # drawing canvas
        self.colors = self.c.colors

        # fixed graphic parameters
        self.txspace = min(0.05 * self.gp['scale_x'], 1*mm)  # Spacing between tick or grid line and text
        self.lxticks = min(0.1 * self.gp['scale_x'], 2*mm)   # Length of ticks

        # presence of axis. Todo: consider simplifying this, invented lately in v1.5 to solve layout issues
        # those values are set when the axis is drawn, and taken into account to draw any specific user grid lines.
        self.hasvl = False  # whether the graph has a line on the vertical axis to the left (l)
        self.hasvr = False  # (...) to the right (r)

    def isdefined(self, gpname):
        if gpname not in self.gp:
            return False
        else:
            return not isempty(self.gp[gpname])

    def pincoord(self, be_y0, be_y):
        """
        Establishes the correspondance between hazard values and 'physical' coordinates on the canvas.
        To avoid potential inconsistencies, the coordinates should be changed only with this function, so that
        every use mapping from hazard to canvas is done in the same way.
        Note: be_y0, be_y0+be_y define the drawing area on the canvas and correspond to haz_axis_bottom, haz_axis_top;
        (however it is permitted to enter data outside the haz_ range, they will remain invisible but may have
        a visible impact trough interpolation from a visible data point)

        :param be_y0: bottom of the drawing area on the canvas
        :param be_y: height of the drawing area on the canvas
        """
        # All of the following are 'protected' variables: they should not be changed from outside the EmberGraph class.
        # PyCharm (at least) provides a warning against this because it would like to have it in __init__;
        # Such a change would not be possible without a broader refactoring and does not appear needed.
        self._protected = ()
        self._y0 = be_y0
        self._y1 = be_y0 + be_y
        self._y = be_y
        self._hz0 = self.gp['haz_axis_bottom']
        self._hz1 = self.gp['haz_axis_top']
        self._hz = self._hz1 - self._hz0
        self._protected = ('_y0', '_y1', '_y', '_hz0', '_hz1', '_hz')

    # Need to allow reading y0 and y without it being regarded as a violation of its "protected" status (_y)
    def get_y0(self):
        return self._y0

    def get_y1(self):
        return self._y1

    def get_y(self):
        return self._y

    def __setattr__(self, key, value):
        """
        Enforces protection of a tuple of protected variables when changing attributes

        :param key: the name of the attribute to be changed
        :param value: the value of the attribute to be change
        """
        if hasattr(self, '_protected') and key in self._protected:
            raise Exception("Attempt at changing a protected variable (set by pincoord): " + str(key))
        object.__setattr__(self, key, value)

    def haztocan(self, hazvalue):
        """
        Calculates the position in canvas coordinate for a given hazard value.

        :param hazvalue: a value on the y-axis (hazard axis, e.g. temperature)
        :return: the result of the scaling to the y canevas coordinates
        """
        hz0 = self._hz0
        hz = self._hz
        y = self._y
        y0 = self._y0
        return y0 + y * (hazvalue - hz0) / hz

    def cantohaz(self, canvalue):
        """
        Inverse of haztocan. Provides the hazard value of a given y position on the canvas.

        :param canvalue: a 'physical' position on the y-axis, in canvas coordinates
        :return: the hazard value
        """
        hz0 = self._hz0
        hz = self._hz
        y = self._y
        y0 = self._y0
        return ((canvalue - y0) * hz / y) + hz0

    def hx1to2(self, haz1):
        """
        Experimental service fct for the secondary axis, TBD
        :param haz1:
        :return:
        """
        return self.gp['haz_axis2_factor'] * haz1 + self.gp['haz_axis2_shift']

    def hx2to1(self, haz2):
        """
        Experimental service fct for the secondary axis, TBD
        :param haz2:
        :return:
        """
        return (haz2 - self.gp['haz_axis2_shift']) / self.gp['haz_axis2_factor']

    def vaxis(self, xbas, nbe, showname=True):
        """
        Plots the (one or two) 'hazard' axis graduation values, tick marks and grid lines

        :param xbas: the x coordinate at the left of the ember group (start position and width on the canvas)
        :param nbe: the number of burning ember columns to be included, to calculate the length of grid lines
        :param showname: whether the name of the axis should be drawn.
        :return: the x coordinate at the left of the grid lines, as a starting point to draw the embers
        """
        # Total width of the 'drawing area' (except for tick marks out of the main frame)
        sx = nbe * (self.gp['be_x'] + self.gp['be_int_x'])

        # Set drawing properties (colour of the main horizontal lines)
        self.c.set_stroke_width(0.35 * mm)

        # Draw the name of the axis
        xnam = self.gp['haz_name_x']
        if showname:
            axname = self.gp['haz_name']
            ax2name = self.gp['haz_axis2_name']
            xbas += xnam
        else:
            axname = None
            ax2name = None

        # Start (left) of the grid-lines
        lbx = xbas + self.gp['scale_x']

        # Draw main (left) axis and grid lines (ebx is the right-end of the current drawing area)
        ebx = self._drawaxis(lbx, sx, axname=axname, axunit=self.gp['haz_unit'], axside='left',
                             grid=self.gp['haz_grid_show'], nmticks=self.gp['haz_axis_minorticks'])

        # Draw secondary (right) axis and grid lines
        if self.gp['haz_axis2'] in ["True", "Right"]:
            grid = self.gp['haz_grid_show'] if hlp.isempty(self.gp['haz_grid2_show']) else self.gp['haz_grid2_show']
            ebx = self._drawaxis(lbx, sx, altaxfct=(self.hx1to2, self.hx2to1), axname=ax2name,
                                 axunit=self.gp['haz_axis2_unit'], axside='right', grid=grid,
                                 nmticks=self.gp['haz_axis2_minorticks'])

        # Add any user-defined specific grid lines  (might be delegated as done with _drawaxis above, but more complex)
        axunit = " " + self.gp['haz_unit'] if axname is None or self.gp['haz_unit'] not in axname else ""
        tbx = lbx - self.txspace - self.lxticks * self.hasvl  # right-end of text strings
        if self.gp.lst('haz_grid_lines'):
            glcolors = norm(self.gp.lst('haz_grid_lines_colors'))
            gllabels = self.gp.lst('haz_grid_lines_labels')
            gllaboffs = self.gp.lst('haz_grid_lines_labels_off')
            glends = self.gp.lst('haz_grid_lines_ends')  # Used to get a colored area, eg. 'recent temp'
            self.c.set_stroke_width(0.35 * mm)
            for ic, haz in enumerate(self.gp.lst('haz_grid_lines')):
                glcolor = self.colors[glcolors[ic]] if hlp.hasindex(glcolors, ic) else self.colors['lgrey']
                try:
                    yp = self.haztocan(float(haz))
                except ValueError:
                    hlp.addlogwarn("Could not process data for a custom haz_grid_line")
                    continue
                if hlp.hasindex(glends, ic):
                    # Colored area (between the standard grid-line and grid-line-ends)
                    sy = self.haztocan(glends[ic]) - self.haztocan(haz)
                    self.c.rect(lbx - self.lxticks * self.hasvl, yp,  sx + self.lxticks * self.hasvl, sy,
                                stroke=None, fill=glcolor)
                else:
                    # Grid-lines
                    sy = 0.0
                    self.c.line(lbx - self.lxticks * self.hasvl, yp, lbx + sx, yp, stroke=glcolor)
                # Prepare for drawing label (for colored areas, the text is centered by using sy/2)
                gllabel = gllabels[ic] if hlp.hasindex(gllabels, ic) else (str(haz) + axunit)
                sby = yp + sy / 2.0
                # Handle custom label offsetting (see documentation about haz_grid_lines_labels_off)
                if hlp.hasindex(gllaboffs, ic):
                    oby = sby
                    # Move the label
                    sby += gllaboffs[ic] * self.gp['fnt_size']
                    # Draw a small connecting line
                    xp = tbx + self.gp['fnt_size'] * 0.1
                    obx = xp + self.gp['be_int_x'] / 4.0 + self.gp['fnt_size'] * 0.2
                    yp = sby + self.gp['fnt_size'] * 0.05
                    self.c.line(xp, yp, obx, oby, stroke='lgrey', stroke_width= 0.3 * mm)
                # Add label
                self.c.paragraph(tbx, sby, gllabel, align='right', valign="center", color='dgrey',
                                 font=(None, self.gp['fnt_size']))

        # Draw verical axis line if needed (it can't be done before because it needs to be on top)
        if self.hasvl:
            self.c.line(lbx, self.get_y0(), lbx, self.get_y1())
        if self.hasvr:
            self.c.line(lbx + sx, self.get_y0(), lbx + sx, self.get_y1())

        return lbx, ebx

    def _drawaxis(self, lbx, sx, altaxfct=None, axname='', axunit='', axside='left', grid="all", nmticks=None):
        """
        Generic axis-drawing function, handling left and right axis as well as grid lines
        :param lbx: the x location of the left of the drawing area
        :param sx: the size of the drawing area
        :param altaxfct: if provided, works as 'functions' in matplotlib.axes.Axes.secondary_xaxis;
               must be a 2-tuple of functions which define the transform function and its inverse, that is
               (from the standard axis(1) to the defined axis(2), from the defined axis(2) to the standard(1))
        :param axname: axis name
        :param axunit: axis unit
        :param axside: the side of the drawing area: 'left' or 'right'
        :param grid: whether the horizontal axis grid lines must be drawn (True) or just tick marks (False)
        :param nmticks: number of minor tick marks
        :return:
        """
        withgrid = hlp.norm(grid) == "all"
        if altaxfct is None:
            def ax1toax2(ax): return ax
            def ax2toax1(ax): return ax
        else:
            ax1toax2, ax2toax1 = altaxfct
        # Prepare unit for axis labels: if it is in the axis name, do not include it in the labels:
        if axunit == '':
            axunit = self.gp['haz_unit']
        else:
            axunit = " " + axunit if axname is None or axunit not in axname else ""

        hxend = lbx + sx
        # Draw the name of the axis
        xnam = self.gp['haz_name_x'] * 0.6
        if axside == 'right':
            hxend += self.gp['scale_x']
            if axname:
                xnam = hxend + self.gp['haz_name_x'] * 0.4
            hxend += self.gp['haz_name_x']

        if axname:
            parylen = self.gp['be_y'] + self.gp['be_bot_y'] + self.gp['be_top_y']
            # Warning: the 'reference frame' is rotated -> coordinates work differently
            self.c.paragraph(xnam, self._y0 + self.gp['be_y']/2.0, axname, width=parylen,
                             font=(self.gp['fnt_name'], self.gp['fnt_size']), align='center', rotate=90)

        # Get nice looking levels for the horizontal lines
        glines, labfmt, mticks = hlp.nicelevels(ax1toax2(self._hz0), ax1toax2(self._hz1),
                                                nalevels=self.gp['haz_grid_lines'], enclose=False, nmticks=nmticks)

        # Define line start, line end, axis levels text position, and draw
        olbx = lbx  # Left edge of the drawing area, where a line showing the axis could be drawn
        orbx = lbx + sx  # Same for the right side
        hasvbx = not (withgrid and mticks is None)  # If true, the vertical line showing the axis will be drawn
        if axside == 'right':
            tbx = orbx + self.txspace + self.lxticks * hasvbx  # start of text strings
            ollx = olbx
            orlx = orbx + self.lxticks * hasvbx  # end of lines (= drawing area edge + tick mark)
            talign = 'left'
            self.hasvr = hasvbx
        else:  # Left axis
            tbx = olbx - self.txspace - self.lxticks * hasvbx  # end of text strings
            ollx = olbx - self.lxticks * hasvbx  # start of lines (= drawing area edge - tick mark)
            orlx = orbx
            talign = 'right'
            self.hasvl = hasvbx

        color='lgrey'
        if withgrid:
            if axside == 'right':
                color='grey'
        else:
            # No grid, just ticks (adapt the length of lines)
            color='black'
            if axside == 'right':
                ollx = orbx
            else:
                orlx = olbx

        # Draw the main ticks or grid and their labels
        for haz in glines:
            yp = self.haztocan(ax2toax1(haz))
            self.c.line(ollx, yp, orlx, yp, stroke=color)
            gllabel = labfmt.format(haz) + axunit
            # ^^^PyCharm is not happy whenever a string is used as format because it could be "insecure";
            #    I don't think that there is any risk as long as it is actually prescribed among a list of valid strings
            #    as done in "helpers" (labmfmt can only come from hlp.nicelevels).
            #    See https://stackoverflow.com/questions/15356649
            self.c.string(tbx, yp - self.gp['fnt_size'] * 0.3, gllabel, align=talign,
                          font=(None, self.gp['fnt_size']))

        # Minor ticks
        if mticks is not None:
            for haz in mticks:
                if axside == 'right':
                    ollx = orbx
                else:
                    orlx = olbx
                yp = self.haztocan(ax2toax1(haz))
                self.c.line(ollx, yp, orlx, yp)

        self.c.setLineStyle="plain"

        return hxend

    def drawlegend(self, emberbox, isinside):
        """
        Draws a legend (colour bar)

        :param emberbox: a box representing the ember diagram area to which the legend needs to be attached OR
                         in which the legend needs to be drawn
        :param isinside: True if the legend needs to be inside emberbox,
                         False if it needs to be attached outside emberbox
                         (needed because isinside is decided together with emberbox, it is not an input parameter)
        :return: additional horizontal space that is needed because it is occupied by the legend.
        """
        c = self.c
        gp = self.gp
        if norm(gp['leg_pos']) in ['under', 'in-grid-horizontal']:
            ishoriz = True
        else:
            ishoriz = False
            if norm(gp['leg_pos']) not in ['right', 'in-grid-vertical']:
                hlp.addlogwarn("Parameter leg_pos has an unknown value: " + str(gp['leg_pos']))

        # pseudo-ember used as legend:
        rlevels = self.cdefs[0]
        # include each level twice to have color transition + uniform area:
        plotlevels = np.arange(len(rlevels) * 2, dtype=float)
        plotlevels = plotlevels / plotlevels[-1]  # normalize
        colorlevels = np.repeat(rlevels, 2)
        colorlevels = [cbyinterp(clev, self.csys, self.cdefs) for clev in colorlevels]

        # Intermediate variables for the position of the legend

        # Size of the legend area
        # Here x and y are in 'legend coordinates', ie x is along the main axis of the legend (vertical OR horizontal)
        ltot_y_h = gp['leg_bot_y'] + gp['leg_y'] + gp['leg_top_y']
        # For vertical embers, the width depends on the (drawn) length of the risk level names:
        l_cnames = max((stringwidth(name, fontsize=gp['fnt_size']) for name in self.cnames))
        ltot_y_v = gp['leg_y'] + gp['leg_bot_y'] + max(l_cnames, gp['leg_top_y'])
        ltot_y = ltot_y_h if ishoriz else ltot_y_v
        ltot_x = gp['leg_x']
        # Allow the text to extend up to 10% beyond the ember on each side
        # (better could be done if needed, this is a rough trick to have a slightly better design):
        ltot_xtext = ltot_x * 0.2

        # Extension of the canvas space when the legend is outside the current graphic area (=> addright):
        if ishoriz:  # in-grid-horizontal: needs to increase the size of emberbox if too small !
            addright = max(0.0, ltot_x + ltot_xtext - emberbox[2])  # by how much is the legend wider than emberbox ?
            emberbox[2] += addright
        elif not isinside:  # legend on the right : entirely in additional space, but outside emberbox.
            addright = ltot_y
        else:
            addright = 0.0  # in-grid-vertical

        #  Center of emberbox
        boxmid = ((emberbox[0] + emberbox[2] / 2.0), (emberbox[1] + emberbox[3] / 2.0))
        #  Center of the legend area
        lmid_x = boxmid[0] if (ishoriz or isinside) else (emberbox[0] + emberbox[2] + ltot_y / 2.0)
        lmid_y = boxmid[1] if (isinside or not ishoriz) else (emberbox[1] - ltot_y / 2.0)

        #  Position of the legend's burning ember (basis for the entire legend):
        #  Here xpos, ypos are in canvas coordinates.
        if ishoriz:
            xmin = lmid_x - ltot_x / 2.0
            xmax = lmid_x + ltot_x / 2.0
            ymin = lmid_y - ltot_y / 2.0 + gp['leg_bot_y']
            ymax = ymin + gp['leg_y']
        else:  # vertical legend
            xmin = lmid_x - ltot_y / 2.0  # the ember is on the left of the legend
            xmax = xmin + gp['leg_y']
            ymin = lmid_y - ltot_x / 2.0
            ymax = lmid_y + ltot_x / 2.0

        # Draw the 'ember' (for a legend, all y ranges are identical : axis, ember, and valid range):
        Ember.drawlinear(self, xmin, xmax, ymin, ymax, ymin, ymax, ymin, ymax, plotlevels, colorlevels)

        # Draw the text of the legend and connect text to colors with lines
        # -----------------------------------------------------------------
        # Styling parameters for this section:
        c.set_stroke_width(0.5 * mm)
        font_risk=(None, min(gp['fnt_size'], (55.0 / len(rlevels))))  # font family to None = default

        # Position of the lines (link between ember and risk level) relative to the 'ember'(halfway in the solid colors)
        xlines = (plotlevels[1::2] + plotlevels[:-1:2]) / 2.0 * self.gp['leg_x']
        xwidth = xlines[1]-xlines[0]
        # Draw the lines, name of risk levels, and title of paragraph
        if ishoriz:
            for i, xline in enumerate(xlines):
                c.line(xmin + xline, ymin - gp['leg_bot_y'] * 0.4, xmin + xline, (ymin + ymax) / 2.0)
                c.paragraph(xmin + xline, ymin - gp['leg_bot_y'] * 0.4, self.cnames[i], align="center", valign="top",
                            font=font_risk, width=xwidth)
            if gp['leg_title']:
                width = ltot_x + ltot_xtext
                c.paragraph(xmin - ltot_xtext / 2.0 + width / 2.0, ymax + gp['leg_top_y'] * 0.3,
                            gp['leg_title'], width=width, align="center", font=(None, gp['fnt_size']))
        else:  # Vertical ember
            for i, xline in enumerate(xlines):
                c.line((xmin + xmax) / 2.0, ymin + xline, xmax + gp['leg_bot_y'] * 0.5, ymin + xline)
                c.string(xmax + gp['leg_bot_y'] * 0.6, ymin + xline - 1 * mm, self.cnames[i])
            if gp['leg_title']:
                c.paragraph(xmin, ymax + gp['leg_x'] * 0.05, gp['leg_title'], width=ltot_y, align="left",
                            breakwords=False, font=(None, gp['fnt_size']))

        c.set_stroke_width(0.35 * mm)

        # Draw the legend for the confidence level marks. This is currently in term of placement within the global
        # layout; to further improve, one should consider using ReportLab's flowable elements, and would most likely
        # need to have each part of a figure able to return its dimensions on the canvas before being drawn, to
        # enable better placement.
        if gp['leg_conf']:
            if norm(gp['leg_pos']) == 'under':
                self.drawconflegend(lmid_x + (ltot_x + ltot_xtext)/2.0 + 0.5*cm,
                                    ymax + gp['leg_top_y'] * 0.85)
                # Unfinished: the legend might extend beyond the right limit of the graph, fixing this is not easy.
            if norm(gp['leg_pos']) == 'right':
                self.drawconflegend(xmin, ymin - 0.5*cm)

        # Return the horizontal length added to the draw area in the canvas.
        return addright

    def drawconflegend(self, xbas, ybas):
        """
        Draws a legend for the confidence level marks (e.g. * = low confidence).
        Use of this legend is currently limited in terms of layout. Improving the layout would require changes in
        EmberGraph.drawlegend(). To facilitate this, it might be useful to allow drawconflegend to run without drawing,
        only return the width/height of the area needed for drawing.
        It would probably be even better to construct legends as ReportLab "widgets", or "flowables"
        (a quick overview does not tell me which of these would be the best... flowables appear more appropriate
        because they have to return their sizes, but it means all our diagram elements would have to be flowables?)

        :param xbas:
        :param ybas:
        :return: the length of the confidence level's legend, on the horizontal axis
        """
        cfnames = self.gp.lst('conf_levels_file')
        cfsymbs = self.gp.lst('conf_levels_graph')
        tfsize = self.gp['fnt_size']
        sfsize = tfsize * self.gp['conf_levels_graph']
        padding = tfsize * 0.6  # space around the legend's text
        xp = xbas  # Start of the text (! padding removed - may need further thinking?)
        yp = ybas - padding - tfsize
        xslen = 2.0 * sfsize  # Width of the column of conf symbols
        yslin = 1.2 * tfsize  # Height of a line
        self.c.string(xp, yp, "Confidence levels")
        xlen = 0
        for cfsymb, cfname in zip(cfsymbs, cfnames):
            yp -= yslin
            self.c.string(xp, yp - 1 * mm, cfsymb, font=('Helvetica', sfsize))
            namelen = self.c.string(xp + xslen, yp, cfname)
            xlen = max(xlen, namelen)

        xlen = xlen + xslen + 2.0*padding

        return xlen

class ColourPalette:
    """
    Reads the color palette. Importantly, this also defines the "risk scale" (sequence of risk indexes & colours).
    The palette is defined by:
     - its color system (RGB, CMYK...): csys
     - names of risk levels associated to colors : cnames (see Excel sheet)
     - a risk level index: cdefs[0] (1D numpy array of risk indexes)
     - the color densities for each color corresponding to a risk index :
         cdefs[i] (1D numpy array of color densities for each risk index, given i=#color within the color system)
     - the set of transitions that it defines: transnames_risk is a dict linking transition names to risk levels,
         such as {"high to very high": (2, 1)}, which means that this transition extends from risk index 2 to index 2+1
    Todo: further improve this class, which is a quick conversion from the former function (getcpal)
    """

    def __init__(self, wbcol, prefcsys=None, cpalname=None):
        """
        Creates an EmberFactory colour palette by reading it from an Excel workbook
        :param wbcol: an Excel workbook from openpyxl
        :param prefcsys: a colour system choice from the user, among (RGB, CMYK, *standard);
                        'RGB' or 'CMYK' will use *default* palettes defined below;
                        'standard' means that the user makes no choice in the UI;
    -                    When 'standard' is included, it will go through several steps to get a palette, using
                        1) cpalname if set (this should come from the parameter in the spreadsheet),
                        2) 'ACTIVE-P' if it is set; if is also unavailable,
                        3) revert to the internal default (RGB-SRCCL-C7).
                        ACTIVE-P is a legacy parameter which may be provided in the 'colour' spreadsheet (read here).
                        Note: this is cluttered due to legacy support; ACTIVE-P might be dropped in the future.
        :param cpalname: the name of the desired palette, used only if the color sheet does not set 'ACTIVE-P'
        """
        self.cnames = []
        self.csys = None
        self.cdefs = None
        read = False
        ctmp = []
        cref = 1.0  # Reference (max) value of the color range (optional parameter)
        sht = wbcol["Color definitions"]
        # Default palette (if no palette defined in the color sheet or provided as cpalname
        if prefcsys == 'RGB':  # if prefcsys is set to RGB or CMYK, it gets the priority over any parameter
            cpalname = 'RGB-SRCCL-C7'
        elif prefcsys == 'CMYK':
            cpalname = 'CMYK-IPCC'
        elif not cpalname:
            # if prefcsys did not specify a colour system and cpalname is not set,
            # then we set a default here and will overwrite it below if 'ACTIVE-P' is found
            cpalname = 'RGB-SRCCL-C7'

        for row in sht.rows:
            key = hlp.stripped(row[0].value)
            name = hlp.stripped(row[1].value)
            inda = [acell.value for acell in row[2:]]  # input data
            if key == 'ACTIVE-P' and 'standard' in prefcsys:
                cpalname = name  # ACTIVE-P is a legacy parameter
            elif key == 'PALETTE' and cpalname == name:
                hlp.addlogmes('Will use color palette: ' + cpalname)
                read = True
            elif key == '' or key is None:
                read = False
            elif key == 'HEADERS' and read:
                if inda[1:4] == ['Red', 'Green', 'Blue']:
                    self.csys = 'RGB'
                elif inda[1:5] == ['Cyan', 'Magenta', 'Yellow', 'Black']:
                    self.csys = 'CMYK'
                else:
                    raise Exception("Unknown color system (see colors in sheet 'Color definitions').")
            elif key == 'DATA' and read:
                self.cnames.append(name)
                ctmp.append(inda[:1 + len(self.csys)])
            elif key == 'REFERENCE' and read:
                # The "reference" is an arbitrary number that is the maximum of colour values, typically 1, 100, or 255.
                # (default value is 1, see above)
                try:
                    cref = float(inda[0])
                except ValueError:
                    raise ValueError\
                        ("REFERENCE value for the colors is wrong or misplaced (must be 3rd col in palette definition)")
        if len(self.cnames) < 2:
            raise Exception("Colour palette '{}' could not be found or was incorrectly defined.".format(cpalname))
        cdiv = [1.0] + ([cref] * (len(ctmp[0]) - 1))  # We need to divide each line by the ref, but not element 0
        self.cdefs = (np.array(ctmp) / cdiv).transpose()  # color definitions array
        del ctmp
        hlp.addlogmes("Palette risk levels and colors: " + str(self.cdefs))
        self.name = cpalname

        # transnames_risk is a dict linking transition names to their (base risk level, risk level change),
        # such as {"high to very high": (2, 1)}, which means that this transition extends from index 2 to index 2+1
        self.transnames_risk={}
        ridx = self.cdefs[0]
        for ibeg in range(len(self.cnames)-1):
            transname = hlp.norm(self.cnames[ibeg]) + " to " + hlp.norm(self.cnames[ibeg+1])
            self.transnames_risk[transname] = (ridx[ibeg], ridx[ibeg+1] - ridx[ibeg])

            # Downward risk transitions (including for increasing benefits <0 risk index)
            transname = hlp.norm(self.cnames[ibeg+1]) + " to " + hlp.norm(self.cnames[ibeg])
            self.transnames_risk[transname] = (ridx[ibeg+1], ridx[ibeg] - ridx[ibeg+1])
