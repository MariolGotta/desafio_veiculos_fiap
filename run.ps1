# run.ps1
$env:PYTHONIOENCODING="utf-8"
$env:PYTHONUTF8="1"
$env:LC_ALL="C.UTF-8"
Write-Host "🚀 Iniciando API com configurações UTF-8..."
uvicorn app.main:app --reload