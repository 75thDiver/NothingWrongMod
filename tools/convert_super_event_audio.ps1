param(
    [string]$Source = "$PSScriptRoot/../DESIGN/previews/russian_civil_war/source_super_event.mp3",
    [string]$Destination = "$PSScriptRoot/../sound/super_events/nw14_russia_on_fire.wav"
)
# Run with Windows PowerShell 5.1: uses the installed Windows media codecs.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.StorageFolder, Windows.Storage, ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Transcoding.MediaTranscoder, Windows.Media.Transcoding, ContentType=WindowsRuntime] | Out-Null
[Windows.Media.MediaProperties.MediaEncodingProfile, Windows.Media.MediaProperties, ContentType=WindowsRuntime] | Out-Null
[Windows.Media.MediaProperties.AudioEncodingQuality, Windows.Media.MediaProperties, ContentType=WindowsRuntime] | Out-Null

function Wait-WinRT($Operation, [Type]$ResultType) {
    $method = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
        $_.Name -eq 'AsTask' -and $_.IsGenericMethodDefinition -and
        $_.GetGenericArguments().Count -eq 1 -and $_.GetParameters().Count -eq 1 -and
        $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
    } | Select-Object -First 1
    $task = $method.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.GetAwaiter().GetResult()
}

$sourcePath = (Resolve-Path -LiteralPath $Source).Path
$destinationPath = [IO.Path]::GetFullPath($Destination)
if (Test-Path -LiteralPath $destinationPath) { throw "Output already exists: $destinationPath" }
New-Item -ItemType Directory -Path (Split-Path $destinationPath) -Force | Out-Null
$inputFile = Wait-WinRT ([Windows.Storage.StorageFile]::GetFileFromPathAsync($sourcePath)) ([Windows.Storage.StorageFile])
$folder = Wait-WinRT ([Windows.Storage.StorageFolder]::GetFolderFromPathAsync((Split-Path $destinationPath))) ([Windows.Storage.StorageFolder])
$outputFile = Wait-WinRT ($folder.CreateFileAsync([IO.Path]::GetFileName($destinationPath))) ([Windows.Storage.StorageFile])
$profile = [Windows.Media.MediaProperties.MediaEncodingProfile]::CreateWav([Windows.Media.MediaProperties.AudioEncodingQuality]::High)
$profile.Audio.SampleRate = 44100
$profile.Audio.ChannelCount = 2
$profile.Audio.BitsPerSample = 16
$profile.Audio.Bitrate = 1411200
$transcoder = New-Object Windows.Media.Transcoding.MediaTranscoder
$prepared = Wait-WinRT ($transcoder.PrepareFileTranscodeAsync($inputFile, $outputFile, $profile)) ([Windows.Media.Transcoding.PrepareTranscodeResult])
if (-not $prepared.CanTranscode) { throw "Windows cannot transcode: $($prepared.FailureReason)" }
$method = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.IsGenericMethodDefinition -and
    $_.GetGenericArguments().Count -eq 1 -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncActionWithProgress`1'
} | Select-Object -First 1
$task = $method.MakeGenericMethod([double]).Invoke($null, @($prepared.TranscodeAsync()))
$task.GetAwaiter().GetResult()
Get-Item -LiteralPath $destinationPath | Select-Object FullName, Length
