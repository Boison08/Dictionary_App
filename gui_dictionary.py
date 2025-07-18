# Install required libraries:
# pip install kivy
# pip install kivymd

#Names of group members
# 1. Clement Yeboah Adjapong
# 2. Brian Okyere Akosah
# 3. Simeon Anyinmyamfo Awotwe Boison
# 4. Kwesi Odartey Dadzie
# 5. Salma Niina Ibrahim
# 6. Kobina Ansu Adjei Kyeremeh
# 7. Ahmed Mohammed
# 8. Adam Musah Wandaogo

# Run the app here:

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from bst_dictionary import BSTDictionary  

# Set window size
Window.size = (320, 550)

class SmallToast(MDLabel):
    """Custom toast notification widget for small, temporary messages"""
    duration = NumericProperty(0.5)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Configure the visual appearance of the toast
        self.font_size = '17sp'  
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': 0.5, 'y': 0.1}
        self.background_color = (0.2, 0.2, 0.2, 0.9)
        self.padding = (15, 10)
        self.text_color = (1, 1, 1, 1)

class RecentSearchItem(TwoLineListItem):
    """Custom list item for recent searches with delete functionality"""
    def __init__(self, word, delete_callback, search_callback, **kwargs):
        super().__init__(**kwargs)
        self.word = word
        self.text = word
        self.secondary_text = "Recently searched"
        
        # Create container for delete button
        self.delete_box = BoxLayout(
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={'center_y': 0.5, 'right': 1}  # Added right alignment
        )
        
        # Add delete button with callback
        delete_icon = MDIconButton(
            icon='delete',
            theme_text_color="Custom",
            text_color=(0.8, 0, 0, 1),
            size_hint=(None, None),
            size=(40, 40),
            on_release=lambda x: delete_callback(word)
        )
        
        self.delete_box.add_widget(delete_icon)
        self.add_widget(self.delete_box)
        self.bind(size=self._update_delete_box_pos)
        
        # Make the item clickable for searching
        self.bind(on_release=lambda x: search_callback(word))

    def _update_delete_box_pos(self, instance, value):
        """Update the position of the delete button when the item size changes"""
        self.delete_box.pos = (
            self.width - self.delete_box.width - dp(10),  # 10dp padding from right
            self.height / 2 - self.delete_box.height / 2   # Vertical center
        )

class DictionaryApp(MDApp):
    """Main application class for the Dictionary app"""
    
    def show_snackbar(self, message):
        """Display a temporary notification message above the navigation tabs"""
        MDSnackbar(
            MDLabel(
                text=message,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            ),
            y=dp(75),  # Position just above the bottom navigation
            pos_hint={"center_x": 0.5},
            size_hint_x=0.95,
            md_bg_color=self.theme_cls.primary_color,
            radius=[5, 5, 5, 5],
            duration=0.5
        ).open()

    def build(self):
        """Initialize and build the main UI structure"""
        # Initialize dictionary backend
        self.dictionary = BSTDictionary()
        
        # Configure theme
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"

        # Create main layout structure
        main_layout = MDBoxLayout(orientation='vertical', spacing=15, padding=0)

        # Add toolbar
        self.toolbar = MDTopAppBar(
            title="Dictionary App",
            elevation=0,
            left_action_items=[['menu', lambda x: self.open_menu(x)]],
            md_bg_color=self.theme_cls.primary_dark,
            specific_text_color=(1, 1, 1, 1),
            type="top"
        )
        main_layout.add_widget(self.toolbar)

        # Set up bottom navigation with tabs
        bottom_nav = MDBottomNavigation()
        
        # Create and configure search tab
        search_tab = self._create_search_tab()
        
        # Create and configure edit tab
        edit_tab = self._create_edit_tab()
        
        # Create and configure recent searches tab
        recent_tab = self._create_recent_tab()

        # Add all tabs to navigation
        bottom_nav.add_widget(search_tab)
        bottom_nav.add_widget(edit_tab)
        bottom_nav.add_widget(recent_tab)

        main_layout.add_widget(bottom_nav)
        
        # Initialize word of the day
        Clock.schedule_once(lambda dt: self.update_word_of_day(), 0)
        
        return main_layout

    def _create_search_tab(self):
        """Create and configure the search tab interface"""
        search_tab = MDBottomNavigationItem(name='search', text='Search', icon='magnify')
        search_layout = MDBoxLayout(orientation='vertical', spacing=20, padding=10)

        # Main scroll view for search tab
        search_scroll = MDScrollView(
            do_scroll_x=False,
            scroll_timeout=0
        )

        search_content = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10,
            size_hint_y=None
        )
        search_content.bind(minimum_height=search_content.setter('height'))

        # Word of the Day Card
        word_of_day_card = MDCard(
            orientation='vertical',
            padding=10,
            size_hint=(1, None),
            height=170,
            elevation=1,
            md_bg_color=self.theme_cls.primary_color
        )

        wod_title = MDLabel(
            text="Word of the Day",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="center",
            bold=True,
            font_style="Subtitle1"
        )

        self.wod_word = MDLabel(
            text="",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="center",
            bold=True,
            font_size="30sp",
            font_style="H5"
        )

        self.wod_meaning = MDLabel(
            text="",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="center"
        )

        word_of_day_card.add_widget(wod_title)
        word_of_day_card.add_widget(self.wod_word)
        word_of_day_card.add_widget(self.wod_meaning)

        search_content.add_widget(word_of_day_card)
        
        # Search Input and Button

        self.search_input = MDTextField(
            hint_text="Search for a word",
            mode="rectangle",
            on_text=self.update_suggestions,
            on_text_validate=self.search_word  # Add this line to handle Enter key
        )
        search_button = MDRaisedButton(text="Search", on_release=self.search_word)


        # Suggestion List
        self.suggestion_list = MDList()
        suggestion_scroll = MDScrollView(
            size_hint=(1, None), 
            #height=150,
            do_scroll_x=False,
            scroll_timeout=0
        )
        suggestion_scroll.add_widget(self.suggestion_list)

        # Result Card
        self.result_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            size_hint_y=None,
            padding=10,
            spacing=(0),
            elevation=1
        )

        self.result_label = MDLabel(
            text="",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,  # Use the theme's primary color
            halign="center",
            bold=True,
            font_style="H5",
            size_hint_y=None
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))

        self.definition_label = MDLabel(
            text="",
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            padding=(10, 10)
        )
        self.definition_label.bind(texture_size=self.definition_label.setter('size'))

        self.usage_label = MDLabel(
            text="",
            italic=True,
            halign="center",
            size_hint_y=None,
            theme_text_color="Secondary"
        )
        self.usage_label.bind(texture_size=self.usage_label.setter('size'))

        self.result_card.add_widget(self.result_label)
        self.result_card.add_widget(self.definition_label)
        self.result_card.add_widget(self.usage_label)

        # In the build() method, update the widget order:

        # Create a spacer widget
        spacer = Widget(size_hint_y=None, height=30)  # Adjust height value as needed

        # Update the widget order
        search_content.clear_widgets()
        search_content.add_widget(word_of_day_card)
        search_content.add_widget(self.search_input)
        search_content.add_widget(search_button)
        search_content.add_widget(spacer)  # Add spacer here
        search_content.add_widget(self.result_card)
        search_content.add_widget(suggestion_scroll)

        search_scroll.add_widget(search_content)
        search_layout.add_widget(search_scroll)
        search_tab.add_widget(search_layout)
        return search_tab

    def _create_edit_tab(self):
        """Create and configure the edit tab interface"""
        edit_tab = MDBottomNavigationItem(name='edit', text='Edit', icon='pencil')
        edit_layout = MDBoxLayout(orientation='vertical', spacing=0, padding=8)
        
        # Main scroll view for edit tab
        edit_scroll = MDScrollView(
            do_scroll_x=False,
            scroll_timeout=0
        )
        edit_content = MDBoxLayout(
            orientation='vertical',
            spacing=40,
            padding=10,
            size_hint_y=None
        )
        edit_content.bind(minimum_height=edit_content.setter('height'))

        # Define input fields for the Edit Tab
        self.word_input = MDTextField(
            hint_text="Enter word",
            mode="rectangle",
            size_hint=(1, None),
            height=40
        )

        self.meaning_input = MDTextField(
            hint_text="Enter meaning",
            mode="rectangle",
            size_hint=(1, None),
            height=40
        )

        self.example_input = MDTextField(
            hint_text="Enter example sentence(optional)",
            mode="rectangle",
            size_hint=(1, None),
            height=40,
        )

        self.delete_input = MDTextField(
            hint_text="Enter word to delete",
            mode="rectangle",
            size_hint=(1, None),
            height=40
        )

        self.button = MDRaisedButton(
            text="Add Word",
            on_release=self.insert_word,
            
        )
        

        # Insert Section
        insert_section = MDCard(
            orientation='vertical',
            padding=20,
            size_hint=(1, None),
            height=390,
            spacing=20,
            elevation=0
        )
        insert_section.add_widget(MDLabel(
            text="Add New Word",
            theme_text_color="Primary",
            halign="center",
            bold=True
        ))
        insert_section.add_widget(self.word_input)
        insert_section.add_widget(self.meaning_input)
        insert_section.add_widget(self.example_input)
        insert_section.add_widget(self.button)

        # Delete Section
        delete_section = MDCard(
            orientation='vertical',
            padding=15,
            spacing=20,
            size_hint=(1, None),
            height=230,
            elevation=0
        )

        delete_section.add_widget(MDLabel(
            text="Delete Word",
            theme_text_color="Primary",
            halign="center",
            bold=True
        ))

        clear_button = MDRaisedButton(
            text="Delete Word",
            on_release=self.delete_word
        )

        delete_section.add_widget(self.delete_input)
        delete_section.add_widget(clear_button)

        # Add sections to the content
        edit_content.add_widget(insert_section)
        edit_content.add_widget(delete_section)

        # Add content to the scroll view
        edit_scroll.add_widget(edit_content)
        edit_layout.add_widget(edit_scroll)
        edit_tab.add_widget(edit_layout)
        return edit_tab

    def _create_recent_tab(self):
        """Create and configure the recent searches tab interface"""
        recent_tab = MDBottomNavigationItem(name='recent', text='Recent', icon='history')
        recent_layout = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10,
            size_hint_y=1
        )

        # Main scroll view for recent tab - increased height to 95%
        recent_scroll = MDScrollView(
            do_scroll_x=False,
            scroll_timeout=0,
            size_hint_y=5  # Increased from 0.9 to 0.95
        )

        recent_content = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10,
            size_hint_y=None
        )
        recent_content.bind(minimum_height=recent_content.setter('height'))

        # Recent list
        self.recent_list = MDList()
        recent_content.add_widget(self.recent_list)
        recent_scroll.add_widget(recent_content)

        # Add scroll view first
        recent_layout.add_widget(recent_scroll)

        # Clear History Button at the bottom with reduced spacing
        button_container = MDBoxLayout(
            orientation='vertical',
            padding=(0, 1)  # Reduced vertical padding
        )

        clear_button = MDRaisedButton(
            text="Clear History",
            on_release=self.clear_recent_searches,
            pos_hint={'center_x': .5, 'center_y': .5}
        )

        button_container.add_widget(clear_button)
        recent_layout.add_widget(button_container)
        recent_tab.add_widget(recent_layout)
        return recent_tab

    def scroll_to_top(self, scroll_widget):
        """Smoothly scroll to the top of the given scroll widget"""
        Animation(scroll_y=1, duration=0.3).start(scroll_widget)

    def scroll_to_bottom(self, scroll_widget):
        """Smoothly scroll to the bottom of the given scroll widget"""
        Animation(scroll_y=0, duration=0.3).start(scroll_widget)

    def get_suggestions(self, prefix):
        """Get a list of words from the dictionary that start with the given prefix."""
        words = self.dictionary.inorder_traversal()
        return [word[0] for word in words if word[0].startswith(prefix)][:5]

    def update_suggestions(self, instance, value):
        """Update the suggestion list based on the user's input."""
        value = value.strip().lower()
        self.suggestion_list.clear_widgets()

        if not value:
            return

        suggestions = self.get_suggestions(value)

        for suggestion in suggestions:
            item = OneLineListItem(
                text=suggestion,
                on_release=lambda x=suggestion: self.select_suggestion(x)
            )
            self.suggestion_list.add_widget(item)
        
        # Auto scroll to top when new suggestions appear
        Clock.schedule_once(lambda dt: self.scroll_to_top(self.suggestion_list.parent.parent), 0.1)

    def select_suggestion(self, word):
        """Handle the selection of a suggestion."""
        self.search_input.text = word
        self.search_word(None)

    def open_menu(self, instance):
        """Create a dropdown menu with a nice theme toggle."""
        menu_items = [
            {
                "text": "Dark Mode" if self.theme_cls.theme_style == "Light" else "Light Mode",
                "viewclass": "OneLineIconListItem",
                "icon": "weather-sunny" if self.theme_cls.theme_style == "Dark" else "weather-night",
                "height": dp(56),
                "on_release": lambda: self.toggle_theme(),
            }
        ]
        
        # Updated menu configuration
        self.menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width=dp(200),
            max_height=dp(56),
            radius=[24, 0, 24, 0],
            elevation=2,
            md_bg_color=self.theme_cls.primary_light,
            background_color=None  # Remove deprecated property
        )
        self.menu.open()

    def update_word_of_day(self):
        """Update the Word of the Day display with a new random word"""
        word_of_day = self.dictionary.word_of_the_day
        if word_of_day:
            self.wod_word.text = word_of_day[0].upper()
            self.wod_meaning.text = word_of_day[1]

    def toggle_theme(self):
        new_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        self.theme_cls.theme_style = new_style
        self.show_snackbar(f"{new_style} Mode")
        if hasattr(self, 'menu'):
            self.menu.dismiss()

    def view_recent_searches(self):
        """Display recent searches in a toast."""
        recent_words = ", ".join(self.dictionary.recent_searches[-5:])
        toast(f"Recent Searches: {recent_words}" if recent_words else "No recent searches")

    def insert_word(self, instance):
        """Handle new word insertion into dictionary"""
        word = self.word_input.text.strip().lower()
        meaning = self.meaning_input.text.strip()
        example = self.example_input.text.strip()

        if word and meaning:
            self.dictionary.insert(word, meaning, example)
            self.show_snackbar(f'Word "{word}" added!')
            # Clear input fields
            self.word_input.text = ""
            self.meaning_input.text = ""
            self.example_input.text = ""
        else:
            self.show_snackbar('Word and Meaning are required!')

    def search_word(self, *args):
        """Search for a word in the dictionary."""
        word = self.search_input.text.strip().lower()
        if not word:
            self.show_snackbar("Please enter a word to search")
            return
            
        result = self.dictionary.search(word)
        if result:
            self.result_label.text = f'{result.word.upper()}'
            self.definition_label.text = f'{result.meaning}'
            self.usage_label.text = f'{result.example_sentence}' if result.example_sentence else ''
            self.update_recent_searches(word)
        else:
            # Clear the result card
            self.result_label.text = ''
            self.definition_label.text = ''
            self.usage_label.text = ''
            # Show not found message in snackbar
            self.show_snackbar(f'"{word}" not found. Go to Edit tab to add new words.')
        
        # Update card height after content change
        Clock.schedule_once(lambda dt: self.update_result_card_height(), 0.1)

    def delete_word(self, instance):
        """Handle word deletion from dictionary"""
        word = self.delete_input.text.strip().lower()
        if self.dictionary.search(word):
            self.dictionary.delete(word)
            self.show_snackbar(f'Word "{word}" deleted!')
            # Clear input field
            self.delete_input.text = ""
        else:
            self.show_snackbar(f'Word "{word}" not found.')

    def update_recent_searches(self, word):
        """Update the recent searches list."""
        if word in self.dictionary.recent_searches:
            self.dictionary.recent_searches.remove(word)
        self.dictionary.recent_searches.insert(0, word)
        self.update_recent_searches_display()
        
        # Auto scroll to top when new recent searches are added
        Clock.schedule_once(lambda dt: self.scroll_to_top(self.recent_list.parent.parent), 0.1)

    def search_word_directly(self, word):
        """Search for a word directly from recent searches."""
        self.search_input.text = word
        self.search_word(None)

    def update_result_card_height(self, *args):
        """Update the height of the result card based on its content."""
        padding = 20  # Total vertical padding
        spacing = 10  # Space between widgets
        
        # Force labels to recalculate their heights
        self.result_label.texture_update()
        self.definition_label.texture_update()
        self.usage_label.texture_update()
        
        # Calculate total height
        total_height = (
            self.result_label.texture_size[1] +
            self.definition_label.texture_size[1] +
            (self.usage_label.texture_size[1] if self.usage_label.text else 0) +
            padding +
            (spacing * 2)  # Spacing between elements
        )
        
        # Set minimum height
        min_height = 100
        self.result_card.height = max(total_height, min_height)

    def clear_recent_searches(self, instance):
        """Clear all recent searches."""
        self.dictionary.recent_searches.clear()
        self.recent_list.clear_widgets()
        self.show_snackbar('Recent searches cleared')

    def remove_recent_search(self, word):
        """Remove a word from recent searches."""
        if word in self.dictionary.recent_searches:
            self.dictionary.recent_searches.remove(word)
            self.show_snackbar(f'Removed "{word}" from recent searches')
            self.update_recent_searches_display()

    def update_recent_searches_display(self):
        """Update the display of recent searches."""
        self.recent_list.clear_widgets()
        for item in self.dictionary.recent_searches[:5]:
            recent_item = RecentSearchItem(
                item,
                delete_callback=self.remove_recent_search,
                search_callback=self.search_word_directly
            )
            self.recent_list.add_widget(recent_item)


if __name__ == '__main__':
    DictionaryApp().run()