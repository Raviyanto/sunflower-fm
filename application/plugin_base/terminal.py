try:
	import vte
except:
	vte = None

from gi.repository import Gtk, Gdk
from plugin_base.plugin import PluginBase
from accelerator_group import AcceleratorGroup

# button text constants
BUTTON_TEXT_MENU 	= u'\u2699'
BUTTON_TEXT_RECYCLE = u'\u267B'


class Terminal(PluginBase):
	"""Base class for terminal based plugins

	This class will provide basic VTE GTK+ component wrapped in VBox.

	You are strongly encouraged to use predefined methods rather than
	defining your own.

	"""

	_vte_present = False

	def __init__(self, parent, notebook, path=None):
		super(Terminal, self).__init__(parent, notebook, path)

		self._menu = None

		# change list icon
		self._title_bar.set_icon_from_name('terminal')

		# recycle button
		self._recycle_button = Gtk.Button()

		if self._parent.options.getboolean('main', 'tab_button_icons'):
			# set icon
			image_recycle = Gtk.Image()
			image_recycle.set_from_icon_name('reload', Gtk.IconSize.MENU)
			self._recycle_button.set_image(image_recycle)
		else:
			# set text
			self._recycle_button = Gtk.Button(BUTTON_TEXT_RECYCLE)

		self._recycle_button.set_focus_on_click(False)
		self._recycle_button.set_tooltip_text(_('Recycle terminal'))
		self._recycle_button.set_relief((
									Gtk.ReliefStyle.NONE,
									Gtk.ReliefStyle.NORMAL
									)[self._parent.options.getint('main', 'button_relief')])

		self._recycle_button.connect('clicked', self._recycle_terminal)

		# terminal menu button
		self._menu_button = Gtk.Button()

		if self._parent.options.getboolean('main', 'tab_button_icons'):
			# set icon
			image_menu = Gtk.Image()
			image_menu.set_from_icon_name(Gtk.STOCK_EDIT, Gtk.IconSize.MENU)
			self._menu_button.set_image(image_menu)
		else:
			# set text
			self._menu_button = Gtk.Button(BUTTON_TEXT_MENU)

		self._menu_button.set_focus_on_click(False)
		self._menu_button.set_tooltip_text(_('Terminal menu'))
		self._menu_button.set_relief((
									Gtk.ReliefStyle.NONE,
									Gtk.ReliefStyle.NORMAL
									)[self._parent.options.getint('main', 'button_relief')])

		self._menu_button.connect('clicked', self._show_terminal_menu)

		# pack buttons
		self._title_bar.add_control(self._recycle_button)
		self._title_bar.add_control(self._menu_button)

		if vte is not None:
			self._vte_present = True
			self._terminal = vte.Terminal()
			self._terminal.connect('window-title-changed', self._update_title)
		else:
			self._terminal = Gtk.Label(_('Python VTE module is not installed on this system!'))

		# terminal container
		self._container = Gtk.ScrolledWindow()
		self._container.set_shadow_type(Gtk.ShadowType.IN)

		policy = (
				Gtk.PolicyType.NEVER,
				Gtk.PolicyType.AUTOMATIC
			)[self._parent.options.getboolean('main', 'terminal_scrollbars')]
		self._container.set_policy(policy, policy)

		# pack terminal
		self._container.add(self._terminal)
		self.pack_start(self._container, True, True, 0)

		# connect events to main object
		self._connect_main_object(self._terminal)

		# create menu
		self._create_menu()

	def _update_title(self, widget, data=None):
		"""Update title with terminal window text"""
		self._change_title_text(self._terminal.get_window_title())
		return True

	def _update_terminal_status(self, widget, data=None):
		"""Update status bar text with terminal data"""
		self.update_status(self._terminal.get_status_line())

	def _recycle_terminal(self, widget, data=None):
		"""Recycle terminal"""
		pass

	def _create_terminal(self, widget, data=None):
		"""Create terminal tab in parent notebook"""
		self._parent.create_terminal_tab(self._notebook, self.path)
		return True

	def _create_menu(self):
		"""Create terminal menu"""
		self._menu = Gtk.Menu()

		# copy
		self._menu_item_copy = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_COPY, None)
		self._menu_item_copy.connect('activate', self._copy_selection)
		self._menu.append(self._menu_item_copy)

		# paste
		self._menu_item_paste = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_PASTE, None)
		self._menu_item_paste.connect('activate', self._paste_selection)
		self._menu.append(self._menu_item_paste)

		# show all items
		self._menu.show_all()
		self._menu.connect('hide', self._handle_menu_hide)

	def _prepare_menu(self):
		"""Prepare terminal menu before showing"""
		self._menu_item_copy.set_sensitive(self._terminal.get_has_selection())
		self._menu_item_paste.set_sensitive(self._parent.is_clipboard_text())

	def _handle_menu_hide(self, widget, data=None):
		"""Handle hide event for terminal menu"""
		self._disable_object_block()
		oposite_object = self._parent.get_oposite_object(self)
		oposite_object._disable_object_block()

	def _duplicate_tab(self, widget, data=None):
		"""Creates new tab with same path"""
		PluginBase._duplicate_tab(self, None, self.path)
		return True

	def _get_menu_position(self, menu, button):
		"""Get history menu position"""
		# get coordinates
		window_x, window_y = self._parent.window.get_position()
		button_x, button_y = button.translate_coordinates(self._parent, 0, 0)
		button_h = button.get_allocation().height

		# calculate absolute menu position
		pos_x = window_x + button_x
		pos_y = window_y + button_y + button_h

		return (pos_x, pos_y, True)

	def _show_terminal_menu(self, widget, data=None):
		"""History button click event"""
		# prepare menu for drawing
		self._prepare_menu()

		# show the menu on calculated location
		self._enable_object_block()
		oposite_object = self._parent.get_oposite_object(self)
		oposite_object._enable_object_block()

		self._menu.popup(
						None, None,
						self._get_menu_position,
						1, 0, widget
					)

	def _configure_accelerators(self):
		"""Configure accelerator group"""
		group = AcceleratorGroup(self._parent)
		keyval = Gdk.keyval_from_name

		# give parent chance to register its own accelerator group
		PluginBase._configure_accelerators(self)

		# modify plugin accelerator group so we can have terminal autocomplete with tab
		plugin_group = self._accelerator_groups[0]
		plugin_group.disable_accelerator('focus_oposite_object')

		# configure accelerator group
		group.set_name('terminal')
		group.set_title(_('Terminal'))

		# add all methods to group
		group.add_method('create_terminal', _('Create terminal tab'), self._create_terminal)
		group.add_method('copy_to_clipboard', _('Copy selection to clipboard'), self._copy_selection)
		group.add_method('paste_from_clipboard', _('Paste from clipboard'), self._paste_selection)
		group.add_method('focus_oposite_object', _('Focus oposite object'), self._parent.focus_oposite_object)

		# configure accelerators
		group.set_accelerator('create_terminal', keyval('z'), Gdk.ModifierType.CONTROL_MASK)
		group.set_accelerator('copy_to_clipboard', keyval('c'), Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK)
		group.set_accelerator('paste_from_clipboard', keyval('v'), Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK)
		group.set_accelerator('focus_oposite_object', keyval('Tab'), Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK)

		# add accelerator group to the list
		self._accelerator_groups.append(group)

	def _copy_selection(self, widget=None, data=None):
		"""Copy selection from terminal"""
		if self._terminal.get_has_selection():
			self._terminal.copy_clipboard()

		return True

	def _paste_selection(self, widget=None, data=None):
		"""Paste selection from terminal"""
		self._terminal.paste_clipboard()
		return True

	def feed_terminal(self, text):
		"""Feed terminal process with specified text"""
		self._terminal.feed_child(text)

	def apply_settings(self):
		"""Apply terminal settings"""
		# let parent class do its work
		PluginBase.apply_settings(self)

		# button relief
		self._recycle_button.set_relief((
									Gtk.ReliefStyle.NONE,
									Gtk.ReliefStyle.NORMAL
									)[self._parent.options.getint('main', 'button_relief')])

		self._menu_button.set_relief((
									Gtk.ReliefStyle.NONE,
									Gtk.ReliefStyle.NORMAL
									)[self._parent.options.getint('main', 'button_relief')])

		# apply scrollbar policy
		policy = (
				Gtk.PolicyType.NEVER,
				Gtk.PolicyType.AUTOMATIC
			)[self._parent.options.getboolean('main', 'terminal_scrollbars')]
		self._container.set_policy(policy, policy)

