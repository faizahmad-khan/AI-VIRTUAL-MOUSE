# Docker Troubleshooting Guide

This guide helps resolve common Docker-related issues when running the AI Virtual Mouse.

## 1. Camera Not Detected

### Problem
Container starts but camera feed shows no input.

### Solutions

**Check if camera device exists:**
```bash
ls -la /dev/video*
```

**If no /dev/video0, your camera might be at /dev/video1 or higher:**
```bash
# Edit docker-compose.yml and change:
--device=/dev/video0:/dev/video0
# To:
--device=/dev/video1:/dev/video1
```

**On macOS with USB camera:**
```bash
# You may need to pass camera permissions differently
docker run -it --rm \
  --privileged \
  --device=/dev/video0 \
  ... (other options)
```

**Check camera permissions (Linux):**
```bash
# Add your user to the video group
sudo usermod -aG video $USER
# Log out and back in for changes to take effect
```

---

## 2. X11 Display Issues

### Problem
Error: `Cannot connect to display` or OpenCV window won't show.

### Linux Solutions

**Enable X11 forwarding:**
```bash
# Before running docker command:
xhost +local:docker
export DISPLAY=:0
```

**Check DISPLAY variable:**
```bash
echo $DISPLAY
# Should output something like ":0" or ":1"
```

**If X11 socket not found:**
```bash
# Make sure X11 is running:
ps aux | grep -i x11
# Or check for Xvfb
ps aux | grep -i xvfb
```

### macOS Solutions

**Install XQuartz:**
```bash
# Using Homebrew
brew install --cask xquartz

# Or download from: https://www.xquartz.org/
```

**Set DISPLAY correctly:**
```bash
export DISPLAY=host.docker.internal:0
```

**Start XQuartz:**
```bash
# XQuartz should auto-start, or manually launch it
open -a XQuartz
```

**Grant access to local Docker connections:**
```bash
xhost +local:docker
```

### Windows Solutions

**Install VcXsrv or Xvfb-run:**
- Download VcXsrv: https://sourceforge.net/projects/vcxsrv/
- Or use WSL2 with Xvfb

**Configure VcXsrv:**
1. Launch VcXsrv
2. Set display to :0
3. Enable "Disable access control"

**Set DISPLAY in PowerShell/CMD:**
```bash
set DISPLAY=host.docker.internal:0
# Or in PowerShell:
$env:DISPLAY="host.docker.internal:0"
```

---

## 3. Permission Denied Errors

### Problem
`Permission denied: /dev/video0` or similar device errors.

### Solutions

**Run with --privileged flag (already in docker-compose.yml):**
```bash
# Already configured, but if running manually:
docker run -it --privileged ...
```

**On Linux, add user to video group:**
```bash
sudo usermod -aG video $USER
newgrp video
```

**Check container permissions:**
```bash
docker exec <container_id> ls -la /dev/video0
```

---

## 4. Container Exits Immediately

### Problem
Container starts but exits after a few seconds.

### Solutions

**Check logs:**
```bash
# Using docker-compose
docker-compose logs -f

# Using docker run
docker logs <container_id>
```

**Common causes:**
- Missing camera: `/dev/video0` doesn't exist
- No DISPLAY set: GUI application can't connect
- Python error in the application: Check logs for stack trace

---

## 5. Docker Image Too Large

### Problem
Build or run is slow, image takes up too much space.

### Solutions

**Clean up unused images and layers:**
```bash
docker image prune -a
docker system prune -a
```

**Use .dockerignore:**
The project includes a `.dockerignore` file to exclude unnecessary files. If you added new files, make sure to add them to `.dockerignore`.

**Check image size:**
```bash
docker images ai-virtual-mouse
```

---

## 6. Configuration Changes Not Reflected

### Problem
Modified `config.yaml` but changes don't appear in the container.

### Solutions

**Ensure volume is mounted correctly:**
```bash
# Check docker-compose.yml has:
volumes:
  - ./config.yaml:/app/config.yaml
```

**Verify volume mount:**
```bash
docker inspect <container_id> | grep -A 10 "Mounts"
```

**Restart container after config changes:**
```bash
docker-compose restart
# Or
docker restart <container_id>
```

---

## 7. Logs Not Being Saved

### Problem
`logs/` directory is empty or doesn't exist.

### Solutions

**Create logs directory:**
```bash
mkdir -p logs
chmod 777 logs
```

**Check volume mount:**
```bash
# Verify logs are mounted in docker-compose.yml:
volumes:
  - ./logs:/app/logs
```

**Check container logs:**
```bash
# See what's happening inside the container
docker-compose logs -f
```

---

## 8. Mouse Control Not Working

### Problem
Hand gestures detected but mouse doesn't move.

### Solutions

**Ensure container has display access:**
```bash
xhost +local:docker  # Linux/macOS
```

**Check PyAutoGUI can access mouse:**
```bash
docker exec <container_id> python -c "import pyautogui; print(pyautogui.size())"
```

**On some systems, you may need to configure:**
```bash
# Check if you're using Wayland (newer Linux)
echo $XDG_SESSION_TYPE
# If "wayland", X11 setup is more complex
```

---

## 9. Health Check Failing

### Problem
`docker ps` shows status as "unhealthy".

### Solutions

**Check health check status:**
```bash
docker inspect --format='{{.State.Health.Status}}' <container_id>
```

**View detailed health info:**
```bash
docker inspect --format='{{json .State.Health}}' <container_id> | python -m json.tool
```

**The health check verifies the Python process is running. If failing:**
1. Check logs: `docker-compose logs`
2. Verify application isn't crashing
3. Consider increasing `interval` or `timeout` in docker-compose.yml

---

## 10. Network/Connectivity Issues

### Problem
Container can't connect to external services.

### Solutions

**Check Docker network:**
```bash
docker network ls
docker inspect bridge
```

**Test connectivity from container:**
```bash
docker exec <container_id> ping 8.8.8.8
```

**For docker-compose services:**
```bash
# Services can reach each other by name
docker-compose exec ai-mouse ping other-service
```

---

## Getting More Help

If you encounter issues not listed here:

1. **Check logs first:**
   ```bash
   docker-compose logs -f
   ```

2. **Run in debug mode:**
   ```bash
   # Edit docker-compose.yml to increase logging level
   # Or run python in interactive mode temporarily
   ```

3. **Test X11 connection separately:**
   ```bash
   # Linux
   xhost
   
   # macOS
   xhost
   # Should show "access control enabled, only authorized clients may connect"
   ```

4. **Report issues on GitHub** with the output from:
   ```bash
   docker --version
   docker-compose --version
   uname -a
   xhost  # If applicable
   docker-compose logs
   ```

