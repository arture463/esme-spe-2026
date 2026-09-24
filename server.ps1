# Lightweight PowerShell Static HTTP Server for ESME Course Portal
param([int]$Port = 8000)

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrEmpty($projectDir)) { $projectDir = (Get-Location).Path }
Set-Location $projectDir

$mimeMap = @{
    ".html" = "text/html; charset=utf-8"
    ".htm"  = "text/html; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".pdf"  = "application/pdf"
    ".svg"  = "image/svg+xml"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".zip"  = "application/zip"
    ".ipynb"= "application/json; charset=utf-8"
}

$candidatePorts = @($Port, 8000, 8081, 8088, 3000, 5000, 8888) | Select-Object -Unique

$started = $false
$listener = $null
$actualPort = $Port
$prefix = ""

foreach ($p in $candidatePorts) {
    try {
        $candidateListener = New-Object System.Net.HttpListener
        $candidatePrefix = "http://localhost:$p/"
        $candidateListener.Prefixes.Add($candidatePrefix)
        $candidateListener.Start()
        $listener = $candidateListener
        $actualPort = $p
        $prefix = $candidatePrefix
        $started = $true
        break
    } catch {
        # Port busy, continue to next port
    }
}

if (-not $started) {
    Write-Host "Impossible de démarrer le serveur : tous les ports testés sont occupés." -ForegroundColor Red
    exit 1
}

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  PORTAIL DE COURS ESME SPÉ (S03) - SERVEUR DÉMARRÉ" -ForegroundColor Cyan
Write-Host "  Adresse : $prefix" -ForegroundColor Yellow
if ($actualPort -ne $Port) {
    Write-Host "  (Note : Le port $Port était occupé, bascule automatique sur le port $actualPort)" -ForegroundColor Magenta
}
Write-Host "  (Appuyez sur Ctrl+C dans cette fenêtre pour arrêter)" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Green

# Auto-open browser
Start-Process $prefix

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        $urlPath = [System.Uri]::UnescapeDataString($request.Url.LocalPath).TrimStart('/')
        if ([string]::IsNullOrEmpty($urlPath)) { $urlPath = "index.html" }
        
        $localPath = Join-Path $projectDir ($urlPath -replace '/', '\')
        
        if (Test-Path $localPath -PathType Leaf) {
            $ext = [System.IO.Path]::GetExtension($localPath).ToLower()
            $mime = if ($mimeMap.ContainsKey($ext)) { $mimeMap[$ext] } else { "application/octet-stream" }
            
            $response.ContentType = $mime
            $response.AddHeader("Access-Control-Allow-Origin", "*")
            $response.AddHeader("Cache-Control", "no-cache")
            
            $fileBytes = [System.IO.File]::ReadAllBytes($localPath)
            $response.ContentLength64 = $fileBytes.Length
            $response.OutputStream.Write($fileBytes, 0, $fileBytes.Length)
        } else {
            $response.StatusCode = 404
            $msg = [System.Text.Encoding]::UTF8.GetBytes("Fichier non trouvé : $urlPath")
            $response.OutputStream.Write($msg, 0, $msg.Length)
        }
        $response.Close()
    } catch {
        # continue loop
    }
}
