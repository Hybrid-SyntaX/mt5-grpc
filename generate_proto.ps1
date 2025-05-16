$protoDir = "proto"
$outputDir = "src/mt5_grpc/generated_proto"

function Generate-Proto-Files{
    param (
        [string]$directory
    )

    # Ensure output dirs exist
    New-Item -ItemType Directory -Force -Path $directory | Out-Null

    $protos = @("enums.proto", "messages.proto", "services.proto")

    Write-Host "Generating Python code..."
    foreach ($proto in $protos) {
        python -m grpc_tools.protoc --proto_path=$protoDir --python_out=$directory --pyi_out=$directory --grpc_python_out=$directory "$protoDir/$proto"
    }

}

function Fix-Imports {
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

Write-Host "Generating proto files..."
Generate-Proto-Files $outputDir

Write-Host "Fixing imports..."
Fix-Imports -directory $outputDir


Write-Host "Done!"
