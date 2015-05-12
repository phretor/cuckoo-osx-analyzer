# CREDIT: http://www.contrib.andrew.cmu.edu/~somlo/OSXKVM/

# Mount the installer image:
sudo hdiutil attach /Applications/Install\ OS\ X\ Yosemite.app/Contents/SharedSupport/InstallESD.dmg -noverify -nobrowse -mountpoint /Volumes/install_app

# Convert the boot image to a sparse bundle:
sudo hdiutil convert /Volumes/install_app/BaseSystem.dmg -format UDSP -o /tmp/Yosemite

# Increase the sparse bundle capacity for packages, kernel, etc.:
sudo hdiutil resize -size 8g /tmp/Yosemite.sparseimage

# Mount the sparse bundle target for further processing:
sudo hdiutil attach /tmp/Yosemite.sparseimage -noverify -nobrowse -mountpoint /Volumes/install_build

# Remove Package link and replace with actual files:
sudo rm /Volumes/install_build/System/Installation/Packages
sudo cp -rp /Volumes/install_app/Packages /Volumes/install_build/System/Installation/

# NEW: As of Yosemite, there are additional installer dependencies:
sudo cp -rp /Volumes/install_app/BaseSystem* /Volumes/install_build/

# NEW: As of Yosemite, we also need a kernel image!
# Assuming we're executing these steps on a Yosemite machine:
sudo cp -rp /System/Library/Kernels /Volumes/install_build/System/Library/
# NOTE: on older versions of OS X, it is possible to extract the
#       necessary files (/System/Library/Kernels/*) from the
#       /Volumes/install_app/Packages/Essentials.pkg package,
#       using third party software.

# Unmount both the installer image and the target sparse bundle:
sudo hdiutil detach /Volumes/install_app
sudo hdiutil detach /Volumes/install_build

# Resize the partition in the sparse bundle to remove any free space:
sudo hdiutil resize -size $(hdiutil resize -limits /tmp/Yosemite.sparseimage | tail -n 1 | awk '{ print $1 }')b /tmp/Yosemite.sparseimage

# Convert the sparse bundle to ISO/CD master:
sudo hdiutil convert /tmp/Yosemite.sparseimage -format UDTO -o /tmp/Yosemite

# Remove the sparse bundle:
sudo rm /tmp/Yosemite.sparseimage

# Rename the ISO and move it to the desktop:
sudo mv /tmp/Yosemite.cdr ~/Desktop/Yosemite.iso

echo "Almost done!"
echo
echo "No you're ready to create the VM, using a PIIX3 chipset, with a properly large disk and"
echo "the ISO mounted on the virtual DVD (first-boot only)."
echo
echo "Remember to issue the following command on your VirtualBox host before your first boot:"
echo
echo "  $ VBoxManage modifyvm '<VM NAME HERE>' --cpuidset 1 000206a7 02100800 1fbae3bf bfebfbff"
echo
echo "Booting for the first time takes a while. Also, before installing, open the Disk Utility in"
echo "the guest and create an HFS+-formatted partition, or the installer won't see any available"
echo "target disk."
echo
echo "More info can be found at the following links:"
echo
echo "   * https://gist.github.com/frdmn/de12c894a385bc8e6bff"
echo "   * http://sqar.blogspot.de/2014/10/installing-yosemite-in-virtualbox.html"
echo
echo " Enjoy!"
