# 🎥 Advanced Screen Recorder

A powerful, user-friendly screen recording application built with Python and Tkinter. Features a real-time preview window that lets you visually select and resize your recording area before capturing.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🎯 **Visual Area Selection**
- **Interactive Preview Window**: Resize and position a semi-transparent overlay to select your recording area
- **Real-time Preview**: See exactly what will be recorded before you start
- **Precise Control**: Pixel-perfect area selection with live coordinates display

### ⚙️ **Advanced Recording Options**
- **Adjustable Frame Rate**: 10-60 FPS with real-time slider control
- **Quality Settings**: Low, Medium, High, Ultra quality presets
- **Multiple Formats**: MP4, AVI, MOV output support
- **Custom Output Path**: Choose your preferred save location

### 🚀 **Professional Features**
- **Live Recording Timer**: Real-time duration display
- **Smart Filenames**: Automatic timestamped file naming
- **Status Monitoring**: Clear visual feedback on recording status
- **Error Handling**: Robust error management and user notifications
- **Non-blocking UI**: Smooth interface that stays responsive during recording

## 🖼️ Screenshots

### Main Interface
The clean, intuitive control panel with all recording settings:

```
┌─────────────────────────────┐
│     Advanced Screen Recorder │
├─────────────────────────────┤
│  📍 Recording Area          │
│  [Select Area & Preview]    │
│  Area: 800x600 at (100,100)│
├─────────────────────────────┤
│  ⚙️  Recording Settings      │
│  Frame Rate: [30] FPS       │
│  Quality: [High] ▼          │
│  Format: [.mp4] ▼           │
│  Output: ~/Desktop [Browse] │
├─────────────────────────────┤
│  [Start Recording] [Stop]   │
│  Status: Ready to record    │
│  Timer: 00:00:00           │
└─────────────────────────────┘
```

### Preview Window
The resizable preview overlay showing your selected recording area in real-time.

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/azario0/advanced-screen-recorder.git
cd advanced-screen-recorder
```

2. **Install dependencies**
```bash
pip install opencv-python pillow pyautogui
```

3. **Run the application**
```bash
python screen_recorder.py
```

## 📖 Usage Guide

### Basic Recording

1. **Launch** the application
2. **Click** "Select Area & Preview" to open the preview window
3. **Resize and position** the red preview window over your desired recording area
4. **Click** "Start Preview" to see a live preview of what will be recorded
5. **Click** "Confirm Area" when you're satisfied with the selection
6. **Adjust** frame rate, quality, and output settings as needed
7. **Click** "Start Recording" to begin capturing
8. **Click** "Stop Recording" when finished

### Advanced Configuration

#### Frame Rate Settings
- **10-20 FPS**: Good for tutorials, lower file size
- **30 FPS**: Standard for most content
- **60 FPS**: Smooth motion, gaming, high-action content

#### Quality Presets
- **Low**: Smaller file size, basic quality
- **Medium**: Balanced size and quality
- **High**: Good quality for most uses
- **Ultra**: Maximum quality, larger files

#### Output Formats
- **MP4**: Best compatibility, recommended for most uses
- **AVI**: Good for editing, larger file sizes
- **MOV**: Optimized for macOS/QuickTime

## 🛠️ Technical Details

### Architecture
- **GUI Framework**: Tkinter for cross-platform compatibility
- **Video Processing**: OpenCV for efficient video encoding
- **Screen Capture**: PyAutoGUI for fast screen grabbing
- **Image Processing**: PIL/Pillow for image manipulation
- **Threading**: Multi-threaded design for responsive UI

### Performance
- **Optimized Capture**: Efficient screen grabbing with minimal CPU overhead
- **Smart Frame Rate Control**: Precise timing for consistent frame rates
- **Memory Management**: Automatic cleanup of video resources
- **Thread Safety**: Safe concurrent operations

### File Output
- **Smart Naming**: Auto-generated filenames with timestamps
- **Multiple Codecs**: Format-optimized video encoding
- **Quality Control**: Bitrate optimization based on quality settings

## 🔧 Configuration

### Default Settings
```python
Frame Rate: 30 FPS
Quality: High
Format: MP4
Output Path: ~/Desktop
Recording Area: 800x600 pixels
```

### Customization
All settings can be adjusted through the GUI interface. The application remembers your recording area between preview sessions.

## 📋 Requirements

### System Requirements
- **OS**: Windows 7+, macOS 10.12+, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: Varies by recording length and quality
- **Display**: Any resolution supported

### Python Dependencies
```
opencv-python>=4.5.0
Pillow>=8.0.0
pyautogui>=0.9.50
numpy>=1.19.0
```

## 🐛 Troubleshooting

### Common Issues

**Recording not starting**
- Check if all dependencies are installed
- Ensure output directory exists and is writable
- Try running as administrator (Windows) or with appropriate permissions

**Preview window not showing**
- Update your graphics drivers
- Try different quality settings
- Check if screen capture permissions are enabled (macOS)

**Poor recording quality**
- Increase quality setting
- Adjust frame rate
- Check available disk space
- Close other resource-intensive applications

**Performance issues**
- Lower frame rate setting
- Reduce recording area size
- Close unnecessary applications
- Use SSD storage for output

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenCV** team for excellent video processing capabilities
- **Tkinter** for the robust GUI framework
- **PyAutoGUI** for reliable screen capture functionality
- **PIL/Pillow** for image processing support

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/azario0/advanced-screen-recorder/issues) page
2. Create a new issue with detailed information about your problem
3. Include your Python version, OS, and error messages

## 🔮 Future Enhancements

- [ ] Audio recording support
- [ ] Multiple monitor selection
- [ ] Video compression options
- [ ] Hotkey controls
- [ ] Pause/resume functionality
- [ ] Region presets saving
- [ ] Video editing capabilities
- [ ] Live streaming support

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

---

**Made with ❤️ by [azario0](https://github.com/azario0)**

*Built for creators, developers, and educators who need reliable screen recording.*