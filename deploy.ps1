# Script para generar el empaquetado del plugin de QGIS de forma limpia
# Genera un archivo ZIP que solo contiene los archivos trackeados por Git

$pluginName = "buscador"
$zipFile = "buscador.zip"

Write-Host "--- Iniciando empaquetado agéntico para QGIS ---" -ForegroundColor Cyan

# 1. Limpiar archivos antiguos si existen
if (Test-Path $zipFile) {
    Remove-Item $zipFile
    Write-Host "[-] Archivo ZIP antiguo eliminado." -ForegroundColor Yellow
}

# 2. Generar el ZIP usando git archive
# Esto asegura que SOLO se incluya el código "limpio" y mapea todo dentro de una carpeta 'buscador'
git archive --prefix="$pluginName/" -o $zipFile HEAD

if ($?) {
    Write-Host "[+] Archivo $zipFile generado con éxito." -ForegroundColor Green
    Write-Host "[i] El ZIP contiene la carpeta estructurada '$pluginName/' requerida por QGIS." -ForegroundColor Gray
} else {
    Write-Host "[!] Error al generar el ZIP. Verifica que Git esté instalado y tengas commits." -ForegroundColor Red
}

Write-Host "--- Proceso completado ---" -ForegroundColor Cyan
