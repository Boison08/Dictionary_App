# BST Dictionary with GUI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Kivy](https://img.shields.io/badge/Kivy-2.0.0-green)
![KivyMD](https://img.shields.io/badge/KivyMD-0.104.2-orange)

A feature-rich dictionary application that combines the efficiency of a Binary Search Tree with a modern mobile-friendly GUI.

## Features

- ⚡ **Fast operations** (O(log n) average case) for insert, search and delete
- 📱 **Beautiful mobile UI** built with Kivy/KivyMD
- 🔄 **Automatic persistence** using JSON storage
- 🔍 **Smart search** with autocomplete suggestions
- 📅 **Word of the Day** feature
- 📚 **Recent searches** history
- 🌓 **Dark/Light mode** toggle

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bst-dictionary.git
cd bst-dictionary
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python GUI_DICTIONARY.py
```

### Basic Operations:
- **Search**: Type a word in the search bar
- **Add**: Navigate to Edit tab → Add new word
- **Delete**: Edit tab → Select word → Delete
- **Toggle Theme**: Click the theme switcher icon

## Project Structure

```
bst-dictionary/
├── BST_DICTIONARY.py      # Core BST implementation
├── GUI_DICTIONARY.py      # KivyMD user interface
├── dictionary.json        # Word database
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## Contributing

Contributions are welcome! Please open an issue or submit a PR for:
- Performance improvements
- Additional features
- UI/UX enhancements
- Bug fixes

## License

MIT License

