#!/usr/bin/python
#
# Copyright (C) 2008  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Luke Macken <lmacken[at]redhat.com>
#            Miroslav Lichvar <mlichvar[at]redhat.com>
#            Edward Sheldrake <ejsheldrake[at]gmail.com>
#	     Arnaud Valensi <arnaud.valensi[at]gmail.com>

import xdg.Menu, xdg.DesktopEntry, xdg.Config
import re, sys, os
from xml.sax.saxutils import escape

icons = True

try:
	from gi.repository import Gtk
except ImportError:
	icons = False

def icon_attr(entry):
	if icons is False:
		return ''

	name = entry.getIcon()

	if os.path.exists(name):
		return ' icon="' + name + '"'

	# work around broken .desktop files
	# unless the icon is a full path it should not have an extension
	name = re.sub('\..{3,4}$', '', name)

	# imlib2 cannot load svg
	iconinfo = theme.lookup_icon(name, 22, Gtk.IconLookupFlags.NO_SVG)
	if iconinfo:
		iconfile = iconinfo.get_filename()
		iconinfo.free()
		if iconfile:
			return ' icon="' + iconfile + '"'
	return ''

def escape_utf8(s):
	return escape(s.encode('utf-8', 'xmlcharrefreplace'))

def entry_name(entry):
	return escape_utf8(entry.getName())

def walk_menu(entry):
	if isinstance(entry, xdg.Menu.Menu) and entry.Show is True:
		print '<menu id="%s" label="%s"%s>' \
			% (entry_name(entry),
			entry_name(entry),
			escape_utf8(icon_attr(entry)))
		map(walk_menu, entry.getEntries())
		print '</menu>'
	elif isinstance(entry, xdg.Menu.MenuEntry) and entry.Show is True:
		print '	<item label="%s"%s>' % \
			(entry_name(entry.DesktopEntry).replace('"', ''),
			escape_utf8(icon_attr(entry.DesktopEntry)))
		command = re.sub(' -caption "%c"| -caption %c', ' -caption "%s"' % entry_name(entry.DesktopEntry), entry.DesktopEntry.getExec())
		command = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', command)
		if entry.DesktopEntry.getTerminal():
			command = 'xterm -title "%s" -e %s' % \
				(entry_name(entry.DesktopEntry), command)
		print '		<action name="Execute">' + \
			'<command>%s</command></action>' % command
		print '	</item>'

menu_list = []
submenu_list = []
submenu = []

def generate_awesome_menu(entry):
	global submenu
	global submenu_list
	if isinstance(entry, xdg.Menu.Menu) and entry.Show is True:
		global menu_list
		menu_list.append(entry_name(entry))

		if submenu:
			submenu_list.append(submenu);
			submenu = []
		map(generate_awesome_menu, entry.getEntries())
	elif isinstance(entry, xdg.Menu.MenuEntry) and entry.Show is True:
		second = re.sub(' -caption "%c"| -caption %c', ' -caption "%s"' % entry_name(entry.DesktopEntry), entry.DesktopEntry.getExec())
		second = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', second)
		if entry.DesktopEntry.getTerminal():
			second = 'xterm -title "%s" -e %s' % \
				(entry_name(entry.DesktopEntry), second)
		first = entry_name(entry.DesktopEntry).replace('"', '')
		first = first.replace('"', '\\"')
		second = second.replace('"', '\\"')
		submenu.append((first, second));

def generate_main_menu():
	global submenu_list
	global menu_list

	# print submenu_list
	# print menu_list

	i = 0
	for elem in submenu_list:
		print "submenu%d =\n{" % i
		j = 0
		for entry in elem:
			if j == len(elem) - 1:
				print "  { \"%s\", \"%s\" }" % (entry[0], entry[1])
			else:
				print "  { \"%s\", \"%s\" }," % (entry[0], entry[1])
			j += 1
		print '}'
		i += 1
	print 'myappmenu =\n{'
	i = 0
	for entry in menu_list:
		if i == len(menu_list) - 1:
			print "  { \"%s\", submenu%d }" % (entry, i)
		else:
			print "  { \"%s\", submenu%d }," % (entry, i)
		i += 1
	print '}'

if len(sys.argv) > 1:
	menufile = sys.argv[1] + '.menu'
else:
	menufile = 'applications.menu'

lang = os.environ.get('LANG')
if lang:
	xdg.Config.setLocale(lang)

# lie to get the same menu as in GNOME
xdg.Config.setWindowManager('GNOME')

if icons:
  theme = Gtk.IconTheme.get_default()

menu = xdg.Menu.parse(menufile)

#map(walk_menu, menu.getEntries())
map(generate_awesome_menu, menu.getEntries())

generate_main_menu()

