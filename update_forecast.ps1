taskkill /im OmniExplorer4.exe /f
$PATH = "~\Desktop\tmp"
If(!(test-path -PathType container $PATH))
{
      New-Item -ItemType Directory -Path $PATH
}

$PATH = "~\Desktop\wind_tmp"
If(!(test-path -PathType container $PATH))
{
      New-Item -ItemType Directory -Path $PATH
}

rm ~/Desktop/tmp/*.png
rm ~/Desktop/wind_tmp/*.png
scp esh563@gadi.nci.org.au:/g/data/w40/esh563/chart_discussion_figs/ACCESS_G/*.png "C:/Users/OmniGlobe Admin/Desktop/tmp"
scp esh563@gadi.nci.org.au:/g/data/w40/esh563/chart_discussion_figs/ACCESS_G_wind/*.png "C:/Users/OmniGlobe Admin/Desktop/wind_tmp"
$COUNT=(Get-ChildItem -Path ~/Desktop/tmp | Measure-Object).Count
$COUNT_WIND=(Get-ChildItem -Path ~/Desktop/wind_tmp | Measure-Object).Count
if ($COUNT=240){
    Write-Output "Copying into Content directory"
    New-Item -Force -Type Directory C:/OmniGlobe/Content/ACCESS_G_mslp
    Copy-Item -Force -Recurse ~/Desktop/tmp/* C:/OmniGlobe/Content/ACCESS_G_mslp
}else {
        Write-Output "Missing Files - Skipping this update"
}
if ($COUNT_WIND=240){
    Write-Output "Copying into Content directory"
    New-Item -Force -Type Directory C:/OmniGlobe/Content/ACCESS_G_wind
    Copy-Item -Force -Recurse ~/Desktop/wind_tmp/* C:/OmniGlobe/Content/ACCESS_G_wind
}else {
        Write-Output "Missing Files - Skipping this wind update"
}
C:\OmniGlobe\Program\OmniExplorer4.exe
