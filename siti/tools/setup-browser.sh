#!/bin/sh
# Prepara un Chromium headless per gli ispettori delle skill di design (taste / impeccable).
# Le sessioni cloud non scaricano browser dai CDN di Google o Playwright: questo binario arriva
# dentro un pacchetto npm (registry consentito). Uso: sh tools/setup-browser.sh && export CHROME_PATH=/tmp/pp-chrome.sh
set -e
DIR=/tmp/pp-chromium
if [ ! -x /tmp/chromium ]; then
  mkdir -p "$DIR" && cd "$DIR"
  [ -f package.json ] || npm init -y >/dev/null
  npm i @sparticuz/chromium@latest >/dev/null 2>&1
  node -e "require('@sparticuz/chromium').default.executablePath().then(p=>console.log('chromium:',p))"
fi
cat > /tmp/pp-chrome.sh <<'EOF'
#!/bin/sh
exec /tmp/chromium --no-sandbox --disable-gpu --disable-dev-shm-usage --no-zygote "$@"
EOF
chmod +x /tmp/pp-chrome.sh
echo "OK · export CHROME_PATH=/tmp/pp-chrome.sh"
