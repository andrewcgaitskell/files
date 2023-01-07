# MacBookAir

# Ubuntu

sudo apt-get install hfsprogs

sudo umount /media/andrewcgaitskell/FileBackup1

sudo blkid

sudo mkdir /media/andrewcgaitskell/FileBackup

sudo mount -t hfsplus -o force,rw /dev/sda1 /media/andrewcgaitskell/FileBackup

cd /media/andrewcgaitskell/FileBackup

sudo mkdir ubunto20230107

sudo cp -r /home/andrewcgaitskell/Documents /media/andrewcgaitskell/FileBackup/ubunto20230107


