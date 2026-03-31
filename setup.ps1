$ProjectDir = (Get-Item -Path ".\").FullName
$AliasName = (Get-Item -Path ".\").Name

$ProfilePath = $PROFILE
if (-not (Test-Path -Path $ProfilePath)) {
    New-Item -Type File -Path $ProfilePath -Force
}

$FunctionString = @"

function $AliasName {
    if (`$args[0] -eq 'search') {
        `$searchArgs = `$args[1..`$args.Count]
        python "$ProjectDir\src\retriever.py" `$searchArgs
    }
    else {
        python "$ProjectDir\scripts\aim_cli.py" `$args
    }
}
"@

Add-Content -Path $ProfilePath -Value $FunctionString
Write-Host "Installing '$AliasName' PowerShell function to $ProfilePath"
Write-Host "Installation complete! Please restart your PowerShell to use '$AliasName search' and '$AliasName tui'."
