param(
    [string]$PreviewDir = (Join-Path (Split-Path -Parent $PSScriptRoot) 'DESIGN\previews\russian_civil_war')
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$data = Get-Content -LiteralPath (Join-Path $PreviewDir 'preview_data.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$titles = @{
    overview = 'РОССИЯ В ОГНЕ — обзор политической карты'
    europe = 'Европейская Россия и Прибалтика'
    caucasus = 'Кавказ, Дон и Черноморский регион'
    central_asia = 'Центральная Азия'
    east = 'Сибирь и Дальний Восток'
    moldova = 'Одесса, Бессарабия и Приднестровье — State ID по автору'
}
$labels = @{
    overview = @('SOV','CROWN','RSB','RUK','BLR','FER','POL','FIN','KIR','ALA','TRK','TUR','JAP','BLF','BLW','ROM')
    europe = @('SOV','CROWN','DON','DNR','AKV','KUB','AFSR','RUK','BLR','KAL','BLF','BLW','POL','FIN','ROM')
    caucasus = @('DON','KUB','AFSR','ABK','MNT','TCF','ARM','KAL','TRP','TUR','ROM')
    central_asia = @('SOV','KIR','ALA','TRK','RSB','SIK')
    east = @('SOV','RSB','FER','JAP','MON','SIK')
    moldova = @('ROM','RUK','SOV')
}
$legend = @{
    overview = @('SOV','CROWN','DON','DNR','AKV','KUB','AFSR','RSB','RUK','BLR','FER','ABK','MNT','TCF','ARM','KAL','TRP','BLF','BLW','KIR','ALA','TRK','POL','FIN','TUR','JAP','ROM')
    europe = @('SOV','CROWN','DON','DNR','AKV','KUB','AFSR','RUK','BLR','KAL','BLF','BLW','POL','FIN','ABK','MNT','TCF','ARM','TRP','ROM')
    caucasus = @('SOV','CROWN','DON','DNR','AKV','KUB','AFSR','RUK','ABK','MNT','TCF','ARM','KAL','TRP','TUR','ROM')
    central_asia = @('SOV','RSB','KIR','ALA','TRK','SIK','KAL','TUR')
    east = @('SOV','RSB','FER','JAP','MON','SIK','KIR','ALA')
    moldova = @('SOV','RUK','ROM')
}
$confirmedCapitals = @('SOV','CROWN','RSB','RUK','BLR')

function Get-Color([string]$hex) {
    return [System.Drawing.ColorTranslator]::FromHtml('#' + $hex)
}

foreach ($viewName in @('overview','europe','caucasus','central_asia','east','moldova')) {
    $view = $data.views.$viewName
    $basePath = Join-Path $PreviewDir ($viewName + '_base.png')
    $base = [System.Drawing.Bitmap]::FromFile($basePath)
    $header = 90
    $margin = 18
    $side = 392
    $footer = 55
    $canvas = [System.Drawing.Bitmap]::new(($base.Width + $side + 3 * $margin), ($base.Height + $header + $footer))
    $graphics = [System.Drawing.Graphics]::FromImage($canvas)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $graphics.Clear([System.Drawing.Color]::FromArgb(244, 246, 243))

    $titleFont = [System.Drawing.Font]::new('Segoe UI', 22, [System.Drawing.FontStyle]::Bold)
    $subFont = [System.Drawing.Font]::new('Segoe UI', 10)
    $mapFont = [System.Drawing.Font]::new('Segoe UI', $(if ($viewName -eq 'overview') { 10 } else { 13 }), [System.Drawing.FontStyle]::Bold)
    $idFont = [System.Drawing.Font]::new('Segoe UI', 9, [System.Drawing.FontStyle]::Bold)
    $legendFont = [System.Drawing.Font]::new('Segoe UI', 10)
    $legendSmall = [System.Drawing.Font]::new('Segoe UI', 8)
    $ink = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(25, 39, 49))
    $light = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(225, 255, 255, 255))
    $capitalBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(255, 221, 103))
    $capitalPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(24, 37, 46), 2)
    $mapX = $margin
    $mapY = $header

    $graphics.DrawString($titles[$viewName], $titleFont, $ink, [float]$margin, 12.0)
    $graphics.DrawString('Сплошная заливка — фиксированное распределение; двухцветные полосы — исходы 50/50 только для четырёх указанных штатов.',
        $subFont, $ink, [float]$margin, 57.0)
    $graphics.DrawImage($base, $mapX, $mapY, $base.Width, $base.Height)

    if ($viewName -ne 'overview') {
        foreach ($item in $data.states.PSObject.Properties) {
            $state = $item.Value
            if ($null -eq $state.center) { continue }
            $cx = [double]$state.center[0]
            $cy = [double]$state.center[1]
            if ($cx -lt $view.crop[0] -or $cx -gt $view.crop[2] -or $cy -lt $view.crop[1] -or $cy -gt $view.crop[3]) { continue }
            $x = [float]($mapX + ($cx - $view.crop[0]) * $view.scale)
            $y = [float]($mapY + ($cy - $view.crop[1]) * $view.scale)
            $idText = $item.Name
            $size = $graphics.MeasureString($idText, $idFont)
            $box = [System.Drawing.RectangleF]::new(($x - $size.Width / 2 - 2), ($y - $size.Height / 2 - 1), ($size.Width + 4), ($size.Height + 2))
            $graphics.FillRectangle($light, $box)
            $graphics.DrawString($idText, $idFont, $ink, ($box.X + 2), ($box.Y + 1))
        }
    }

    $placed = [System.Collections.Generic.List[System.Drawing.RectangleF]]::new()
    foreach ($actorId in $labels[$viewName]) {
        $anchor = $view.anchors.$actorId
        if ($null -eq $anchor) { continue }
        $actor = $data.actors.$actorId
        $labelText = if ($actor.map_name) { $actor.map_name } else { $actor.name }
        if ($labelText.Length -gt 28 -and $viewName -eq 'overview') {
            $labelText = $labelText.Substring(0, 27) + '…'
        }
        $x = [float]($mapX + [double]$anchor[0])
        $y = [float]($mapY + [double]$anchor[1])
        $size = $graphics.MeasureString($labelText, $mapFont)
        $left = [float][Math]::Max($mapX + 3, [Math]::Min($mapX + $base.Width - $size.Width - 14, $x + 11))
        $top = [float][Math]::Max($mapY + 3, [Math]::Min($mapY + $base.Height - $size.Height - 12, $y - 22))
        $rect = [System.Drawing.RectangleF]::new($left, $top, ($size.Width + 9), ($size.Height + 5))
        for ($attempt = 0; $attempt -lt 8; $attempt++) {
            $overlap = $false
            foreach ($older in $placed) { if ($rect.IntersectsWith($older)) { $overlap = $true; break } }
            if (-not $overlap) { break }
            $nextY = $rect.Y + $rect.Height + 3
            if ($nextY + $rect.Height -gt $mapY + $base.Height) {
                $nextY = [Math]::Max($mapY + 2, $rect.Y - 2 * ($rect.Height + 3))
            }
            $rect.Y = [float]$nextY
        }
        $placed.Add($rect)
        $color = Get-Color $actor.color
        $pen = [System.Drawing.Pen]::new($color, 2)
        $graphics.DrawLine($pen, $x, $y, $rect.X, ($rect.Y + $rect.Height / 2))
        $graphics.FillRectangle($light, $rect)
        $graphics.DrawRectangle($pen, $rect.X, $rect.Y, $rect.Width, $rect.Height)
        $graphics.DrawString($labelText, $mapFont, $ink, ($rect.X + 4), ($rect.Y + 2))
        if ($confirmedCapitals -contains $actorId) {
            $graphics.FillEllipse($capitalBrush, ($x - 6), ($y - 6), 12, 12)
            $graphics.DrawEllipse($capitalPen, ($x - 6), ($y - 6), 12, 12)
        }
        $pen.Dispose()
    }

    $legendX = $base.Width + 2 * $margin
    $legendTop = $header + 12
    $graphics.DrawString('УЧАСТНИКИ И СТАТУС', [System.Drawing.Font]::new('Segoe UI', 14, [System.Drawing.FontStyle]::Bold),
        $ink, [float]$legendX, [float]$legendTop)
    $legendY = $legendTop + 37
    foreach ($actorId in $legend[$viewName]) {
        $actor = $data.actors.$actorId
        $brush = [System.Drawing.SolidBrush]::new((Get-Color $actor.color))
        $graphics.FillRectangle($brush, $legendX, $legendY + 2, 20, 17)
        $graphics.DrawRectangle([System.Drawing.Pens]::Black, $legendX, $legendY + 2, 20, 17)
        $shortName = if ($actor.legend_name) { $actor.legend_name } else { $actor.name }
        if ($shortName.Length -gt 31) { $shortName = $shortName.Substring(0, 30) + '…' }
        $graphics.DrawString($shortName, $legendFont, $ink, [float]($legendX + 28), [float]$legendY)
        $status = switch ($actor.status) {
            'approved' { $actor.bloc }
            'proposed' { 'проект границы' }
            'legacy proposal' { 'старый контур · проект' }
            'range pending review' { 'диапазон требует проверки' }
            'conditional approved' { '50% при начале войны' }
            'probabilistic outcome' { ('50/50 · ' + $actor.bloc) }
            'approved by author' { $actor.bloc }
            default { $actor.bloc }
        }
        if ($actorId -eq 'CROWN') { $status = 'Российская империя' }
        if ($actorId -eq 'AKV') { $status = "марионетка Дона при появлении`nтерритория — возможный исход 50/50" }
        $graphics.DrawString($status, $legendSmall, $ink, [float]($legendX + 28), [float]($legendY + 19))
        $legendY += $(if ($actorId -eq 'AKV') { 45 } elseif ($viewName -eq 'overview') { 29 } else { 31 })
        $brush.Dispose()
    }
    $graphics.DrawString('● столица по сценарию; остальные метки — географические ориентиры.',
        $subFont, $ink, [float]$margin, [float]($header + $base.Height + 14))
    $graphics.DrawString('Схема сценарных передач; довоенные history/states и география карты не менялись.',
        $subFont, $ink, [float]$margin, [float]($header + $base.Height + 32))
    $resultPath = Join-Path $PreviewDir ($viewName + '.png')
    $canvas.Save($resultPath, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output $resultPath

    $base.Dispose(); $graphics.Dispose(); $canvas.Dispose()
    $titleFont.Dispose(); $subFont.Dispose(); $mapFont.Dispose(); $idFont.Dispose(); $legendFont.Dispose(); $legendSmall.Dispose()
    $ink.Dispose(); $light.Dispose(); $capitalBrush.Dispose(); $capitalPen.Dispose()
}
