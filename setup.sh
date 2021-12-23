mkdir -p ~/.streamlit/
echo "[theme]
primaryColor='#0013f7'
backgroundColor='#ffffff'
secondaryBackgroundColor='#f9ef91'
textColor='#000000'
font='monospace'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml