#Computer Name
$ComputerSystem = Get-WmiObject Win32_ComputerSystem -namespace "root\CIMV2"
$ComputerName = $ComputerSystem.Name

#IP addresses
$Interfaces = Get-NetIPAddress -AddressFamily IPv4
$IPAddresses = @()

ForEach ($Interface in $Interfaces) {
    If (!($Interface.IPAddress.StartsWith("127")) -and !($Interface.IPAddress.StartsWith("169"))) {
        $IPAddresses += $Interface.IPAddress
    }
}

$IPAddresses = $IPAddresses -join ", "

#User
$User = whoami
$User = $User.Split("\")[1]

#Timestamp (Last seen)
$Timestamp = Get-Date -Format "yyyy-MM-dd, HH:mm"

#OS 
$ComputerInfo = Get-ComputerInfo 
$OS = $ComputerInfo.WindowsProductName + ", " + $ComputerInfo.WindowsVersion + ", " + $ComputerInfo.OSArchitecture
$OSInstallDate = $ComputerInfo.OsInstallDate.ToString("yyyy-MM-dd")

#Serial number
$BIOS = Get-WmiObject Win32_BIOS -namespace "root\CIMV2"
$SerialNumber = $BIOS.SerialNumber

#Computer Model
$ComputerModel = $ComputerSystem.Model

#CPU
$CPU = Get-WmiObject Win32_Processor -namespace "root\CIMV2"
$CPU = $CPU.Name

#Memory
$Memory = (get-wmiobject -class "win32_physicalmemory" -namespace "root\CIMV2").Capacity / 1GB
$Memory = $memory.ToString() + " GB"

#Harddisk
$HardDisk = Get-PhysicalDisk
$HardDiskCapacity = ([Math]::Floor([decimal]($media.Size / 1000000000))).ToString() + " GB"
$HardDiskMediaType = $media.MediaType
$HardDisk = $HardDiskCapacity + ", " + $HardDiskMediaType

#JSON
$JSON = @{
    computerName = $ComputerName
    ipAddresses = $IPAddresses
    user = $User
    timestamp = $Timestamp
    os = $OS
    osInstallDate = $OSInstallDate
    serialNumber = $SerialNumber
    computerModel = $ComputerModel
    cpu = $CPU
    memory = $Memory
    hardDisk = $HardDisk
} | ConvertTo-Json

#POST to backend
Invoke-WebRequest -Uri http://localhost:8080/api/script-device `
                  -Method POST `
                  -Body $JSON `
                  -ContentType "application/json"




