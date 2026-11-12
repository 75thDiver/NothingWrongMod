param(
    [string]$OutDir = (Join-Path (Split-Path -Parent $PSScriptRoot) 'DESIGN\previews\state_id_atlas')
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$fullOutDir = [System.IO.Path]::GetFullPath($OutDir)
$resolvedTemp = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath()).TrimEnd('\') + '\'
$workDir = Join-Path ([System.IO.Path]::GetTempPath()) ('nw-state-id-atlas-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $workDir | Out-Null

try {
    $generator = Join-Path $PSScriptRoot 'render_state_id_atlas.py'
    & python $generator --work-dir $workDir --out-dir $fullOutDir
    if ($LASTEXITCODE -ne 0) { throw "Python atlas generator failed with exit code $LASTEXITCODE" }

    $manifestPath = Join-Path $workDir 'manifest.json'
    $data = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $tileAudit = [System.Collections.Generic.List[object]]::new()
    $ink = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(27, 43, 52))
    $labelFill = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(244, 255, 255, 255))
    $linePen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(185, 52, 66, 74), 1.2)
    $labelPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(190, 48, 63, 70), 1)
    $locatorPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(230, 35, 51, 60), 3)
    $titleFont = [System.Drawing.Font]::new('Segoe UI', 22, [System.Drawing.FontStyle]::Bold)
    $subFont = [System.Drawing.Font]::new('Segoe UI', 11)
    $idFont = [System.Drawing.Font]::new('Segoe UI', 15, [System.Drawing.FontStyle]::Bold)
    $locatorFont = [System.Drawing.Font]::new('Segoe UI', 28, [System.Drawing.FontStyle]::Bold)

    foreach ($tile in $data.pages) {
        $base = [System.Drawing.Bitmap]::FromFile($tile.base_image)
        $maxWidth = 1740.0
        $maxHeight = 1020.0
        $scale = [Math]::Min(4.0, [Math]::Min($maxWidth / $base.Width, $maxHeight / $base.Height))
        $mapWidth = [int][Math]::Round($base.Width * $scale)
        $mapHeight = [int][Math]::Round($base.Height * $scale)
        $marginX = 34
        $mapX = $marginX
        $mapY = 88
        $subtitle = 'Numbers are internal State IDs; names and owners are in atlas_index.csv.'
        $canvasWidth = [Math]::Max(620, [int]($mapWidth + 2 * $marginX))
        $canvasHeight = $mapY + $mapHeight + 48
        $canvas = [System.Drawing.Bitmap]::new($canvasWidth, $canvasHeight)
        $graphics = [System.Drawing.Graphics]::FromImage($canvas)
        $graphics.Clear([System.Drawing.Color]::FromArgb(244, 246, 243))
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
        $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
        $graphics.DrawString($tile.title, $titleFont, $ink, 28.0, 10.0)
        $graphics.DrawString($tile.subtitle, $subFont, $ink, 30.0, 52.0)
        $destRect = [System.Drawing.Rectangle]::new($mapX, $mapY, $mapWidth, $mapHeight)
        $graphics.DrawImage($base, $destRect)

        $anchors = [System.Collections.Generic.List[object]]::new()
        foreach ($state in $tile.states) {
            $x = $mapX + ([double]$state.center[0] - [double]$tile.render_bbox[0]) * $scale
            $y = $mapY + ([double]$state.center[1] - [double]$tile.render_bbox[1]) * $scale
            $nearest = [double]::MaxValue
            foreach ($other in $tile.states) {
                if ([int]$other.id -eq [int]$state.id) { continue }
                $dx = [double]$state.center[0] - [double]$other.center[0]
                $dy = [double]$state.center[1] - [double]$other.center[1]
                $distance = [Math]::Sqrt($dx * $dx + $dy * $dy) * $scale
                if ($distance -lt $nearest) { $nearest = $distance }
            }
            $anchors.Add([pscustomobject]@{ Id = [int]$state.id; X = [double]$x; Y = [double]$y; Nearest = $nearest })
        }

        $placed = [System.Collections.Generic.List[System.Drawing.RectangleF]]::new()
        $displaced = 0
        $unplaced = 0
        $maxShift = 0.0
        foreach ($anchor in ($anchors | Sort-Object Nearest, Id)) {
            $idText = [string]$anchor.Id
            $measure = $graphics.MeasureString($idText, $idFont)
            $boxWidth = [float]($measure.Width + 7)
            $boxHeight = [float]($measure.Height + 3)
            $chosen = $null
            for ($ring = 0; $ring -le 24 -and $null -eq $chosen; $ring++) {
                $offsets = [System.Collections.Generic.List[object]]::new()
                if ($ring -eq 0) {
                    $offsets.Add([pscustomobject]@{ X = 0; Y = 0; D = 0 })
                }
                else {
                    for ($dy = -$ring; $dy -le $ring; $dy++) {
                        for ($dx = -$ring; $dx -le $ring; $dx++) {
                            if ([Math]::Max([Math]::Abs($dx), [Math]::Abs($dy)) -ne $ring) { continue }
                            $offsets.Add([pscustomobject]@{ X = $dx; Y = $dy; D = ($dx * $dx + $dy * $dy) })
                        }
                    }
                }
                foreach ($offset in ($offsets | Sort-Object D, Y, X)) {
                    $cx = [float]($anchor.X + $offset.X * 19)
                    $cy = [float]($anchor.Y + $offset.Y * 19)
                    $rect = [System.Drawing.RectangleF]::new(($cx - $boxWidth / 2), ($cy - $boxHeight / 2), $boxWidth, $boxHeight)
                    if ($rect.Left -lt $mapX -or $rect.Top -lt $mapY -or
                        $rect.Right -gt ($mapX + $mapWidth) -or $rect.Bottom -gt ($mapY + $mapHeight)) { continue }
                    $overlap = $false
                    foreach ($older in $placed) {
                        if ($rect.IntersectsWith($older)) { $overlap = $true; break }
                    }
                    if (-not $overlap) { $chosen = $rect; break }
                }
            }

            if ($null -eq $chosen) {
                $unplaced++
                $chosen = [System.Drawing.RectangleF]::new(
                    [float]($anchor.X - $boxWidth / 2),
                    [float]($anchor.Y - $boxHeight / 2),
                    $boxWidth,
                    $boxHeight
                )
            }
            else {
                $placed.Add($chosen)
            }
            $shiftX = [double]($chosen.X + $chosen.Width / 2 - $anchor.X)
            $shiftY = [double]($chosen.Y + $chosen.Height / 2 - $anchor.Y)
            $shift = [Math]::Sqrt($shiftX * $shiftX + $shiftY * $shiftY)
            if ($shift -gt 3) {
                $displaced++
                if ($shift -gt $maxShift) { $maxShift = $shift }
                $graphics.DrawLine($linePen, [float]$anchor.X, [float]$anchor.Y,
                    [float]($chosen.X + $chosen.Width / 2), [float]($chosen.Y + $chosen.Height / 2))
            }
            $graphics.FillRectangle($labelFill, $chosen)
            $graphics.DrawRectangle($labelPen, $chosen.X, $chosen.Y, $chosen.Width, $chosen.Height)
            $graphics.DrawString($idText, $idFont, $ink, ($chosen.X + 3), ($chosen.Y + 1))
        }

        $outputPath = Join-Path (Join-Path $fullOutDir 'maps') ($tile.code + '.png')
        $canvas.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        $tileAudit.Add([pscustomobject]@{
            page = $tile.code
            expected_labels = $tile.states.Count
            placed_labels = $tile.states.Count - $unplaced
            displaced_labels = $displaced
            unplaced_labels = $unplaced
            max_displacement_px = [Math]::Round($maxShift, 1)
            output = $outputPath
        })
        $graphics.Dispose()
        $canvas.Dispose()
        $base.Dispose()
    }

    $locatorBase = [System.Drawing.Bitmap]::FromFile((Join-Path $workDir 'locator.base.png'))
    $locatorScale = [Math]::Min(1880.0 / $locatorBase.Width, 690.0 / $locatorBase.Height)
    $locatorWidth = [int][Math]::Round($locatorBase.Width * $locatorScale)
    $locatorHeight = [int][Math]::Round($locatorBase.Height * $locatorScale)
    $locatorX = 40
    $locatorY = 78
    $locatorCanvas = [System.Drawing.Bitmap]::new(($locatorWidth + 80), ($locatorHeight + 124))
    $locatorGraphics = [System.Drawing.Graphics]::FromImage($locatorCanvas)
    $locatorGraphics.Clear([System.Drawing.Color]::FromArgb(244, 246, 243))
    $locatorGraphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $locatorGraphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
    $locatorGraphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $locatorGraphics.DrawString($data.locator.title, $titleFont, $ink, 36.0, 10.0)
    $locatorGraphics.DrawString($data.locator.subtitle, $subFont, $ink, 38.0, 48.0)
    $locatorGraphics.DrawImage($locatorBase, [System.Drawing.Rectangle]::new($locatorX, $locatorY, $locatorWidth, $locatorHeight))
    for ($column = 0; $column -le 4; $column++) {
        $x = [float]($locatorX + $locatorWidth * $column / 4)
        $locatorGraphics.DrawLine($locatorPen, $x, [float]$locatorY, $x, [float]($locatorY + $locatorHeight))
    }
    for ($row = 0; $row -le 2; $row++) {
        $y = [float]($locatorY + $locatorHeight * $row / 2)
        $locatorGraphics.DrawLine($locatorPen, [float]$locatorX, $y, [float]($locatorX + $locatorWidth), $y)
    }
    for ($row = 0; $row -lt 2; $row++) {
        for ($column = 0; $column -lt 4; $column++) {
            $code = ('{0}{1}' -f ([char](65 + $column)), ($row + 1))
            $cellX = $locatorX + $locatorWidth * ($column + 0.5) / 4
            $cellY = $locatorY + $locatorHeight * ($row + 0.5) / 2
            $size = $locatorGraphics.MeasureString($code, $locatorFont)
            $rect = [System.Drawing.RectangleF]::new(
                [float]($cellX - $size.Width / 2 - 7), [float]($cellY - $size.Height / 2 - 4),
                [float]($size.Width + 14), [float]($size.Height + 8)
            )
            $locatorGraphics.FillRectangle($labelFill, $rect)
            $locatorGraphics.DrawRectangle($labelPen, $rect.X, $rect.Y, $rect.Width, $rect.Height)
            $locatorGraphics.DrawString($code, $locatorFont, $ink, ($rect.X + 7), ($rect.Y + 4))
        }
    }
    $locatorGraphics.DrawString($data.locator.footer, $subFont, $ink,
        38.0, [float]($locatorY + $locatorHeight + 12))
    $locatorCanvas.Save((Join-Path $fullOutDir '00_locator.png'), [System.Drawing.Imaging.ImageFormat]::Png)
    $locatorGraphics.Dispose()
    $locatorCanvas.Dispose()
    $locatorBase.Dispose()

    $audit = [pscustomobject]@{
        source_active_state_count = $data.source.active_state_count
        mapped_state_count = $data.source.mapped_state_count
        page_count = $data.pages.Count
        pages = @($tileAudit)
        all_labels_placed = (($tileAudit | Measure-Object -Property unplaced_labels -Sum).Sum -eq 0)
    }
    $audit | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $fullOutDir 'annotation_audit.json') -Encoding UTF8
    Write-Output ("Created {0} state-ID sheets for {1} active states in {2}" -f $data.pages.Count, $data.source.active_state_count, $fullOutDir)
    Write-Output ("All labels placed without fallback: {0}" -f $audit.all_labels_placed)
}
finally {
    $resolvedWork = [System.IO.Path]::GetFullPath($workDir)
    if ($resolvedWork.StartsWith($resolvedTemp, [System.StringComparison]::OrdinalIgnoreCase) -and
        (Split-Path -Leaf $resolvedWork).StartsWith('nw-state-id-atlas-', [System.StringComparison]::OrdinalIgnoreCase)) {
        Remove-Item -LiteralPath $resolvedWork -Recurse -Force
    }
}
