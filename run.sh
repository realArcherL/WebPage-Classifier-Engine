python3 WebPageDownloader.py
exit_status=$?
last_dir=$(ls -td -- */ | head -n 1 | cut -d'/' -f1)
if [ "${exit_status}" == 0 ];
then
    echo "Storing screenshots in the directory : ${last_dir}"
    python3 screenshot.py "${last_dir}"
fi
