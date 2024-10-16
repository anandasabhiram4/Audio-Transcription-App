import subprocess

# Run a simple FFmpeg command to get the version
try:
    result = subprocess.run(['/opt/homebrew/bin/ffmpeg', '-version'], capture_output=True, text=True)
    print("FFmpeg version output:", result.stdout)
except Exception as e:
    print("Error running ffmpeg:", e)
