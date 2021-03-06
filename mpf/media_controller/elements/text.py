"""Contains the parent class of the Text DisplayElement"""

# text.py
# Mission Pinball Framework
# Written by Brian Madden & Gabe Knuth
# Released under the MIT License. (See license info at the end of this file.)

# Documentation and more info at http://missionpinball.com/mpf

import pygame

from mpf.media_controller.core.display import DisplayElement


class Text(DisplayElement):


    """Represents an animation display element.

    Args:
        slide: The Slide object this animation is being added to.
        machine: The main machine object.
        text: A string of the text you'd like to display. If you have the
            multi-language plug-in enabled, this text will be run through the
            language engine before it's displayed.
        x: The horizontal position offset for the placement of this element.
        y: The vertical position offset for the placement of this element.
        h_pos: The horizontal anchor.
        v_pos: The vertical anchor.

    Note: Full documentation on the use of the x, y, h_pos, and v_pos arguments
    can be found at: https://missionpinball.com/docs/displays/display-elements/positioning/

    """

    def __init__(self, slide, machine, text, x=None, y=None, h_pos=None,
                 v_pos=None, layer=0, **kwargs):

        super(Text, self).__init__(slide, x, y, h_pos, v_pos, layer)

        # todo move these defaults to mpfconfing.yaml
        self.text = ''
        self.fonts = machine.display.fonts
        self.language = machine.language
        self.slide = slide

        self.adjust_colors(**kwargs)

        kwargs['color'] = self.adjusted_color
        kwargs['bg_color'] = self.adjusted_bg_color

        if 'number_grouping' in kwargs and kwargs['number_grouping']:

        # todo this only works for ints
        # todo move enabling this and separator char to config

            # find the numbers in the string
            number_list = [int(s) for s in text.split() if s.isdigit()]

            # group the numbers and replace them in the string
            for item in number_list:
                grouped_item = self.group_digits(item)
                text = text.replace(str(item), grouped_item)

        if 'double_zeros' in kwargs and kwargs['double_zeros']:
            text = self.double_zeros(text)

        # Are we set up for multi-language>
        if self.language:
            text = self.language.text(text)

        self.text = text

        # Set defaults
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = text

        self.layer = layer
        self.element_surface = self.fonts.render(text=self.text, **kwargs)

        # todo add logic around color/shade

        # todo trim this to a certain size? Or force it to fit in the size?

        self.set_position(x, y, h_pos, v_pos)

    def group_digits(self, text, separator=',', group_size=3):
        """Enables digit grouping (i.e. adds comma separators between
        thousands digits).

        Args:
            text: A string of the text which will be searched for numbers to
                group.
            separator: String of the character(s) you'd like to add between the
                digit groups. Default is a comma. (",")
            group_size: How many digits you want in each group. Default is 3.

        Returns: A string with the separator added. If no numbers were found in
            the string that was passed, the original string will be returned.

        Note: This code came from here:
        http://code.activestate.com/recipes/439357-simple-digit-grouping/

        MPF uses this method instead of the Python locale settings because the
        locale settings are a mess. They're set system-wide and it's really hard
        to make them work cross-platform and there are all sorts of external
        dependencies, so this is just way easier.

        This method only identifies integers.

        """

        if text < 0:
            prefix = '-'
            text = -text;
        else:
            prefix = ''
        string = "{0}".format(text)
        dot_index = string.find('.');
        string_size = len(string) if dot_index == -1 else dot_index

        if string_size > group_size:
            groups = []
            first_group_size = string_size % group_size;
            if first_group_size:
                groups.append(string[0:first_group_size])
            for i in range(first_group_size, string_size, group_size):
                groups.append(string[i:i+group_size])
            return_string = separator.join(groups)

            if dot_index == -1:
                return_string = return_string
            else:
                return_string + string[dot_index:]
        else:
            return_string = string

        return prefix + return_string

    def double_zeros(self, number):
        """Formats a number so if it's zero then it returns a string of "00".

        Args:
            number: The input value as int or string.

        Returns: String "00" if the input is 0. Otherwise returns whatever it
            received unchanged.
        """

        if number == 0 or number == "0":
            return "00"
        else:
            return number

display_element_class = Text
create_asset_manager = False

# The MIT License (MIT)

# Copyright (c) 2013-2015 Brian Madden and Gabe Knuth

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
