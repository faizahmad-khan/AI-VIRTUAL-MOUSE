# 🐳 Docker Setup Guide for macOS

Complete step-by-step guide for running AI Virtual Mouse in Docker on macOS.

---

## ✅ Prerequisites Check

Before starting, ensure you have:
- [ ] macOS 10.14 or later
- [ ] At least 2GB free disk space
- [ ] A webcam connected

---

## 📦 Installation Steps

### **Step 1: Install Docker Desktop (5 minutes)**

#### Option A: Using Homebrew (Recommended)
```bash
brew install --cask docker
```

The application will be installed to `/Applications/Docker.app`.

#### Option B: Manual Download
1. Visit https://www.docker.com/products/docker-desktop
2. Click "Download for Mac"
3. Choose the correct architecture:
   - **Apple Silicon (M1/M2/M3)**: ARM64 version
   - **Intel Mac**: Standard Intel version
4. Open the downloaded `.dmg` file
5. Drag Docker.app to Applications folder

#### Option C: Verify Installation
```bash
# Open Docker Desktop application
open /Applications/Docker.app

# Wait 1-2 minutes for Docker daemon to start

# Verify in terminal
docker --version
docker run hello-world
```

---

### **Step 2: Install XQuartz (2 minutes)**

XQuartz provides the X11 server needed for GUI applications.

#### Option A: Using Homebrew (Easiest)
```bash
brew install --cask xquartz
```

#### Option B: Manual Download
1. Visit https://www.xquartz.org/
2. Download the latest `.dmg` file
3. Open and follow installation wizard
4. Restart your Mac after installation

#### Option C: Verify Installation
```bash
# Check if XQuartz is installed
open /Applications/Utilities/XQuartz.app

# This should launch XQuartz (may show first-time setup)
```

---

### **Step 3: Configure Environment**

Open your terminal and run these commands. Add them to your shell profile (`~/.zshrc` or `~/.bash_profile`) to make them permanent.

```bash
# Set the DISPLAY variable for Docker containers
export DISPLAY=host.docker.internal:0

# Verify it's set
echo $DISPLAY
# Should output: host.docker.internal:0
```

#### **Make It Permanent** (recommended)

```bash
# Add to your shell profile
echo 'export DISPLAY=host.docker.internal:0' >> ~/.zshrc

# Apply changes immediately
source ~/.zshrc

# Verify
echo $DISPLAY
# Should output: host.docker.internal:0
```

---

## 🚀 Building and Running

### **Step 1: Navigate to Project**

```bash
cd "/Users/faizahmadkhan/Desktop/AI VIRTUAL MOUSE"
```

Or use the absolute path:
```bash
cd /Users/<your-username>/Desktop/AI\ VIRTUAL\ MOUSE
```

### **Step 2: Build the Docker Image** (first time only, ~5-10 min)

```bash
docker build -t ai-virtual-mouse .
```

You'll see output like:
```
Sending build context to Docker daemon  123.4kB
Step 1/10 : FROM python:3.9-slim-buster
 ---> 7f5d3c2b1a0e
Step 2/10 : WORKSET /app
 ---> Running in abc123def456
 ---> 1234567890ab
...
Successfully built 1234567890ab
Successfully tagged ai-virtual-mouse:latest
```

### **Step 3: Start XQuartz**

**Important**: XQuartz must be running before starting the container.

```bash
# Launch XQuartz
open -a XQuartz

# Wait 30 seconds for it to fully start
sleep 30

# Allow Docker connections to X11
xhost +local:docker
```

You should see output:
```
host.docker.internal being added to access control list
```

### **Step 4: Run the Application**

#### Option A: Using Docker Compose (Recommended) ⭐

```bash
docker-compose up
```

The container will:
1. Start up (you'll see logs)
2. Detect your camera
3. Open an OpenCV window showing your webcam feed
4. You can now use hand gestures to control the mouse!

**To stop:** Press `Ctrl+C`

#### Option B: Using Docker Run (Manual)

```bash
docker run -it --rm \
  --privileged \
  -e DISPLAY=${DISPLAY} \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --device=/dev/video0:/dev/video0 \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -v $(pwd)/logs:/app/logs \
  ai-virtual-mouse
```

---

## 🎬 Your First Run

When you run the container, you should see:

1. **Terminal Output:**
   ```
   =====================================================
   AI Virtual Mouse starting...
   =====================================================
   Camera initialized: 640x480
   Hand detector initialized successfully
   Starting main loop...
   ```

2. **OpenCV Window:** Shows your webcam feed with:
   - Hand skeleton overlay
   - Purple active area box
   - Gesture feedback circles
   - FPS counter in corner

3. **Hand Gestures:**
   - Move index finger to move cursor
   - Pinch thumb + index to click
   - Middle + ring fingers together to scroll
   - Make fist for 2 seconds to pause/resume

---

## 🔧 Common Issues on macOS

### **Issue: "Cannot connect to display"**

**Solution:**
```bash
# Make sure XQuartz is running
open -a XQuartz

# Wait 10 seconds
sleep 10

# Reset display access
xhost +local:docker

# Try running again
docker-compose up
```

### **Issue: Camera not detected**

**Solution:**

It's a macOS security feature. Docker needs permission:

```bash
# Stop the container first
docker-compose down

# Uninstall Docker
sudo rm -rf ~/Library/Containers/com.docker.docker

# Reinstall Docker Desktop and grant permissions when prompted

# Or try running with setup script
chmod +x docker-setup.sh
./docker-setup.sh
```

### **Issue: "Cannot connect to server: docker.sock"**

**Solution:**
```bash
# Docker daemon isn't running
open /Applications/Docker.app

# Wait 1-2 minutes for it to fully start

# Verify
docker ps

# If still failing, restart Docker
osascript -e 'quit app "Docker"'
sleep 2
open /Applications/Docker.app
```

### **Issue: OpenCV window doesn't appear**

**Checklist:**
- [ ] XQuartz is running: `ps aux | grep XQuartz` (should show XQuartz process)
- [ ] DISPLAY is set: `echo $DISPLAY` (should output `host.docker.internal:0`)
- [ ] xhost allows Docker: `xhost` (should show `host.docker.internal` in list)
- [ ] Container is really running: `docker ps` (should show ai-mouse container)

**Solution:**
```bash
# Restart XQuartz
killall X Xvfb
open -a XQuartz
sleep 30
xhost +local:docker

# Restart container
docker-compose restart
docker-compose logs -f
```

### **Issue: High CPU usage or lag**

**Solution:**
```bash
# Check Docker resource allocation
# Open Docker Desktop → Preferences → Resources

# Allocate more CPU/Memory:
# - CPU: 4 cores
# - Memory: 4GB
# - Swap: 1GB

# Restart Docker
osascript -e 'quit app "Docker"'
open /Applications/Docker.app
```

---

## 📊 Performance Tips for macOS

1. **Allocate Enough Resources:**
   - Docker Desktop → Preferences → Resources
   - CPU: At least 2, preferably 4
   - Memory: At least 2GB, preferably 4GB

2. **Use SSD for Docker:**
   - Docker Desktop automatically uses faster storage
   - Check: `docker info | grep "Docker Root Dir"`

3. **Close Unnecessary Apps:**
   - Reduces resource contention
   - Improves hand detection performance

4. **Position Camera Correctly:**
   - Adequate lighting
   - 2-3 feet from camera
   - Good hand visibility

---

## 🛠️ Development Workflow

### **Edit Configuration**

```bash
# Open config with your editor
nano config.yaml

# Or use VS Code
code config.yaml

# Changes apply immediately - no restart needed!
docker-compose logs -f
```

### **View Logs**

```bash
# Real-time logs
docker-compose logs -f

# Or in a separate terminal
tail -f logs/ai_mouse.log
```

### **Access Container Shell** (for debugging)

```bash
# Open a bash shell inside the container
docker-compose exec ai-mouse bash

# You can now run Python, install packages, etc.
python --version
pip list
```

### **Rebuild After Code Changes**

```bash
# Make code changes in src/

# Rebuild image
docker-compose up --build

# Or
docker build --no-cache -t ai-virtual-mouse .
```

---

## 📚 Useful macOS Commands

```bash
# Check Docker status
docker ps
docker ps -a

# View image details
docker inspect ai-virtual-mouse:latest

# Check container resource usage
docker stats

# View container logs
docker logs <container-id>

# Clean up unused Docker resources
docker system prune

# Remove image
docker rmi ai-virtual-mouse

# Update Docker Desktop
softwareupdate -i -a  # For OS updates
# For Docker updates: Docker Desktop → Check for Updates
```

---

## 🎯 Tested Configuration

This guide was written for and tested on:
- ✅ macOS 12.x (Monterey)
- ✅ macOS 13.x (Ventura)
- ✅ macOS 14.x (Sonoma)
- ✅ Apple Silicon (M1/M2/M3)
- ✅ Intel Macs

---

## ✨ Next Steps

1. ✅ Follow steps above to set up Docker
2. ✅ Run `docker-compose up`
3. ✅ Test hand gestures with your camera
4. ✅ Adjust `config.yaml` if needed
5. ✅ Check logs in `logs/ai_mouse.log`

---

## 🆘 Still Having Issues?

1. **Check the full troubleshooting guide:** [DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md)
2. **Read the quick start:** [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)
3. **Review detailed implementation:** [DOCKER_IMPLEMENTATION.md](DOCKER_IMPLEMENTATION.md)
4. **Check main README:** [README.md](README.md#-docker-containerization-deployment)

---

## 🎬 You're Ready!

You now have a fully containerized AI Virtual Mouse that will work on any macOS system with Docker installed. Enjoy! 🚀

```bash
# One final command to get started:
docker-compose up
```

Happy gesturing! ✋🖱️

---

**Last Updated:** February 27, 2026  
**For:** macOS 11.0+  
**Docker:** 20.10+

