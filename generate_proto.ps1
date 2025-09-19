$protoDir = "proto"
$pythonOutputDir = "python/mt5_grpc/generated_proto"
$goOutputDir = "go/mt5grpc/generated_proto"

$protos = @("enums.proto", "messages.proto", "services.proto")

function Generate-Python-Proto-Files{
    param (
        [string]$directory
    )

    # Ensure output dirs exist
    New-Item -ItemType Directory -Force -Path $directory | Out-Null

    Write-Host "Generating Python code..."
    foreach ($proto in $protos) {
        python -m grpc_tools.protoc --proto_path=$protoDir --python_out=$directory --pyi_out=$directory --grpc_python_out=$directory "$protoDir/$proto"
    }

}

function Generate-Go-Proto-Files{
    param (
        [string]$directory
    )

    # Ensure output dirs exist
    New-Item -ItemType Directory -Force -Path $directory | Out-Null

    Write-Host "Generating Go code..."
        foreach ($proto in $protos) {
            protoc  --proto_path=$protoDir  --go_out=$directory  --go_opt=paths=source_relative  --go-grpc_out=$directory  --go-grpc_opt=paths=source_relative  "$protoDir/$proto"
    }

}

function Fix-Python-Imports {
    param (
        [string]$directory
    )

    Get-ChildItem -Path $directory -Filter "*.py" | ForEach-Object {
        $content = Get-Content $_.FullName
        $fixed = $content | ForEach-Object {
            if ($_ -match '^import .*_pb2 as .*__pb2') {
                $_ -replace '^import ', 'from . import '
            } else {
                $_
            }
        }
        $fixed | Set-Content $_.FullName
    }
}

Write-Host "Generating python proto files..."
Generate-Python-Proto-Files $pythonOutputDir

Write-Host "Fixing python imports..."
Fix-Python-Imports -directory $pythonOutputDir

Write-Host "Generating go proto files..."
Generate-Go-Proto-Files $goOutputDir

Write-Host "Done!"
