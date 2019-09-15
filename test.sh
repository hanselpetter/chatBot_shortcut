WORKSPACE=".";
mkdir -p "${WORKSPACE}/temp/script";

curl -sS $(curl -s https://api.github.com/repos/camalot/chatbotscriptupdater/releases/latest \
| jq -r '.assets[0] .browser_download_url') > ${WORKSPACE}/temp/script/chatbotscriptupdater.zip
mkdir -p ${WORKSPACE}/temp/script/libs/updater/
unzip -d ${WORKSPACE}/temp/script/libs/updater/ ${WORKSPACE}/temp/script/chatbotscriptupdater.zip;
rm "${WORKSPACE}/temp/script/chatbotscriptupdater.zip";
