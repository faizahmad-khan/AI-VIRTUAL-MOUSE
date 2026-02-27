# Docker Quick Start Guide

Get the AI Virtual Mouse running in Docker in just 3 minutes!

## 🚀 Fastest Way to Get Started

### Step 1: Install Docker
- **macOS/Windows**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: `sudo apt install docker.io docker-compose` (Ubuntu/Debian)

### Step 2: Prepare Your System

#### **macOS Users:**
```bash
# Install XQuartz for GUI support
brew install --cask xquartz

# Launch XQuartz
open -a XQuartz

# Then in a terminal, set display:
export DISPLAY=host.docker.internal:0
```

#### **Linux Users:**
```bash
# Ensure X11 is available and set display:
export DISPLAY=:0

# Allow Docker to access X11:
xhost +local:docker
```

#### **Windows Users:**
```bash
# Install XVCsrv: https://sourceforge.net/projects/vcxsrv/
# Or use Windows Subsystem for Linux (WSL2)

# Set display variable:
set DISPLAY=host.docker.internal:0
```

### Step 3: Build and Run

```bash
# Navigate to the AI Virtual Mouse directory
cd /path/to/AI\ VIRTUAL\ MOUSE

# Option A: Using the setup script (Linux/macOS)
chmod +x docker-setup.sh
./docker-setup.sh

# Option B: Manual setup
docker build -t ai-virtual-mouse .
docker-compose up
```

That's it! Your virtual mouse should be running.

---

## 📋 Common Commands

### **Start the Application**
```bash
docker-compose up
```

### **Stop the Application**
```bash
docker-compose down
```

### **View Live Logs**
```bash
docker-compose logs -f
```

### **Run in Background**
```bash
docker-compose up -d
```

### **Rebuild Image** (after code changes)
```bash
docker-compose up --build
```

### **Access Container Shell** (for debugging)
```bash
docker-compose exec ai-mouse bash
```

### **View Container Health**
```bash
docker ps
```

---

## 🔧 Configuration

### **Change Camera**
If you have multiple cameras:
```yaml
# Edit docker-compose.yml
devices:
  - /dev/video1:/dev/video1  # Change 0 to 1, 2, etc.
```

### **Adjust Settings**
Edit `config.yaml` directly - changes apply immediately:
```yaml
cursor:
  smoothening: 5
clicks:
  left_click_distance: 30
```

### **Enable Debug Logging**
Edit `config.yaml`:
```yaml
logging:
  level: DEBUG
```

---

## 🐛 Troubleshooting

### **"Cannot connect to display"**
```bash
# Make sure X server is running and DISPLAY is set
echo $DISPLAY
# Should show :0, :1, or host.docker.internal:0

# Reset display permissions
xhost +local:docker
```

### **"Camera not found"**
```bash
# List available cameras
ls -la /dev/video*

# Find available cameras (Linux)
v4l2-ctl --list-devices
```

### **"Container exits immediately"**
```bash
# Check logs for errors
docker-compose logs

# Look for Python errors or missing dependencies
```

### **For More Help**
See [DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md)

---

## 📊 Monitoring & Debugging

### **View Health Status**
```bash
docker ps
# Look at STATUS column - should show "Up (healthy)"
```

### **See Resource Usage**
```bash
docker stats
```

### **Run Command in Container**
```bash
docker-compose exec ai-mouse python -c "import cv2; print(cv2.__version__)"
```

### **Full Container Inspection**
```bash
docker inspect <container_id>
```

---

## 🎯 Pro Tips

1. **Volume Mounts**: Your `config.yaml` and `logs/` are accessible from your host - edit them directly!

2. **Multi-Hand Support**: Edit `config.yaml` to detect multiple hands:
   ```yaml
   hand_detection:
     max_num_hands: 2
   ```

3. **Performance**: Docker adds minimal overhead - virtual mouse runs at full speed

4. **Updates**: Pull latest code and rebuild:
   ```bash
   git pull
   docker-compose up --build
   ```

5. **Share with Others**: Just share `docker-compose.yml` and `config.yaml` - they can run immediately

---

## 🚢 Next Steps

- Read the full [README.md](README.md)
- Check [DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md) for advanced setup
- Adjust settings in [config.yaml](config.yaml)
- Review documentation in [docs/](docs/)

Happy gesture controlling! 🖱️✋

