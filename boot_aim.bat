@echo off
TITLE A.I.M. - Sovereign Memory Interface Bootloader
REM ==============================================================================
REM A.I.M. Antigravity Proxy Injector
REM This daemon officially launches the IDE bound behind a transparent MITM proxy.
REM It strictly captures the JSON pipeline over HTTPS without touching .pb files.
REM ==============================================================================

echo [A.I.M] Initializing Node/Chromium SSL bypass for local MITM proxy interception...
SET NODE_TLS_REJECT_UNAUTHORIZED=0

echo [A.I.M] Forcing HTTPS API calls through localhost:8080 (aim-proxy.py)...
SET HTTPS_PROXY=http://127.0.0.1:8080
SET HTTP_PROXY=http://127.0.0.1:8080
SET ALL_PROXY=http://127.0.0.1:8080

REM Create an explicit virtual environment proxy launch if missing
pip install mitmproxy >nul 2>&1

echo [A.I.M] Spinning up mitmdump daemon background process...
start "A.I.M. Proxy DataJack" cmd /c "python -c \"from mitmproxy.tools.main import mitmdump; mitmdump(['-s', 'src/plugins/datajack/aim-proxy.py', '-p', '8080', '--set', 'termlog_verbosity=error', '--set', 'block_global=false'])\""

REM Allowing the proxy 2 seconds to bind its socket correctly
timeout /t 2 /nobreak >nul

echo [A.I.M] System Armed. Launching Antigravity IDE...
REM Explicitly opening the IDE executable natively tracked in AppData
START "" "C:\Users\kingb\AppData\Local\Programs\Antigravity\Antigravity.exe"

exit
