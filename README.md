xdg-menu-to-awesome-wm
======================

Converts a xdg-menu like gnome menu awesome wm format

How To
======================
$ python awesome-xdg-menu.py > ~/.config/awesome/menu.lua

After you have to add "menu.lua" in your "rc.lua", mine look like this:

-- {{{ Menu
-- Create a laucher widget and a main menu

myawesomemenu = {
   { "manual", terminal .. " -e man awesome" },
   { "fluxbox", "/bin/bash /home/valens_a/bin/reflux" },
   { "edit config", editor_cmd .. " " .. awful.util.getdir("config") .. "/rc.lua" },
   { "restart", awesome.restart },
   { "quit", awesome.quit }
}

-- Our generated menu is "myappmenu"
-- require("menu") add the file "menu.lua"
require("menu")
mymainmenu = awful.menu({ items = { { "awesome", myawesomemenu, beautiful.awesome_icon },
-- The next line add our menu (myappmenu)
	        	  	    { "app", myappmenu, beautiful.awesome_icon },
                                    { "open terminal", terminal }
                                  }
                        })

mylauncher = awful.widget.launcher({ image = image(beautiful.awesome_icon),
                                     menu = mymainmenu })


-- }}}
