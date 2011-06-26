from gi.repository import Gtk
from widgets.settings_page import SettingsPage

VISIBLE_ALWAYS		= 0
VISIBLE_WHEN_NEEDED	= 1
VISIBLE_NEVER		= 2

EXPAND_NONE 	= 0
EXPAND_ACTIVE	= 1
EXPAND_ALL		= 2


class DisplayOptions(SettingsPage):
	"""Display options extension class"""

	def __init__(self, parent, application):
		SettingsPage.__init__(self, parent, application, 'display', _('Display'))

		notebook = Gtk.Notebook()

		# main window options
		label_main_window = Gtk.Label(_('Main window'))
		vbox_main_window = Gtk.VBox(False, 0)
		vbox_main_window.set_border_width(5)

		self._checkbox_hide_on_close = Gtk.CheckButton(_('Hide main window on close'))
		self._checkbox_show_toolbar = Gtk.CheckButton(_('Show toolbar'))
		self._checkbox_show_command_bar = Gtk.CheckButton(_('Show command bar'))
		self._checkbox_show_command_entry = Gtk.CheckButton(_('Show command entry'))

		self._checkbox_hide_on_close.connect('toggled', self._parent.enable_save, True)
		self._checkbox_show_toolbar.connect('toggled', self._parent.enable_save)
		self._checkbox_show_command_bar.connect('toggled', self._parent.enable_save)
		self._checkbox_show_command_entry.connect('toggled', self._parent.enable_save)

		# tab options
		label_tabs = Gtk.Label(_('Tabs'))
		vbox_tabs = Gtk.VBox(False, 0)
		vbox_tabs.set_border_width(5)

		self._checkbox_focus_new_tab = Gtk.CheckButton(_('Focus new tab after opening'))
		self._checkbox_button_relief = Gtk.CheckButton(_('Show normal button relief'))
		self._checkbox_button_icons = Gtk.CheckButton(_('Show icons instead of text in tab buttons'))
		self._checkbox_tab_close_button = Gtk.CheckButton(_('Show close button'))
		self._checkbox_always_show_tabs = Gtk.CheckButton(_('Show tab(s) even if there is only one'))
		self._checkbox_ubuntu_coloring = Gtk.CheckButton(_('Use Ubuntu coloring method for tab title bars'))

		self._checkbox_focus_new_tab.connect('toggled', self._parent.enable_save)
		self._checkbox_button_relief.connect('toggled', self._parent.enable_save)
		self._checkbox_button_icons.connect('toggled', self._parent.enable_save, True)
		self._checkbox_tab_close_button.connect('toggled', self._parent.enable_save)
		self._checkbox_always_show_tabs.connect('toggled', self._parent.enable_save)
		self._checkbox_ubuntu_coloring.connect('toggled', self._parent.enable_save)

		# status bar
		table = Gtk.Table(2, 2, False)
		table.set_col_spacing(0, 5)
		table.set_row_spacings(5)

		label_status_bar = Gtk.Label(_('Show status bar:'))
		label_status_bar.set_alignment(0, 0.5)

		list_status_bar = Gtk.ListStore(str, int)
		list_status_bar.append((_('Always'), VISIBLE_ALWAYS))
		list_status_bar.append((_('When needed'), VISIBLE_WHEN_NEEDED))
		list_status_bar.append((_('Never'), VISIBLE_NEVER))

		cell_status_bar = Gtk.CellRendererText()

		self._combobox_status_bar = Gtk.ComboBox(list_status_bar)
		self._combobox_status_bar.connect('changed', self._parent.enable_save)
		self._combobox_status_bar.pack_start(cell_status_bar)
		self._combobox_status_bar.add_attribute(cell_status_bar, 'text', 0)

		# expand tabs
		label_expand_tab = Gtk.Label(_('Expanded tabs:'))
		label_expand_tab.set_alignment(0, 0.5)

		list_expand_tab = Gtk.ListStore(str, int)
		list_expand_tab.append((_('None'), EXPAND_NONE))
		list_expand_tab.append((_('Active'), EXPAND_ACTIVE))
		list_expand_tab.append((_('All'), EXPAND_ALL))

		cell_expand_tab = Gtk.CellRendererText()

		self._combobox_expand_tabs = Gtk.ComboBox(list_expand_tab)
		self._combobox_expand_tabs.connect('changed', self._parent.enable_save)
		self._combobox_expand_tabs.pack_start(cell_expand_tab)
		self._combobox_expand_tabs.add_attribute(cell_expand_tab, 'text', 0)

		# operation options
		label_other = Gtk.Label(_('Other'))
		vbox_other = Gtk.VBox(False, 0)
		vbox_other.set_border_width(5)

		self._checkbox_hide_window_on_minimize = Gtk.CheckButton(_('Hide operation window on minimize'))
		self._checkbox_human_readable_size = Gtk.CheckButton(_('Show sizes in human readable format'))

		self._checkbox_hide_window_on_minimize.connect('toggled', self._parent.enable_save)
		self._checkbox_human_readable_size.connect('toggled', self._parent.enable_save)

		# pack UI
		table.attach(label_status_bar, 0, 1, 0, 1, xoptions=Gtk.FILL)
		table.attach(self._combobox_status_bar, 1, 2, 0, 1, xoptions=Gtk.FILL)

		table.attach(label_expand_tab, 0, 1, 1, 2, xoptions=Gtk.FILL)
		table.attach(self._combobox_expand_tabs, 1, 2, 1, 2, xoptions=Gtk.FILL)

		vbox_main_window.pack_start(self._checkbox_hide_on_close, False, False, 0)
		vbox_main_window.pack_start(self._checkbox_show_toolbar, False, False, 0)
		vbox_main_window.pack_start(self._checkbox_show_command_bar, False, False, 0)
		vbox_main_window.pack_start(self._checkbox_show_command_entry, False, False, 0)

		vbox_tabs.pack_start(self._checkbox_focus_new_tab, False, False, 0)
		vbox_tabs.pack_start(self._checkbox_button_relief, False, False, 0)
		vbox_tabs.pack_start(self._checkbox_button_icons, False, False, 0)
		vbox_tabs.pack_start(self._checkbox_tab_close_button, False, False, 0)
		vbox_tabs.pack_start(self._checkbox_always_show_tabs, False, False, 0)
		vbox_tabs.pack_start(self._checkbox_ubuntu_coloring, False, False, 0)
		vbox_tabs.pack_start(table, False, False, 5)

		vbox_other.pack_start(self._checkbox_hide_window_on_minimize, False, False, 0)
		vbox_other.pack_start(self._checkbox_human_readable_size, False, False, 0)

		notebook.append_page(vbox_main_window, label_main_window)
		notebook.append_page(vbox_tabs, label_tabs)
		notebook.append_page(vbox_other, label_other)

		self.pack_start(notebook, True, True, 0)

	def _load_options(self):
		"""Load display options"""
		options = self._application.options

		self._checkbox_hide_on_close.set_active(options.getboolean('main', 'hide_on_close'))
		self._checkbox_focus_new_tab.set_active(options.getboolean('main', 'focus_new_tab'))
		self._checkbox_show_toolbar.set_active(options.getboolean('main', 'show_toolbar'))
		self._checkbox_show_command_bar.set_active(options.getboolean('main', 'show_command_bar'))
		self._checkbox_show_command_entry.set_active(options.getboolean('main', 'show_command_entry'))
		self._checkbox_button_relief.set_active(bool(options.getint('main', 'button_relief')))
		self._checkbox_button_icons.set_active(options.getboolean('main', 'tab_button_icons'))
		self._checkbox_tab_close_button.set_active(options.getboolean('main', 'tab_close_button'))
		self._checkbox_always_show_tabs.set_active(options.getboolean('main', 'always_show_tabs'))
		self._checkbox_ubuntu_coloring.set_active(options.getboolean('main', 'ubuntu_coloring'))
		self._checkbox_hide_window_on_minimize.set_active(options.getboolean('main', 'hide_operation_on_minimize'))
		self._checkbox_human_readable_size.set_active(options.getboolean('main', 'human_readable_size'))
		self._combobox_status_bar.set_active(options.getint('main', 'show_status_bar'))
		self._combobox_expand_tabs.set_active(options.getint('main', 'expand_tabs'))

	def _save_options(self):
		"""Save display options"""
		options = self._application.options

		# for config parser to get boolean, you need to set string :/. makes sense?
		_bool = ('False', 'True')

		# save options
		options.set('main', 'hide_on_close', _bool[self._checkbox_hide_on_close.get_active()])
		options.set('main', 'focus_new_tab', _bool[self._checkbox_focus_new_tab.get_active()])
		options.set('main', 'show_toolbar', _bool[self._checkbox_show_toolbar.get_active()])
		options.set('main', 'show_command_bar', _bool[self._checkbox_show_command_bar.get_active()])
		options.set('main', 'show_command_entry', _bool[self._checkbox_show_command_entry.get_active()])
		options.set('main', 'button_relief', int(self._checkbox_button_relief.get_active()))
		options.set('main', 'tab_button_icons', _bool[self._checkbox_button_icons.get_active()])
		options.set('main', 'tab_close_button', _bool[self._checkbox_tab_close_button.get_active()])
		options.set('main', 'always_show_tabs', _bool[self._checkbox_always_show_tabs.get_active()])
		options.set('main', 'ubuntu_coloring', _bool[self._checkbox_ubuntu_coloring.get_active()])
		options.set('main', 'hide_operation_on_minimize', _bool[self._checkbox_hide_window_on_minimize.get_active()])
		options.set('main', 'human_readable_size', _bool[self._checkbox_human_readable_size.get_active()])
		options.set('main', 'show_status_bar', self._combobox_status_bar.get_active())
		options.set('main', 'expand_tabs', self._combobox_expand_tabs.get_active())
