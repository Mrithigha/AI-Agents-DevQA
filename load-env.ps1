Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#][^=]+)=(.+)$') {
    [System.Environment]::SetEnvironmentVariable(
      $matches[1].Trim(), 
      $matches[2].Trim(), 
      'Process'
    )
  }
}
Write-Host "Environment variables loaded successfully." -ForegroundColor Green