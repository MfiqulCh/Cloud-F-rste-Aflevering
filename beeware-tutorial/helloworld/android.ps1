# Remove the directory if it exists
if (Test-Path -Path "build/helloworld/android") {
    Remove-Item -Path "build/helloworld/android" -Recurse -Force
}

# Execute the Briefcase commands
briefcase create android
briefcase build android
briefcase package android
briefcase run android
