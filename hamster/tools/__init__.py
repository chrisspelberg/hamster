# - coding: utf-8 -

# Copyright (C) 2007-2009 Toms Bauģis <toms.baugis at gmail.com>

# This file is part of Project Hamster.

# Project Hamster is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Project Hamster is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Project Hamster.  If not, see <http://www.gnu.org/licenses/>.

import datetime as dt

def add_hint(entry, hint):
    entry.hint = hint        
    
    def _set_hint(self, widget, event):
        if self.get_text(): # don't mess with user entered text
            return 

        self.modify_text(gtk.STATE_NORMAL, gtk.gdk.Color("gray"))
        hint_font = pango.FontDescription(gtk.Style().font_desc.to_string())
        hint_font.set_style(pango.STYLE_ITALIC)
        self.modify_font(hint_font)
        
        self.set_text(self.hint)
        
    def _set_normal(self, widget, event):
        self.modify_text(gtk.STATE_NORMAL, gtk.Style().fg[gtk.STATE_NORMAL])
        hint_font = pango.FontDescription(gtk.Style().font_desc.to_string())
        self.modify_font(hint_font)

        if self.get_text() == self.hint:
            self.set_text("")

    import types
    instancemethod = types.MethodType

    entry._set_hint = instancemethod(_set_hint, entry, gtk.Entry)
    entry._set_normal = instancemethod(_set_normal, entry, gtk.Entry)
    
    entry.connect('focus-in-event', entry._set_normal)
    entry.connect('focus-out-event', entry._set_hint)

    entry._set_hint(entry, None)



def format_duration(minutes, human = True):
    """formats duration in a human readable format.
    accepts either minutes or timedelta"""
    
    if isinstance(minutes, dt.timedelta):
        minutes = duration_minutes(minutes)
        
    if not minutes:
        if human:
            return ""
        else:
            return "00:00"
    
    hours = minutes / 60
    minutes = minutes % 60
    formatted_duration = ""
    
    if human:
        if minutes % 60 == 0:
            # duration in round hours
            formatted_duration += _("%dh") % (hours)
        elif hours == 0:
            # duration less than hour
            formatted_duration += _("%dmin") % (minutes % 60.0)
        else:
            # x hours, y minutes
            formatted_duration += _("%dh %dmin") % (hours, minutes % 60)
    else:
        formatted_duration += "%02d:%02d" % (hours, minutes)
    
    
    return formatted_duration

def duration_minutes(duration):
    """returns minutes from duration, otherwise we keep bashing in same math"""
    return duration.seconds / 60 + duration.days * 24 * 60
